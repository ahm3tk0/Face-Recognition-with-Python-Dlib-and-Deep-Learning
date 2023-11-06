import dlib
from glob import glob
import cv2
import numpy as np
import os
from numpy import dot
from numpy.linalg import norm

# load the face detector, landmark predictor, and face recognition model
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
face_encoder = dlib.face_recognition_model_v1("models/dlib_face_recognition_resnet_model_v1.dat")

# change this to include other image formats you want to support (e.g. .webp)
VALID_EXTENSIONS = ['.png', '.jpg', '.jpeg']


def get_image_paths(root_dir, class_names):
    """ grab the paths to the images in our dataset"""
    image_paths = []

    # loop over the class names
    for class_name in class_names:
        # grab the paths to the files in the current class directory
        class_dir = os.path.sep.join([root_dir, class_name])
        class_file_paths = glob(os.path.sep.join([class_dir, '*.*']))

        # loop over the file paths in the current class directory
        for file_path in class_file_paths:
            # extract the file extension of the current file
            ext = os.path.splitext(file_path)[1]

            # if the file extension is not in the valid extensions list, ignore the file
            if ext.lower() not in VALID_EXTENSIONS:
                print("Skipping file: {}".format(file_path))
                continue

            # add the path to the current image to the list of image paths
            image_paths.append(file_path)

    return image_paths


def face_rects(image):
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = face_detector(gray, 1)
    size = 0
    rect=[]
    for item in rects:
        con_tmp = convert_and_trim_bb(image, item)
        size_tmp = con_tmp[2] * con_tmp[3]
        if size_tmp > size:
            size = size_tmp
            rect = [item]
    # return the bounding boxes
    return rect


def face_landmarks(image):
    return [shape_predictor(image, face_rect) for face_rect in face_rects(image)]


def face_encodings(image):
    # compute the facial embeddings for each face
    # in the input image. the compute_face_descriptor
    # function returns a 128-d vector that describes the face in an image
    return [np.array(face_encoder.compute_face_descriptor(image, face_landmark))
            for face_landmark in face_landmarks(image)]


def nb_of_matches(known_encodings, unknown_encoding):
    # compute the euclidean distance between the current face encoding
    # and all the face encodings in the database
    distances = np.linalg.norm(known_encodings - unknown_encoding, axis=1)
    # keep only the distances that are less than the threshold
    small_distances = distances <= 0.6
    # return the number of matches
    cos_sim = dot(known_encodings, unknown_encoding) / (norm(known_encodings) * norm(unknown_encoding))
    return sum(small_distances),cos_sim





def convert_and_trim_bb(image, rect):
    # extract the starting and ending (x, y)-coordinates of the
    # bounding box
    startX = rect.left()
    startY = rect.top()
    endX = rect.right()
    endY = rect.bottom()
    # ensure the bounding box coordinates fall within the spatial
    # dimensions of the image
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(endX, image.shape[1])
    endY = min(endY, image.shape[0])
    # compute the width and height of the bounding box
    w = endX - startX
    h = endY - startY
    # return our bounding box coordinates
    return (startX, startY, w, h)