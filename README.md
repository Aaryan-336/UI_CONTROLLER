# 🛸 Ultra Air Command Console (Pro Edition)

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0+-green.svg?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-teal.svg?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)

> A professional-grade, real-time computer vision interface for gesture-based system control, air drawing, and emotion-driven automation.

---

## ✨ Key Features

-   **🛸 Holographic Air Menu**: Pinch to summon a lightweight, futuristic selection wheel for quick mode switching.
-   **🎭 ML Blendshape Emotions**: Real-time facial emotion recognition using MediaPipe's professional blendshape scores (Happy, Surprised, Neutral).
-   **🖊️ Smooth Air Drawing**: Professional-grade sketching with OneEuro signal filtering and tapered, interpolated lines.
-   **🔊 System Control**: Precision volume and brightness adjustment via gesture-based absolute mapping.
-   **⚡ Pro-Performance Architecture**: Threaded camera capture and optimized ML pipelines ensuring 30+ FPS stability.
-   **🎵 Spotify Integration**: Automatically triggers customized Spotify playlists based on your detected emotions.

---

## 🎮 Gesture Controls

| Gesture | Action |
| :--- | :--- |
| **Pinch (Thumb + Index)** | Summon/Select from Air Menu |
| **1 Finger (Index Up)** | Draw in Air (while in Air Draw mode) |
| **5 Fingers (Palm)** | Direct Volume Mode / Face Tracking |
| **Fist (Closed Hand)** | Reset / Clear Canvas / Idle Mode |
| **Smile / Surprise** | Trigger Emotion-based Spotify Mix |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have **Python 3.14+** installed. The system is optimized for macOS but supports cross-platform environments.

### 2. Installation
Clone the repository and run the automated setup script:
```bash
git clone https://github.com/Aaryan-336/UI_CONTROLLER.git
cd UI_CONTROLLER
chmod +x setup_and_run.sh
./setup_and_run.sh
```

---

## 🛠️ Tech Stack

-   **Core Engine**: Python 3.14
-   **Computer Vision**: OpenCV, MediaPipe Tasks
-   **Signal Processing**: OneEuro Filter for ultra-smooth tracking
-   **System Interaction**: AppleScript (macOS), Subprocess API
-   **UI/UX**: Custom bitwise-blended holographic overlays

---

## 📸 Usage Tips
-   **Switching Cameras**: Press the **'C'** key in the app window to toggle between your built-in webcam and external/iPhone cameras.
-   **Exiting**: Press **'Q'** or **ESC** to safely close the application.
-   **Clearing Drawing**: Use the **Fist** gesture or select **CLEAR ALL** from the Air Menu.

---

Developed with ❤️ by **Antigravity AI** for **Aaryan Khanna**.
