function viewDeleteProduct({ id_marca }) {
    if (!id_marca) return;

    const confirmado = confirm("¿Estás seguro de que deseas eliminar esta marca?");
    if (!confirmado) return;

    fetch(`/api/v1/marcas/${id_marca}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) throw new Error("Error al eliminar la marca");

        if (response.status === 204) {
            return null;
        }

        return response.json();
    })
    .then(data => {
        alert("Marca eliminado exitosamente.");
        $('#tabla-marcas').DataTable().ajax.reload(null, false);
    })
    .catch(error => {
        alert("Ocurrió un error al eliminar: " + error.message);
    });
}
