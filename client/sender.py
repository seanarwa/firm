import os
import requests
import threading
import logging as log

# local modules
import config

def connect():

    if not config.data_service_enabled:
        log.error("Unable to connect data sender: data service option is disabled")
        return False

    log.info("Attempting to connect to firm-ds ...")
    log.info("/GET %s", config.data_service_host)
    response = requests.get(config.data_service_host)

    log.info("firm-ds response body: %s", response.content)

    if response.status_code != 200:
        log.error("Error occured when trying to connect to %s", config.data_service_host)
        log.error("Status code: %d", response.status_code)
        return False
    
    log.info("Successfully connected to firm-ds")
    return True

def send_image(image_file_name):

    log.debug("Sending image %s to firm-ds ...", image_file_name)

    image_file_path = os.path.join(config.image_output_directory, image_file_name)
    with open(image_file_path, 'rb') as img_file:
        files = {'image': img_file}
        data = {'name': image_file_name}
        response = requests.post(config.data_service_host, files=files, data=data)
        if response.status_code == 200:
            log.debug("Image successfully sent to firm-ds")
        else:
            log.error("Error occured when trying to send image to firm-ds")

    return
