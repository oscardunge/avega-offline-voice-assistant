import sounddevice as sd
import soundfile as sf
import requests
import subprocess
import time
import os
import sounddevice as sd


import numpy as np
import librosa  # pip install librosa
import keyboard


# --- KONFIG ---
RECORD_SECONDS = 5
INPUT_WAV = "input.wav"
REPLY_WAV = "reply.wav"

WHISPER_URL = "http://localhost:8080/inference"

LLM_CMD = ["ollama", "run", "mistral"]

PIPER_MODEL = "en_US-amy-medium.onnx"

# PIPER_MODEL = "sv_SE-lisa-medium.onnx"
PIPER_CMD = ["piper", "--model", PIPER_MODEL, "--output_file", REPLY_WAV]


sd.default.device = (1, None)  # Use your external microphone

# --- FUNKTIONER ---


TARGET_SR = 16000



SAMPLE_RATE = 48000      # your hardware
CHANNELS = 2             # your hardware
TARGET_SR = 16000        # whisper.cpp requirement
KEY_TO_RECORD = "space"


def record_audio():
    print(f"Tryck och håll ned {KEY_TO_RECORD} för att prata...")

    # Wait for user to press key to record
    keyboard.wait("space")
    print(f"🎙️ Lyssnar... släpp {KEY_TO_RECORD} för att stoppa.")

    # StStart recording
    recording = []
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16")
    stream.start()

    while keyboard.is_pressed("space"):
        data, _ = stream.read(1024)
        recording.append(data)

    stream.stop()
    stream.close()

    print("⏹️ Inspelning stoppad.")

    # Add many recording-blocks a 1024/48000 =21 milliseconds
    audio = np.concatenate(recording, axis=0)

    # Convertera to float32
    audio_f = audio.astype(np.float32) / 32768.0

    # Stereo → mono
    if audio_f.ndim == 2 and audio_f.shape[1] == 2:
        audio_f = audio_f.mean(axis=1)

    # Resample 48k → 16k
    audio_resampled = librosa.resample(audio_f, orig_sr=SAMPLE_RATE, target_sr=TARGET_SR)

    # to int16
    audio_int16 = (audio_resampled * 32767).astype(np.int16)

    # save as WAV
    sf.write("input.wav", audio_int16, TARGET_SR, subtype="PCM_16")

    print("🎧 Klar – skickar till Whisper.")


def run_whisper():
    print("🧠 Kör Whisper via Docker API...")
    data = {"language": "en"} # <-- FORCE SWEDISH

    with open(INPUT_WAV, "rb") as f:
        files = {
            "file": ("input.wav", f, "audio/wav")
        }
        response = requests.post(WHISPER_URL, files=files, data=data)

    if response.status_code != 200:
        print("❌ Whisper API fel:", response.text)
        return ""

    text = response.json().get("text", "").strip()
    print(f"📝 Whisper text: {text}")
    return text



def run_llm(prompt):
    print("🤖 Kör lokal LLM (Ollama via HTTP)...")

    payload = {
        "model": "mistral",
        "prompt": prompt
    }

    r = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)

    reply = ""
    for line in r.iter_lines():
        if line:
            data = line.decode("utf-8")
            if '"response"' in data:
                reply += data.split('"response":"')[1].split('"')[0]

    print(f"💬 LLM svar: {reply}")
    reply = (
        reply.replace("\\n", " ")
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("\t", " ")
            .replace("\\", "") 
            .strip()
    )

    reply = " ".join(reply.split())
    reply = reply.strip()
    reply = reply.lstrip()


    return reply



def run_piper(text: str):
    print("🔊 Genererar tal med Piper...")
    cmd = PIPER_CMD + [text]
    # cmd = PIPER_CMD + ["--text", text]
    subprocess.run(cmd, check=True)
    print("✅ reply.wav skapad.")

def play_audio():
    if os.name == "nt":
        os.startfile(REPLY_WAV)
    else:
        subprocess.run(["aplay", REPLY_WAV])

# --- MAIN LOOP ---

def main():
    print("🚀 Offline röstassistent startad. Ctrl+C för att avsluta.\n")
    while True:
        record_audio()
        user_text = run_whisper()

        #print(user_text)
        if not user_text:
            print("❗ Ingen text uppfattad, försöker igen...\n")
            continue

        prompt = f"Answer with 6 words.\n\nUser: {user_text}\nAssistent:"
        #prompt = f"Svara med 6 ord på svenska.\n\nAnvändare: {user_text}\nAssistent:"
        reply_text = run_llm(prompt)

        run_piper(reply_text)
        play_audio()

        print("\n--- Ny runda ---\n")
        time.sleep(1)

if __name__ == "__main__":
    main()





