// introduce backgrounds dinamicamente

document.querySelectorAll('.dynamic-hover-container').forEach((el) => {
  const bg = el.getAttribute('brand-background');
  if (bg) {
    el.style.setProperty('--brand-bg', `url(${bg})`);
  }
});
