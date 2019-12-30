import argparse
import signal
import sys
import os
import gc
import logging as log
import cv2 as cv
from flask import Flask
from flask import request
from flask.logging import default_handler
from queue import Queue
from threading import Thread
import multiprocessing
import time
import json
import numpy as np
import base64
from PIL import Image

app = Flask(__name__)

# local modules
import config
import face_encoding
# import face_core
import sender

# globals
queue = None
pool = None

def worker(worker_queue):

	while True:

		image = worker_queue.get(True)
		encodings = face_encoding.process([image])

		encoding = encodings[0] if len(encodings) > 0 else []

		insert_visit = {
			'image': "this is an image",
			'imageEncoding': encoding.tolist()
		}

		sender.send_request(config.services_mongodb + '/visit', json.dumps(insert_visit), sender.HTTP_HEADERS)

		print("Face match complete at process %d" % (os.getpid()))
		print("Current queue size: %d" % (worker_queue.qsize()))

		del image
		del encodings
		gc.collect()

def print_banner(app_name, app_version):
	spaced_text = " " + str(app_name) + " " + str(app_version) + " "
	banner = spaced_text.center(78, '=')
	filler = ''.center(78, '=')
	log.info(filler)
	log.info(banner)
	log.info(filler)

def graceful_shutdown():
	log.info('Gracefully shutting down %s ...', config.app_name)
	queue.close()
	pool.terminate()
	pool.close()
	pool.join()
	sys.exit(0)

def signal_handler(sig, frame):
	log.debug("%s received", signal.Signals(2).name)
	log.debug("Attemping to initiate graceful shutdown ...")
	graceful_shutdown()

@app.route('/', methods=['GET'])
def get_index():
	return str(config.app_name) + " is running"

@app.route('/', methods=['POST'])
def post_index():

	global queue, pool

	if not os.path.exists(config.image_output_directory):
		os.makedirs(config.image_output_directory)

	image_file = request.files['image']
	image_file_buf = image_file.read()
	npimg = np.fromstring(image_file_buf, np.uint8)
	image = cv.imdecode(npimg, cv.IMREAD_COLOR)
	# queue.put((image, image_file_buf))
	queue.put(image)

	log.debug("Queued process with image %s" % (image_file.filename))
	log.debug("Current queue size: %d" % (queue.qsize()))

	return ""

def main():

	global app, queue, pool

	signal.signal(signal.SIGINT, signal_handler)

	# set path to main.py path
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	parser = argparse.ArgumentParser(
		description='Entrypoint script for face-identity-registry-matching (FIRM)'
	)
	parser.add_argument(
		'-f',
		'--config_file',
		help='Path to configuration file.',
		default='config/app.yaml'
	)
	args = parser.parse_args()

	config.load(args.config_file)

	queue = multiprocessing.Queue()
	pool = multiprocessing.Pool(config.processing_num_of_workers, worker, (queue, ))

	print_banner(config.app_name, config.app_version)

	logger = log.getLogger('werkzeug')
	logger.setLevel(log.ERROR)
	app.run(host='127.0.0.1', port=config.flask_port, debug=config.flask_debug)

if __name__ == "__main__":
	main()
