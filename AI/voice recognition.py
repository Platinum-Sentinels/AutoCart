import openai
import speech_recognition as sr
import os
from dotenv import load_dotenv
load_dotenv()
from PM import seach_with_Ai
# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_KEY')
# Function for voice recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak now.")
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing your input...")
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Function to interact with ChatGPT
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=15,
        )
        reply = response["choices"][0]["message"]["content"]
        print("\nChatGPT's Response:")
        print(reply)
        return reply
    except Exception as e:
        print(f"Error interacting with ChatGPT: {e}")
        return None

# Main function
if __name__ == "__main__":
    result = ""
    spoken_text = recognize_speech()
    if spoken_text:
        result = ask_openai(spoken_text)
    seach_with_Ai(result)
    
    
