import sys
import face_recognition

known_image = face_recognition.load_image_file('faces/simon.jpg')
known_encodings = face_recognition.face_encodings(known_image)

unknown_image = face_recognition.load_image_file('faces/unknown.jpg')
unknown_encodings = face_recognition.face_encodings(unknown_image)

if len(known_encodings) == 0:
    print("Couldn't find a face in the known image")
    sys.exit()

if len(unknown_encodings) == 0:
    print("Couldn't find a face in the unknown image")
    sys.exit()

for unknown_encoding in unknown_encodings:
    result = face_recognition.compare_faces(known_encodings, unknown_encoding)
    print(result)
