try { const saved = localStorage.getItem('theme'); if (saved === 'light' || saved === 'dark') document.documentElement.dataset.theme = saved; } catch {}
document.addEventListener('DOMContentLoaded', () => {
 const button = document.querySelector('#theme');
 button.addEventListener('click', () => {
  const dark = document.documentElement.dataset.theme ? document.documentElement.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  const next = dark ? 'light' : 'dark'; document.documentElement.dataset.theme = next;
  try { localStorage.setItem('theme', next); } catch {}
 });
});
