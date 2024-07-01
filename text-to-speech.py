import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

def generate_speech(client, text, model="tts-1", voice="alloy", response_format="mp3", speed=1.0):
    response = client.audio.speech.create(
        model=model,
        input=text,
        voice=voice,
        response_format=response_format,
        speed=speed
    )
    return response.content

def save_audio_file(audio_content, output_path):
    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_content)

def main():
    parser = argparse.ArgumentParser(description="Generate speech using OpenAI's TTS model")
    parser.add_argument('--text', type=str, required=True, help="Text to generate audio for")
    parser.add_argument('--model', type=str, default="tts-1", help="Model to use for speech generation")
    parser.add_argument('--voice', type=str, default="alloy", help="Voice to use for speech generation")
    parser.add_argument('--response_format', type=str, default="mp3", help="Format of the generated audio")
    parser.add_argument('--speed', type=float, default=1.0, help="Speed of the generated audio")
    parser.add_argument('--output', type=str, required=True, help="Path to save the generated audio file")
    
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Generate speech
    audio_content = generate_speech(
        client=client,
        text=args.text,
        model=args.model,
        voice=args.voice,
        response_format=args.response_format,
        speed=args.speed
    )

    # Save the audio file
    save_audio_file(audio_content, args.output)
    
    print(f"Audio saved to {args.output}")

if __name__ == "__main__":
    main()
