import os
import sys
import time
import yaml
from pathlib import Path
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
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.value = file_path
            self.refresh()

class TextToSpeechApp(App):
    CSS = """
    Screen {
        background: $surface;
        align: center middle;
    }

    #file_input, #voice_input, #speed_input {
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
            Label("Enter the path to the text file:"),
            FileInput(id="file_input", placeholder="Double click to browse or enter path..."),
            Horizontal(
                Container(
                    Label("Voice:"),
                    Input(id="voice_input", placeholder="Enter voice..."),
                ),
                Container(
                    Label("Speed:"),
                    Input(id="speed_input", placeholder="Enter speed..."),
                ),
            ),
            Button("Generate Speech", id="generate_button", variant="primary"),
            ProgressBar(id="progress", total=100, show_eta=False),
            Static(id="status", expand=True),
            classes="container"
        )

    def on_mount(self) -> None:
        self.load_config()
        self.title = "Text-to-Speech Generator"
        self.sub_title = "Generate speech from text files with OpenAI"
        
        # Set default values
        if self.config['default']['tts_voice']:
            self.query_one("#voice_input").value = self.config['default']['tts_voice']
        
        if self.config['default']['tts_speed']:
            self.query_one("#speed_input").value = str(self.config['default']['tts_speed'])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate_button":
            self.generate_speech()

    @work(thread=True)
    def generate_speech(self) -> None:
        file_path = self.query_one("#file_input").value
        voice = self.query_one("#voice_input").value
        speed = self.query_one("#speed_input").value

        if not file_path:
            self.query_one("#status").update("Please enter a file path.")
            return
        
        file_path = file_path.strip("\"'")
        
        if not os.path.exists(file_path):
            self.query_one("#status").update("File not found. Please check the path.")
            return

        self.query_one("#progress").update(progress=0)
        self.query_one("#status").update("Initializing...")
        
        self.update_progress(10)

        # Load config and initialize OpenAI client
        client = OpenAI(api_key=self.config['openai']['api_key'])

        # Read text from file
        with open(file_path, 'r') as file:
            text = file.read()

        self.query_one("#status").update("Generating speech...")
        self.update_progress(20)

        try:
            audio_content = self.generate_speech_content(
                client=client,
                text=text,
                model=self.config['openai']['tts_model'],
                voice=voice,
                speed=float(speed) if speed else 1.0
            )
            self.update_progress(80)

            # Save the audio file
            output_path = file_path.rsplit('.', 1)[0] + '.tts.mp3'
            self.save_audio_file(audio_content, output_path)
            self.update_progress(100)

            self.query_one("#status").update(f"Audio saved to {output_path}")
        except Exception as e:
            self.query_one("#status").update(f"Error during speech generation: {e}")

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
            
            required_keys = ['api_key', 'tts_model']
            for key in required_keys:
                if key not in self.config['openai']:
                    raise KeyError(f"Config file missing required key: openai.{key}")
            
            if 'default' not in self.config:
                raise KeyError("'default' key not found in config")
            
            default_keys = ['tts_voice', 'tts_speed']
            for key in default_keys:
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

    def generate_speech_content(self, client, text, model, voice, speed):
        response = client.audio.speech.create(
            model=model,
            input=text,
            voice=voice,
            response_format="mp3",
            speed=speed
        )
        return response.content

    def save_audio_file(self, audio_content, output_path):
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_content)

def main():
    app = TextToSpeechApp()
    app.run()

if __name__ == "__main__":
    main()