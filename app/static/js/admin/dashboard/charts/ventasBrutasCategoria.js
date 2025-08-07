const fetchData = async () => {
  const data = await fetch('/api/pedidos/categoria');
  const res = await data.json();
  return res.data;
};

const renderVentasBrutasCategoria = async () => {
  const canvas = document.getElementById('ventas-brutas-por-categoria');
  if (!canvas) return console.error("Canvas no encontrado");

  const ctx = canvas.getContext('2d');

  try {
    const data = await fetchData();

    const datasets = data.map((item, index) => ({
      label: item.categoria,
      data: [item.ganancias],
      backgroundColor: getColor(index),
      borderColor: 'rgba(0,0,0,0.7)',
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

const getColor = (index) => {
  const colors = [
    'rgba(255, 99, 132, 0.6)',
    'rgba(54, 162, 235, 0.6)',
    'rgba(255, 206, 86, 0.6)',
    'rgba(75, 192, 192, 0.6)',
    'rgba(153, 102, 255, 0.6)',
    'rgba(255, 159, 64, 0.6)'
  ];
  return colors[index % colors.length];
};

export default renderVentasBrutasCategoria;
