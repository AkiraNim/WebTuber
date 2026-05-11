import cv2
import mediapipe as mp
import asyncio
import websockets
import threading
import json
import sys

import mediapipe.python.solutions.face_mesh as mp_face_mesh
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.drawing_styles as mp_drawing_styles

# --- Global State Variable ---
current_vtuber_data = {"level": 0.0}

# --- WebSocket Server Setup ---
async def state_sender(websocket):
    global current_vtuber_data
    try:
        while True:
            message = json.dumps(current_vtuber_data)
            await websocket.send(message)
            await asyncio.sleep(0.03) # 30+ FPS updates
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
print("A camera window will open. Press 'q' on the window to quit.")
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
                
                # --- DRAWING THE LANDMARKS ---
                # 1. Draws the face mesh "spider web"
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                
                # 2. Draws bold outlines around the lips and eyes
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )
                # -----------------------------
                
                upper_lip = face_landmarks.landmark[13].y
                lower_lip = face_landmarks.landmark[14].y
                mouth_distance = lower_lip - upper_lip
                
                # --- CALIBRATION LIMITS ---
                min_mouth = 0.002 # Distance when completely closed
                max_mouth = 0.025 # Distance when wide open
                
                clamped_dist = max(min_mouth, min(mouth_distance, max_mouth))
                mouth_level = (clamped_dist - min_mouth) / (max_mouth - min_mouth)
                
                current_vtuber_data["level"] = mouth_level

                # Add text directly to the camera window for easy calibration
                cv2.putText(frame, f"Mouth Level: {mouth_level:.2f} (0 to 1)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Raw Dist: {mouth_distance:.4f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Show the camera window
        cv2.imshow('VTuber Tracker - Press Q to quit', frame)

        # Listen for the 'q' key to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nShutting down VTuber Brain...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)