# avega-offline-voice-assistant

## System requirements

- Python 3.10 or later
- Docker Desktop (https://www.docker.com/products/docker-desktop)
- [curl](https://curl.se/windows/) (for Windows: curl.exe)
- [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Ollama](https://ollama.com/download) (for running language models)

## Installation

1. Install Docker Desktop according to the instructions at https://www.docker.com/products/docker-desktop
2. Install Python packages in requirements
3. Install Piper voices, English (current Enlish voice needs  "en_US-amy-medium.onnx", Swedish current voice needs "sv_SE-lisa-medium.onnx")
4. Use correct script ie suffix English or Swedish
5. [Optional] Install WSL (Windows Subsystem for Linux) if you plan to run Linux-native tools.
   - See Microsoft’s guide: https://learn.microsoft.com/en-us/windows/wsl/install
6. Install curl for Windows:
   - Download curl.exe from [curl.se/windows/](https://curl.se/windows/)
7. Install Ollama following their [official guide](https://ollama.com/download)

# 🖥️ Offline AI Setup: Ollama + LLaMA/Mistral + Whisper + Piper

This project demonstrates how to run a fully **offline AI stack** on a laptop, enabling **speech-to-text**, **LLM-based conversation**, and **text-to-speech** — all without relying on cloud services.

***

## ✅ Features
I’m running Ollama with LLaMA/Mistral7 (LLM), Whisper (speech-to-text for prompts), and Piper (text-to-speech) on my laptop

*   **Continuous conversation in Swedish** (or English)
*   **Completely offline** — no external API calls
*   Modular architecture using:
    *   **Ollama** for running LLaMA/Mistral7 LLM
    *   **Whisper** for speech-to-text (prompts)
    *   **Piper** for text-to-speech responses

***

## 🛠️ Architecture

*   **Whisper** → Runs inside a **Docker container**
*   **Ollama** → Runs in **WSL** with Linux + virtual environment
*   **Piper** → Installed as a **Python module**

***

## 🔍 Why LLaMA/Mistral?

*   Supports **fine-tuning on custom data**
*   Efficient VRAM usage — **Ollama Mistral uses \~5 GB**, perfect for laptops with **6 GB VRAM**

***

## ⚠️ Notes

*   Speech recognition in Swedish requires **very clear pronunciation**
*   English may perform better — worth testing!

***

### Example Workflow

1.  Speak → **Whisper** converts audio to text
2.  Text → **Ollama (LLaMA/Mistral)** processes and generates response
3.  Response → **Piper** converts text back to speech

***


