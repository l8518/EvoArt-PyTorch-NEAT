from flask import Flask

app = Flask(__name__)


@app.route('/')
def root():
    return 'This would return a video stream'


def get_instance():
    return app
