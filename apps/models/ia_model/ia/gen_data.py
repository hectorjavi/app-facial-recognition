import cv2
import os
import imutils



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def create_person_folder(data_path, person_name):
    person_path = os.path.join(data_path, person_name)
    if not os.path.exists(person_path):
        print('Carpeta creada: ', person_path)
        os.makedirs(person_path)
    return person_path


def detect_faces(video_path, face_cascade, person_path, max_images=500):
    cap = cv2.VideoCapture(video_path)
    count = 1
    while True:
        ret, frame = cap.read()
        if ret == False or count > max_images:
            break
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = frame.copy()
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x_temp, y_temp, w_temp, h_temp) in faces:
            x = max(0, x_temp - 10)
            y = max(0, y_temp - 10)
            w = min(frame.shape[1] - x, w_temp + 20)
            h = min(frame.shape[0] - y, h_temp + 20)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rostro = aux_frame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(person_path, 'rostro_{}.jpg'.format(count)), rostro)
            count += 1

    cap.release()
    cv2.destroyAllWindows()


def data_generation(person_name, data_path, video_path, max_images):
    person_path = create_person_folder(data_path, person_name)
    detect_faces(
        video_path=str(video_path),
        face_cascade=face_cascade,
        person_path=person_path,
        max_images=max_images
    )
