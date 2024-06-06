# Whisper Transcribe

Whisper Transcribe is an essential tool for content creators who need high-quality captions for their videos. Using OpenAI's Whisper model for Speech to Text and Chat Completions, this project extracts audio from video files, transcribes the audio, and corrects dialects while maintaining the timing of the original video. Perfect for YouTube creators, Whisper Transcribe ensures your captions are accurate and contextually appropriate, enhancing accessibility and viewer engagement.

## Features

- Extracts audio from video files
- Automatically splits the audio into smaller segments (Whisper model max filesize: 25 MB)
- Transcribes audio using OpenAI's Whisper model
- Corrects dialects in the transcription using Chat Completions (context-aware)

## Prerequisites

### Get an OpenAI API Key

1. Go to the [OpenAI API Keys page](https://platform.openai.com/api-keys).
2. Log in or sign up for an account.
3. Click on "Create new secret key" and copy your API key.

### Install FFmpeg

#### Windows

- **Option 1: Download from the official website**:
  1. Download the latest build from the [official website](https://ffmpeg.org/download.html).
  2. Extract the ZIP file to a location on your computer, e.g., `C:\ffmpeg`.
  3. Add the `bin` directory of `ffmpeg` to your system's PATH.

- **Option 2: Install using Chocolatey**:
  1. Install Chocolatey from [chocolatey.org](https://chocolatey.org/install).
  2. Open Command Prompt as Administrator and run:
     ```cmd
     choco install ffmpeg
     ```

- **Option 3: Install using winget**:
  1. Open Command Prompt as Administrator and run:
     ```cmd
     winget install ffmpeg
     ```

#### macOS

- Install FFmpeg using [Homebrew](https://brew.sh/):
  ```bash
  brew install ffmpeg
  ```

#### Linux

- Install FFmpeg using your package manager:
  ```bash
  sudo apt-get install ffmpeg
  ```

## Usage (Windows Executable)

1. Download the latest release from the [Releases](https://github.com/ptmrio/whisper-transcribe/releases) page.
2. Extract the ZIP file to a directory of your choice.
3. Open the directory and create a `.env` file with your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Open Command Prompt in the directory where `whisper.exe` is located.
5. Run the executable with the required arguments:
   ```cmd
   whisper.exe --file="path_to_your_file.mp4" --language="DE"
   ```

6. After processing, the transcription will be saved to a file named `your_file.transcription.json` in the same directory as the original video or audio file. You can open this file with any text editor, copy the transcription, and paste it into a timing editor like YouTube Studio to auto-match the timing of your captions.

## Installation (Universal with Python)

### Clone the Repository

1. Clone the repository:
   ```bash
   git clone https://github.com/ptmrio/whisper-transcribe.git
   cd whisper-transcribe
   ```

### Install Dependencies

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from the provided example:
   ```bash
   cp .env.example .env
   ```

3. Add your OpenAI API key to the `.env` file:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Python Script

1. Run the script with the required arguments:
   ```bash
   python whisper.py --file="path_to_your_file.mp4" --language="DE"
   ```

## Parameters

- `--file` (str, required): Path to the audio or video file.
- `--model` (str, default="whisper-1"): Model to use for transcription.
- `--language` (str): Language of the input audio (ISO-639-1 format).
- `--prompt` (str): Optional text to guide the model's style.
- `--response_format` (str, default="json"): Format of the transcript output.
- `--temperature` (float, default=0): Sampling temperature between 0 and 1.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ptmrio/whisper-transcribe/blob/main/LICENSE) file for details.

## Donations

If you find this project useful, consider donating to support its development:

- [PayPal](https://paypal.me/Petermeir)

Thank you for your support!