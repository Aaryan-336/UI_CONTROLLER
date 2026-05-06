#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
#  Gesture Volume Control — One-shot Setup & Run Script
#  Works on macOS, Linux, and Windows (Git Bash / WSL)
# ─────────────────────────────────────────────────────────

set -e  # Exit immediately on any error

echo "╔══════════════════════════════════════════════╗"
echo "║    Gesture Volume Control — Setup & Run      ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 not found. Install from https://python.org (3.9+)"
    exit 1
fi
PY=$(python3 --version)
echo "[OK] $PY detected"

# 2. Create virtual environment if it doesn't already exist
if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment in .venv/ ..."
    python3 -m venv .venv
    echo "[OK]  Virtual environment created"
else
    echo "[OK]  Existing .venv found — reusing it"
fi

# 3. Activate venv  (works on macOS/Linux; Git Bash on Windows uses the same path)
# shellcheck disable=SC1091
source .venv/bin/activate
echo "[OK]  Virtual environment activated"

# 4. Upgrade pip quietly
pip install --upgrade pip -q

# 5. Install core dependencies
echo "[INFO] Installing / verifying: opencv-python  mediapipe  numpy ..."
pip install opencv-python mediapipe numpy -q
echo "[OK]  All dependencies ready"

# ── OPTIONAL platform extras ──────────────────────────────
#   macOS  : osascript is built-in — no extra packages needed
#   Windows: uncomment the next line for real volume control via pycaw
# pip install pycaw comtypes -q
#   Linux  : ensure 'amixer' is available: sudo apt install alsa-utils
# ─────────────────────────────────────────────────────────

echo ""
echo "[READY] Launching…"
echo "        👍  Pinch thumb + index finger to adjust volume"
echo "        ✋  Spread fingers wide  → 100%"
echo "        🤏  Pinch fully closed  →   0%"
echo "        ⌨️   Press  Q  or  ESC  to quit"
echo ""

python3 gesture_volume_control.py
