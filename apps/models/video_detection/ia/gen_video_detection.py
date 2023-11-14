import cv2

def cargar_modelo(modelo_path):
    face_recognizer = cv2.face_LBPHFaceRecognizer.create()
    face_recognizer.read(modelo_path)
    return face_recognizer

def reconocer_rostros(faces, gray, face_recognizer, labels_model):
    if len(faces) == 0:
        return None, None

    (x, y, w, h) = faces[0]  # Tomar solo el primer rostro detectado
    rostro = gray[y:y+h, x:x+w]
    rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
    result = face_recognizer.predict(rostro)
    confidence = result[1]

    if confidence < 70:
        label = labels_model[result[0]]
    else:
        label = "Desconocido"
        
    return label, confidence

def video_detection_model(input_video_path, output_video_path, modelo_path, labels_model):
    face_recognizer = cargar_modelo(modelo_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(3))
    height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            label, confidence = reconocer_rostros([(x, y, w, h)], gray, face_recognizer, labels_model)

            # Dibujar resultados en el frame original
            cv2.putText(frame, '{}'.format(label), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            if confidence < 70:
                cv2.putText(frame, '{}'.format(label), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        out.write(frame)

    cap.release()
    out.release()
