import os
from flask import Flask, request, jsonify
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import json

# Define the texts for system instructions
textsi_1 = """You are an academic assistant designed to help students with their studies. Your primary role is to provide clear, accurate, and helpful information on a wide range of academic topics. Respond in a friendly, supportive, and encouraging tone. Imagine you are a knowledgeable and approachable teacher. Use simple and clear language to explain complex concepts. Avoid jargon unless necessary, and always provide definitions for technical terms. When asked for definitions or explanations, start with a brief overview and then provide more detailed information."""

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
    system_instruction=[textsi_1]
)
chat = model.start_chat()

# Function to generate content using Vertex AI
def multiturn_generate_content(chat, user_input):
    response = chat.send_message(
        [user_input],
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return response.to_dict()  # Convert the response to a dictionary

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Student Planner App!"

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.json.get('message')
    ai_response = multiturn_generate_content(chat, user_message)  # Call your Python function
    return jsonify({'reply': ai_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
