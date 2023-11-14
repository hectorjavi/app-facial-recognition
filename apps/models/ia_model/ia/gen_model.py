import cv2
import os
import numpy as np


def get_subdirectories(path):
    subdirectories = [entry.name for entry in os.scandir(path) if entry.is_dir()]
    return subdirectories



def load_faces_data(data_path, info_label):
    people_list = get_subdirectories(data_path)
    labels = []
    faces_data = []
    for name_dir in people_list:
        person_path = os.path.join(data_path, name_dir)
        for file_name in os.listdir(person_path):
            labels.append(info_label[str(name_dir)])
            faces_data.append(cv2.imread(os.path.join(person_path, file_name), 0))

    return faces_data, labels

def train_face_recognizer(faces_data, labels):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces_data, np.array(labels))
    return face_recognizer

def save_face_recognizer_model(face_recognizer, model_path):
    face_recognizer.write(model_path)

def gen_model(data_path, model_path, dict_label_name_dir):
    faces_data, labels = load_faces_data(
        data_path=data_path,
        info_label=dict_label_name_dir
    )
    face_recognizer = train_face_recognizer(faces_data, labels)
    save_face_recognizer_model(face_recognizer, str(model_path))

# if __name__ == "__main__":
#     data_path = 'Data'  # Cambia a la ruta donde hayas almacenado Data
#     model_path = 'modeloLBPHFace.xml'
#     gen_model(data_path, model_path)
