// Get references to HTML elements
const urlInput = document.getElementById('urlInput');
const generateButton = document.getElementById('generateButton');
const transcriptionOutput = document.getElementById('transcriptionOutput');

// Add event listener to the generate button
generateButton.addEventListener('click', generateTranscription);

// Function to generate the transcription
function generateTranscription() {
    const url = urlInput.value;

    // Validate the URL
    if (!isValidUrl(url)) {
        transcriptionOutput.innerHTML = 'Invalid URL. Please enter a valid YouTube URL.';
        return;
    }

    // Send the URL to the backend and retrieve the transcription in real-time
    // You will need to make an API request to your backend server to handle this process
    // You can use the Fetch API or a library like Axios to make the request

    // Display the transcription output
    transcriptionOutput.innerHTML = 'Transcription in progress...';
}

// Function to validate the URL
function isValidUrl(url) {
    // Regular expression to validate YouTube URLs
    const youtubeUrlRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+/;

    return youtubeUrlRegex.test(url);
}
