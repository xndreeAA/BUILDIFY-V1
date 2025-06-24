const toggle = document.getElementById('menu-toggle');
const menu = document.getElementById('menu');
// desplegar - ocultar, el menu hamburguesa 
toggle.addEventListener('click', () => {
    menu.classList.toggle('show');
});
