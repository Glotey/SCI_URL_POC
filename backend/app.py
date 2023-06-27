from flask import Flask, request, jsonify
from youtube_dl import YoutubeDL
from pydub import AudioSegment
import torch
import torchaudio
import os
# from nemo.collections.asr.models import JasperEncoderDecoder
from nemo.collections.asr.models import EncDecCTCModel

# from torchaudio.models.quartznet import quartznet5x5, quartznet10x5, quartznet15x5

# print(quartznet5x5)  # QuartzNet 5x5 model
# print(quartznet10x5)  # QuartzNet 10x5 model
# print(quartznet15x5)  # QuartzNet 15x5 model




app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Get the YouTube URL from the request
    url = request.form.get('url')

    # Validate the URL (you can use a regular expression or a library like 'valid-url')

    # Download the YouTube video and convert it to audio
    audio_path = download_and_convert_audio(url)

    # Perform transcription using the Nemo ASR model
    transcription = perform_transcription(audio_path)

    # Save the transcription to a local text file
    save_transcription(transcription)

    # Return the transcription as the API response
    return jsonify({'transcription': transcription})



import subprocess

def download_and_convert_audio(url):
    # Download the YouTube video using youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(app.root_path, "data", "video", "%(title)s.%(ext)s")
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_title = info.get('title', None)
        audio_filename = f"{video_title}.wav" if video_title else 'audio.wav'

    # Get the absolute paths of the video and audio files
    video_path = os.path.abspath(os.path.join(app.root_path, "data", "video", f"{video_title}.mp4"))
    audio_path = os.path.abspath(os.path.join(app.root_path, "data", "video", audio_filename))

    # Convert the video to audio using FFmpeg
    subprocess.run(["ffmpeg", "-i", video_path, audio_path])

    # Delete the downloaded video file
    os.remove(video_path)

    return audio_path


def perform_transcription(audio_path):
    checkpoint_path = "./backend/model/JasperEncoder-STEP-247400.pt"  # Update with the correct path to your checkpoint file

    # Initialize the ASR model
    model = EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base")
    
    # Load the model weights from the checkpoint
    model.load_state_dict(torch.load(checkpoint_path, map_location="cuda" if torch.cuda.is_available() else "cpu"))


    # Move the model to the desired device (e.g., GPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Perform transcription using the loaded model
    def perform_transcription(audio_path):
        # Load and preprocess the audio
        audio, sr = torchaudio.load(audio_path)
        audio = audio.to(device)

        # Perform transcription
        with torch.no_grad():
            predicted_transcripts = model.transcribe(audio)

        return predicted_transcripts

def save_transcription(transcription):
    with open('transcription.txt', 'w') as file:
        file.write(transcription)

if __name__ == '__main__':
    app.run(debug=True)
