# Forked Video Creator

This is a customized fork of the original `video-creator` project, enhanced with features such as:

- ✅ **Automatic uploading to TikTok and YouTube Shorts**
- 🎵 **Custom background music** to avoid copyright strikes
- 🧩 Minor adjustments to better suit personal workflow
- 🤖 AI video **description and Title** genorator
- Better LLM for content Generation along with a MUCH better sounding TTS for audio

> ⚠️ Note: `requirements.txt` may be incomplete or broken. I recommend using it to install most dependencies and manually installing any that fail. I used Python 3.10.

---

## 🔐 Setup Overview

### YouTube Auto Upload (Google OAuth2)
To enable automatic YouTube uploads, you must configure Google OAuth:

1. Create a **Google Cloud Project** and enable the **YouTube Data API v3**.
2. Create an OAuth 2.0 Client and download:
   - `client_secrets.json`
   - After first-time auth: `upload_video.py-oauth2.json`
3. Refer to Google's [OAuth setup docs](https://developers.google.com/youtube/registering_an_application) for detailed instructions.

### TikTok Auto Upload
TikTok uploading requires authenticated cookies:

1. Install the **Cookie-Editor** Chrome extension.
2. Log in to TikTok via browser.
3. Export your session cookies as a `.json` file (e.g., `tiktok_cookies.json`).
4. Follow the TikTok API docs for further help if needed.


### Run All Together
- Simply run the 'run_pipeline.sh' and it will run all files needed, it is recomended to run 'main.py' first before doing this as you may be asked to upload certain details for the first time by the TikTok Uploader.
- Outputs will be stored into a folder called 'error', file names are **Year Month Day Time**.
- I have it scheduled to run on my home server in a linux container to run multiple times a day via Cron Job so it is all automated.

---

## 🎬 Example Content

See sample videos on:

- [YouTube Shorts – @RedditCampfireStories](https://www.youtube.com/@RedditCampfireStories/shorts)  
- [TikTok – @redditcampfirestories](https://www.tiktok.com/@redditcampfirestories)

---








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
ollama run llama3.2
ollama run gemma3:27b-it-qat
```

### 5. Usage
```bash
cd video-creator
python main.py
```
