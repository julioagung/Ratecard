// Ambil jumlah followers TikTok & Instagram secara live.
// Dipanggil dari browser via /api/followers (lihat netlify.toml).
// Hasil di-cache di CDN Netlify selama 1 jam supaya tidak kena rate-limit.

const TIKTOK_USER = 'allaboutjuliooutfit';
const INSTAGRAM_USER = 'julio_agung';

const BROWSER_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';

async function getTikTok() {
  const res = await fetch(`https://www.tiktok.com/@${TIKTOK_USER}`, {
    headers: { 'User-Agent': BROWSER_UA, 'Accept-Language': 'en-US,en;q=0.9' },
  });
  const html = await res.text();

  const match = html.match(
    /<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application\/json">([\s\S]*?)<\/script>/
  );
  if (match) {
    const data = JSON.parse(match[1]);
    const stats = data?.__DEFAULT_SCOPE__?.['webapp.user-detail']?.userInfo?.stats;
    if (stats) return { followers: stats.followerCount, likes: stats.heartCount };
  }

  // Fallback: cari langsung angka di HTML
  const followers = html.match(/"followerCount":(\d+)/);
  const likes = html.match(/"heartCount":(\d+)/);
  if (!followers) throw new Error('TikTok: data tidak ditemukan');
  return { followers: Number(followers[1]), likes: likes ? Number(likes[1]) : null };
}

async function getInstagram() {
  // Baca meta description di halaman profil ("2,015 Followers, ...").
  // Pakai UA crawler link-preview karena Instagram melayani meta tag ke crawler tanpa login.
  try {
    const res = await fetch(`https://www.instagram.com/${INSTAGRAM_USER}/`, {
      headers: { 'User-Agent': 'facebookexternalhit/1.1', 'Accept-Language': 'en-US,en;q=0.9' },
    });
    const html = await res.text();
    const match = html.match(/([\d.,]+[KM]?)\s+Followers/i);
    if (match) return { followers: parseCompact(match[1]) };
  } catch {}

  // Fallback: endpoint web API
  const res = await fetch(
    `https://i.instagram.com/api/v1/users/web_profile_info/?username=${INSTAGRAM_USER}`,
    { headers: { 'User-Agent': BROWSER_UA, 'x-ig-app-id': '936619743392459' } }
  );
  const data = await res.json();
  const count = data?.data?.user?.edge_followed_by?.count;
  if (typeof count !== 'number') throw new Error('Instagram: data tidak ditemukan');
  return { followers: count };
}

function parseCompact(str) {
  const mult = /M$/i.test(str) ? 1e6 : /K$/i.test(str) ? 1e3 : 1;
  const num = parseFloat(str.replace(/[KM]$/i, '').replace(/,/g, ''));
  return Math.round(num * mult);
}

export default async () => {
  const [tiktok, instagram] = await Promise.allSettled([getTikTok(), getInstagram()]);

  const body = {
    tiktok: tiktok.status === 'fulfilled' ? tiktok.value : null,
    instagram: instagram.status === 'fulfilled' ? instagram.value : null,
    updatedAt: new Date().toISOString(),
  };

  return new Response(JSON.stringify(body), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=300',
      'Netlify-CDN-Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
};

export const config = { path: '/api/followers' };
