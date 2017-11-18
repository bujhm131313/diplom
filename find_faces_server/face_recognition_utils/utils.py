import face_recognition


def get_face_coordinates(img):
    image = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(image)

    return face_locations
