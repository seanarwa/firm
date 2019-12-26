import argparse
import signal
import sys
import os
import time
import logging as log
from queue import Queue
from threading import Thread
import cv2 as cv

# local modules
import config
import face_detection
import face_encoding
import sender

# globals
queue = Queue()
camera = None

class Worker(Thread):

	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			frames = self.queue.get()
			try:
				frames = face_detection.process(frames)
				for frame in frames:
					image_file_name = save_frame(frame)
					# sender.send_frame(frame)
					sender.send_image(image_file_name)
			finally:
				self.queue.task_done()

def print_banner(app_version):
    spaced_text = " FIRM " + str(app_version) + " "
    banner = spaced_text.center(78, '=')
    filler = ''.center(78, '=')
    log.info(filler)
    log.info(banner)
    log.info(filler)

def graceful_shutdown():
	log.info('Gracefully shutting down FIRM ...')
	if camera is not None:
		camera.release()
	cv.destroyAllWindows()
	sys.exit(0)

def signal_handler(sig, frame):
	log.debug("%s received", signal.Signals(2).name)
	log.debug("Attempting to initiate graceful shutdown ...")
	graceful_shutdown()

def start_capture():

	global queue
	global camera

	log.info("Starting capture ...")

	camera = cv.VideoCapture(config.camera_port, cv.CAP_DSHOW)

	while True:

		ret, orig_frame = camera.read()
		if not ret:
			continue

		orig_frame = cv.flip(orig_frame, 1)
		queue.put([orig_frame])

		cv.imshow(config.app_name + " " + config.app_version, orig_frame)

		log.debug("")

		if cv.waitKey(1) == 27:
			graceful_shutdown()

	return

def save_frame(frame):
    image_name = str(time.time()) + "." + config.image_type
    path = os.path.join(config.image_output_directory, image_name)
    cv.imwrite(path, frame, config.cv_image_params)
    log.debug("Locally saved %s", image_name)
    log.debug("Image size: %s KB", float(os.stat(path).st_size / 1000))
    return image_name

def main():

	global queue

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

	for x in range(100):
		worker = Worker(queue)
		# setting daemon to True will ignore lifetime of other threads
		worker.daemon = True
		worker.start()

	# load app.yaml
	config.load(args.config_file)

	print_banner(config.app_version)

	success = True

	if config.data_service_enabled:
		success = sender.connect()

	if success:
		start_capture()

if __name__ == "__main__":
    main()
