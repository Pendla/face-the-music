import os
import sys
import collections

import face_recognition

def find_images_by_person(path, supported_formats=['jpg', 'jpeg', 'png']):
    """Walks through sub-folders at the given path and finds images in each
    sub-folder with the given supported formats. The folder structure is
    assumed to be such that each sub-folder contains images of one person, and
    that sub-folder is named after a unique identifier for that person.

    Example:
        If the path is 'faces/' the folder-structure should be as follows:
        faces/
            john/1.jpg
            john/2.png
            doe/1.png
            doe/3.jpeg

        This folder structure will give a result as follows:
            {
                'john': ['faces/john/1.jpg', 'faces/john/2.png'],
                'doe': ['faces/doe/1.png', 'faces/doe/3.jpeg']
            }

    Params:
        path: The base path to start the search for images from.
        supported_formats: A list of supported file formats that should be
            returned in the final list of files.

    Returns:
        A dictionary with keys taken from the sub-folders names in path, and
        where each value is a list of paths to each image for that person. The
        resulting image paths are relative to the given path parameter.
    """
    result = collections.defaultdict(list)
    for (current_dir, dir_names, file_names) in os.walk(path):
        # Construct a list of filepaths of the files in the current directory.
        # The filepaths will have the same base as the path parameter.
        # Furthermore only files with a supported format will be in the list.
        image_files = [
            current_dir + "/" + f for f in file_names
                if f.endswith(tuple(supported_formats))
        ]

        if not image_files:
            continue

        # By assumption of the subfolder file structure of the given path,
        # we find the identifier by taking the name of the current directory.
        identifier = current_dir.split('/')[-1]

        result[identifier].extend(image_files)

    return result
