import renderVentasCategoria from './ventasCategoria.js';
import renderHistorialVentasTotales from './historialTotalVentas.js';
import renderComparativaVentasMesPasado from './comparativaVentasMesPasado.js';
import renderMasMenosVendido from './masMenosVendido.js';
import renderVentasBrutasCategoria from './ventasBrutasCategoria.js';
import renderMasMenosVendidoCategoria from './masMenosVendidoCategoria.js';

document.addEventListener('DOMContentLoaded', () => {
    
    renderHistorialVentasTotales();
    renderVentasCategoria();
    renderComparativaVentasMesPasado();
    renderMasMenosVendido();
    renderVentasBrutasCategoria();
    renderMasMenosVendidoCategoria();
});