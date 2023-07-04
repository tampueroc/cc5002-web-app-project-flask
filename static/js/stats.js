function populate_chart_donaciones(data_donaciones) {
    const chartData = Object.entries(data_donaciones).map(([category, value]) => ({
        name: category,
        y: value
    }));

    Highcharts.chart('container-donaciones', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Donaciones por tipo'
        },
        series: [{
            name: 'Cantidad de donaciones',
            data: chartData
        }]
    });
}

function populate_chart_pedidos(data_pedidos) {
    const chartData = Object.entries(data_pedidos).map(([category, value]) => ({
        name: category,
        y: value
    }));

    Highcharts.chart('container-pedidos', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Pedidos por tipo'
        },
        series: [{
            name: 'Cantidad de pedidos',
            data: chartData
        }]
    });
}

fetch("http://localhost:5000/get-stats-data")
        .then((response) => response.json())
        .then((data) => {
            let data_donaciones = data.donaciones;
            populate_chart_donaciones(data_donaciones);
            let data_pedidos = data.pedidos;
            populate_chart_pedidos(data_pedidos);
        });
        