const params = new URLSearchParams(window.location.search);
const sessionId = params.get("session_id");

const iframe = document.getElementById("factura_preview");
const descargarBtn = document.getElementById("descargar_factura_btn");
const previewBtn = document.getElementById("preview_btn");

const fetchData =  async () => {
    const res = await fetch(`/api/v1/pedidos/get-pedido-by-session?session_id=${sessionId}`);
    const data = await res.json();
    return data
}

document.addEventListener("DOMContentLoaded", () => {
    const renderDatosFactura = async () => {
        const data = await fetchData();

        if (data.success === false) {
            const checkout_resume = document.querySelectorAll(".confirmation-message")[1];
            checkout_resume.innerHTML = `<p>Generando factura... por favor espera ⏳</p>`;

            console.log("Factura aún no disponible, reintentando...");
            setTimeout(renderDatosFactura, 2000);
            return;
        }

        const pedido = data.data;

        if (!pedido.factura) {
            console.log("Pedido encontrado pero sin factura, reintentando...");
            setTimeout(renderDatosFactura, 2000);
            return;
        }

        if (pedido.id_pedido) {
            localStorage.setItem("id_pedido", pedido.id_pedido);
            console.log("Pedido guardado en localStorage:", pedido.id_pedido);
        }

        if (pedido.factura) {
            const pdfUrl = pedido.factura.factura_url_pdf_cloud || pedido.factura.factura_url_pdf_stripe;
            if (pdfUrl) {
                iframe.src = pdfUrl + "#toolbar=0&navpanes=0&scrollbar=0";

                descargarBtn.onclick = () => {
                    window.open(pdfUrl, "_blank");
                };

                previewBtn.onclick = () => {
                    window.open(pdfUrl, "_blank");
                };
            }

            const factura = pedido.factura;

            const checkout_resume = document.querySelectorAll(".confirmation-message")[1];
            checkout_resume.innerHTML = `
                <p>
                    Gracias por tu compra en <strong>Buildify</strong>.
                    Tu compra ha sido correctamente procesada.  
                    En breve recibirás un e-mail con los detalles de tu compra al correo <a href="mailto:${pedido.email}">${pedido.email}</a>.
                </p>
                <br>
                <p> <strong>Factura:</strong> #${factura.numero_factura}</p>
                <p><strong>Fecha de compra:</strong> ${pedido.fecha_pedido}</p>
                <p><strong>Total:</strong> ${factura.total} ${factura.moneda}</p>
            `;
        }
    };

    renderDatosFactura();
});