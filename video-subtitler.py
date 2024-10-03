import os
import sys
import time
import yaml
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
from openai import OpenAI
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, Input, Label, ProgressBar, Static
from textual import work

class FileInput(Input):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_click_time = 0

    def on_click(self, event):
        current_time = time.time()
        if current_time - self.last_click_time < 0.3:  # Double-click detected
            self.show_file_dialog()
        self.last_click_time = current_time

    def show_file_dialog(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio/Video files", "*.mp3 *.wav *.mp4 *.avi *.mov *.mpeg *.mpg")]
        )
        if file_path:
            self.value = file_path
            self.refresh()

class TranscriptionApp(App):
    
    CSS = """
    Screen {
        background: $surface;
        align: center middle;
    }

    #file_input, #language_input, #prompt_input {
        width: 100%;
        margin: 1 0;
    }
    
    #progress {
        height: 1;
        margin: 1 0;
    }

    #status {
        height: 1;
    }

    .container {
        margin: 1 1;
    }

    Horizontal {
        height: 6;
        margin: 1 0;
    }

    Button {
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Enter the path to the audio or video file:"),
            FileInput(id="file_input", placeholder="Double click to browse or enter path..."),
            Horizontal(
                Container(
                    Label("Language (optional):"),
                    Input(id="language_input", placeholder="Enter language code..."),
                ),
                Container(
                    Label("Prompt (optional):"),
                    Input(id="prompt_input", placeholder="Enter prompt..."),
                ),
            ),
            Button("Transcribe", id="transcribe_button", variant="primary"),
            ProgressBar(id="progress", total=100, show_eta=False),
            Static(id="status", expand=True),
            classes="container"
        )


    def on_mount(self) -> None:
        self.load_config()
        self.title = "Video Subtitler"
        self.sub_title = "Transcribe audio and video files with OpenAI"
        
        # set default values only if not empty
        if self.config['default']['language']:
            self.query_one("#language_input").value = self.config['default']['language']
            
        if self.config['default']['stt_prompt']:
            self.query_one("#prompt_input").value = self.config['default']['stt_prompt']

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "transcribe_button":
            self.transcribe_file()

    @work(thread=True)
    def transcribe_file(self) -> None:
        file_path = self.query_one("#file_input").value
        language = self.query_one("#language_input").value
        prompt = self.query_one("#prompt_input").value

        if not file_path:
            self.query_one("#status").update("Please enter a file path.")
            return
        
        file_path = file_path.strip("\"'")
        
        if not os.path.exists(file_path):
            self.query_one("#status").update("File not found. Please check the path.")
            return

        self.query_one("#progress").update(progress=0)
        self.query_one("#status").update("Initializing...")
        
        self.update_progress(1)

        # Load config and initialize OpenAI client
        client = OpenAI(api_key=self.config['openai']['api_key'])

        # Extract audio if the file is a video (5% of progress)
        if file_path.lower().endswith(('.mp4', '.mpeg', '.mpg', '.mov', '.avi')):
            self.query_one("#status").update("Extracting audio from video...")
            audio_file_path = self.extract_audio_from_video(file_path)
            self.update_progress(5)
        else:
            audio_file_path = file_path
            self.update_progress(5)

        # Split audio if necessary (5% of progress)
        if os.path.getsize(audio_file_path) > 25 * 1024 * 1024:
            self.query_one("#status").update("Splitting audio file...")
            file_parts = self.split_audio(audio_file_path)
            self.update_progress(10)
        else:
            file_parts = [audio_file_path]
            self.update_progress(10)

        # 3. Transcribe audio (80% of progress, from 10% to 90%)
        full_transcription = ""
        total_parts = len(file_parts)
        transcription_progress_per_part = 80 / total_parts

        for i, part in enumerate(file_parts, 1):
            self.query_one("#status").update(f"Transcribing part {i} of {total_parts}...")
            transcription = self.transcribe_audio(client, part, language, prompt)
            full_transcription += transcription['text'] + "\n" if isinstance(transcription, dict) else transcription.text + "\n"
            if part != audio_file_path:
                os.remove(part)
            self.update_progress(10 + i * transcription_progress_per_part)

        # 4. Correct transcription (last 10% of progress)
        self.query_one("#status").update("Correcting transcription...")
        corrected_transcription = self.correct_transcription(client, full_transcription.strip(), prompt)

        output_file = f"{file_path}.transcription.txt"
        with open(output_file, "w") as f:
            f.write(corrected_transcription)

        # Clean up extracted audio file if it was created
        if file_path.lower().endswith(('.mp4', '.mpeg', '.mpg', '.mov', '.avi')):
            os.remove(audio_file_path)

        self.update_progress(100)
        self.query_one("#status").update(f"Transcription saved to {output_file}")

    def update_progress(self, percentage):
        self.query_one("#progress").update(progress=percentage)

    def load_config(self):
        self.config = {}
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        config_path = os.path.join(base_path, 'config.yaml')
        
        try:
            with open(config_path, 'r') as config_file:
                self.config = yaml.safe_load(config_file)
            
            if 'openai' not in self.config:
                raise KeyError("'openai' key not found in config")
            
            required_keys = ['api_key', 'stt_model', 'completions_model', 'temperature']
            for key in required_keys:
                if key not in self.config['openai']:
                    raise KeyError(f"Config file missing required key: openai.{key}")
            
            if 'default' not in self.config:
                raise KeyError("'default' key not found in config")
            
            required_keys = ['language', 'stt_prompt', 'tts_voice', 'tts_speed']
            for key in required_keys:
                if key not in self.config['default']:
                    raise KeyError(f"Config file missing required key: default.{key}")
            
        except FileNotFoundError:
            error_msg = f"Config file not found: {config_path}"
            self.query_one("#status").update(error_msg)
        except yaml.YAMLError as e:
            error_msg = f"Error parsing config file: {e}"
            self.query_one("#status").update(error_msg)
        except KeyError as e:
            error_msg = f"Configuration error: {e}"
            self.query_one("#status").update(error_msg)
            
    def extract_audio_from_video(self, video_path):
        audio_path = f"{Path(video_path).stem}.mp3"
        audio = AudioSegment.from_file(video_path)
        audio.export(audio_path, format="mp3")
        return audio_path

    def split_audio(self, file_path, max_size=24 * 1024 * 1024):
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
        
    def transcribe_audio(self, client, file_path, language=None, prompt=None):
        try:
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model=self.config['openai']['stt_model'],
                    file=audio_file,
                    response_format="json",
                    language=language if language else None,
                    prompt=prompt if prompt else None,
                    temperature=self.config['openai']['temperature']
                )
            return transcription
        except Exception as e:
            self.query_one("#status").update(f"Error during transcription: {e}")
            return None

    def correct_transcription(self, client, transcription, prompt=None):
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant for improving transcriptions. You only reply with the improved transcription as requested. NO additional comments or remarks."},
            {"role": "system", "content": "The following transcription might be dialect. Based on context make adequate corrections of the text without altering the sentences structure so that the video timing is still correct. Return only the text without further comments so it can be copied as is."}
        ]
        
        if prompt:
            messages.append({"role": "system", "content": "Special terms or phrases to consider: " + prompt})
            
        messages.append({"role": "user", "content": transcription})
        
        response = client.chat.completions.create(
            messages=messages,
            model=self.config['openai']['completions_model']
        )
        return response.choices[0].message.content

def main():
    app = TranscriptionApp()
    app.run()

if __name__ == "__main__":
    main()