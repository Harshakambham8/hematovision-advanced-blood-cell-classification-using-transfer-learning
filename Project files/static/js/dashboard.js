// Dashboard Charts Handler using Chart.js
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Class Distribution Doughnut Chart on Dashboard
    const classChartCanvas = document.getElementById('classDistributionChart');
    if (classChartCanvas && window.dashboardData) {
        const distData = window.dashboardData.class_distribution || {};
        const labels = Object.keys(distData);
        const dataValues = Object.values(distData);

        new Chart(classChartCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: [
                        '#0284c7', // Neutrophil - Cyan
                        '#ef4444', // Eosinophil - Red
                        '#f59e0b', // Monocyte - Amber
                        '#10b981'  // Lymphocyte - Emerald
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { font: { family: 'Inter', size: 12 } }
                    }
                }
            }
        });
    }

    // 2. Initialize Top-4 Probabilities Bar Chart on Result Page
    const probChartCanvas = document.getElementById('probChart');
    if (probChartCanvas && window.resultData) {
        const topProbs = window.resultData.top_probabilities || {};
        const labels = Object.keys(topProbs);
        const values = Object.values(topProbs);

        new Chart(probChartCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Probability (%)',
                    data: values,
                    backgroundColor: [
                        'rgba(2, 132, 199, 0.85)',
                        'rgba(239, 68, 68, 0.85)',
                        'rgba(245, 158, 11, 0.85)',
                        'rgba(16, 185, 129, 0.85)'
                    ],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { callback: value => value + '%' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});
