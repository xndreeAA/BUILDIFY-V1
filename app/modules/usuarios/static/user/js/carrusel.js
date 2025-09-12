// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {

    //  Consumir API del carrusel
    fetch('/api/v1/carrusel/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const items = data.data; // Datos recibidos del backend
                const contenedor = document.getElementById('carrusel-home');

                // Si no hay elementos en el carrusel, mostrar mensaje
                if (!items || items.length === 0) {
                    contenedor.innerHTML = "<p>No hay imágenes en el carrusel.</p>";
                    return;
                }

                //  Generar dinámicamente los slides del carrusel
                items.forEach((item, index) => {
                    const slide = document.createElement("article");
                    slide.className = "carrusel-slide";

                    // El primer slide se marca como activo (visible por defecto)
                    if (index === 0) slide.classList.add("active");

                    // Plantilla HTML de cada slide
                    slide.innerHTML = `
                        <img src="${item.url_imagen}" alt="${item.titulo || 'Carrusel'}">
                        <div class="carrusel-texto">
                            <h1>${item.titulo || ''}</h1>
                            <p>${item.descripcion || ''}</p>
                            <div class="btnH">
                                <button class="btn-styled">Explorar productos</button>
                            </div>
                        </div>
                    `;

                    // Insertar el slide en el contenedor principal
                    contenedor.appendChild(slide);
                });

                //  Lógica de rotación automática de slides
                let current = 0;
                const slides = document.querySelectorAll(".carrusel-slide");

                // Cada 5 segundos cambia el slide visible
                setInterval(() => {
                    slides[current].classList.remove("active"); // Ocultar slide actual
                    current = (current + 1) % slides.length;    // Calcular siguiente índice
                    slides[current].classList.add("active");    // Mostrar nuevo slide
                }, 5000);
            } else {
                console.error(" Error al cargar carrusel");
            }
        })
        .catch(error => {
            // Manejo de errores en la petición
            console.error(" Error en la petición:", error);
        });
});
