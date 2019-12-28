import os
import time
import logging as log
import cv2 as cv
import numpy as np
import face_recognition

# local modules
import config

def process(frames):

    encodings = get_dlib_encodings(frames)

    return encodings

def get_dlib_encodings(frames):

    if len(frames) == 0:
        return []

    log.debug("Encoding faces ...")

    start_exec_time = time.time()
    results = []

    for frame in frames:

        rgb_small_frame = None

        if config.dlib_frame_resize_enabled:
            resize_scale = config.dlib_frame_resize_scale
            small_frame = cv.resize(frame, (0, 0), fx=resize_scale, fy=resize_scale)
            rgb_small_frame = small_frame[:, :, ::-1]
        else:
            rgb_small_frame = frame[:, :, ::-1]

        h, w = rgb_small_frame.shape[:2]
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            known_face_locations=[(0, w, h, 0)],
            num_jitters=0
        )
        results.extend(face_encodings)

    exec_time = time.time() - start_exec_time
    log.debug("Total face(s) encoded: %s", len(results))
    log.debug("Total execution time: %s", exec_time)

    return results

def save_frame(frame):
    image_name = str(time.time()) + "." + config.image_type
    path = os.path.join(config.image_output_directory, image_name)
    cv.imwrite(path, frame, config.cv_image_params)
    log.debug("Locally saved %s", image_name)
    log.debug("Image size: %s KB", float(os.stat(path).st_size / 1000))
    return image_name
