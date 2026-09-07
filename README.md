# JarvisAI

A lightweight, local voice assistant loop built in Python. It listens through your microphone, transcribes speech locally using OpenAI Whisper, queries a self-hosted LLM via Ollama, and responds aloud with Kokoro TTS.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-Astral-DE5FE9?style=flat&logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-000000?style=flat&logo=ollama&logoColor=white)](https://ollama.com/)
[![Llama 3.2](https://img.shields.io/badge/Llama_3.2-3B-0467DF?style=flat&logo=meta&logoColor=white)](https://ai.meta.com/llama/)
[![Whisper](https://img.shields.io/badge/Whisper-base.en-412991?style=flat&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![Kokoro TTS](https://img.shields.io/badge/Kokoro-82M_TTS-FF9D00?style=flat&logo=huggingface&logoColor=white)](https://huggingface.co/hexgrad/Kokoro-82M)

---

## How It Works

The assistant runs as a local conversational loop without external cloud API dependencies:

1. **Audio Capture**: `speech_recognition` listens through the microphone and adjusts for ambient noise.
2. **Transcription**: OpenAI Whisper (`base.en`) transcribes the speech into text locally.
3. **Inference**: The transcription is sent to a local Ollama server running `llama3.2:3b`.
4. **Synthesis**: Kokoro TTS generates natural 24kHz audio (`af_heart` voice) streamed directly to your speakers via `sounddevice`.

## Prerequisites

- **Python**: 3.12 or newer
- **Package Manager**: [uv](https://github.com/astral-sh/uv) is recommended, though standard `pip` works as well
- **Audio Drivers**: PortAudio installed on your system (required for microphone input via `sounddevice` and `PyAudio`)
  - Windows: Handled automatically by pre-compiled binary wheels
  - macOS: `brew install portaudio`
  - Linux: `sudo apt install portaudio19-dev`
- **Ollama**: Running on your local machine or local network with the model installed:
  ```bash
  ollama pull llama3.2:3b
  ```

## Installation

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd jarvisai
```

Install dependencies using `uv`:

```bash
uv sync
```

Or using standard `pip`:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install .
```

## Configuration

### Ollama Endpoint

Set your Ollama host IP address in `main.py`:

```python
ip = "127.0.0.1"  # Or your local network host IP (e.g., 10.0.0.16)
url = f"http://{ip}:11434/api/generate"
```

If Ollama is hosted on a separate machine on your local network, start Ollama bound to all interfaces:

```bash
OLLAMA_HOST="0.0.0.0:11434" OLLAMA_ORIGINS="*" ollama serve
```

## Usage

Start the assistant:

```bash
uv run main.py
```

Once initialized, the terminal will display `Listening...`. Speak into your microphone; the transcribed prompt and assistant reply will print to the console while the response plays through your speakers.

Press `Ctrl + C` at any time to stop.

## Customization

- **Voice Profile**: Modify `voice="af_heart"` in `pipeline(text, voice="af_heart", speed=1.0)` to switch voices (e.g., `am_adam`, `af_bella`, `am_michael`, `af_sky`).
- **Whisper Model**: In `r.recognize_whisper(audio, model="base.en")`, choose `tiny.en` for faster response times or `small.en` / `medium.en` for improved accuracy.
- **LLM Model**: Change `"model": "llama3.2:3b"` to any other model available in your Ollama setup.

## Todo

- [ ] Wake-word activation (only dispatch prompts when keywords like "Jarvis" or "Hey Jarvis" are detected)
- [ ] Voice command controls (such as exiting the program by voice)
- [ ] Optimized voice recognition loop and reduced latency
- [ ] System automation: allow the LLM to inspect, open, and control local files
- [ ] Web access: tool-calling for real-time data lookup (weather, stock prices, live information)
- [ ] Computer vision and real-time object recognition
- [ ] Docker container support