import argparse
import signal
import sys
import logging as log
import cv2 as cv

# local modules
import config
import face_detection
import sender

camera = None

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
	log.debug("Attemping to initiate graceful shutdown ...")
	graceful_shutdown()

def start_webcam():

	global camera

	log.info("Starting webcam ...")

	camera = cv.VideoCapture(config.camera_port, cv.CAP_DSHOW)

	while True:

		ret, orig_frame = camera.read()
		if not ret:
			continue

		orig_frame = cv.flip(orig_frame, 1)
		frames = face_detection.process(orig_frame)
		# encodings = face_detection.get_dlib_encodings(frames)

		for frame in frames:
			image_file_name = face_detection.save_frame(frame)
			sender.send_image(image_file_name)
			# sender.send_frame(frame)

		cv.imshow(config.app_name + " " + config.app_version, orig_frame)

		log.debug("")

		if cv.waitKey(1) == 27:
			graceful_shutdown()
	return

def main():

	signal.signal(signal.SIGINT, signal_handler)

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

	print_banner(config.app_version)

	success = True

	if config.data_service_enabled:
		success = sender.connect()

	if success:
		start_webcam()

if __name__ == "__main__":
    main()
