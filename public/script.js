// Smooth reveal on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(el => {
    if (el.isIntersecting) {
      el.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .why-item, .about-inner, .collab-inner')
  .forEach(el => {
    el.classList.add('fade-up');
    observer.observe(el);
  });

// WhatsApp links — pesan otomatis sesuai package yang dipilih
const WA_NUMBER = '62895329361249';

document.querySelectorAll('[data-wa-package]').forEach(link => {
  const pkg = link.dataset.waPackage;
  const text = pkg
    ? `Halo Julio, saya tertarik collab untuk package ${pkg}.\n\nNama / Brand:\nProduk:\nTimeline campaign:`
    : `Halo Julio, saya tertarik untuk collab.\n\nNama / Brand:\nPackage:\nProduk:\nTimeline campaign:`;
  link.href = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;
  link.target = '_blank';
  link.rel = 'noopener';
});

// Live follower count dari TikTok & Instagram (via Netlify Function)
function formatCount(n) {
  if (n >= 1e6) return (n / 1e6).toLocaleString('id-ID', { maximumFractionDigits: 1 }) + 'M+';
  if (n >= 1e4) return (n / 1e3).toLocaleString('id-ID', { maximumFractionDigits: 1 }) + 'K+';
  return n.toLocaleString('id-ID');
}

function setStat(key, value) {
  if (typeof value !== 'number') return;
  document.querySelectorAll(`[data-stat="${key}"]`).forEach(el => {
    el.textContent = formatCount(value);
  });
}

fetch('/api/followers')
  .then(res => res.ok ? res.json() : Promise.reject())
  .then(data => {
    setStat('tiktok-followers', data.tiktok?.followers);
    setStat('tiktok-likes', data.tiktok?.likes);
    setStat('instagram-followers', data.instagram?.followers);
  })
  .catch(() => { /* tetap pakai angka default di HTML */ });

// Inject fade-up CSS dynamically
const style = document.createElement('style');
style.textContent = `
  .fade-up { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
  .fade-up.visible { opacity: 1; transform: translateY(0); }
`;
document.head.appendChild(style);
