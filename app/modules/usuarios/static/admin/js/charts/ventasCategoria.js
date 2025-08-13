import paleta from "../utils/colors.js";

const colores = Object.values(paleta);

const fetchData = async () => {
  const data = await fetch('/api/v1/pedidos/categoria');
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
      responsive: false,
      maintainAspectRatio: false 
    },
    data: {
      labels: keys,
      datasets: [
        {
          label: keys,
          data: values,
          backgroundColor: [...colores],
          borderColor: 'rgba(0, 0, 0, 1)',
          borderWidth: 1
        }
      ]
    }
  });
};

export default renderVentasCategoria;