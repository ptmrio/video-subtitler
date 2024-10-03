# Video Subtitler & Text-to-Speech Generator

## Overview

This project provides two standalone tools for **Video Subtitling** and **Text-to-Speech** generation using OpenAI's models. The **Video Subtitler** extracts and transcribes audio from video files, while the **Text-to-Speech Generator** converts text files into speech. Both tools are distributed as `.exe` files for easy use, and they leverage OpenAI’s **Whisper** for transcription and **TTS** for generating speech.

## Features

### Video Subtitler

- Transcribes audio and video files using OpenAI's **Whisper** speech-to-text model.
- Supports video formats like `.mp4`, `.mov`, `.mpeg`, and more.
- Extracts audio from video files and splits large audio files for optimal transcription.
- Offers transcription correction using GPT for refined and accurate text output.
- Customizable with language and prompt settings.

![Text-to-Speech Generator](https://github.com/ptmrio/video-subtitler/blob/main/screenshots/tts.png)

### Text-to-Speech Generator

- Converts text files into speech using OpenAI's **TTS** model.
- Customizable voice selection and speed settings for more control over the output.
- Outputs audio as `.mp3` files.

![Video Subtitler](https://github.com/ptmrio/video-subtitler/blob/main/screenshots/video-subtitler.png)

## Prerequisites

### FFmpeg Installation

FFmpeg is required to handle video and audio processing. Install FFmpeg based on your operating system:

- **Windows Option 1: Install using winget (recommended)**:

  1. Open Command Prompt as Administrator and run:
     ```cmd
     winget install ffmpeg
     ```

- **Windows Option 2: Download from the official website**:

  1. Download the latest build from the [official website](https://ffmpeg.org/download.html).
  2. Extract the ZIP file to a location on your computer, e.g., `C:\ffmpeg`.
  3. Add the `bin` directory of `ffmpeg` to your system's PATH.

- **macOS**: Install via Homebrew:
  ```bash
  brew install ffmpeg
  ```
- **Linux**: Install via APT:
  ```bash
  sudo apt-get install ffmpeg
  ```

### OpenAI API Key

- Obtain an OpenAI API key from [OpenAI's platform](https://platform.openai.com/signup).
- Set this API key in the `config.yaml` file as described in the configuration section.

## Installation

### Windows

1. **Download the ZIP**:

   - Go to the [Releases](https://github.com/ptmrio/video-subtitler/releases) page on GitHub and download the latest `.zip` file.
   - Extract the contents to a directory on your system.

2. **Set Up Configuration**:
   - Rename the `config.example.yaml` file to `config.yaml` and set up the configuration parameters.
   - Basically you only need to set the `openai.api_key` parameter with your OpenAI API key.
   - The `prompt` parameter can be used to teach Video Subtitler about special words or phrases (trademarks, unusual names) that may appear in your video.
   - Example `config.yaml`:
     ```yaml
     openai:
       api_key: sk-XXX
       stt_model: whisper-1
       tts_model: tts-1
       completions_model: gpt-4o
       temperature: 0
     default:
       language: EN
       stt_prompt: PhraseVault, Video Subtitler
       tts_voice: echo
       tts_speed: 1
     ```

### macOS/Linux

1. **Clone the Repository**:
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/ptmrio/video-subtitler.git
     cd video-subtitler
     ```

2. **Set Up Configuration**:
   - see step 2 in the Windows installation instructions.

3. **Install Dependencies**:
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   
4. **Run the Application**:
   - Run the application using Python:
     ```bash
     python video_subtitler.py
     ```
     or
     ```bash
     python text_to_speech.py
     ```


## Usage

### Text-to-Speech Generator

1. Navigate to the downloaded and extracted folder and run the `text-to-speech.exe` file.
2. Enter the path to your `.txt` text-file, customize the voice and speed (if necessary), and click **Generate Speech**.
3. The application will convert the text into speech and save the result as an `.tts.mp3` file.

### Video Subtitler

1. Navigate to the downloaded and extracted folder and run the `video-subtitler.exe` file.
2. Provide the path to your audio or video file and configure optional settings such as language or custom prompts.
3. Click **Transcribe** to begin transcription. The resulting transcription will be saved as a `.transcription.txt` file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Donations

If you find this project useful, consider donating to support its development.

Thank you for your support!