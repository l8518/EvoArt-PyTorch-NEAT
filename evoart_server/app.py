import concurrent
import json

import tornado.ioloop
from tornado import gen, web, httpclient
import time
import os
import tornado
from tornado.concurrent import run_on_executor

from shared.cppn_renderer import CppnRenderer
from shared.audio_preprocessor import AudioPreprocessor
import time
import io
import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from evoart_server import EvolutionManager
from collections import ChainMap

evolution_manager = EvolutionManager()
audio_preprocessor = AudioPreprocessor(evolution_manager.get_cppn_freq_bands_inputs())
best_individual = evolution_manager.get_best_individual()
cppn = evolution_manager.transform_cppn(best_individual)
last_frame = b""
thumb_frames = {}
popids = evolution_manager.current_population_ids()
print(popids)

# cppns = { pop_id: evolution_manager.transform_cppn(evolution_manager.get_individual(pop_id)) for pop_id in  popids }
cppns = {pop_id: evolution_manager.transform_cppn(evolution_manager.get_individual(pop_id)) for pop_id in popids}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./templates/index.html", title="My title")


class VisualRenderer(tornado.web.RequestHandler):

    async def get(self):
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Connection', 'close')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--frame')
        self.set_header('Expires', 'Mon, 3 Jan 2000 12:34:56 GMT')
        self.set_header('Pragma', 'no-cache')

        my_boundary = "--frame\n"
        print(last_frame)
        while True:
            await gen.sleep(0.05)
            img = last_frame
            self.write(my_boundary)
            self.write("Content-type: image/png\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(img))
            self.write(img)
            await self.flush()


class PopulationHandler(tornado.web.RequestHandler):

    def get(self):
        val = {
            "population": evolution_manager.current_population_ids()
        }
        self.write(json.dumps(val))


class RenderIndividualHander(tornado.web.RequestHandler):

    async def get(self, popnum):
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Connection', 'close')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--frame')
        self.set_header('Expires', 'Mon, 3 Jan 2000 12:34:56 GMT')
        self.set_header('Pragma', 'no-cache')

        my_boundary = "--frame\n"
        print(last_frame)
        while True:
            await gen.sleep(0.10)

            img = thumb_frames[int(popnum)]
            self.write(my_boundary)
            self.write("Content-type: image/png\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(img))
            self.write(img)
            await self.flush()


class SelectIndividualHandler(tornado.web.RequestHandler):

    def post(self, popnum):
        evolution_manager.evolve(popnum)
        global best_individual
        best_individual = evolution_manager.get_best_individual()
        global cppn
        cppn = evolution_manager.transform_cppn(best_individual)

        # Refresh all cppns:
        global cppns
        cppns = {pop_id: evolution_manager.transform_cppn(evolution_manager.get_individual(pop_id)) for pop_id in
                 evolution_manager.current_population_ids()}

        self.write(json.dumps({}))


def render_pop(pop_id, pop_cppn, intensity_band):
    return {pop_id: CppnRenderer().get_frame(pop_cppn, 50, 50, intensity_band, 4)}


def render():
    global last_frame
    global thumb_frames
    global cppns
    while True:
        time.sleep(0.10)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            intensity_band = audio_preprocessor.current_intensity_band
            renderings = [executor.submit(render_pop, popid, popcppn, intensity_band) for (popid, popcppn) in
                          cppns.items()]
            for future in concurrent.futures.as_completed(renderings):
                try:
                    pass
                except Exception as exc:
                    print('%r generated an exception: %s' % (exc))
        thumb_results = [render.result() for render in renderings]
        last_frame = CppnRenderer().get_frame(cppn, 50, 50, intensity_band, 4)
        thumb_frames = dict(ChainMap(*thumb_results))


def get_instance():
    audio_preprocessor.hook_audio()
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(render)
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/video", VisualRenderer),
        (r"/current_population", PopulationHandler),
        (r"/render_individual/([^/]+)", RenderIndividualHander),
        (r"/select_individual/([^/]+)", SelectIndividualHandler)
    ])
