"""
================================================================
  ULTRA AIR COMMAND CONSOLE (PRO EDITION)
  Author: Antigravity AI
  Features: OneEuro Smoothing, Blendshape Emotions, 
            Interpolated Drawing, Threaded Capture.
================================================================
"""

import cv2
import numpy as np
import math
import time
import platform
import subprocess
import os
import urllib.request
import threading
from collections import deque
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ─────────────────────────────────────────────
#  ONE EURO FILTER (Signal Smoothing)
# ─────────────────────────────────────────────

class OneEuroFilter:
    def __init__(self, min_cutoff=1.0, beta=0.007, d_cutoff=1.0):
        self.min_cutoff, self.beta, self.d_cutoff = min_cutoff, beta, d_cutoff
        self.x_prev, self.dx_prev, self.t_prev = None, 0, None

    def __call__(self, x, t=None):
        t = time.time() if t is None else t
        if self.x_prev is None:
            self.x_prev, self.t_prev = x, t
            return x
        te = t - self.t_prev
        if te <= 0: return self.x_prev
        ad = 1.0 / (1.0 + 2 * math.pi * te * self.d_cutoff)
        dx = (x - self.x_prev) / te
        dx_hat = ad * dx + (1 - ad) * self.dx_prev
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = 1.0 / (1.0 + 2 * math.pi * te * cutoff)
        x_hat = a * x + (1 - a) * self.x_prev
        self.x_prev, self.dx_prev, self.t_prev = x_hat, dx_hat, t
        return x_hat

# ─────────────────────────────────────────────
#  THREADED CAPTURE (Performance)
# ─────────────────────────────────────────────

class ThreadedCamera:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.running = False
        self.cap.release()

# ─────────────────────────────────────────────
#  MODULAR MODULES
# ─────────────────────────────────────────────

class DrawingEngine:
    def __init__(self, shape):
        self.canvas = np.zeros(shape, dtype=np.uint8)
        self.prev_pt = None
        self.color = (255, 180, 0) # Neon Cyan

    def update(self, pt, active):
        if not active or pt is None:
            self.prev_pt = None
            return
        if self.prev_pt is not None:
            # Interpolation for silky lines
            dist = math.hypot(pt[0]-self.prev_pt[0], pt[1]-self.prev_pt[1])
            thickness = int(np.interp(dist, [2, 50], [12, 18]))
            cv2.line(self.canvas, self.prev_pt, pt, self.color, thickness, cv2.LINE_AA)
        self.prev_pt = pt

    def get_blended(self, frame):
        # Convert canvas to grayscale for masking
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Use bitwise operations for robust blending
        bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        
        return cv2.add(bg, fg)

class EmotionProcessor:
    def __init__(self, model_path):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options, output_face_blendshapes=True, num_faces=1)
        self.detector = vision.FaceLandmarker.create_from_options(options)
        self.current_emotion = "Neutral"
        self.emotion_score = 0
        self.start_time = 0
        self.cooldown = 0
        self.face_rect = None

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        
        self.face_rect = None
        if res.face_landmarks and res.face_blendshapes:
            lms = res.face_landmarks[0]
            shapes = {s.category_name: s.score for s in res.face_blendshapes[0]}
            
            # Extract Face Box
            x_min = int(min(l.x for l in lms) * frame.shape[1])
            y_min = int(min(l.y for l in lms) * frame.shape[0])
            x_max = int(max(l.x for l in lms) * frame.shape[1])
            y_max = int(max(l.y for l in lms) * frame.shape[0])
            self.face_rect = (x_min, y_min, x_max, y_max)

            # Emotion Logic (ML Blendshapes)
            smile = (shapes.get('mouthSmileLeft', 0) + shapes.get('mouthSmileRight', 0)) / 2
            surprised = shapes.get('jawOpen', 0)
            
            if smile > 0.6: self.current_emotion, self.emotion_score = "Happy", smile
            elif surprised > 0.5: self.current_emotion, self.emotion_score = "Surprised", surprised
            else: self.current_emotion, self.emotion_score = "Neutral", 0

class HolographicMenu:
    def __init__(self):
        self.options = ["VOLUME", "BRIGHTNESS", "AIR DRAW", "EMOTION", "CLEAR ALL"]
        self.is_open = False
        self.pos = (0, 0)
        self.hover_idx = -1
        self.width = 240
        self.h_item = 50

    def update(self, cursor, pinching):
        if not self.is_open:
            if pinching:
                self.is_open = True
                self.pos = (cursor[0] - 120, cursor[1] - 25)
            return None

        x, y = self.pos
        self.hover_idx = -1
        for i in range(len(self.options)):
            iy = y + i * self.h_item
            if x < cursor[0] < x + self.width and iy < cursor[1] < iy + self.h_item:
                self.hover_idx = i
                break
        
        if not pinching:
            choice = self.options[self.hover_idx] if self.hover_idx != -1 else None
            self.is_open = False
            return choice
        return None

    def draw(self, frame):
        if not self.is_open: return
        x, y = self.pos
        # Lightweight Menu (No heavy blending)
        cv2.rectangle(frame, (x, y), (x + self.width, y + len(self.options)*self.h_item), (20, 20, 20), -1)
        cv2.rectangle(frame, (x, y), (x + self.width, y + len(self.options)*self.h_item), (255, 200, 0), 2)

        for i, opt in enumerate(self.options):
            iy = y + i*self.h_item
            is_hover = (i == self.hover_idx)
            if is_hover:
                cv2.rectangle(frame, (x+2, iy+2), (x+self.width-2, iy+self.h_item-2), (80, 60, 0), -1)
            
            cv2.putText(frame, opt, (x + 30, iy + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

class ProConsole:
    def __init__(self):
        self.h_model = "hand_landmarker.task"
        self.f_model = "face_landmarker.task"
        self._check_models()

        self.hand_detector = vision.HandLandmarker.create_from_options(
            vision.HandLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=self.h_model)))
        
        self.emotions = EmotionProcessor(self.f_model)
        self.menu = HolographicMenu()
        self.canvas = None
        self.mode = "IDLE"
        
        self.f_x, self.f_y = OneEuroFilter(), OneEuroFilter()
        self.f_val = OneEuroFilter(0.5, 0.01)
        self.pct = 50
        
        self.spotify_triggered = False
        self.trigger_time = 0

    def _check_models(self):
        urls = {
            self.h_model: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
            self.f_model: "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
        }
        for path, url in urls.items():
            if not os.path.exists(path): urllib.request.urlretrieve(url, path)

    def run(self):
        cam = ThreadedCamera(0)
        p_time = time.time()
        
        while True:
            ret, frame = cam.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            if self.canvas is None: self.canvas = DrawingEngine(frame.shape)

            # 1. Hands (Main Loop - High Frequency)
            h_res = self.hand_detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, 
                                                      data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            
            fingers = -1
            cursor = None
            pinching = False

            if h_res.hand_landmarks:
                l = h_res.hand_landmarks[0]
                cx = int(self.f_x(l[8].x * w)); cy = int(self.f_y(l[8].y * h))
                cursor = (cx, cy)
                dist = math.hypot(l[4].x-l[8].x, l[4].y-l[8].y) * w
                pinching = dist < 35
                
                # Finger Logic
                f_count = 0
                if l[4].x < l[3].x: f_count += 1
                for t, p in [(8,6), (12,10), (16,14), (20,18)]:
                    if l[t].y < l[p].y: f_count += 1
                fingers = f_count

                # Menu logic (ONLY way to switch modes now)
                choice = self.menu.update(cursor, pinching)
                if choice:
                    if choice == "CLEAR ALL": self.mode = "IDLE"; self.canvas.canvas[:] = 0
                    else: self.mode = choice

                # Actions (Active only if menu is closed)
                if not self.menu.is_open:
                    if self.mode in ["VOLUME", "BRIGHTNESS"]:
                        self.pct = self.f_val(np.interp(dist, [35, 230], [0, 100]))
                        if self.mode == "VOLUME" and platform.system() == "Darwin":
                            subprocess.run(["osascript", "-e", f"set volume output volume {int(self.pct)}"], capture_output=True)
                    elif self.mode == "AIR DRAW":
                        # Fixed string mismatch: AIR DRAW instead of DRAWING
                        self.canvas.update(cursor, fingers == 1)

            # 2. Emotions (Sub-frequency / Selective)
            if self.mode == "EMOTION" or fingers == 5: # Auto-check in volume/palm or manual
                self.emotions.process(frame)
                if self.emotions.face_rect:
                    x1, y1, x2, y2 = self.emotions.face_rect
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{self.emotions.current_emotion}", (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Spotify Trigger Logic
                if self.emotions.current_emotion in ["Happy", "Surprised"]:
                    if not self.spotify_triggered and time.time() - self.trigger_time > 15: # Cooldown 15s
                        self.spotify_triggered = True
                        self.trigger_time = time.time()
                
                if self.spotify_triggered:
                    cv2.rectangle(frame, (w//2-200, h-80), (w//2+200, h-20), (20, 20, 20), -1)
                    cv2.putText(frame, f"PLAYING {self.emotions.current_emotion} MIX...", (w//2-160, h-40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)
                    if time.time() - self.trigger_time > 2.0: # Persist for 2s then open
                        subprocess.run(["open", f"https://open.spotify.com/search/{self.emotions.current_emotion}"])
                        self.spotify_triggered = False

            # 3. UI Layer
            frame = self.canvas.get_blended(frame)
            self.menu.draw(frame)
            
            if cursor:
                cv2.circle(frame, cursor, 12, (255,255,255), 2)
                cv2.circle(frame, cursor, 4, (0, 255, 170), -1)

            # HUD Dashboard
            cv2.rectangle(frame, (0, 0), (w, 70), (10, 10, 10), -1)
            cv2.putText(frame, f"SYSTEM: {self.mode}", (40, 45), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 170), 2)
            fps = 1.0 / max(time.time() - p_time, 0.001)
            p_time = time.time()
            cv2.putText(frame, f"FPS: {int(fps)}", (w-150, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

            if self.mode in ["VOLUME", "BRIGHTNESS"]:
                cv2.rectangle(frame, (40, 100), (340, 120), (40, 40, 40), -1)
                cv2.rectangle(frame, (40, 100), (40 + int(self.pct*3), 120), (0, 255, 170), -1)
                cv2.putText(frame, f"{int(self.pct)}%", (360, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

            cv2.imshow("Pro Console Ultra", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        
        cam.stop(); cv2.destroyAllWindows()

if __name__ == "__main__":
    ProConsole().run()
