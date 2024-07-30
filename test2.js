import axios from 'axios';

// Function to send user input to the server and handle the response
async function sendMessage(userInput) {
    try {
        const response = await axios.post('https://academiaatlas-45e6821ef7ff.herokuapp.com/api/chat', {
            message: userInput
        });

        const aiResponse = response.data.reply;
        console.log('Server response:', response.data);
        console.log('AI:', aiResponse);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Test the function with a sample user input
const userInput = "Hello, can you help me with my studies?";
sendMessage(userInput);

