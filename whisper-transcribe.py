import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence
from openai import OpenAI
from dotenv import load_dotenv

def transcribe_audio(client, file_path, model="whisper-1", language=None, prompt=None, response_format="json", temperature=0):
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format=response_format,
            language=language,
            prompt=prompt,
            temperature=temperature
        )
        return transcription

def split_audio(file_path, max_size=24 * 1024 * 1024):
    audio = AudioSegment.from_file(file_path)
    chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40)

    output_files = []
    current_chunk = AudioSegment.empty()
    current_size = 0

    for chunk in chunks:
        chunk_size = len(chunk.raw_data)
        if current_size + chunk_size > max_size:
            output_file = f"{file_path}_part_{len(output_files)}.mp3"
            current_chunk.export(output_file, format="mp3")
            output_files.append(output_file)
            current_chunk = AudioSegment.empty()
            current_size = 0

        current_chunk += chunk
        current_size += chunk_size

    if len(current_chunk.raw_data) > 0:
        output_file = f"{file_path}_part_{len(output_files)}.mp3"
        current_chunk.export(output_file, format="mp3")
        output_files.append(output_file)

    return output_files

def extract_audio_from_video(video_path):
    audio_path = f"{os.path.splitext(video_path)[0]}.mp3"
    audio = AudioSegment.from_file(video_path)
    audio.export(audio_path, format="mp3")
    return audio_path

def correct_transcription(client, transcription):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant for improving transcriptions. You only reply with the improved transcription as requested. NO additional comments or remarks."},
            {"role": "user", "content": "The following transcription might be dialect. Based on context make adequate corrections of the text without altering the sentences structure so that the video timing is still correct. Return only the text without further comments so it can be copied as is."},
            {"role": "user", "content": transcription}
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using OpenAI's Whisper model")
    parser.add_argument('--file', type=str, required=True, help="Path to the audio or video file")
    parser.add_argument('--model', type=str, default="whisper-1", help="Model to use for transcription")
    parser.add_argument('--language', type=str, help="Language of the input audio (ISO-639-1 format)")
    parser.add_argument('--prompt', type=str, help="Optional text to guide the model's style")
    parser.add_argument('--response_format', type=str, default="json", help="Format of the transcript output")
    parser.add_argument('--temperature', type=float, default=0, help="Sampling temperature between 0 and 1")
    
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Extract audio if the file is a video
    if args.file.endswith(('.mp4', '.mpeg', '.mpg', '.mov', '.avi')):
        audio_file_path = extract_audio_from_video(args.file)
    else:
        audio_file_path = args.file

    # Check the file size
    if os.path.getsize(audio_file_path) > 25 * 1024 * 1024:
        file_parts = split_audio(audio_file_path)
    else:
        file_parts = [audio_file_path]

    full_transcription = ""

    for part in file_parts:
        transcription = transcribe_audio(
            client=client,
            file_path=part,
            model=args.model,
            language=args.language,
            prompt=args.prompt,
            response_format=args.response_format,
            temperature=args.temperature
        )
        full_transcription += transcription['text'] + "\n" if isinstance(transcription, dict) else transcription.text + "\n"
        if part != audio_file_path:
            os.remove(part)  # Delete the temporary audio chunk after transcription

    corrected_transcription = correct_transcription(client, full_transcription.strip())

    output_file = f"{args.file}.transcription.txt"
    with open(output_file, "w") as f:
        f.write(corrected_transcription)
    
    print(f"Transcription saved to {output_file}")

    # Clean up extracted audio file if it was created
    if args.file.endswith(('.mp4', '.mpeg', '.mpg', '.mov', '.avi')):
        os.remove(audio_file_path)

if __name__ == "__main__":
    main()
