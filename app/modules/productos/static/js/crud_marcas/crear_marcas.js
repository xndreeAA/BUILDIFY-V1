const categoriaSelect = document.getElementById('categoria-select');
const marcaSelect = document.getElementById('marca-select');
const detallesContainer = document.getElementById('detalles-dinamicos');
const formNuevaMarca = document.getElementById('form-nueva-marca');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

formNuevaMarca.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formNuevaMarca);

    const payload = {
        nombre: formData.get("nombre")
    };

    console.log(payload);
    try {
        const res = await fetch('/api/v1/marcas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });

        const json = await res.json();

        if (res.ok && json.success) {
            const idProducto = json.data.id_producto;
            alert('Marca creada exitosamente con ID: ' + idProducto);
        } else {
            alert('Error al crear Marca: ' + (json.message || 'Desconocido'));
        }

    
    } catch (err) {
        console.error(err);
        alert('Error en la petición');
    }
});