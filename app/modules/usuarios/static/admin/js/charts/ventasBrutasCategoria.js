import paleta from "../utils/colors.js";

const fetchData = async () => {
  const data = await fetch('/api/v1/pedidos/categoria');
  const res = await data.json();
  return res.data;
};

const colores = Object.values(paleta);

const renderVentasBrutasCategoria = async () => {
  const canvas = document.getElementById('ventas-brutas-por-categoria');
  if (!canvas) return console.error("Canvas no encontrado");

  const ctx = canvas.getContext('2d');

  try {
    const data = await fetchData();

    const datasets = data.map((item, index) => ({
      label: item.categoria,
      data: [item.ganancias],
      backgroundColor: colores[index],
      borderColor: 'rgba(0, 0, 0, 1)',
      borderWidth: 1,
    }));

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Ganancias por categoría'],
        datasets
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          },
          tooltip: {
            enabled: true
          }
        }
      }
    });

  } catch (e) {
    console.error(e);
  }
};

export default renderVentasBrutasCategoria;
