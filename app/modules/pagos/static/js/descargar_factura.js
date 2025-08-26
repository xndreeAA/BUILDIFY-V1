const params = new URLSearchParams(window.location.search);
const sessionId = params.get("session_id");

const iframe = document.getElementById("factura_preview");
const descargarBtn = document.getElementById("descargar_factura_btn");
const previewBtn = document.getElementById("preview_btn");

fetch(`/api/v1/pedidos/get-pedido-by-session?session_id=${sessionId}`)
    .then(res => res.json())
    .then(data => {
        console.log(data);

        if (data.id_pedido) {
            localStorage.setItem("id_pedido", data.id_pedido);
            console.log("Pedido guardado en localStorage:", data.id_pedido);
        }

        
        if (data.factura) {
            const pdfUrl = data.factura.factura_url_pdf_cloud || data.factura.factura_url_pdf_stripe;
            if (pdfUrl) {
                iframe.src = pdfUrl + "#toolbar=0&navpanes=0&scrollbar=0";

                descargarBtn.onclick = () => {
                    window.open(pdfUrl, "_blank");
                };

                previewBtn.onclick = () => {
                    window.open(pdfUrl, "_blank");
                };
            }

            const factura = data.factura;

            const checkout_resume = document.querySelectorAll(".confirmation-message")[1];

            checkout_resume.innerHTML = `
                <p>
                    Gracias por tu compra en <strong>Buildify</strong>.
                    Tu compra ha sido correctamente procesada.  
                    En breve recibirás un e-mail con los detalles de tu compra al correo <a href="mailto:${data.email}">${data.email}</a>.
                </p>
                <br>
                <p> <strong>Factura:</strong> #${factura.numero_factura}</p>
                <p><strong>Fecha de compra:</strong> ${data.fecha_pedido}</p>
                <p><strong>Total:</strong> ${factura.total} ${factura.moneda}</p>
            `;
        }
    })
    .catch(err => console.error("Error obteniendo pedido:", err));
