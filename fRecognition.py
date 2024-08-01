import face_recognition
import cv2
import numpy as np

#TODO need to find a way to break out of loop when program hears wakeword
def recognize_face(keyword_index):
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    detecting_face = True
    i_known_image = face_recognition.load_image_file("")
    # v_known_image = face_recognition.load_image_file("")
    b_known_image = face_recognition.load_image_file("")
    b_face_encoding = face_recognition.face_encodings(b_known_image)[0]
    i_face_encoding = face_recognition.face_encodings(i_known_image)[0]
    # l_known_image = face_recognition.load_image_file("")
    # t_known_image = face_recognition.load_image_file("")
    faces = [b_known_image, i_known_image]

    known_face_encodings = [b_face_encoding, i_face_encoding]

    known_face_names = [
        "Brian",
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    while keyword_index < 0:
        ret, frame = video_capture.read()
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
        process_this_frame = not process_this_frame
#Release camera, then return names of people found in frame.
    video_capture.release()
    cv2.destroyAllWindows()
    return face_names
