// Webcam-based attention tracking using getDisplayMedia or getUserMedia

async function startAttentionTracking() {
    try {
        const video = document.getElementById('webcamFeed');
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        
        // Continuously send frames for analysis
        setInterval(async () => {
            await sendFrameForAnalysis(video);
        }, 2000); // Every 2 seconds
        
    } catch (error) {
        console.error('Camera access error:', error);
    }
}

async function sendFrameForAnalysis(video) {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('frame', blob);
        
        try {
            const response = await fetch(`${API_BASE}/track-attention`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            updateAttentionMetrics(data);
            
        } catch (error) {
            console.error('Error tracking attention:', error);
        }
    }, 'image/jpeg');
}

function updateAttentionMetrics(data) {
    document.getElementById('gazeDirection').textContent = data.gaze_direction;
    document.getElementById('focusLevel').textContent = 
        Math.round(data.focus_level) + '%';
    document.getElementById('engagementScore').textContent = 
        Math.round(data.engagement_score) + '%';
}


