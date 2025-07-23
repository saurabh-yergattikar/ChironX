// --- Upload Handler ---
document.getElementById('videoUpload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    // Show video preview
    const videoPreview = document.getElementById('videoPreview');
    videoPreview.src = URL.createObjectURL(file);
    videoPreview.style.display = 'block';
    // Prepare form data
    const formData = new FormData();
    formData.append('video', file);
    appendLog('Uploading video...');
    try {
        const res = await fetch('http://localhost:5001/analyze', {
            method: 'POST',
            body: formData
        });
        if (!res.ok) throw new Error('Backend error');
        const data = await res.json();
        appendLog('Analysis complete!');
        // Play audio feedback
        if (data.audio_url) playAudio('http://localhost:5001' + data.audio_url);
        // Show logs
        if (data.logs) data.logs.forEach(appendLog);
        // Draw overlay
        if (data.metrics) drawOverlay(data.metrics);
    } catch (err) {
        appendLog('Error: ' + err.message);
    }
});

// --- Live Mode Handler ---
document.getElementById('startLive').addEventListener('click', async () => {
    appendLog('Live mode not implemented in MVP.');
});

// --- Audio Playback ---
function playAudio(url) {
    const audio = document.getElementById('feedbackAudio');
    audio.src = url;
    audio.play();
}

// --- Log Update ---
function appendLog(msg) {
    const log = document.getElementById('log');
    log.innerHTML += `<div>${msg}</div>`;
    log.scrollTop = log.scrollHeight;
}

// --- Overlay Drawing ---
function drawOverlay(metrics) {
    const canvas = document.getElementById('overlay');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Example: Draw text for detected chord and flaws
    ctx.font = '20px Arial';
    ctx.fillStyle = 'red';
    ctx.fillText('Chord: ' + (metrics.chord || '-'), 10, 30);
    ctx.fillText('Accuracy: ' + (metrics.accuracy || '-') + '%', 10, 60);
    if (metrics.flaws) {
        ctx.fillStyle = 'orange';
        metrics.flaws.forEach((flaw, i) => {
            ctx.fillText('Flaw: ' + flaw, 10, 100 + i * 30);
        });
    }
} 