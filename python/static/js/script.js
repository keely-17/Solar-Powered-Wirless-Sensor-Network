const UPDATE_INTERVAL = 300000; // 5 minutes in milliseconds

function showLoading(elementId) {
    document.getElementById(elementId).innerHTML = 'Loading...';
}

function showError(elementId, message) {
    document.getElementById(elementId).innerHTML = `Error: ${message}`;
}

function fetchLatestData() {
    showLoading('latest-data');
    fetch('/api/latest')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('temperature').textContent = data.temperature;
            document.getElementById('humidity').textContent = data.humidity;
            document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString();
        })
        .catch(error => {
            showError('latest-data', 'Failed to fetch latest data');
            console.error('Error:', error);
        });
}

function fetchHistoricalData() {
    const date = document.getElementById('date-picker').value;
    const resultsDiv = document.getElementById('historical-results');
    showLoading('historical-results');
    fetch(`/api/data/${date}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            resultsDiv.innerHTML = '';
            if (data.length === 0) {
                resultsDiv.innerHTML = 'No data available for this date.';
                return;
            }
            data.forEach(entry => {
                resultsDiv.innerHTML += `
                    <p>
                        Timestamp: ${new Date(entry.timestamp).toLocaleString()},
                        Temperature: ${entry.temperature}°F,
                        Humidity: ${entry.humidity}%
                    </p>
                `;
            });
        })
        .catch(error => {
            showError('historical-results', 'Failed to fetch historical data');
            console.error('Error:', error);
        });
}

// Initial fetch and set up interval
fetchLatestData();
setInterval(fetchLatestData, UPDATE_INTERVAL);