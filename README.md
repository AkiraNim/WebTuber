🎙️ Audio-Reactive Web VTuber (PNGTuber)
A lightweight, browser-based VTuber/PNGTuber avatar that reacts to your microphone volume in real-time. Built entirely with HTML, CSS, and Vanilla JavaScript, it requires no complex software, no heavy AI models, and no background processes.

Perfect for streamers and content creators looking for an easy, resource-friendly avatar that works seamlessly with OBS Studio!

✨ Features
Real-Time Audio Tracking: Uses the browser's native Web Audio API to detect microphone input with zero lag.

Proportional Frame Animation: Smoothly transitions between multiple frames (e.g., 11 states from closed to wide open) based exactly on how loud you speak.

In-Browser Calibration: See your live volume levels on the screen to easily adjust sensitivity.

OBS Ready: Designed specifically to be used as a Browser Source in OBS Studio with a native transparent background.

No Backend Required: Runs 100% locally in your browser.

🚀 How to Use
Prepare your frames: Extract or draw your avatar frames (e.g., frame_1.png to frame_11.png).

Organize: Place your images in the project folder (or an images/ subfolder) and update the file paths in the script.js array.

Open the App: Open index.html in your web browser.

Allow Microphone: Click the "Start Microphone" button and grant the browser permission to listen.

Calibrate: Speak normally and look at the volume numbers on the screen. Adjust the minVolume and maxVolume variables inside script.js to match your specific microphone's sensitivity.

🎥 Using with OBS Studio
Open OBS Studio and add a new Browser Source.

Check the box for "Local file" and browse to find your index.html file.

Set your desired width and height (e.g., 800x800).

Important: Ensure OBS has permission to use your microphone. The avatar will automatically load with a transparent background and react to your voice on stream!

🛠️ Built With
HTML5

CSS3 (Configured for OBS Transparency)

Vanilla JavaScript (Web Audio API)
