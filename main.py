import tornado
from tornado.ioloop import IOLoop

import evoart_server.app

def run_evoart_server():
    app_evo = evoart_server.app.get_instance()


    server = tornado.httpserver.HTTPServer(app_evo)
    server.bind(8888)
    server.start()
    IOLoop.current().start()

    return

if __name__ == "__main__":
    run_evoart_server()
    print("finished")
