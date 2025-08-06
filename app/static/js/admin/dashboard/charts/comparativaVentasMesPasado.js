const fetchData = async () => {
    const data = await fetch('/api/pedidos/historial-ventas-totales?fill=true');
    const res = await data.json();
    return res.data;
}

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
}



const renderComparativaVentasMesPasado = async () => {
    
    const canvas = document.getElementById('comparativa-ventas-mes-pasado');
    if (!canvas) return console.error("Canvas no encontrado");
    const ctx = canvas.getContext('2d');

    try {
        
        const data = await fetchData()

        const fecha = new Date();
        const anio_actual = fecha.getFullYear();
        const mes_actual = fecha.getMonth() + 1;

        let mes_pasado = mes_actual - 1;
        
        switch (mes_pasado) {
            case 0:
                mes_pasado = 12;
                anio_actual--;
                break;
            default:
                break;
        }

        const mes_pasado_data = data[anio_actual.toString()].meses[mes_pasado];
        const mes_pasado_label = month_map[mes_pasado];

        const mes_actual_data = data[anio_actual].meses[mes_actual];
        const mes_actual_label = month_map[mes_actual];

        const labels = [mes_pasado_label, mes_actual_label];
        const data_months = [mes_pasado_data, mes_actual_data];

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: ["julio", "agosto"],
                    data: data_months,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
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
}

export default renderComparativaVentasMesPasado