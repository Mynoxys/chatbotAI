import fetch from 'node-fetch'; // Use import instead of require

async function sendMessage(userInput) {
    if (userInput.trim() === '') {
        console.log('Input is empty');
        return;
    }

    try {
        const response = await fetch('https://academiaatlas-45e6821ef7ff.herokuapp.com/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Server response:', data); // Log the server response

        // Extract the plain text version of the AI response
        const aiMessage = extractPlainText(data.reply);
        console.log('AI:', aiMessage);
    } catch (error) {
        console.error('Error:', error);
    }
}

function extractPlainText(response) {
    // Use a regular expression to remove unwanted characters and formatting
    const plainText = response.replace(/\\n/g, '\n').replace(/\\'/g, "'").replace(/\\"/g, '"').replace(/\s*\+\s*/g, '');
    return plainText;
}

// Manually input the user message here
const userInput = 'Hi ai';
sendMessage(userInput);
