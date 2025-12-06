// Automatically use the current origin
const API_BASE = window.location.origin + '/api';

// DOM Elements
const startReadingBtn = document.getElementById('startReadingBtn');
const pauseReadingBtn = document.getElementById('pauseReadingBtn');
const getHintBtn = document.getElementById('getHintBtn');
const getMentorFeedbackBtn = document.getElementById('getMentorFeedbackBtn');
const endSessionBtn = document.getElementById('endSessionBtn');

const readingContent = document.getElementById('readingContent');
const mentorFeedback = document.getElementById('mentorFeedback');

// Performance Metrics Elements
const accuracyDisplay = document.getElementById('accuracyScore');
const fluencyDisplay = document.getElementById('fluencyScore');
const wordsReadDisplay = document.getElementById('wordsRead');

// State
let isReading = false;
let mediaRecorder;
let audioChunks = [];
let silenceTimer;
let currentPassageText = "";
let audioContext; 
let analyser;     
let microphone;   
let animationFrameRequest; 

// Sample passages
const passages = [
    {
        id: 1,
        text: "The sun shone brightly over the mountains. Birds sang their morning songs. Children played in the park, laughing and running freely. It was a perfect day for adventure.",
        difficulty: "beginner"
    },
    {
        id: 2,
        text: "Photography is the art of capturing moments in time. Through a camera lens, photographers preserve memories, emotions, and stories. Each photograph tells a unique narrative about the world around us.",
        difficulty: "intermediate"
    }
];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPassage();
    setupEventListeners();
});

function setupEventListeners() {
    startReadingBtn.addEventListener('click', startReading);
    pauseReadingBtn.addEventListener('click', pauseReading);
    getHintBtn.addEventListener('click', getHint);
    getMentorFeedbackBtn.addEventListener('click', getMentorFeedback);
    endSessionBtn.addEventListener('click', endSession);
}

function loadPassage() {
    const randomPassage = passages[Math.floor(Math.random() * passages.length)];
    currentPassageText = randomPassage.text;
    
    readingContent.innerHTML = `
        <p id="passageText" style="font-size: 1.2em; line-height: 1.6;">${randomPassage.text}</p>
        <small style="color:#666; margin-top: 15px; display: block; font-weight: bold;">
            Difficulty: ${randomPassage.difficulty.toUpperCase()}
        </small>
    `;
}



async function startReading() {
    try {
        // 1. Get audio stream
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // 2. Audio Analysis Setup (Detects speaking volume)
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
        analyser.fftSize = 256;
        
        // 3. MediaRecorder Setup
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await analyzeReading(audioBlob);
            
            // Cleanup Audio Context
            if(audioContext && audioContext.state !== 'closed') {
                audioContext.close();
            }
        };

        // 4. Start camera tracking (NEW)
        if (typeof startAttentionTracking === 'function') {
            startAttentionTracking();
        }

        // 5. Start recording
        mediaRecorder.start();
        isReading = true;
        
        // 6. UI Updates
        startReadingBtn.disabled = true;
        pauseReadingBtn.disabled = false;
        startReadingBtn.textContent = 'Recording...';
        
        // 7. Start voice detection loop
        detectVoiceActivity();
        
        // 8. Start silence timer
        resetSilenceTimer();

    } catch (error) {
        console.error('Microphone access denied:', error);
        alert('Please allow microphone access to read aloud.');
    }
}



// --- NEW FUNCTION: Loop that checks volume levels ---
function detectVoiceActivity() {
    if (!isReading) return;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyser.getByteFrequencyData(dataArray);

    // Calculate average volume
    let sum = 0;
    for(let i = 0; i < bufferLength; i++) {
        sum += dataArray[i];
    }
    const average = sum / bufferLength;

    // Threshold: 10 is usually good for background noise vs speaking
    if (average > 10) {
        // You are speaking! Reset the "stop" timer.
        resetSilenceTimer();
    }

    // Keep checking every frame (approx 60 times a second)
    animationFrameRequest = requestAnimationFrame(detectVoiceActivity);
}

function pauseReading() {
    if (mediaRecorder && isReading) {
        mediaRecorder.stop();
        stopWebcam();
        isReading = false;
        
        // Stop the timers and loops
        clearTimeout(silenceTimer);
        cancelAnimationFrame(animationFrameRequest);
        
        startReadingBtn.disabled = false;
        pauseReadingBtn.disabled = true;
        startReadingBtn.textContent = '🎙️ Start Reading';
    }
}

function resetSilenceTimer() {
    clearTimeout(silenceTimer);
    silenceTimer = setTimeout(() => {
        if (isReading) {
            pauseReading(); // Auto-stop
            console.log(" Recording stopped due to silence.");
            alert("Recording stopped because we didn't hear you for 5 seconds.");
        }
    }, 5000); // 5 seconds silence limit
}

async function analyzeReading(audioBlob) {
    const formData = new FormData();
    // Send the blob as a file named "recording.webm"
    formData.append('audio', audioBlob, 'recording.webm'); 
    formData.append('expected_text', currentPassageText);
    
    try {
        accuracyDisplay.textContent = '...';
        
        const response = await fetch(`${API_BASE}/analyze-speech`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.analysis) {
            updatePerformanceMetrics(data.analysis);
        } else {
             console.error("Backend returned no analysis:", data);
             accuracyDisplay.textContent = 'Err';
        }
        
    } catch (error) {
        console.error('Error analyzing reading:', error);
        accuracyDisplay.textContent = 'Err';
    }
}

function updatePerformanceMetrics(analysis) {
    accuracyDisplay.textContent = Math.round(analysis.accuracy_score) + '%';
    fluencyDisplay.textContent = Math.round(analysis.fluency_score) + '%';
    wordsReadDisplay.textContent = analysis.correct_words + '/' + analysis.total_words;
}

async function getHint() {
    try {
        const response = await fetch(`${API_BASE}/get-support`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                text: currentPassageText, 
                support_type: 'hints' 
            })
        });

        const data = await response.json();

        if (data.hints) {
            let msg = '💡 Pronunciation Hints:\n\n';
            for (const [word, hint] of Object.entries(data.hints)) {
                msg += `🔹 ${word}: ${hint.tip}\n`;
            }
            alert(msg);
        }
    } catch (error) {
        console.error('Error getting hints:', error);
    }
}

async function getMentorFeedback() {
    try {
        const accVal = parseInt(accuracyDisplay.textContent) || 0;

        const response = await fetch(`${API_BASE}/get-mentor-feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                performance_data: { accuracy: accVal },
                learner_age: 'teen',
                personality: 'friendly'
            })
        });
        
        const data = await response.json();
        
        mentorFeedback.innerHTML = `
            <div style="background:#f0f9ff; padding: 15px; border-radius: 8px; border-left: 4px solid #2180E8;">
                <p style="font-size: 1.1em; color:#2180E8;"><strong>${data.encouragement}</strong></p>
                <hr style="border: 0; border-top: 1px solid rgba(221, 221, 221, 1); margin: 10px 0;">
                <p><strong> Insights:</strong></p>
                <ul>${data.insights.map(i => `<li>${i}</li>`).join('')}</ul>
                <p><strong> Recommendations:</strong></p>
                <ul>${data.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>
            </div>
        `;
        
    } catch (error) {
        console.error('Error getting mentor feedback:', error);
    }
}

async function endSession() {
    try {
        const response = await fetch(`${API_BASE}/end-session`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        const summaryText = data.summary || "Session ended successfully.";
        
        alert('📋 SESSION SUMMARY:\n\n' + summaryText);
        
        loadPassage(); 
        accuracyDisplay.textContent = '0%';
        fluencyDisplay.textContent = '0%';
        wordsReadDisplay.textContent = '0';
        mentorFeedback.innerHTML = '<p>Your personalized feedback will appear here...</p>';
        
    } catch (error) {
        console.error('Error ending session:', error);
    }
    stopWebcam();
}

function stopWebcam() {
    const video = document.getElementById('webcamFeed');
    if (video && video.srcObject) {
        const tracks = video.srcObject.getTracks();
        tracks.forEach(track => track.stop()); // Stops the camera light
        video.srcObject = null;
    }
}
