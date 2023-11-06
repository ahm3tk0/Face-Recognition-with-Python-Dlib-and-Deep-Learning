import pickle
import cv2
import os

from utils import get_image_paths
from utils import face_encodings
from utils import nb_of_matches

root_dir = "dataset"
class_names = os.listdir(root_dir)

# get the paths to the images
image_paths = get_image_paths(root_dir, class_names)
# initialize a dictionary to store the name of each person and the corresponding encodings



# load the encodings + names dictionary
with open("encodings.pickle", "rb") as f:
    name_encodings_dict = pickle.load(f)
names = []
nb_current_image = 1
for image_path in image_paths:
    if int(image_path.split(os.path.sep)[-1].split('_')[-1].split('.')[0]) != 1:
        print(f"Image processed {nb_current_image}/{len(image_paths)-len(class_names)}")
        # load the input image
        image = cv2.imread(image_path)
        # get the 128-d face embeddings for each face in the input image
        encodings_image = face_encodings(image)
        # this list will contain the names of each face detected in the image

        if encodings_image==[]:
            names.append({" Test Photo Name":image_path.split(os.path.sep)[-1],"Matching Face Poto Name":None,"Similarity":None,"Find_Face":False,"Correct_Similarity":None})
        # loop over the encodings
        for encoding in encodings_image:
            # initialize a dictionary to store the name of the
            # person and the number of times it was matched
            counts = {}
            similarity = {}
            # loop over the known encodings
            for (name, encodings) in name_encodings_dict.items():
                # compute the number of matches between the current encoding and the encodings
                # of the known faces and store the number of matches in the dictionary
                if encodings==[]:
                    pass
                else:
                    counts[name],similarity[name] = nb_of_matches(encodings, encoding)
            # check if all the number of matches are equal to 0
            # if there is no match for any name, then we set the name to "Unknown"
            if all(count == 0 for count in counts.values()):
                name = "Unknown"
                correct_sim = False
            # otherwise, we get the name with the highest number of matches
            else:
                name = max(similarity, key=similarity.get)
                if image_path.split(os.path.sep)[-1].split('_')[:-1]==name.split('_')[:-1]:
                    correct_sim = True
                else:
                    correct_sim = False
            # add the name to the list of names
            names.append({" Test Photo Name":image_path.split(os.path.sep)[-1],"Matching Face Poto Name":name,"Similarity":similarity[name][0],"Find_Face":True,"Correct_Similarity":correct_sim})
            nb_current_image += 1

with open("labels_lfw.pickle", "wb") as f:
    pickle.dump(names, f)