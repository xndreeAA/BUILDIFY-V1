//Este script maneja los clic en tarjetas de productos y redirigiría a /product_details/<id>.
// Se puede reutilizar desde cualquier categoria
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.cards_container').forEach(card => {
        const productId = card.dataset.id;

        // Solo elementos específicos disparan redirección
        card.querySelectorAll('.enlace-detalle').forEach(el => {
            el.addEventListener('click', (event) => {
                event.stopPropagation(); // Evita burbujeo
                if (productId) {
                    window.location.href = `/user/product_details/${productId}`;
                }
            });
        });
    });

    
});
