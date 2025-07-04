const categoriaSelect = document.getElementById('categoria-select');
const marcaSelect = document.getElementById('marca-select');
const detallesContainer = document.getElementById('detalles-dinamicos');
const formNuevoProducto = document.getElementById('form-nuevo-producto');
const inputImagenes = document.getElementById('input-imagenes');
const imagenPrincipalSelect = document.getElementById('imagen-principal-select');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

let archivosSeleccionados = [];

async function cargarCategorias() {
    const res = await fetch('/api/categorias');
    const json = await res.json();
    const categorias = json.data;

    categoriaSelect.innerHTML = `<option value="">Seleccione una categoría</option>`;
    categorias.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id_categoria;
        option.textContent = cat.nombre;
        categoriaSelect.appendChild(option);
    });
}

async function cargarMarcas() {
    const res = await fetch('/api/marcas');
    const json = await res.json();
    const marcas = json.data;

    marcaSelect.innerHTML = `<option value="">Seleccione una marca</option>`;
    marcas.forEach(marca => {
        const option = document.createElement('option');
        option.value = marca.id_marca;
        option.textContent = marca.nombre;
        marcaSelect.appendChild(option);
    });
}

inputImagenes.addEventListener('change', () => {
    const nuevosArchivos = Array.from(inputImagenes.files);

    nuevosArchivos.forEach(nuevo => {
        if (!archivosSeleccionados.some(a => a.name === nuevo.name)) {
            archivosSeleccionados.push(nuevo);
        }
    });
    imagenPrincipalSelect.innerHTML = `<option value="">Seleccione una imagen</option>`;
    archivosSeleccionados.forEach(file => {
        const option = document.createElement('option');
        option.value = file.name;
        option.textContent = file.name;
        imagenPrincipalSelect.appendChild(option);
    });

    inputImagenes.value = '';
});
categoriaSelect.addEventListener('change', async (e) => {
    const id_categoria = e.target.value;

    if (!id_categoria) {
        detallesContainer.innerHTML = '';
        return;
    }

    const res = await fetch(`/api/detalles/campos/${id_categoria}`);
    const json = await res.json();

    if (!json.success) {
        detallesContainer.innerHTML = '<p>Error cargando campos</p>';
        return;
    }

    const campos = json.campos;
    detallesContainer.innerHTML = campos.map(campo => {
        let input;
        if (campo.tipo === 'checkbox') {
            input = `
                <label>${campo.nombre}:
                <input type="checkbox" name="${campo.nombre}">
                </label>`;
        } else {
            input = `
                <label>${campo.nombre}:
                <input type="${campo.tipo}" name="${campo.nombre}">
                </label>`;
        }
        return input;
    }).join('');
});

formNuevoProducto.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formNuevoProducto);

    const id_marca = parseInt(formData.get("id_marca"));
    const id_categoria = parseInt(formData.get("id_categoria"));

    if (isNaN(id_categoria)) {
        alert("Debe seleccionar una categoría válida.");
        return;
    }

    if (isNaN(id_marca)) {
        alert("Debe seleccionar una marca válida.");
        return;
    }

    const payload = {
        nombre: formData.get("nombre"),
        precio: parseFloat(formData.get("precio")),
        stock: parseInt(formData.get("stock")),
        id_marca: id_marca,
        id_categoria: id_categoria,
        detalles: {}
    };

    const detallesInputs = document.querySelectorAll('#detalles-dinamicos input');
    detallesInputs.forEach(input => {
        const name = input.name;
        if (input.type === 'checkbox') {
            payload.detalles[name] = input.checked;
        } else if (input.type === 'number') {
            const value = input.value.trim();
            payload.detalles[name] = value === '' ? null : parseFloat(value);
        } else {
            payload.detalles[name] = input.value.trim();
        }
    });

    try {
        const res = await fetch('/api/productos', {
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
            alert('Producto creado exitosamente con ID: ' + idProducto);

            if (archivosSeleccionados.length > 0) {
                const nombrePrincipal = imagenPrincipalSelect.value;
                const categoriaTexto = categoriaSelect.options[categoriaSelect.selectedIndex].textContent;

                const imagenesFormData = new FormData();
                imagenesFormData.append('id_producto', idProducto);
                imagenesFormData.append('categoria', categoriaTexto);

                archivosSeleccionados.forEach(archivo => {
                    imagenesFormData.append('imagenes', archivo);
                    const esPrincipal = archivo.name === nombrePrincipal;
                    imagenesFormData.append('es_principal', esPrincipal);
                });

                try {
                    const uploadRes = await fetch('/api/productos/subir-imagen', {
                        method: 'POST',
                        body: imagenesFormData,
                        credentials: 'include',
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    });

                    const uploadJson = await uploadRes.json();
                    if (uploadRes.ok && uploadJson.success) {
                        alert('Imágenes subidas correctamente');
                    } else {
                        alert('Error al subir imágenes: ' + (uploadJson.message || 'Desconocido'));
                    }
                } catch (err) {
                    console.error('Error en subida de imágenes:', err);
                    alert('Error en la petición de imágenes');
                }
            }

        } else {
            alert('Error al crear producto: ' + (json.message || 'Desconocido'));
        }

    } catch (err) {
        console.error(err);
        alert('Error en la petición');
    }
});

cargarCategorias();
cargarMarcas();
