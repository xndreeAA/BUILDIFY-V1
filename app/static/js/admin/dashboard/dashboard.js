console.log("Dashboard increíble gracias a David");

const fetchData = async () => {
  const data = await fetch('/api/pedidos/categoria');
  const res = await data.json();
  return res.data;
};

const ctx = document.getElementById('ctx').getContext('2d');

const renderChart = async () => {
  const data = await fetchData();
  const keys = data.map((item) => item.categoria);
  const values = data.map((item) => item.cantidad);

  new Chart(ctx, {
    type: 'doughnut',
    options: {
      animation: true,
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          enabled: true
        }
      }
    },
    data: {
      labels: keys,
      datasets: [
        {
          label: 'Pedidos por categoría',
          data: values,
          borderRadius: 20,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: 'rgba(0, 0, 0, 1)',
          borderWidth: 1
        }
      ]
    }
  });
};

renderChart();
