const fetchData = async () => {
  const data = await fetch('/api/pedidos/categoria');
  const res = await data.json();
  console.log(res);
  
  return res.data;
};

const renderVentasCategoria = async () => {

  const canvas = document.getElementById('numero-pedidos-por-categoria')
  if (!canvas) return console.error("Canvas no encontrado");
  const ctx = canvas.getContext('2d');


  const data = await fetchData();
  const keys = data.map((item) => item.categoria);  
  const values = data.map((item) => item.cantidad);

  console.log(keys, values);

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
      },
      responsive: false, // 👈 esto es clave
      maintainAspectRatio: false 
    },
    data: {
      labels: keys,
      datasets: [
        {
          label: keys,
          data: values,
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

export default renderVentasCategoria;