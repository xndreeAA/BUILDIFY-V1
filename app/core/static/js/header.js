document.addEventListener('DOMContentLoaded', () => {
    // Menú hamburguesa
    const toggle = document.getElementById('menu-toggle');
    const menu = document.getElementById('menu');
    toggle.addEventListener('click', () => {
        menu.classList.toggle('active');
    });

    // Menú flotante usuario
    const userIcon = document.getElementById('user-icon');
    const userMenu = document.getElementById('user-menu');

    userIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        userMenu.style.display = (userMenu.style.display === 'block') ? 'none' : 'block';
    });

    // Cerrar si se hace click fuera
    document.addEventListener('click', () => {
        userMenu.style.display = 'none';
    });

    userMenu.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});