console.log("Carrito activo");

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document.addEventListener("DOMContentLoaded", () => {
    const productosContainer = document.querySelector(".products-container");

    // Delegación de eventos para botones "Añadir al carrito"
    productosContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("btn-agregar")) {
            e.preventDefault();

            const boton = e.target;
            const id_producto = boton.dataset.id;

            // Buscar el input de cantidad usando el id dinámico
            const inputCantidad = document.getElementById(`cantidad-${id_producto}`);
            const cantidad = inputCantidad ? parseInt(inputCantidad.value) : 1;

            // Llamada a la API para añadir al carrito
            fetch(`/api/v1/carrito/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
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
                        alert(data.error || "Error al añadir al carrito");
                    }
                })
                .catch(error => console.error("❌ Error al añadir al carrito:", error));
        }
    });
});
