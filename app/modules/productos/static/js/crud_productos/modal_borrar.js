function viewDeleteProduct({ id_producto }) {
    if (!id_producto) return;

    const confirmado = confirm("¿Estás seguro de que deseas eliminar este producto?");
    if (!confirmado) return;

    fetch(`/api/v1/productos/${id_producto}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) throw new Error("Error al eliminar el producto");

        // Si el código de estado es 204 No Content, no hace .json()
        if (response.status === 204) {
            return null;
        }

        return response.json(); // Solo si hay contenido
    })
    .then(data => {
        // Si response fue 204, data será null
        alert("Producto eliminado exitosamente.");
        $('#tabla-productos').DataTable().ajax.reload(null, false);
    })
    .catch(error => {
        alert("Ocurrió un error al eliminar: " + error.message);
    });
}
