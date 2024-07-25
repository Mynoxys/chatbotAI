import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/google-credentials.json"
from flask import Flask, request, jsonify
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import json
import logging
from logging import FileHandler, WARNING

# Define the texts for system instructions
textsi_1 = """You are an academic assistant designed to help students with their studies. Your primary role is to provide clear, accurate, and helpful information on a wide range of academic topics."""
textsi_2 = """Respond in a friendly, supportive, and encouraging tone. Imagine you are a knowledgeable and approachable teacher."""
textsi_3 = """Use simple and clear language to explain complex concepts. Avoid jargon unless necessary, and always provide definitions for technical terms."""
textsi_4 = """When asked for definitions or explanations, start with a brief overview and then provide more detailed information."""
textsi_5 = """Offer study tips and techniques, such as the Pomodoro method, to help students manage their time effectively."""

# Define generation and safety settings
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Initialize the Vertex AI model and start the chat
vertexai.init(project="test-429206", location="us-central1")
model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=[textsi_1, textsi_2, textsi_3, textsi_4, textsi_5]
)
chat = model.start_chat(response_validation=False)  # Disable response validation

# Function to generate content using Vertex AI
def multiturn_generate_content(chat, user_input):
    response = chat.send_message(
        [user_input],
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return response.to_dict()  # Convert the response to a dictionary

# Function to extract relevant part of the AI response
def extract_relevant_part(ai_response):
    candidates = ai_response.get('candidates', [])
    for candidate in candidates:
        content = candidate.get('content', {})
        parts = content.get('parts', [])
        for part in parts:
            text_answer = part.get('text', '')
            if text_answer:
                return text_answer
    return "No relevant response found."

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Jarvis AI Back-end!"

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.json.get('message')
    app.logger.warning(f'Received message: {user_message}')
    ai_response = multiturn_generate_content(chat, user_message)
    relevant_part = extract_relevant_part(ai_response)
    return jsonify({'reply': relevant_part})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


