function fetchLatestData() {
    fetch('/api/latest')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').textContent = data.temperature.toFixed(1);
            document.getElementById('humidity').textContent = data.humidity.toFixed(1);
            document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString();
        })
        .catch(error => console.error('Error:', error));
}

function fetchHistoricalData() {
    const date = document.getElementById('date-picker').value;
    fetch(`/api/historical/${date}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('historical-results');
            resultsDiv.innerHTML = '';
            data.forEach(record => {
                resultsDiv.innerHTML += `
                    <p>
                        Time: ${new Date(record.timestamp).toLocaleTimeString()},
                        Temperature: ${record.temperature.toFixed(1)}°F,
                        Humidity: ${record.humidity.toFixed(1)}%
                    </p>
                `;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('historical-results').innerHTML = 'Error fetching historical data.';
        });
}

// Fetch latest data immediately when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchLatestData();
    // Then set up the interval to fetch every 30 minutes
    setInterval(fetchLatestData, 1800000);
});

// Set up event listener for the historical data form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            fetchHistoricalData();
        });
    }
});