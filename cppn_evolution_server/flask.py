from flask import Flask, render_template
from shared.audio_preprocessor import AudioPreprocessor
import os
import time
import neat


# Init the flask server
app = Flask(__name__)

# Load Python-NEAT config
config_path = os.path.join(os.path.dirname(__file__), "../neat.cfg")
config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path,
)

freq_bands = config.genome_config.num_inputs - 3
audio_preprocessor = AudioPreprocessor(freq_bands)

@app.route('/')
def index():
    return render_template('./index.html')


def get_instance():
    audio_preprocessor.hook_audio()
    return app
