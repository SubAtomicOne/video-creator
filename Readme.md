# This is a fork with Features that I wanted such as autouploading to TikTok and YouTube!
I have not updated the requirments.txt as it was broken for me and I had to manually install all of them so I would try to use the requirments.txt to install the bulk and then add the rest of the files.

You need to set up a google oauth api for the auto upload to youtube, plenty of instructions online. With that, you will need to create a few authorization files such as upload_video.py-oauth2.json and client_secrets.json. 

Also, I changed the background music as it was flagged for copyright on one of my videos.

For the TikTok api, use the docs to help, but you will need to create a json file with your cookies, I used a Chrome extension called Cookie-Editor to get mine.

Below is the normal documentation from the original fork.

Example videos can be found on my YouTube page or TikTok Page.
https://www.youtube.com/@RedditCampfireStories/shorts
https://www.tiktok.com/@redditcampfirestories







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
