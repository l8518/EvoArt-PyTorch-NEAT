import concurrent
import cppn_visualization_server.flask
import cppn_evolution_server.flask

def run_vis():
    flask_vis = cppn_evolution_server.flask.get_instance()
    return flask_vis.run()

def run_evo():
    flask_evo = cppn_visualization_server.flask.get_instance()
    return flask_evo.run(port=5001)

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_vis)
        executor.submit(run_evo)
    print("finished")
