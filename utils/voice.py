import speech_recognition as sr
import os
import tempfile
import playsound
from gtts import gTTS

# recognizer object
recognizer = sr.Recognizer()

def listen_from_mic():
    """
    Listen from microphone and return recognized text.
    """
    with sr.Microphone() as source:
        print("🎙️ Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"👂 You said: {text}")
            return text
        except sr.UnknownValueError:
            print("⚠️ Didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Speech recognition error: {e}")
            return ""
        except Exception as e:
            print(f"⚠️ Mic error: {e}")
            return ""

def speak(text: str):
    """
    Convert text to speech and play it.
    """
    temp_path = None
    try:
        # make safe temp mp3 file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        tts = gTTS(text=text, lang="en")
        tts.save(temp_path)
        playsound.playsound(temp_path)

    except Exception as e:
        print(f"⚠️ TTS Error: {e}")

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except PermissionError:
                # file busy, ignore
                pass
