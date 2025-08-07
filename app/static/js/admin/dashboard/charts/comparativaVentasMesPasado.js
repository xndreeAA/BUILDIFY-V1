const fetchData = async () => {
  const data = await fetch('/api/pedidos/historial-ventas-totales?fill=true');
  const res = await data.json();
  return res.data;
};

const month_map = {
  1: 'Enero',
  2: 'Febrero',
  3: 'Marzo',
  4: 'Abril',
  5: 'Mayo',
  6: 'Junio',
  7: 'Julio',
  8: 'Agosto',
  9: 'Septiembre',
  10: 'Octubre',
  11: 'Noviembre',
  12: 'Diciembre'
};

const renderComparativaVentasMesPasado = async () => {
  const canvas = document.getElementById('comparativa-ventas-mes-pasado');
  if (!canvas) return console.error("Canvas no encontrado");

  const ctx = canvas.getContext('2d');

  try {
    const data = await fetchData();

    const fecha = new Date();
    let anio_actual = fecha.getFullYear();
    const mes_actual = fecha.getMonth() + 1;

    let mes_pasado = mes_actual - 1;
    if (mes_pasado === 0) {
      mes_pasado = 12;
      anio_actual--;
    }

    const mes_pasado_data = data[anio_actual.toString()].meses[mes_pasado];
    const mes_actual_data = data[fecha.getFullYear().toString()].meses[mes_actual];

    const mes_pasado_label = month_map[mes_pasado];
    const mes_actual_label = month_map[mes_actual];

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [''],
        datasets: [
          {
            label: mes_pasado_label,
            data: [mes_pasado_data],
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          },
          {
            label: mes_actual_label,
            data: [mes_actual_data],
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }
        ]
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
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

  } catch (error) {
    console.log(error);
  }
};

export default renderComparativaVentasMesPasado;
