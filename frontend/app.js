// --- Drag & Drop Upload ---
const uploadArea = document.getElementById('uploadArea');
const videoUpload = document.getElementById('videoUpload');
const videoPreview = document.getElementById('videoPreview');
const progressBar = document.getElementById('progressBar');
const progressBarInner = document.getElementById('progressBarInner');
const results = document.getElementById('results');
const audioPlayer = document.getElementById('audioPlayer');
const feedbackAudio = document.getElementById('feedbackAudio');
const log = document.getElementById('log');

// Drag & drop events
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        videoUpload.files = e.dataTransfer.files;
        handleVideoUpload(e.dataTransfer.files[0]);
    }
});
uploadArea.addEventListener('click', () => videoUpload.click());
videoUpload.addEventListener('change', (e) => {
    if (e.target.files[0]) handleVideoUpload(e.target.files[0]);
});

async function handleVideoUpload(file) {
    // Reset UI
    results.style.display = 'none';
    audioPlayer.style.display = 'none';
    log.innerHTML = '';
    progressBar.style.display = 'block';
    progressBarInner.style.width = '10%';
    // Show video preview
    videoPreview.src = URL.createObjectURL(file);
    videoPreview.style.display = 'block';
    // Prepare form data
    const formData = new FormData();
    formData.append('video', file);
    appendLog('Uploading video...');
    try {
        progressBarInner.style.width = '40%';
        const res = await fetch('http://localhost:5001/analyze', {
            method: 'POST',
            body: formData
        });
        progressBarInner.style.width = '70%';
        if (!res.ok) throw new Error('Backend error');
        const data = await res.json();
        progressBarInner.style.width = '100%';
        setTimeout(() => progressBar.style.display = 'none', 500);
        appendLog('Analysis complete!');
        // Show prompt to play video for feedback
        appendLog('<b>Watch your performance. Feedback will appear after the video finishes playing.</b>');
        results.style.display = 'none';
        audioPlayer.style.display = 'none';
        // Remove any previous event listeners
        videoPreview.onended = null;
        // When video ends, show feedback/results and play audio
        videoPreview.onended = () => {
            showResults(data);
            if (data.audio_url) playAudio('http://localhost:5001' + data.audio_url);
            appendLog('<b>Your feedback is ready below!</b>');
        };
    } catch (err) {
        progressBar.style.display = 'none';
        showToast('Error: ' + err.message, true);
        appendLog('Error: ' + err.message);
    }
}

document.getElementById('startLive').addEventListener('click', () => {
    showToast('Live mode not implemented in MVP.', false);
});

function playAudio(url) {
    feedbackAudio.src = url;
    audioPlayer.style.display = 'flex';
    feedbackAudio.play();
}

function appendLog(msg) {
    log.innerHTML += `<div>${msg}</div>`;
    log.scrollTop = log.scrollHeight;
}

function showResults(data) {
    results.innerHTML = '';
    results.style.display = 'flex';
    // Analyzer Card
    if (data.metrics) {
        const flaws = data.metrics.flaws || [];
        let flawHtml = '';
        if (Array.isArray(flaws) && flaws.length && typeof flaws[0] === 'object') {
            flawHtml = '<ul style="margin:0 0 0 1em;padding:0;">' + flaws.map(f =>
                `<li style="margin-bottom:0.7em;">
                    <b>${f.description || ''}</b><br>
                    <span style='color:#e67e22;'>${f.reason || ''}</span><br>
                    <span style='color:#43a047;'>Tip: ${f.tip || ''}</span><br>
                    ${(typeof f.timestamp === 'number' && !isNaN(f.timestamp)) ? `<span style='color:#4f8cff;'>At ${formatTime(f.timestamp)}</span><br>` : ''}
                </li>`
            ).join('') + '</ul>';
        } else if (Array.isArray(flaws) && flaws.length) {
            flawHtml = '<ul>' + flaws.map(f => `<li>${f}</li>`).join('') + '</ul>';
        }
        results.appendChild(makeCard('Analyzer', 'psychology', `Chord: <b>${data.metrics.chord || '-'}</b><br>Accuracy: <b>${data.metrics.accuracy || '-'}%</b><br>${flawHtml}`));
    }
    // Coach Card
    if (data.coach) results.appendChild(makeCard('Coach', 'emoji_events', `${data.coach.feedback_text}<br><b>Drill:</b> <code>${data.coach.drill}</code><br><span style='color:#4f8cff;'>${data.metrics && data.metrics.drill_context ? data.metrics.drill_context : ''}</span>`));
    // Automator Card
    if (data.audio_url) results.appendChild(makeCard('Automator', 'volume_up', `Audio feedback ready! <span style="color:var(--primary)">Press play below.</span>`));

    // Progress History Chart
    // Audio Waveform with Flaw Highlights
    if (data.audio_url && data.metrics && Array.isArray(data.metrics.flaws)) {
        showWaveform('http://localhost:5001' + data.audio_url, data.metrics.flaws);
    }
}

function formatTime(seconds) {
    if (typeof seconds !== 'number') return '';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
}

function showProgressChart(history) {
    const chartEl = document.getElementById('progressChart');
    chartEl.style.display = 'block';
    if (window._progressChart) window._progressChart.destroy();
    window._progressChart = new Chart(chartEl.getContext('2d'), {
        type: 'line',
        data: {
            labels: history.map((_, i) => `Session ${i + 1}`),
            datasets: [{
                label: 'Accuracy',
                data: history,
                borderColor: '#4f8cff',
                backgroundColor: 'rgba(79,140,255,0.08)',
                tension: 0.3,
                pointRadius: 5,
                pointBackgroundColor: '#ffb74d',
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { min: 0, max: 100, ticks: { stepSize: 20 } } }
        }
    });
}

function showWaveform(audioUrl, flaws) {
    const waveformDiv = document.getElementById('waveform');
    waveformDiv.style.display = 'block';
    waveformDiv.innerHTML = '';
    if (window._wavesurfer) { window._wavesurfer.destroy(); window._wavesurfer = null; }
    const ws = WaveSurfer.create({
        container: waveformDiv,
        waveColor: '#b3cfff',
        progressColor: '#4f8cff',
        height: 60,
        barWidth: 2,
        responsive: true
    });
    window._wavesurfer = ws;
    ws.load(audioUrl);
    ws.on('ready', () => {
        // Highlight flaw regions
        if (Array.isArray(flaws)) {
            flaws.forEach(f => {
                if (f.timestamp !== undefined && !isNaN(f.timestamp)) {
                    ws.addRegion({
                        start: Math.max(0, f.timestamp - 0.5),
                        end: f.timestamp + 0.5,
                        color: 'rgba(229,57,53,0.25)',
                        drag: false,
                        resize: false
                    });
                }
            });
        }
    });
}

function makeCard(title, icon, content) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `<span class="material-icons">${icon}</span><div><div class="card-title">${title}</div><div class="card-content">${content}</div></div>`;
    return card;
}

function showToast(msg, isError) {
    let toast = document.createElement('div');
    toast.textContent = msg;
    toast.style.position = 'fixed';
    toast.style.bottom = '30px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%)';
    toast.style.background = isError ? 'var(--error)' : 'var(--success)';
    toast.style.color = '#fff';
    toast.style.padding = '1em 2em';
    toast.style.borderRadius = '8px';
    toast.style.fontWeight = 'bold';
    toast.style.boxShadow = '0 2px 12px rgba(0,0,0,0.15)';
    toast.style.zIndex = 9999;
    toast.style.opacity = 0;
    toast.style.transition = 'opacity 0.4s';
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = 1; }, 50);
    setTimeout(() => { toast.style.opacity = 0; setTimeout(()=>toast.remove(), 400); }, 2500);
} 