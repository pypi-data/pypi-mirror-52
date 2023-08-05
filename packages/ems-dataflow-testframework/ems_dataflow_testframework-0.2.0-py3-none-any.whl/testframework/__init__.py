from os import path

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

RESOURCES = full_path = path.abspath("testframework/resources")


def resource(resource_name: str):
    return path.join(RESOURCES, resource_name)
