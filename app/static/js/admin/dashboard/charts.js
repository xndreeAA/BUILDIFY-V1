import renderVentasCategoria from './charts/ventasCategoria.js';
import renderHistorialVentasTotales from './charts/historialTotalVentas.js';
import renderComparativaVentasMesPasado from './charts/comparativaVentasMesPasado.js';

document.addEventListener('DOMContentLoaded', () => {
    renderVentasCategoria();
    renderHistorialVentasTotales();
    renderComparativaVentasMesPasado();
});