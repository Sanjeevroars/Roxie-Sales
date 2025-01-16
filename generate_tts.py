from dotenv import load_dotenv
import os
from openai import OpenAI
import uuid

# Load environment variables
load_dotenv()
ROXIE_API_KEY = os.getenv("Roxie.api_key")

def text_to_speech(text, save_dir="assets"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    client = OpenAI(api_key=ROXIE_API_KEY)

    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text
    )

    filename = f"speech_{uuid.uuid4()}.mp3"
    file_path = os.path.join(save_dir, filename)

    response.stream_to_file(file_path)


# text_to_speech("What is your name?")
# text_to_speech("What is your contact number?")
# text_to_speech("How can I assist you today?")
# text_to_speech("I'm sorry, I can only assist with questions related to our company's services.")
# text_to_speech("The contact number you provided is invalid. Please provide JUST the valid contact number.")
# text_to_speech("What date would you like to book the appointment?")
# text_to_speech("Our Sales team will contact you shortly.")
# text_to_speech("Which particular model are you interested in?")
# text_to_speech("Roxie is always available. Have a great day!")