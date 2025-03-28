import ollama
import json
from vosk import Model, KaldiRecognizer
import pyaudio

MODEL_NAME = "vosk-model-en-us-0.42-gigaspeech"

def listen_and_transcribe():
    """Mendengarkan suara dan mengonversi menjadi teks."""
    model = Model(MODEL_NAME)
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)

    print("\n🎤 Silakan bicara... (Katakan 'stop' untuk keluar)")
    stream.start_stream()

    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if len(data) == 0:
            continue  # Skip jika data kosong

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())["text"]
            if result:
                return result  # Langsung return teks hasil pengenalan

# Fungsi untuk mengirim teks ke Ollama
def ask_ollama(prompt):
    """Mengirim teks ke model AI Ollama dan mendapatkan respon."""
    response = ollama.chat(
        model="deepseek-r1:14b",  # Ganti dengan model yang tersedia di `ollama ls`
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# Main program
while True:
    user_speech = listen_and_transcribe().strip()

    if user_speech.lower() in ["stop", "berhenti"]:
        print("\n🛑 Keluar...")
        break

    print("\n🔹 Anda berkata:", user_speech)
    
    # Kirim ke Ollama hanya jika ada input
    if user_speech:
        print("\n🤖 AI sedang berpikir...\n")
        ai_response = ask_ollama(user_speech)
        print("💡 AI:", ai_response)
