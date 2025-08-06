const fetchData = async () => {
  const data = await fetch('/api/pedidos/categoria');
  const res = await data.json();
  console.log(res);
  
  return res.data;
};


const renderVentasBrutasCategoria = async () => {

    const canvas = document.getElementById('ventas-brutas-por-categoria');
    if (!canvas) return console.error("Canvas no encontrado");
    const ctx = canvas.getContext('2d');

    try {
        const  data = await fetchData();
        const keys = data.map((item) => item.categoria);
        const values = data.map((item) => item.ganancias);
                
        new Chart(ctx, {
            type: 'bar',
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
                    borderRadius: 5,
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


    } catch (e) {
        console.error(e);
    }

}

export default renderVentasBrutasCategoria;