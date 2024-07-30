import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import json
import logging
from logging import FileHandler, WARNING

# Decode base64 credentials and set environment variable
credentials_base64 = os.environ.get("GOOGLE_CREDENTIALS_BASE64")
if credentials_base64 is None:
    raise ValueError("GOOGLE_CREDENTIALS_BASE64 environment variable is not set")

credentials_path = "/app/google-credentials.json"

with open(credentials_path, "wb") as f:
    f.write(base64.b64decode(credentials_base64))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Define the refined system instruction
system_instruction = """Help students with their studies by providing clear, accurate, and supportive information. Use simple language, give structured explanations, and offer practical study tips. Encourage and motivate students."""

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
    "gemini-1.5-pro-001",
    system_instruction=[system_instruction]
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

# Function to clean up the AI response
def clean_ai_response(ai_response):
    # Replace special characters with their readable equivalents
    cleaned_response = ai_response.replace('\\u2013', '–')  # Replace en dash
    # Add more replacements as needed

    # Remove any unwanted characters (e.g., non-printable characters)
    cleaned_response = ''.join(char for char in cleaned_response if 32 <= ord(char) <= 126)

    # Trim extra whitespace
    cleaned_response = cleaned_response.strip()

    return cleaned_response

# Function to extract relevant part of the AI response
def extract_relevant_part(ai_response):
    candidates = ai_response.get('candidates', [])
    for candidate in candidates:
        content = candidate.get('content', {})
        parts = content.get('parts', [])
        for part in parts:
            text_answer = part.get('text', '')
            if text_answer:
                return clean_ai_response(text_answer)
    return "No relevant response found."

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

