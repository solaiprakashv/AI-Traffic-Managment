document.addEventListener('DOMContentLoaded', function() {
    const ctxTotal = document.getElementById('totalChart').getContext('2d');
    const ctxLane = document.getElementById('laneChart').getContext('2d');
    const laneSelect = document.getElementById('laneSelect');

    let totalChart;
    let laneChart;

    async function fetchData(lane = null) {
        let url = '/data';
        if (lane) {
            url += `?lane=${lane}`;
        }
        try {
            const response = await fetch(url);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching data:', error);
            return { timestamps: [], counts: [] };
        }
    }

    async function initializeCharts() {
        const { timestamps, counts } = await fetchData();
        updateTotalChart(timestamps, counts);
        populateLaneSelect();
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
                borderWidth: 1
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
                            tooltipFormat: 'll'
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
                }
            }
        };

        totalChart = new Chart(ctxTotal, config);
    }

    async function populateLaneSelect() {
        try {
            const response = await fetch('/data');
            const data = await response.json();
            const lanes = [...new Set(data.timestamps.map(ts => ts.split(' ')[0]))];
            lanes.forEach(lane => {
                const option = document.createElement('option');
                option.value = lane;
                option.textContent = lane;
                laneSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error populating lane select:', error);
        }
    }

    laneSelect.addEventListener('change', async function() {
        const lane = this.value;
        const { timestamps, counts } = await fetchData(lane);
        updateLaneChart(timestamps, counts);
    });

    function updateLaneChart(timestamps, counts) {
        if (laneChart) {
            laneChart.destroy();
        }

        const data = {
            labels: timestamps,
            datasets: [{
                label: 'Lane Vehicle Count',
                data: counts,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderWidth: 1
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
                            tooltipFormat: 'll'
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
                }
            }
        };

        laneChart = new Chart(ctxLane, config);
    }

    initializeCharts();
});
