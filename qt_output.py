import sys
import threading
from PyQt6 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
from openai import OpenAI
import pygame
import io
import os
import requests
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

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

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Roxie")
        Widget.resize(480, 680)

        Widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        Widget.setFixedSize(480, 680)

        self.widget = QtWidgets.QWidget(parent=Widget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 480, 680))
        self.widget.setObjectName("Roxie")
        
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 480, 680))
        self.label.setStyleSheet("background-image: url(qt_assets/bg.jpg)")
        self.label.setText("")
        self.label.setObjectName("label")
        
        # Add logo at the center top
        self.logoLabel = QtWidgets.QLabel(parent=self.widget)
        self.logoLabel.setGeometry(QtCore.QRect(0, 0, 480, 480))
        self.logoLabel.setStyleSheet("""
            QLabel {
                background-image: url(qt_assets/Roxie.png);
                background-repeat: no-repeat;
                background-position: center;
            }
        """)
        self.logoLabel.setText("")
        self.logoLabel.setObjectName("logoLabel")
        
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setGeometry(QtCore.QRect(190, 250, 100, 100))
        
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-image: url(qt_assets/mic.png);
                background-repeat: no-repeat;
                background-position: center;
                background-color: #3a77c2;
                border-radius: 50;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #193659;
            }
        """)
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_button_click)

        # Create Quit button
        self.quitButton = QtWidgets.QPushButton(parent=self.widget)
        self.quitButton.setGeometry(QtCore.QRect(205, 540, 70, 70)) 
        self.quitButton.setText("")
        
        self.quitButton.setStyleSheet("""
            QPushButton {
                background-image: url(qt_assets/quit-icon.png);
                background-repeat: no-repeat;
                background-position: center;
                background-color: #FF5733;
                border-radius: 35;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.quitButton.clicked.connect(self.quit_application)

        # Create a QLabel to display "Speak now..." message
        self.speakNowLabel = QtWidgets.QLabel(parent=self.widget)
        self.speakNowLabel.setGeometry(QtCore.QRect(100, 420, 290, 30))  # Position and size
        self.speakNowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.speakNowLabel.setStyleSheet("""
                                         color: white;
                                         font-size: 20px;
                                         font-weight: bold;
                                         """)
        self.speakNowLabel.setText("")  # Initially empty
        
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

        self.chatbot_thread = None
        self.stop_chatbot = False

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Roxie", "Roxie - Your AI Sales Assistant"))

    def on_button_click(self):
        print("Starting assistant...")
        self.pushButton.setDisabled(True)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-image: url(qt_assets/mic.png);
                background-repeat: no-repeat;
                background-position: center;
                background-color: #454545;
                border-radius: 50;
                border: none;
                color: white;
            }
        """)

        self.stop_chatbot = False  
        self.chatbot_thread = threading.Thread(target=self.run_chatbot)
        self.chatbot_thread.start()

    def run_chatbot(self):
        try:
            while not self.stop_chatbot:
                self.main()
                break  
        except Exception as e:
            print(f"Error running the chatbot: {e}")
        finally:
            self.pushButton.setEnabled(True)

    def book_appointment(self, memory):
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
            self.update_transcript(f"Booking appointment for {memory['name']} @ {LOCATION}.")

            # update_transcript(f"Appointment date: {memory['date']}.")
        return "Our Sales team will contact you shortly. Have a great day!"

    def main(self):
        memory = {}
        conversation_history = []

        memory = self.get_initial_details(memory)
        conversation_history.append(f"User: My name is {memory['name']} and my contact number is {memory['contact']}.")

        print("Assistant: How can I assist you today?")
        self.text_to_speech("How can I assist you today?")
        
        try:
            while True:
                user_input = self.speech_to_text()
                if user_input.lower() == "exit":
                    break
                if "finish" in user_input.lower():
                    farewell_message = "Roxie is always available. Have a great day!"
                    print(f"Assistant: {farewell_message}")
                    self.text_to_speech(farewell_message)
                    self.update_transcript(farewell_message)
                    self.pushButton.setEnabled(True)
                    self.pushButton.setStyleSheet("""
                        QPushButton {
                            background-image: url(qt_assets/mic.png);
                            background-repeat: no-repeat;
                            background-position: center;
                            background-color: #3a77c2;
                            border-radius: 50;
                            border: none;
                            color: white;
                        }
                        QPushButton:hover {
                            background-color: #193659;
                        }
                    """)
                    self.speakNowLabel.setText("")  # Clear the message after finish
                    break
                if user_input.lower() == "book an appointment":
                    model_interest = self.ask_model_interest(memory)
                    print(f"Assistant: Your interest in {model_interest} has been noted.")
                    self.text_to_speech(f"Your interest in {model_interest} has been noted.")
                    self.update_transcript(f"Assistant: You are interested in ->{model_interest}")
                    confirmation_message = self.book_appointment(memory)
                    print(f"Assistant: {confirmation_message}")
                    self.text_to_speech(confirmation_message)
                    self.update_transcript(f"Assistant: {confirmation_message}")           
                    break

                if user_input:
                    self.update_transcript(f"User: {user_input}")
                    if self.is_relevant_question(user_input):
                        conversation_history.append(f"User: {user_input}")
                        response = self.chat_with_gpt(conversation_history)
                        conversation_history.append(f"Assistant: {response}")
                        print(f"Assistant: {response}")
                        self.update_transcript(f"Assistant: {response}")
                        
                        playback_thread = threading.Thread(target=self.text_to_speech, args=(response,))
                        playback_thread.start()
                        playback_thread.join()
                    else:
                        irrelevant_response = "I'm sorry, I can only assist with questions related to our company's services."
                        print(f"Assistant: {irrelevant_response}")
                        self.text_to_speech(irrelevant_response)
                        self.update_transcript(f"Assistant: {irrelevant_response}")
        finally:
            self.end_conversation(memory)

    def speech_to_text(self, prompt=None):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source=source)
            
            # Display "Speak now..." in the GUI
            if prompt:
                print(f"Assistant: {prompt}")
                self.text_to_speech(prompt)
            
            print("Speak now...")
            self.speakNowLabel.setText("Listening")  # Update GUI to show "Speak now..."
            
            # Wait for the user to speak
            audio = recognizer.listen(source=source)
            
            # Clear the "Speak now..." message after the input is captured
            self.speakNowLabel.setText("")  # Clear the label after listening

        try:
            text = recognizer.recognize_google(audio)
            if prompt == "What is your contact number?":
                cleaned_contact = self.validate_contact_number(text)
                if cleaned_contact:
                    print(f"You said: {cleaned_contact}")
                    return cleaned_contact
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that")
            self.speakNowLabel.setText("Sorry, I didn't understand that")  # Update label for errors
            self.speech_to_text(prompt=prompt)
        except sr.RequestError:
            print("Request error from Google Speech Recognition service.")
            return ""

    def chat_with_gpt(self, conversation_history):
        self.speakNowLabel.setText("Processing")
        prompt = (
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

    def text_to_speech(self, text):
        # Set label to "Processing" before starting TTS
        self.speakNowLabel.setText("Processing")  # Update GUI to show "Processing"
        
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
            self.play_tts_offline(mp3_file)
        else:
            client = OpenAI(api_key=ROXIE_API_KEY)

            response = client.audio.speech.create(
                model="tts-1",
                voice="shimmer",
                input=text
            )

            self.speakNowLabel.setText("")  # Clear the "Processing" message

            audio_data = response.content
            audio_fp = io.BytesIO(audio_data)
            audio_fp.seek(0)

            pygame.mixer.music.load(audio_fp, 'mp3')
            pygame.mixer.music.play()

            # Wait for the audio to finish playing and clear the label
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)


    def play_tts_offline(self, file_path):
        # Once TTS is done, clear the label
        self.speakNowLabel.setText("")  # Clear the "Processing" message

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        if file_path == os.path.join("assets", "haveAgreatDay.mp3"):
            QtWidgets.QApplication.exit()
            QtWidgets.QApplication.exit()

    def validate_contact_number(self, contact):
        if not contact:
            return None
        cleaned_contact = contact.replace(" ", "")
        
        if cleaned_contact.isdigit() and len(cleaned_contact) == 10:
            return cleaned_contact
        else:
            print("Error: Invalid contact number.")
            return None

    def get_initial_details(self, memory):
        if "name" not in memory:
            memory["name"] = self.speech_to_text("What is your name?")
            self.update_transcript(f"User: {memory['name']}")
        if "contact" not in memory:
            contact = self.speech_to_text("What is your contact number?")
            cleaned_contact = self.validate_contact_number(contact)
            if cleaned_contact:
                memory["contact"] = cleaned_contact
                self.update_transcript(f"My contact number is {memory['contact']}")
            else:
                print("Assistant: The contact number you provided is invalid. Please provide JUST the valid contact number.")
                self.text_to_speech("The contact number you provided is invalid. Please provide JUST the valid contact number.")
                memory = self.get_initial_details(memory)
        return memory

    def ask_model_interest(self, memory):
        while True:
            model = self.speech_to_text("Which particular model are you interested in?")
            if not model:
                print("Assistant: I didn't catch that Could you please repeat?")
                self.text_to_speech("I didn't catch that Could you please repeat?")
                continue
            
            actual_model = self.check_model_availability(model)
            if actual_model:
                memory["model"] = actual_model  
                self.update_transcript(f"User is interested in: {actual_model}")
                return actual_model  
            else:
                response = f"The model {model} is not available in our collection. Please choose a different model."
                print(f"Assistant: {response}")
                self.text_to_speech(response)
                self.update_transcript(f"Assistant: {response}")

    def check_model_availability(self, user_input_model):
        self.speakNowLabel.setText("Processing")  # Update GUI to show "Processing"
        car = client_collection.find_one({"$or": [{"model": user_input_model}, {"aliases": user_input_model}]})
        if car:
            actual_model = car["model"]  
            response = f"Great choice! The {actual_model} is available in our collection."
            print(f"Assistant: {response}")
            self.text_to_speech(response)
            self.update_transcript(f"Assistant: {response}")
            return actual_model  
        return None

    def is_relevant_question(self, user_input):
        keywords = ["car", "model", "price", "variant", "feature", "sales", "service", "sedan", "suv", "hatchback", "person", "family", "toyota", "prius", "corolla", "camry", "rav4"]
        return any(keyword in user_input.lower() for keyword in keywords)

    def update_transcript(self, line):
        try:
            response = requests.post('http://127.0.0.1:5000/api/update_transcript', json={'line': line})
            return response.ok
        except requests.RequestException as e:
            print(f"Failed to update transcript: {e}")
            return False

    def end_conversation(self, memory):
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
        finally:
            QtWidgets.QApplication.exit()
            QtWidgets.QApplication.exit()

    def quit_application(self):
        QtWidgets.QApplication.quit()


def main_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    
    ui = Ui_Widget()
    ui.setupUi(window)
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main_gui()
