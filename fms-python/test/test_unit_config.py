import pytest
import sys
sys.path.append("..")

import config

def test_load():

    config.load("test_unit_config_sample.yaml")
    assert config.app_version != "0.0.0"
    assert config.camera_port == 11
    assert config.draw_enabled == True
    assert config.draw_face == True
    assert config.draw_eyes == True
    assert config.draw_nose == True
    assert config.draw_mouth == True

    return

def test_set_logging():

    config.set_logging("INFO", log_file="result/test_unit_config.log", log_timestamp=False)

    return
