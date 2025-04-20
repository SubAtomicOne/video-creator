# 🎬 Offline AI Video Generator

**Offline AI Video Generator** is a modular pipeline that automatically creates short-form videos using local AI models. It combines multiple components—language generation, text-to-speech, image generation, subtitle alignment, and video rendering—into a fully offline workflow.

Ideal as a demonstration of practical AI integration, media generation, and automation systems in a real-world scenario.

---

## 📌 Key Features

- 🔒 **Fully Offline Workflow**  
  No internet connection required. All models run locally for maximum privacy and portability.

- 🧠 **Content Generation**  
  Uses a local LLM (e.g., via [Ollama](https://ollama.com/)) to generate the video script and associated image prompts.

- 🎙 **Text-to-Speech (TTS)**  
  Converts generated text into natural-sounding audio using [Coqui TTS](https://github.com/coqui-ai/TTS).

- 🖼 **Image Generation**  
  Creates images from prompts using Stable Diffusion models (e.g., `Realistic_Vision_V5.1_noVAE`).

- 📝 **Subtitle Generation**  
  Aligns speech with text using Whisper or whisper.cpp to create subtitle tracks.

- 🎞 **Video Composition**  
  Assembles images, audio, subtitles, and background music into a final MP4 video.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/offline-ai-video-generator.git
cd offline-ai-video-generator
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download & Configure Models
```bash
ollama run ollama3.2
```

### 5. Usage
```bash
cd video-creator
python main.py
```