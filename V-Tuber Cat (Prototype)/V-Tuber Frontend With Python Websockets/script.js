const avatarImg = document.getElementById('avatar');

// Array containing all 11 frames from fully closed to fully open.
// IMPORTANT: Make sure the file names exactly match the images in your folder!
const frames = [
    "../Cato/idle.png",  // Index 0: Fully closed
    "../Cato/frame_2.png", 
    "../Cato/frame_3.png", 
    "../Cato/frame_4.png",
    "../Cato/frame_5.png", 
    "../Cato/frame_6.png", 
    "../Cato/frame_7.png", 
    "../Cato/frame_8.png",
    "../Cato/frame_9.png", 
    "../Cato/frame_10.png", 
    "../Cato/frame_11.png"  // Index 10: Fully open
];

// --- THE BRIDGE (WEBSOCKET CONNECTION) ---
const socket = new WebSocket('ws://localhost:8765');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    // Python will now send a "level" between 0.0 (closed) and 1.0 (wide open)
    if (data.level !== undefined) {
        
        // Map the 0.0 -> 1.0 level to our array indexes (0 to 10)
        let frameIndex = Math.floor(data.level * (frames.length - 1));
        
        // Failsafe: Ensure the index never goes below 0 or above 10
        frameIndex = Math.max(0, Math.min(frameIndex, frames.length - 1));
        
        // Update the image source instantly to match your mouth
        avatarImg.src = frames[frameIndex];
    }
};

socket.onopen = function() {
    console.log("Successfully connected to the Python Brain (Tracking Mode)!");
};

socket.onclose = function() {
    console.log("Disconnected from Python Brain.");
    // Force the mouth closed if the connection drops
    avatarImg.src = frames[0]; 
};