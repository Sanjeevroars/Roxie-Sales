import openai
import speech_recognition as sr
# from google.cloud import texttospeech
from openai import OpenAI
from dotenv import load_dotenv
import pygame
import io
import threading
import os
import requests
import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("openai.api_key")
ROXIE_API_KEY = os.getenv("Roxie.api_key")

pygame.mixer.init()

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "googlecloudvoicetts.json"
# tts_client = texttospeech.TextToSpeechClient()

LOCATION = "Chennai, India"

def load_document(file_path):
    with open(file_path, 'r') as file:
        document_content = file.read()
    return document_content

document_content = load_document('company_specific_info.txt')

def speech_to_text(prompt=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            print(f"Assistant: {prompt}")
            text_to_speech(prompt)
        print("Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Request error from Google Speech Recognition service.")
        return ""

def chat_with_gpt(conversation_history):
    prompt = f"{document_content}\n\n{conversation_history[-1]}"
    messages = [{"role": "system", "content": "You are a helpful sales assistant."},
                {"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=250,
        temperature=0.9
    )
    return response.choices[0].message['content'].strip()

def text_to_speech(text):
    # input_text = texttospeech.SynthesisInput(text=text)
    # voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    # audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # response = tts_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    
    client = OpenAI(api_key=ROXIE_API_KEY)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    audio_data = response.content
    audio_fp = io.BytesIO(audio_data)
    audio_fp.seek(0)
    
    pygame.mixer.music.load(audio_fp, 'mp3')
    
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def get_initial_details(memory):
    if "name" not in memory:
        memory["name"] = speech_to_text("What is your name?")
        update_transcript(f"User: My name is {memory['name']}")
    if "contact" not in memory:
        memory["contact"] = speech_to_text("What is your contact number?")
        update_transcript(f"My contact number is {memory['contact']}")
    return memory

def book_appointment(memory):
    if "date" not in memory:
        memory["date"] = speech_to_text("What date would you like to book the appointment?")
        update_transcript(f"Booking appointment for {memory['name']} at {LOCATION} on {memory['date']}.")
    return "Our Sales team will contact you shortly."

def ask_model_interest(memory):
    model = speech_to_text("Which particular model are you interested in?")
    update_transcript(f"User is interested in: {model}")
    return model

def is_relevant_question(user_input):
    keywords = ["car", "model", "price", "variant", "feature", "appointment", "sales", "service", "toyota", "prius", "corolla", "camry", "rav4"]
    return any(keyword in user_input.lower() for keyword in keywords)

def update_transcript(line):
    try:
        response = requests.post('http://127.0.0.1:5000/api/update_transcript', json={'line': line})
        return response.ok
    except requests.RequestException as e:
        print(f"Failed to update transcript: {e}")
        return False

def end_conversation(memory):
    user_info = {
        "name": memory.get("name", "Unknown"),
        "contact": memory.get("contact", "Unknown"),
        "date": datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    }
    try:
        response = requests.post('http://127.0.0.1:5000/api/end_conversation', json={'user_info': user_info})
        if response.ok:
            print("Conversation saved successfully.")
        else:
            print("Failed to save conversation.")
    except requests.RequestException as e:
        print(f"Failed to save conversation: {e}")

def main():
    memory = {}
    conversation_history = []

    memory = get_initial_details(memory)
    conversation_history.append(f"User: My name is {memory['name']} and my contact number is {memory['contact']}.")

    print("Assistant: How can I assist you today?")
    text_to_speech("How can I assist you today?")
    
    try:
        while True:
            user_input = speech_to_text()
            if user_input.lower() == "exit":
                break
            if "finish" in user_input.lower():
                farewell_message = "Roxie is always available. Have a great day!"
                print(f"Assistant: {farewell_message}")
                text_to_speech(farewell_message)
                update_transcript(farewell_message)
                break
            if user_input.lower() == "book an appointment":
                confirmation_message = book_appointment(memory)
                print(f"Assistant: {confirmation_message}")
                text_to_speech(confirmation_message)
                update_transcript(f"Assistant: {confirmation_message}")

                model_interest = ask_model_interest(memory)
                print(f"Assistant: Great Choice! Your interest in {model_interest} has been noted.")
                text_to_speech(f"Great Choice! Your interest in {model_interest} has been noted.")
                update_transcript(f"Assistant: You are interested in: {model_interest}")
                continue
            if user_input:
                update_transcript(f"User: {user_input}")
                if is_relevant_question(user_input):
                    conversation_history.append(f"User: {user_input}")
                    response = chat_with_gpt(conversation_history)
                    conversation_history.append(f"Assistant: {response}")
                    print(f"Assistant: {response}")
                    update_transcript(f"Assistant: {response}")
                    
                    playback_thread = threading.Thread(target=text_to_speech, args=(response,))
                    playback_thread.start()
                    playback_thread.join()
                else:
                    irrelevant_response = "I'm sorry, I can only assist with questions related to our company's services."
                    print(f"Assistant: {irrelevant_response}")
                    text_to_speech(irrelevant_response)
                    update_transcript(f"Assistant: {irrelevant_response}")
    finally:
        end_conversation(memory)

if __name__ == "__main__":
    main()
