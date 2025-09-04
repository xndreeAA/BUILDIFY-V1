function viewDeleteCategoria({ id_categoria }) {
    if (!id_categoria) return;

    const confirmado = confirm("¿Estás seguro de que deseas eliminar esta categoría?");
    if (!confirmado) return;

    fetch(`/api/v1/categorias/${id_categoria}`, {  
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrfToken },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) throw new Error("Error al eliminar la categoría");
        return response.json();
    })
    .then(data => {
        alert("Categoría eliminada exitosamente.");
        $('#tabla-categorias').DataTable().ajax.reload(null, false);
    })
    .catch(error => {
        alert("Ocurrió un error al eliminar: " + error.message);
    });
}
