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
best_individual = evolution_manager.get_best_individual()
cppn = evolution_manager.transform_cppn(best_individual)

@app.route('/')
def index():
    return render_template('./index.html')


def gen(camera):
    while True:
        time.sleep(0.04)
        frame = camera.get_frame(cppn, 250, 250, audio_preprocessor.current_intensity_band)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/population/<popnum>', methods=['GET'])
def get_population(popnum):
    return popnum


@app.route('/current_population', methods=['GET'])
def get_current_population():
    val = {
        "population": evolution_manager.current_population_ids()
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
    indi = evolution_manager.get_individual(popnum)
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
    global best_individual
    best_individual = evolution_manager.get_best_individual()
    global cppn
    cppn = evolution_manager.transform_cppn(best_individual)
    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/video_feed')
def video_feed():
    return Response(gen(CppnRenderer()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def get_instance():
    audio_preprocessor.hook_audio()
    return app
