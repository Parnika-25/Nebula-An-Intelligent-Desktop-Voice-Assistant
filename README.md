# ✅ Nebula – An Intelligent Desktop Voice Assistant Using Cloud-Based Speech Recognition and System Control

---

## 📌 Project Overview

**Nebula** is an intelligent, modular desktop voice assistant designed to automate and control system-level operations using **natural voice commands**. Unlike traditional assistants that rely on fixed wake-word engines, Nebula uses a **session-based architecture** powered by **cloud-based speech recognition** to deliver high accuracy, flexibility, and stability.

Nebula can open and close applications, control system volume, manage power operations, and respond to user commands in a conversational manner — all running locally on a desktop system with cloud-assisted speech processing.

---

## 🎯 Key Objectives

* Enable hands-free control of desktop applications using voice
* Provide high-accuracy speech recognition using cloud-based STT (AssemblyAI)
* Design a scalable, modular, and maintainable system architecture
* Support real-world desktop automation use cases
* Ensure safety and reliability for system-level actions

---

## 🧠 System Architecture

Nebula follows a **layered, event-driven architecture** with clear separation of concerns.

### 🔹 High-Level Architecture

```
User (Microphone)
        ↓
Cloud-Based Speech Recognition (AssemblyAI)
        ↓
Session Controller (WakeListener)
        ↓
NLP Layer (Language Detection + Intent Parsing)
        ↓
Action Layer (System & Application Control)
        ↓
Operating System (Windows)
```

---

### 🔹 Detailed Component Architecture

```
main.py (Application Entry Point)
        │
        ▼
WakeListener (Session Controller)
        │
        ├── AssemblyAI Engine (Speech-to-Text)
        ├── TTS Engine (Speech Output)
        │
        ▼
NLP Layer
        ├── Language Detector
        └── Intent Parser
        │
        ▼
Action Layer
        ├── Application Indexer (Start Menu Scan)
        ├── Open / Close Applications
        ├── Volume Control
        └── Power Management
        │
        ▼
Windows Operating System
```

---

## 🧱 Module Description

### 1️⃣ Entry Point

**File:** `nebula/main.py`

* Initializes the Nebula backend
* Starts the voice session automatically
* Spawns background listening threads

---

### 2️⃣ Speech-to-Text (STT)

**File:** `nebula/stt/assemblyai_engine.py`

* Records microphone audio
* Sends audio to AssemblyAI cloud API
* Receives high-quality transcribed text
* Session-based recording to avoid continuous listening

---

### 3️⃣ Session Controller

**File:** `nebula/wake/wake_listener.py`

* Controls listening lifecycle
* Starts listening session on application launch
* Stops listening when user says *"stop listening"*
* Routes recognized text to NLP and action layers

---

### 4️⃣ Natural Language Processing (NLP)

#### a) Language Detection

**File:** `nebula/nlp/lang_detector.py`

* Detects spoken language (English / Telugu)
* Enables multilingual expansion

#### b) Intent Parsing

**File:** `nebula/nlp/intent_parser.py`

* Converts raw text into structured intents
* Rule-based system for safety and determinism

Example:

```json
{
  "intent": "system",
  "action": "open",
  "app": "chrome"
}
```

---

### 5️⃣ Action Layer

**File:** `nebula/actions/app_actions.py`

* Dynamically indexes installed applications
* Opens applications using Start Menu shortcuts or system executables
* Closes applications using process inspection (`psutil`)
* Controls system volume
* Handles shutdown and restart commands

---

### 6️⃣ Text-to-Speech (TTS)

**File:** `nebula/tts/tts_engine.py`

* Converts assistant responses into speech
* Thread-safe implementation to avoid audio overlap

---

### 7️⃣ Logging System

**File:** `nebula/logger.py`

* Centralized logging mechanism
* Helps with debugging and runtime monitoring

---

## 🔁 End-to-End Workflow

Example command: **"Open Chrome"**

1. Microphone captures audio
2. AssemblyAI transcribes audio into text
3. Session Controller receives text
4. NLP module detects intent
5. Action layer opens Chrome
6. TTS confirms the action

---

## 🧪 Supported Features

* Open any installed desktop application
* Close any running desktop application
* Control system volume (up / down / mute)
* System power operations (shutdown / restart)
* Continuous voice session
* Safe termination via voice command

---

## 🛠️ Technologies Used

* **Programming Language:** Python 3.10
* **Speech-to-Text:** AssemblyAI (Cloud-based)
* **Text-to-Speech:** pyttsx3
* **Process Control:** psutil
* **Audio Recording:** sounddevice
* **Operating System:** Windows

---

## 🔐 Security & Safety

* API keys stored as environment variables
* No system-critical operations without explicit user intent
* Rule-based command parsing prevents accidental execution

---

## 🚀 Future Enhancements

* System tray integration
* Hotkey-based session triggering
* GUI / Electron frontend
* Telugu voice command expansion
* Screen reading & vision support
* Plugin architecture for extensibility
* EXE packaging for end-user deployment

---

## 📌 Conclusion

Nebula demonstrates a **real-world desktop AI assistant architecture** that combines cloud intelligence with local system automation. The project emphasizes correctness, modularity, and scalability, making it suitable for academic evaluation, research, and future product development.

---

> **Nebula – Speak. Control. Automate.**

1. Wake Phrase System

✔ Custom wake phrase: “nebula wakeup”
✔ Custom greeting: “whatsup boss”
✔ Ultra-fast wake detection
✔ English + Telugu wake phrase support
✔ Background wake listening
✔ Smart noise filtering
✔ Low-power mode when idle

✅ 2. Multilingual AI (English + Telugu)

✔ Telugu voice commands (file actions, music, system controls)
✔ English commands
✔ Auto language detection
✔ Replies in the same language you speak
✔ Telugu & English logs
✔ Option to force language from settings

✅ 3. Advanced Music Control

✔ Play/Pause
✔ Next/Previous
✔ Volume Up/Down
✔ Mute
✔ App automation:

Spotify

YouTube

VLC
✔ Playlist detection
✔ Smart music mode (learns preferences)

✅ 4. Full Screen Reading & Vision

✔ Take screenshots
✔ Extract text from screen
✔ Full-screen description using AI
✔ Understand visual UI elements
✔ Action-based vision:

"Click the blue button"

"Scroll down"

"Open the second file"
✔ Multi-monitor support

✅ 5. Futuristic Sci-Fi UI

✔ Animated hologram orb (Nebula Core)
✔ Live voice-reactive waveform
✔ Neon gradients & glow effects
✔ Smooth transitions & blur
✔ Floating holographic panels
✔ Modern settings panel
✔ Multilingual UI
✔ Minimized/tray icon mode
✔ Dark/Cyberpunk theme

✅ 6. Logs & Activity History (Advanced Mode)

✔ Records every command you speak
✔ Timestamp
✔ What Nebula executed
✔ Screenshot thumbnails
✔ System errors
✔ UI panel with timeline view
✔ Export logs to file
✔ Auto cleanup
✔ Search/filter commands

✅ 7. Background Mode (Professional Mode)

✔ Nebula runs silently after startup
✔ Tray icon control
✔ Auto-start on system boot
✔ Smart sleep mode
✔ Wake phrase always active
✔ Option to disable wake listening from tray
✔ Low CPU usage mode

✅ 8. App & System Automation

✔ Open / Close applications
✔ Adjust Brightness
✔ Shutdown / Restart / Sleep
✔ Network actions (WiFi on/off)
✔ File explorer commands
✔ Browser automation
✔ Auto-click & keyboard macros

✅ 9. Chat + AI Assistant

✔ Ask questions
✔ Explain code
✔ Translate English ↔ Telugu
✔ Tell jokes, stories
✔ General chat
✔ Motivation mode
✔ AI text answers in UI + voice

✅ 10. Installer + Desktop Application

✔ Nebula Setup.exe
✔ Desktop shortcut
✔ Auto-update
✔ Auto-run
✔ Secure packaged backend
✔ Electron + Python combined