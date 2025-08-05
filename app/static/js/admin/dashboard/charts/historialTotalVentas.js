
const contenedor_historial_ventas_totales = document.getElementById('historial-ventas-totales').getContext('2d');

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

const renderHistorialVentasTotales = async () => {
    
    try {
        // const data = await fetchData();

        const data = {
            "2025": {
                meses: {
                    "1": 0.0,
                    "2": 0.0,
                    "3": 0.0,
                    "4": 0.0,
                    "5": 0.0,
                    "6": 0.0,
                    "7": 2259000.0,
                    "8": 1295000.0,
                    "9": 0.0,
                    "10": 0.0,
                    "11": 0.0,
                    "12": 0.0
                },
                    total_ventas: 3554000.0
                },
            "2024": {
                meses: {
                    "1": 1000000.0,
                    "2": 1200000.0,
                    "3": 900000.0,
                    "4": 1100000.0,
                    "5": 1050000.0,
                    "6": 950000.0,
                    "7": 0.0,
                    "8": 0.0,
                    "9": 0.0,
                    "10": 0.0,
                    "11": 0.0,
                    "12": 0.0
                },
                total_ventas: 6200000.0
            },
            
            "2023": {
                meses: {
                    "1": 800000.0,
                    "2": 750000.0,
                    "3": 600000.0,
                    "4": 700000.0,
                    "5": 720000.0,
                    "6": 680000.0,
                    "7": 670000.0,
                    "8": 690000.0,
                    "9": 710000.0,
                    "10": 0.0,
                    "11": 0.0,
                    "12": 0.0
                },
                total_ventas: 7320000.0
            },
            
            "2022": {
                meses: {
                    "1": 500000.0,
                    "2": 530000.0,
                    "3": 550000.0,
                    "4": 580000.0,
                    "5": 600000.0,
                    "6": 620000.0,
                    "7": 640000.0,
                    "8": 660000.0,
                    "9": 680000.0,
                    "10": 700000.0,
                    "11": 720000.0,
                    "12": 740000.0
                },
                total_ventas: 8520000.0
            }
        }

        const data_chart = {
            labels: Object.values(month_map),

            datasets: Object.entries(data).map(year => ({
                label: year[0],
                data: Object.values(year[1].meses),
            }))
        };

        new Chart(contenedor_historial_ventas_totales, {
            
            type: 'line',
            data: data_chart,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Historial de ventas anuales',
                    },
                    colors: {
                        forceOverride: true
                    }
                },
                scales: {
                    y: {
                        suggestedMin: 30,
                    }
                }
            },
        });


        
    } catch (error) {
        
        console.log('Error en la petición:', error);
    }
    
}

export default renderHistorialVentasTotales
