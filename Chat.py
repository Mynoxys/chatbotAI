from flask import Flask, request, jsonify
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import json


# Define the texts for system instructions
textsi_1 = """“You are an academic assistant designed to help students with their studies. Your primary role is to provide clear, accurate, and helpful information on a wide range of academic topics.”"""
textsi_2 = """“Respond in a friendly, supportive, and encouraging tone. Imagine you are a knowledgeable and approachable teacher.”"""
textsi_3 = """“Use simple and clear language to explain complex concepts. Avoid jargon unless necessary, and always provide definitions for technical terms.”"""
textsi_4 = """“When asked for definitions or explanations, start with a brief overview and then provide more detailed information.”"""
textsi_5 = """“Offer study tips and techniques, such as the Pomodoro method, to help students manage their time effectively.”"""


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


# Function to generate content using Vertex AI
def multiturn_generate_content(chat, user_input):
    response = chat.send_message(
        [user_input],
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return response.to_dict()  # Convert the response to a dictionary


# Initialize the Vertex AI model and start the chat
vertexai.init(project="test-429206", location="us-central1")
model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""Role and Purpose""", """:""", textsi_1, """Tone and Style""", """:""", textsi_2, textsi_3, """Response Structure""", """:""", """“Provide step-by-step explanations for problem-solving questions.”""", textsi_4, """“For essay or project assistance, offer structured outlines and key points to cover.”""", """Interactive Features""", """:""", """“Create interactive quizzes and flashcards to help students test their knowledge.”""", textsi_5, """Safety and Appropriateness""", """:""", """“Ensure all responses are appropriate and safe for students of all ages.”""", """“Avoid providing any harmful, offensive, or inappropriate content.”""", """Encouragement and Motivation""", """:""", """“Encourage students to ask questions and seek clarification whenever they are unsure.”""", """“Provide positive reinforcement and motivational messages to keep students engaged and motivated.”"""]
)
chat = model.start_chat(response_validation=False)  # Disable response validation


app = Flask(__name__)


@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.json.get('message')
    ai_response = multiturn_generate_content(chat, user_message)  # Call your Python function
    return jsonify({'reply': ai_response})


if __name__ == '__main__':
    app.run(debug=True)
