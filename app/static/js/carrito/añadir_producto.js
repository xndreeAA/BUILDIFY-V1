const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
document.addEventListener("DOMContentLoaded", () => {
    const botonesAgregar = document.querySelectorAll(".btn-agregar");
    
    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", (e) => {
            e.preventDefault();
            const id_producto = boton.dataset.id;
            const inputCantidad = boton.closest(".container_description")?.querySelector("#cantidad")
            const cantidad = inputCantidad ? parseInt(inputCantidad.value) : 1;
            
            fetch(`/api/carrito/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    id_producto: id_producto,
                    cantidad: cantidad
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error(error));
        });
    });
});