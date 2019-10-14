from flask import Flask, render_template, Response
from shared.cppn_renderer import CppnRenderer
from shared.audio_preprocessor import AudioPreprocessor
import os
import time
import neat
import random
import pytorch_neat.cppn

# Init the flask server
app = Flask(__name__)
cppn = None

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


def get_cppn():
    # Create population
    pop = neat.Population(config)

    # Determine fitness for each genome.
    def eval_genomes(genomes, config):
        for _, genome in genomes:
            genome.fitness = random.randint(1, 200)

    # returns winning genome
    generations_n = 1
    initial_pop = pop.population.values()
    genome = pop.run(eval_genomes, generations_n)
    return create_cppn(genome, config)


def create_cppn(genome, config):
    """
    Create a CPPN and return it's output node
    :param genome:
    :param config:
    :return:
    """
    # Create CPPN and unpack to output nodes
    [o1] = pytorch_neat.cppn.create_cppn(
        genome,
        config,
        ["x_in", "y_in", "rgb_in", *["f_{0}".format(fn) for fn in range(freq_bands)]],
        ["output_node"]
    )
    return o1

@app.route('/')
def index():
    return render_template('./index.html')


def gen(camera):
    while True:
        time.sleep(0.1)
        frame = camera.get_frame(cppn, 250, 250, audio_preprocessor.current_intensity_band)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/population')
def population():
    return "hello_server"

@app.route('/video_feed')
def video_feed():
    return Response(gen(CppnRenderer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def get_instance():
    global cppn
    cppn = get_cppn()
    audio_preprocessor.hook_audio()
    return app
