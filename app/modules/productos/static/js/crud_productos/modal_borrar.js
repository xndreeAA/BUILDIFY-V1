function viewDeleteProduct({ id_producto }) {
    if (!id_producto) return;

    const confirmado = confirm("¿Estás seguro de que deseas eliminar este producto?");
    if (!confirmado) return;

    fetch(`/api/v1/productos/${id_producto}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        credentials: 'include' // Necesario si usas sesión con cookies (Flask-Login, etc.)
    })
    .then(response => {
        if (!response.ok) throw new Error("Error al eliminar el producto");
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Producto eliminado exitosamente.");
            // Recargar la tabla sin recargar la página completa
            $('#tabla-productos').DataTable().ajax.reload(null, false);
        } else {
            alert("No se pudo eliminar el producto.");
        }
    })
    .catch(error => {
        alert("Ocurrió un error al eliminar: " + error.message);
    });
}
