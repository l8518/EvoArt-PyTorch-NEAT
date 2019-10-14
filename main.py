import evoart_server.flask

def run_evoart_server():
    flask_evo = evoart_server.flask.get_instance()
    return flask_evo.run(threaded=True)

if __name__ == "__main__":
    run_evoart_server()
    print("finished")
