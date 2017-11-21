import face_recognition


def get_face_coordinates(img):
    image = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(image)

    return face_locations


def verify_face(known_img, unknown_image):
    known = face_recognition.load_image_file(known_img)
    unknown = face_recognition.load_image_file(unknown_image)

    known_encoding = face_recognition.face_encodings(known)[0]
    unknown_encoding = face_recognition.face_encodings(unknown)[0]

    results = face_recognition.compare_faces([known_encoding],
                                             unknown_encoding)

    return results
