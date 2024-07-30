import axios from 'axios';

// Function to send user input to the server and handle the response
async function sendMessage(userInput) {
    try {
        const response = await axios.post('https://academiaatlas-45e6821ef7ff.herokuapp.com/api/chat', {
            message: userInput
        });

        const aiResponse = response.data.reply;
        const relevantResponse = extractSecondPart(aiResponse);

        console.log('Server response:', response.data);
        console.log('AI:', relevantResponse);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to extract the second part of the AI response
function extractSecondPart(aiResponse) {
    // Split the response into parts based on a delimiter (e.g., double newline)
    const parts = aiResponse.split('\n\n');
    // Return the second part if it exists, otherwise return the original response
    return parts.length > 1 ? parts[1].trim() : aiResponse.trim();
}

// Test the function with a sample user input
const userInput = "Hello, can you help me with my studies?";
sendMessage(userInput);
