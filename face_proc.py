import cv2
import face_recognition
import sqlite3


class FaceProc:
    __DARK_GRAY_COLOR = (30, 30, 30)
    __LIGHT_GRAY_COLOR = (80, 80, 80)
    __WHITE_COLOR = (255, 255, 255)
    __FONT = cv2.FONT_ITALIC

    video_capture = -1
    known_faces = None

    def __init__(self, function='Detector', count=False):
        self.function = function
        self.counter = count

    def set_capture(self, source):
        if source == 'BASE':
            self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        elif source == 'USB':
            self.video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        else:
            self.video_capture = cv2.VideoCapture(source, cv2.CAP_DSHOW)  # видео?

    def set_face_base(self):
        self.known_faces = []
        conn = sqlite3.connect('personality.db')
        cur = conn.cursor()
        cur.execute('SELECT image_path FROM person;')
        all_photo_paths = cur.fetchall()
        print(all_photo_paths)
        for element in all_photo_paths:
            for photo_path in element:
                print(str(photo_path))
                image = face_recognition.load_image_file(str(photo_path))
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(face_encoding)
        # image = face_recognition.load_image_file("face_img/Yana Kondratovich.jpg")
        # face_encoding = face_recognition.face_encodings(image)[0]
        # self.known_faces = [
        #     face_encoding,
        # ]

    def start(self):
        face_names = []
        face_amount = 0
        identified_face_names = []

        if self.video_capture == -1:
            raise Exception('Not set video capture')
        elif self.function == 'Recognition' and not self.known_faces:
            raise Exception('Not set faces base for recognition')
        else:
            while True:
                ret, frame = self.video_capture.read()
                rgb_frame = frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_frame)
                if self.counter:
                    if len(face_locations) > face_amount:
                        face_amount = len(face_locations)
                if self.function == 'Recognition':
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    face_names = []
                    for face_encoding in face_encodings:
                        # Проверяем полученные "развертки" на совпадение с имеющимися в базе, если совпадают, даем имя
                        match = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.50)
                        name = None
                        if match[0]:
                            name = "Yanina Kondratovich"
                        face_names.append(name)
                        # Добавляем опознанных в список
                        if self.counter:
                            if name not in identified_face_names and name is not None:
                                identified_face_names.append(name)
                if self.function == 'Detector':
                    for top, right, bottom, left in face_locations:
                        # Рисуем круг вокруг лица
                        radius = int((bottom - top) / 2 + 20)
                        center_coord = (int(left + (right - left) / 2), int(bottom + (top - bottom) / 2))

                        cv2.circle(frame, center_coord, radius, self.__LIGHT_GRAY_COLOR, 3)
                elif self.function == 'Recognition':
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        if not name:
                            # Для неопознанных лиц рисуем круг вокруг лица
                            radius = int((bottom - top) / 2 + 20)
                            center_coord = (int(left + (right - left) / 2), int(bottom + (top - bottom) / 2))

                            cv2.circle(frame, center_coord, radius, self.__LIGHT_GRAY_COLOR, 3)
                        else:
                            # Для опознанных лиц рисуем рамку с подписью вокруг лица
                            cv2.rectangle(frame, (left, top), (right, bottom), self.__DARK_GRAY_COLOR, 3)
                            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), self.__DARK_GRAY_COLOR, cv2.FILLED)
                            cv2.putText(frame, name, (left + 6, bottom - 6), self.__FONT, 0.5, self.__WHITE_COLOR, 1)
                cv2.rectangle(frame, (0, 20), (150, 0), self.__LIGHT_GRAY_COLOR, cv2.FILLED)
                cv2.putText(frame, 'press "q" to exit', (6, 14), self.__FONT, 0.5, self.__WHITE_COLOR, 1)

                cv2.imshow(self.function, frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if self.counter:
            print('Максимальное количество найденных лиц в кадре: {}'.format(face_amount))
            if self.function == 'Recognition':
                print('Из них опознано: {}'.format(len(identified_face_names)))
                print('Список опознанных лиц: {}'.format(' '.join(identified_face_names)))

    def close(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
