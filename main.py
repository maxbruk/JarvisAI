import sys
import time

import openwakeword
import requests
import sounddevice as sd
import speech_recognition as sr
from kokoro import KPipeline

pipeline = KPipeline(lang_code="a")
r = sr.Recognizer()
source = sr.Microphone()

# # === Speech Engine ===


def Speak(text: str):
    generator = pipeline(text, voice="af_heart", speed=1.0)
    for _, _, audio in generator:
        time.sleep(0.5)
        sd.play(audio, samplerate=24000)
        sd.wait()


def Recognize():
    try:
        with sr.Microphone() as source:
            print("Listening...")

            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_whisper(
                audio, model="base.en", language="english"
            ).lower()
            return text

    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    except sr.UnknownValueError:
        print("Could not understand audio")

    except KeyboardInterrupt:
        print("Program terminated by user")
        sys.exit(1)


def main():

    # To run ollama use - OLLAMA_HOST="0.0.0.0:11434" OLLAMA_ORIGINS="*" /Applications/Ollama.app/Contents/MacOS/Ollama &

    ip = "10.0.0.16"  # <- Change this to your local IP.
    url = f"http://{ip}:11434/api/generate"
    model = openwakeword.Model(wakeword_models=["hey jarvis"])
    talking = False

    with sd.InputStream(samplerate=16000, channels=1, dtype="int16") as stream:

        while True:
            audio_data, _ = stream.read(1280)
            prediction = model.predict(x=audio_data.flatten())
            score = prediction["hey jarvis"]
            print(f"{score:.4f}")

            if score > 0.5 and talking == False:
                print("Command recognized! Listening...")
                model.reset()  # resets the model's internal memory buffer to not trigger the condition several times.
                output = Recognize()
                talking = True

                if output is not None:
                    if "quit" in output.casefold():
                        print("Program terminated by user.")
                        talking = False
                        sys.exit(0)
                    
                    prompt = output
                    print(prompt)
                    talking = False
                    
                    data = {"model": "llama3.2:3b", "prompt": prompt, "stream": False}
                    response = requests.post(url, json=data)

                    print(response.json()["response"])
                    Speak(response.json()["response"])


if __name__ == "__main__":
    main()
