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

def calculate_codecs_by_person(images_by_person):
    """Converts a dictionary with array of image paths as values into a
    dictionary with an array of face codecs as values.

    Params:
        images_by_person: A dictionary where each key is a person and the
            values is an array of paths to images with only that person in the
            image.

    Returns:
        A dictionary with one entry per entry in the images_by_person param.
        The values for each key is an array of face codecs.
    """
    codecs_by_person = collections.defaultdict(list)

    for identifier, img_paths in images_by_person.items():
        for img in [face_recognition.load_image_file(p) for p in img_paths]:
            encodings = face_recognition.face_encodings(img)

            if not encodings:
                print(
                    ("Couldn't find a face in training image {} for {}. "
                     "Skipping this image.").format(img, identifier)
                )
            elif len(encodings) > 1:
                print(
                    ("Found more than 1 face in training image {} for {}. "
                     "Skipping this image.").format(img, identifier)
                )
            else:
                # At this point we know length of encodings is 1. Thus we can
                # safely extract index 0
                codecs_by_person[identifier].append(encodings[0])

    return codecs_by_person
