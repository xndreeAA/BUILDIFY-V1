import renderVentasCategoria from './charts/ventasCategoria.js';
import renderHistorialVentasTotales from './charts/historialTotalVentas.js';
import renderComparativaVentasMesPasado from './charts/comparativaVentasMesPasado.js';
import renderMasMenosVendido from './charts/masMenosVendido.js';
import renderVentasBrutasCategoria from './charts/ventasBrutasCategoria.js';

document.addEventListener('DOMContentLoaded', () => {
    renderHistorialVentasTotales();
    renderVentasCategoria();
    renderComparativaVentasMesPasado();
    renderMasMenosVendido();
    renderVentasBrutasCategoria();
});