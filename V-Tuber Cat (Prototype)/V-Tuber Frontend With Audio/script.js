const avatarImg = document.getElementById('avatar');
const startBtn = document.getElementById('start-btn');
// --- VOLUME DISPLAY REFERENCE REMOVED ---

// Your 11 frames (ensure paths are correct!)
const frames = [
    "../Cato/idle.png", "../Cato/frame_2.png", "../Cato/frame_3.png", "../Cato/frame_4.png",
    "../Cato/frame_5.png", "../Cato/frame_6.png", "../Cato/frame_7.png", "../Cato/frame_8.png",
    "../Cato/frame_9.png", "../Cato/frame_10.png", "../Cato/frame_11.png"
];

// --- CALIBRATION SETTINGS ---
// Adjust these based on your microphone's sensitivity!
const minVolume = 5;   // The background noise level (when you are silent)
const maxVolume = 60;  // The volume when you are talking loudly

let audioContext;
let analyser;
let microphone;
let dataArray;

// 1. Ask for Microphone Permission and Start Listening
startBtn.addEventListener('click', async () => {
    try {
        // Request mic access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Setup Web Audio API
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256; // Defines how detailed the audio analysis is
        
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
        
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        
        // Hide the button once started
        startBtn.style.display = 'none';
        
        // Start the animation loop
        updateAvatar();
        
    } catch (err) {
        console.error("Microphone access denied or error:", err);
        alert("Please allow microphone access to use the VTuber!");
    }
});

// 2. The Animation Loop (Runs 60 times per second)
function updateAvatar() {
    // Tell the browser to run this function again on the next frame
    requestAnimationFrame(updateAvatar);
    
    // Get the current audio data
    analyser.getByteFrequencyData(dataArray);
    
    // Calculate the average volume
    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
    }
    let currentVolume = sum / dataArray.length;
    
    // --- UPDATE TEXT ON SCREEN REMOVED ---
    
    // 3. Map the volume to the frames (0 to 10)
    // Clamp the volume so it doesn't break the math
    let clampedVol = Math.max(minVolume, Math.min(currentVolume, maxVolume));
    
    // Convert to a percentage (0.0 to 1.0)
    let audioLevel = (clampedVol - minVolume) / (maxVolume - minVolume);
    
    // Pick the correct frame based on the percentage
    let frameIndex = Math.floor(audioLevel * (frames.length - 1));
    
    // Safety check
    frameIndex = Math.max(0, Math.min(frameIndex, frames.length - 1));
    
    // Change the image instantly
    avatarImg.src = frames[frameIndex];
}

// Attempt to auto-start the microphone when the page loads
window.addEventListener('load', () => {
    startBtn.click();
});