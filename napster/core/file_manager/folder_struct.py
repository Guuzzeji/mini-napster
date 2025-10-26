import os

from napster.core.constants import BASE_EVERYTHING_FOLDER

def create_base_folder():
    if not os.path.exists(BASE_EVERYTHING_FOLDER):
        os.makedirs(BASE_EVERYTHING_FOLDER)