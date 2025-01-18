import speech_recognition as sr
from openai import OpenAI
import pygame
import io
import threading
import os
import requests
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Initialize pygame mixer to handle audio playback.
pygame.mixer.init()

# Load environment variables from .env file for secure API key management.
load_dotenv()
ROXIE_API_KEY = os.getenv("Roxie.api_key")
OPENAI_API_KEY = os.getenv("openai.api_key")

# Define a constant for the location where appointments are booked.
LOCATION = "Chennai, India"

ENQUIRIES_DIR = os.path.abspath('enquiries')
os.makedirs(ENQUIRIES_DIR, exist_ok=True)

# MongoDB setup to store and retrieve client information.
MONGO_URI = os.getenv("mongoDB.uri")
client = MongoClient(MONGO_URI)
db = client["client_info"]
client_collection = db["client_models"]

def load_document(file_path):
    """
    Load the document content from a specified file.

    Args:
    file_path (str): Path to the file to be read.

    Returns:
    str: Contents of the file.
    """
    with open(file_path, 'r') as file:
        document_content = file.read()
    return document_content

# Load company-specific information from the document for chatbot context.
document_content = load_document('company_specific_info.txt')

def speech_to_text(prompt=None):
    """
    Convert spoken language to text using Google Speech Recognition API.

    Args:
    prompt (str): Optional prompt that is played as TTS before recognizing speech.

    Returns:
    str: Recognized text from the user's speech.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source=source)
        if prompt:
            print(f"Assistant: {prompt}")
            text_to_speech(prompt)
        print("Speak now...")
        audio = recognizer.listen(source=source)
    try:
        text = recognizer.recognize_google(audio)
        if prompt == "What is your contact number?":
            cleaned_contact = validate_contact_number(text)
            if cleaned_contact:
                print(f"You said: {cleaned_contact}")
                return cleaned_contact
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speech_to_text(prompt=prompt)
    except sr.RequestError:
        print("Request error from Google Speech Recognition service.")
        return ""

def chat_with_gpt(conversation_history):
    """
    Interact with GPT-3.5 model to generate a relevant response based on the conversation history.

    Args:
    conversation_history (list): List of conversation exchanges between the assistant and user.

    Returns:
    str: Generated response from GPT-3.5 model.
    """
    prompt = (
        f"{document_content}\n\n"
        f"You are a helpful sales assistant. Always keep responses short and to the point. "
        f"Provide concise and relevant answers based on the conversation context.\n\n"
        f"{conversation_history[-1]}"
    )
    messages = [
        {"role": "system", "content": "You are a helpful sales assistant. Your responses must be concise, no more than 2-3 sentences."},
        {"role": "user", "content": prompt}
    ]
    
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=250,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def play_tts_offline(file_path):
    """
    Play an offline TTS file using pygame mixer.

    Args:
    file_path (str): Path to the MP3 file to be played.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def text_to_speech(text):
    """
    Convert text to speech either from a pre-recorded file or by generating speech via OpenAI API.

    Args:
    text (str): Text to be converted to speech.
    """
    prompt_to_mp3 = {
        "What is your name?": os.path.join("assets", "whatIsYourName.mp3"),
        "What is your contact number?": os.path.join("assets", "whatContactNum.mp3"),
        "How can I assist you today?": os.path.join("assets", "howCanIAssist.mp3"),
        "I'm sorry, I can only assist with questions related to our company's services.": os.path.join("assets", "companyServices.mp3"),
        "The contact number you provided is invalid. Please provide JUST the valid contact number.": os.path.join("assets", "JUSTcontact.mp3"),
        "What date would you like to book the appointment?": os.path.join("assets", "whatDayBook.mp3"),
        "Our Sales team will contact you shortly.": os.path.join("assets", "salesTeamContact.mp3"),
        "Which particular model are you interested in?": os.path.join("assets", "whichModelYouInterestedIn.mp3"),
        "Roxie is always available. Have a great day!": os.path.join("assets", "alwaysAvailable.mp3"),
        "Our Sales team will contact you shortly. Have a great day!": os.path.join("assets", "haveAgreatDay.mp3")
    }

    if text in prompt_to_mp3:
        mp3_file = prompt_to_mp3[text]
        play_tts_offline(mp3_file)
    else:
        """
        Convert text to speech using OpenAI API and play the generated audio.
        """
        client = OpenAI(api_key=ROXIE_API_KEY)

        response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=text
        )

        audio_data = response.content
        audio_fp = io.BytesIO(audio_data)
        audio_fp.seek(0)
        
        pygame.mixer.music.load(audio_fp, 'mp3')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def validate_contact_number(contact):
    """
    Validate that the provided contact number is a 10-digit number.

    Args:
    contact (str): Contact number provided by the user.

    Returns:
    str or None: Validated contact number or None if invalid.
    """
    if not contact:
        return None
    cleaned_contact = contact.replace(" ", "")
    
    if cleaned_contact.isdigit() and len(cleaned_contact) == 10:
        return cleaned_contact
    else:
        print("Error: Invalid contact number.")
        return None

def get_initial_details(memory):
    """
    Gather initial user details such as name and contact number.

    Args:
    memory (dict): Dictionary to store user information during the interaction.

    Returns:
    dict: Updated memory with user details.
    """
    if "name" not in memory:
        memory["name"] = speech_to_text("What is your name?")
        update_transcript(f"User: {memory['name']}")
    if "contact" not in memory:
        contact = speech_to_text("What is your contact number?")
        cleaned_contact = validate_contact_number(contact)
        if cleaned_contact:
            memory["contact"] = cleaned_contact
            update_transcript(f"My contact number is {memory['contact']}")
        else:
            print("Assistant: The contact number you provided is invalid. Please provide JUST the valid contact number.")
            text_to_speech("The contact number you provided is invalid. Please provide JUST the valid contact number.")
            memory = get_initial_details(memory)
    return memory

def book_appointment(memory):
    """
    Assist the user in booking an appointment.

    Args:
    memory (dict): User's memory containing relevant information.

    Returns:
    str: Confirmation message for the appointment.
    """
    if "date" not in memory:
        # memory["date"] = speech_to_text("What date would you like to book the appointment?")
        # update_transcript(f"Booking appointment for {memory['name']} at {LOCATION} on {memory['date']}.")
        update_transcript(f"Booking appointment for {memory['name']} @ {LOCATION}.")

        # update_transcript(f"Appointment date: {memory['date']}.")
    return "Our Sales team will contact you shortly. Have a great day!"

def ask_model_interest(memory):
    """Ask the user about the model they're interested in and check its availability."""
    while True:
        # Ask the user which model they are interested in
        model = speech_to_text("Which particular model are you interested in?")
        if not model:
            print("Assistant: I didn't catch that. Could you please repeat?")
            text_to_speech("I didn't catch that. Could you please repeat?")
            continue
        
        # Check if the model is available
        if check_model_availability(model, memory):
            update_transcript(f"User is interested in: {model}")
            memory["model"] = model
            return model  # Exit loop once a valid model is found
        else:
            response = f"The model {model} is not available in our collection. Please choose a different model."
            print(f"Assistant: {response}")
            text_to_speech(response)
            update_transcript(f"Assistant: {response}")

def check_model_availability(model, memory):
    """Check if the specified model is available in the database."""
    car = client_collection.find_one({"$or": [{"model": model}, {"aliases": model}]})
    if car:
        update_transcript(f"User Interested Model: {model}")
        response = f"Great choice! The {model} is available in our collection."
        print(f"Assistant: {response}")
        text_to_speech(response)
        update_transcript(f"Assistant: {response}")
        
        return True
    else:
        return False

def is_relevant_question(user_input):
    """
    Check if the user's question is relevant to the services offered.

    Args:
    user_input (str): The question asked by the user.

    Returns:
    bool: True if the question is relevant, False otherwise.
    """
    keywords = ["car", "model", "price", "variant", "feature", "appointment", "sales", "service", "sedan", "suv", "hatchback", "person", "family", "toyota", "prius", "corolla", "camry", "rav4"]
    return any(keyword in user_input.lower() for keyword in keywords)

def update_transcript(line):
    """
    Update the conversation transcript on the server.

    Args:
    line (str): Line of conversation to be added to the transcript.
    
    Returns:
    bool: True if successful, False otherwise.
    """
    try:
        response = requests.post('http://127.0.0.1:5000/api/update_transcript', json={'line': line})
        return response.ok
    except requests.RequestException as e:
        print(f"Failed to update transcript: {e}")
        return False

def end_conversation(memory):
    """
    End the conversation, save the user's information, and update the server.

    Args:
    memory (dict): User's memory containing the session details.
    """
    user_info = {
        "name": memory.get("name", "Unknown"),
        "contact": memory.get("contact", "Unknown"),
        "date": datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"),
        "interested_model": memory.get("model", "Not specified"),
        "location": LOCATION
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
    """
    Main function to run the chatbot and handle user interactions.

    Gathers user details, handles conversation, checks model availability, and handles booking.
    """
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
                farewell_message = "Thank You! Roxie is always available. Have a great day!"
                print(f"Assistant: {farewell_message}")
                text_to_speech(farewell_message)
                update_transcript(farewell_message)
                break
            if user_input.lower() == "book an appointment":
                model_interest = ask_model_interest(memory)
                print(f"Assistant: Your interest in {model_interest} has been noted.")
                text_to_speech(f"Your interest in {model_interest} has been noted.")
                update_transcript(f"Assistant: You are interested in ->{model_interest}")
                confirmation_message = book_appointment(memory)
                print(f"Assistant: {confirmation_message}")
                text_to_speech(confirmation_message)
                update_transcript(f"Assistant: {confirmation_message}")           
                break

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
