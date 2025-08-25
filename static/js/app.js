document.addEventListener('DOMContentLoaded', () => {
    // Comprobamos si los datos han sido inyectados en la página.
    if (typeof chartData === 'undefined') {
        console.error('Error: El objeto chartData no se encuentra. Asegúrate de que el script de construcción se ha ejecutado correctamente.');
        return;
    }

    // Paleta de colores extraída del diseño de la infografía
    const colors = {
        primary: '#0A9396',      // teal
        secondary: '#EE9B00',    // orange
        accent: '#005F73',       // darkTeal
        negative: '#AE2012',     // darkRed
        grid: 'rgba(0, 0, 0, 0.08)', // Lighter grid for light background
        text: '#1e293b' // Darker text (slate-800)
    };

    // Configuración común para todos los gráficos
    const commonChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: colors.text } }
        },
        scales: {
            x: {
                ticks: { color: colors.text, maxRotation: 0, autoSkip: true, maxTicksLimit: 7 },
                grid: { color: colors.grid }
            },
            y: {
                ticks: { color: colors.text },
                grid: { color: colors.grid }
            }
        }
    };

    // 1. Crear Gráfico de Liquidez M2
    const createM2Chart = () => {
        const data = chartData.m2_liquidity;
        new Chart(document.getElementById('m2Chart'), {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'M2 Supply (in Billions)',
                    data: data.data,
                    borderColor: colors.primary,
                    backgroundColor: colors.primary.replace(')', ', 0.2)'),
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0
                }]
            },
            options: commonChartOptions
        });
    };

    // 2. Crear Gráfico del Spread
    const createSpreadChart = () => {
        const data = chartData.treasury_spread;
        new Chart(document.getElementById('spreadChart'), {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: '10Y-3M Spread (%)',
                    data: data.data,
                    borderColor: colors.accent,
                    backgroundColor: colors.accent.replace(')', ', 0.2)'),
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0
                }]
            },
            options: commonChartOptions
        });
    };

    // 3. Crear Gráfico Fed Funds vs 10-Year
    const createFedFundsChart = () => {
        const data = chartData.fed_funds_vs_10y;
        new Chart(document.getElementById('fedFundsChart'), {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Fed Funds Rate (%)',
                        data: data.fed_funds,
                        borderColor: colors.primary,
                        tension: 0.3,
                        pointRadius: 0
                    },
                    {
                        label: '10-Year Treasury Yield (%)',
                        data: data.ten_year,
                        borderColor: colors.secondary,
                        tension: 0.3,
                        pointRadius: 0
                    }
                ]
            },
            options: commonChartOptions
        });
    };

    // 4. Crear Gráfico de Rendimiento High-Yield
    const createHighYieldChart = () => {
        const data = chartData.high_yield_index;
        new Chart(document.getElementById('highYieldChart'), {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'High-Yield Index Yield (%)',
                    data: data.data,
                    borderColor: colors.secondary,
                    backgroundColor: colors.secondary.replace(')', ', 0.2)'),
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0
                }]
            },
            options: commonChartOptions
        });
    };

    // Inicializar todos los gráficos
    createM2Chart();
    createSpreadChart();
    createFedFundsChart();
    createHighYieldChart();
});