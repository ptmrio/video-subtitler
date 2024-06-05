# Whisper Transcribe

Whisper Transcribe is a tool for transcribing video (creative captions for YouTube etc.) and correcting dialect using OpenAI's Whisper model (Speech to Text) and Chat Completions. This project extracts audio from video files, transcribes the audio, and corrects the text for dialects while maintaining the timing of the original video.

## Features

- Extracts audio from video files
- Automatically splits the audio into smaller segments (Whisper model max filesize: 25 mb)
- Transcribes audio using OpenAI's Whisper model
- Corrects dialects in the transcription using Chat Completions (context aware)

## Installation

### Prerequisites

#### Install FFmpeg

- **Windows**: Download the latest build from the [official website](https://ffmpeg.org/download.html) and add the `bin` directory to your system's PATH.

- **macOS**: Install FFmpeg using [Homebrew](https://brew.sh/):

  ```bash
  brew install ffmpeg
  ```

- **Linux**: Install FFmpeg using your package manager:

  ```bash
    sudo apt-get install ffmpeg
  ```

  ####

  1. Clone the repository:

  ```bash
  git clone https://github.com/ptmrio/whisper-transcribe.git
  cd project-whisper
  ```

### Install Whisper Transcribe (for Linux and macOS, Windows users can use the executable)

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

## Usage

### Running the Python Script

```bash
python whisper.py --file="path_to_your_file.mp4" --language="DE"
```

### Using the Executable (Windows)

1. Navigate to the `dist` directory:

   ```bash
   cd dist
   ```

2. Create a `.env` file from the provided example:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Run the executable:

   ```bash
   whisper.exe --file="path_to_your_file.mp4" --language="DE"
   ```

### Parameters

- `--file` (str, required): Path to the audio or video file.
- `--model` (str, default="whisper-1"): Model to use for transcription.
- `--language` (str): Language of the input audio (ISO-639-1 format).
- `--prompt` (str): Optional text to guide the model's style.
- `--response_format` (str, default="json"): Format of the transcript output.
- `--temperature` (float, default=0): Sampling temperature between 0 and 1.

#### Contributing, License, and Donations

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ptmrio/whisper-transcribe/blob/main/LICENSE) file for details.

## Donations

If you find this project useful, consider donating to support its development:

- [PayPal](paypal.me/Petermeir)

Thank you for your support!
