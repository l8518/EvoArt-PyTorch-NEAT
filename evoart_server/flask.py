from flask import Flask, render_template, Response, json, send_file
from shared.cppn_renderer import CppnRenderer
from shared.audio_preprocessor import AudioPreprocessor
import time
import io
import random

from evoart_server import EvolutionManager

# Init the flask server
app = Flask(__name__)
evolution_manager = EvolutionManager()
audio_preprocessor = AudioPreprocessor(evolution_manager.get_cppn_freq_bands_inputs())


@app.route('/')
def index():
    return render_template('./index.html')


def gen(camera):
    best_individual = evolution_manager.get_best_individual()
    cppn = evolution_manager.transform_cppn(best_individual)
    while True:
        time.sleep(0.1)
        frame = camera.get_frame(cppn, 250, 250, audio_preprocessor.current_intensity_band)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/population/<popnum>', methods=['GET'])
def get_population(popnum):
    return popnum


@app.route('/popsize', methods=['GET'])
def get_population_size():
    val = {
        "pop_size": evolution_manager.max_population()
    }
    response = app.response_class(
        response=json.dumps(val),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/render_individual/<popnum>', methods=['GET'])
def render_individual(popnum):
    cppnRender = CppnRenderer()
    indi = evolution_manager.get_individual(int(popnum) - 1)
    cppn = evolution_manager.transform_cppn(indi)
    frame = cppnRender.get_frame(cppn, 250, 250, audio_preprocessor.current_intensity_band)
    return send_file(
        io.BytesIO(frame),
        mimetype='image/jpeg',
        as_attachment=True,
        attachment_filename="{0}.jpeg".format(popnum))


@app.route('/select_individual/<popnum>', methods=['POST'])
def select_population(popnum):
    evolution_manager.evolve(popnum)


@app.route('/video_feed')
def video_feed():
    return Response(gen(CppnRenderer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def get_instance():
    audio_preprocessor.hook_audio()
    return app
