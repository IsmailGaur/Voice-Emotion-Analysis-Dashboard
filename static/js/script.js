let analysisResults = null;

// File upload handling
const audioFileInput = document.getElementById('audioFile');
const uploadBox = document.getElementById('uploadBox');
const analyzeBtn = document.getElementById('analyzeBtn');
const fileName = document.getElementById('fileName');

audioFileInput.addEventListener('change', handleFileSelect);

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('drag-over');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('drag-over');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
    
    if (e.dataTransfer.files.length > 0) {
        audioFileInput.files = e.dataTransfer.files;
        handleFileSelect();
    }
});

function handleFileSelect() {
    const file = audioFileInput.files[0];
    if (file) {
        fileName.textContent = `Selected: ${file.name}`;
        analyzeBtn.disabled = false;
    }
}

// Analyze button
analyzeBtn.addEventListener('click', analyzeAudio);

async function analyzeAudio() {
    const file = audioFileInput.files[0];
    if (!file) {
        showError('Please select an audio file');
        return;
    }

    // Show loading
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';

    // Create form data
    const formData = new FormData();
    formData.append('audio', file);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            analysisResults = data;
            displayResults(data);
        } else {
            showError(data.error || 'Analysis failed');
        }
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        document.getElementById('loadingSection').style.display = 'none';
    }
}

function displayResults(data) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';

    // Display summary
    displaySummary(data.statistics);

    // Display emotion changes
    displayEmotionChanges(data.emotion_changes);

    // Display charts
    displayTimelineChart(data.results);
    displayPieChart(data.statistics);
    displayBarChart(data.statistics);

    // Display table
    displayTable(data.results);
}

function displaySummary(stats) {
    document.getElementById('dominantEmotion').textContent = stats.dominant_emotion;
    document.getElementById('totalDuration').textContent = formatTime(stats.total_duration);
    document.getElementById('emotionChanges').textContent = 
        Object.keys(analysisResults.emotion_changes).length;
}

function displayEmotionChanges(changes) {
    const container = document.getElementById('emotionChangesLog');
    
    if (changes.length === 0) {
        container.innerHTML = '<p style="color: #6b7280;">No emotion changes detected</p>';
        return;
    }

    container.innerHTML = changes.map(change => `
        <div class="change-item">
            <div class="change-timestamp">${formatTime(change.timestamp)}</div>
            <div class="change-description">
                <span class="emotion-tag emotion-${change.from_emotion}">${change.from_emotion}</span>
                →
                <span class="emotion-tag emotion-${change.to_emotion}">${change.to_emotion}</span>
                <span style="margin-left: 10px; color: #6b7280;">
                    (confidence: ${(change.confidence * 100).toFixed(1)}%)
                </span>
            </div>
        </div>
    `).join('');
}

function displayTimelineChart(results) {
    const timestamps = results.map(r => formatTime(r.start_time));
    const emotions = results.map(r => r.emotion);
    const confidences = results.map(r => r.confidence);

    // Create emotion-to-number mapping for y-axis
    const uniqueEmotions = [...new Set(emotions)];
    const emotionToNum = {};
    uniqueEmotions.forEach((emotion, idx) => {
        emotionToNum[emotion] = idx;
    });

    const trace = {
        x: timestamps,
        y: emotions.map(e => emotionToNum[e]),
        mode: 'lines+markers',
        type: 'scatter',
        line: {
            shape: 'hv',
            width: 3,
            color: '#6366f1'
        },
        marker: {
            size: 10,
            color: confidences,
            colorscale: 'Viridis',
            showscale: true,
            colorbar: {
                title: 'Confidence',
                tickformat: '.0%'
            }
        },
        text: emotions.map((e, i) => `${e}<br>Confidence: ${(confidences[i] * 100).toFixed(1)}%`),
        hovertemplate: '%{text}<extra></extra>'
    };

    const layout = {
        xaxis: {
            title: 'Time',
            showgrid: true
        },
        yaxis: {
            title: 'Emotion',
            ticktext: uniqueEmotions,
            tickvals: uniqueEmotions.map(e => emotionToNum[e]),
            showgrid: true
        },
        hovermode: 'closest',
        height: 400,
        margin: { t: 20, r: 20, b: 60, l: 80 }
    };

    Plotly.newPlot('timelineChart', [trace], layout, {responsive: true});
}

function displayPieChart(stats) {
    const emotions = Object.keys(stats.emotion_percentages);
    const percentages = Object.values(stats.emotion_percentages);

    const colors = {
        'angry': '#fee2e2',
        'calm': '#dbeafe',
        'disgust': '#fef3c7',
        'fearful': '#e0e7ff',
        'happy': '#d1fae5',
        'neutral': '#f3f4f6',
        'sad': '#ddd6fe',
        'surprised': '#fce7f3'
    };

    const trace = {
        labels: emotions,
        values: percentages,
        type: 'pie',
        marker: {
            colors: emotions.map(e => colors[e] || '#e5e7eb')
        },
        textinfo: 'label+percent',
        textposition: 'auto',
        hovertemplate: '%{label}<br>%{value:.1f}%<extra></extra>'
    };

    const layout = {
        height: 400,
        margin: { t: 20, r: 20, b: 20, l: 20 },
        showlegend: true,
        legend: {
            orientation: 'v',
            x: 1,
            y: 0.5
        }
    };

    Plotly.newPlot('pieChart', [trace], layout, {responsive: true});
}

function displayBarChart(stats) {
    const emotions = Object.keys(stats.emotion_counts);
    const counts = Object.values(stats.emotion_counts);

    const trace = {
        x: emotions,
        y: counts,
        type: 'bar',
        marker: {
            color: '#6366f1',
            opacity: 0.8
        },
        text: counts,
        textposition: 'auto',
        hovertemplate: '%{x}<br>Count: %{y}<extra></extra>'
    };

    const layout = {
        xaxis: {
            title: 'Emotion'
        },
        yaxis: {
            title: 'Frequency'
        },
        height: 400,
        margin: { t: 20, r: 20, b: 60, l: 60 }
    };

    Plotly.newPlot('barChart', [trace], layout, {responsive: true});
}

function displayTable(results) {
    const tbody = document.querySelector('#timelineTable tbody');
    
    tbody.innerHTML = results.map(result => `
        <tr>
            <td>${formatTime(result.start_time)}</td>
            <td>${formatTime(result.end_time)}</td>
            <td>
                <span class="emotion-tag emotion-${result.emotion}">
                    ${result.emotion}
                </span>
            </td>
            <td>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
                </div>
                <span style="font-size: 0.9em; color: #6b7280;">
                    ${(result.confidence * 100).toFixed(1)}%
                </span>
            </td>
        </tr>
    `).join('');
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function showError(message) {
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

// Export functionality
document.getElementById('exportCSV').addEventListener('click', exportCSV);
document.getElementById('exportJSON').addEventListener('click', exportJSON);

function exportCSV() {
    if (!analysisResults) return;

    const results = analysisResults.results;
    let csv = 'Start Time,End Time,Emotion,Confidence\n';
    
    results.forEach(r => {
        csv += `${formatTime(r.start_time)},${formatTime(r.end_time)},${r.emotion},${r.confidence}\n`;
    });

    downloadFile(csv, 'emotion_analysis.csv', 'text/csv');
}

function exportJSON() {
    if (!analysisResults) return;

    const json = JSON.stringify(analysisResults, null, 2);
    downloadFile(json, 'emotion_analysis.json', 'application/json');
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
