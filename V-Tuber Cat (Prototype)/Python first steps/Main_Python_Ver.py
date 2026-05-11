import cv2
import mediapipe as mp
import asyncio
import websockets
import threading
import json
import sys

import mediapipe.python.solutions.face_mesh as mp_face_mesh

# --- Global State Variable ---
# We now store the mouth level (0.0 to 1.0) instead of a text string
current_vtuber_data = {"level": 0.0}

# --- WebSocket Server Setup ---
async def state_sender(websocket):
    global current_vtuber_data
    try:
        while True:
            # Send the continuous mouth level to JavaScript
            message = json.dumps(current_vtuber_data)
            await websocket.send(message)
            await asyncio.sleep(0.03) # Updated to run faster for smoother animation (30+ FPS)
    except websockets.exceptions.ConnectionClosed:
        pass 

async def run_server():
    async with websockets.serve(state_sender, "localhost", 8765):
        await asyncio.Future()  

def start_websocket_thread():
    asyncio.run(run_server())

ws_thread = threading.Thread(target=start_websocket_thread, daemon=True)
ws_thread.start()
print("WebSocket Server Started! Proportional tracking is ACTIVE.")
print("Press Ctrl+C in this terminal to stop the program.")
# ------------------------------

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                upper_lip = face_landmarks.landmark[13].y
                lower_lip = face_landmarks.landmark[14].y
                mouth_distance = lower_lip - upper_lip
                
                # --- CALIBRATION LIMITS ---
                # Adjust these two numbers based on your face/camera!
                min_mouth = 0.002 # The distance when your mouth is completely closed
                max_mouth = 0.025 # The distance when your mouth is wide open (Frame 11)
                
                # 1. Clamp the distance so it doesn't break the math if you open wider than max
                clamped_dist = max(min_mouth, min(mouth_distance, max_mouth))
                
                # 2. Calculate the percentage (from 0.0 to 1.0)
                mouth_level = (clamped_dist - min_mouth) / (max_mouth - min_mouth)
                
                # UPDATE GLOBAL STATE
                current_vtuber_data["level"] = mouth_level

except KeyboardInterrupt:
    print("\nShutting down VTuber Brain...")

finally:
    cap.release()
    sys.exit(0)