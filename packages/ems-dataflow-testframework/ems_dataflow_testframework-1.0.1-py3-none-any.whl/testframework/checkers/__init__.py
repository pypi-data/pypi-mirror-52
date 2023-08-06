import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(funcName)s %(levelname)-8s %(message)s')

current_dir = os.path.dirname(os.path.abspath(__file__))

def resource(resource_name: str):
    return os.path.join(current_dir + "/../resources", resource_name)