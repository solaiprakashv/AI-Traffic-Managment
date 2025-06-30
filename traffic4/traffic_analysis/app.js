document.addEventListener('DOMContentLoaded', function() {
    const ctxTotal = document.getElementById('totalChart').getContext('2d');
    const ctxLane = document.getElementById('laneChart').getContext('2d');

    let totalChart;
    let laneChart;

    async function fetchData() {
        const response = await fetch('/data');
        const data = await response.json();
        return data;
    }

    function updateTotalChart(timestamps, counts) {
        if (totalChart) {
            totalChart.destroy();
        }

        const data = {
            labels: timestamps,
            datasets: [{
                label: 'Total Vehicle Count',
                data: counts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2
            }]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'll HH:mm'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Count'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        };

        totalChart = new Chart(ctxTotal, config);
    }

    document.getElementById('laneSelect').addEventListener('change', async function() {
        const selectedLane = this.value;
        if (selectedLane) {
            const response = await fetch(`/data?lane=${selectedLane}`);
            const laneData = await response.json();
            updateLaneChart(laneData.timestamps, laneData.counts, selectedLane);
        } else {
            // Clear the lane chart if no lane is selected
            if (laneChart) {
                laneChart.destroy();
            }
        }
    });

    function updateLaneChart(timestamps, counts, lane) {
        if (laneChart) {
            laneChart.destroy();
        }

        const data = {
            labels: timestamps,
            datasets: [{
                label: `Lane Count for ${lane}`,
                data: counts,
                borderColor: 'rgba(255, 159, 64, 1)', // Different color for lane chart
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderWidth: 2
            }]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'll HH:mm'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Count'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        };

        laneChart = new Chart(ctxLane, config);
    }

    async function initializeCharts() {
        const { timestamps, counts } = await fetchData();
        updateTotalChart(timestamps, counts);
    }

    initializeCharts();
});