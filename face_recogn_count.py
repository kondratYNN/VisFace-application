# Импорт библиотек и константы
import cv2
import face_recognition
import pynput

DGRAY_COLOR = (30, 30, 30)
LGRAY_COLOR = (80, 80, 80)
WHITE_COLOR = (255, 255, 255)
FONT = cv2.FONT_ITALIC


# Получаем доступ к камере ноутбука
video_capture = cv2.VideoCapture(0)
print('1 stage')

# Загружаем известные программе лица
image = face_recognition.load_image_file("face_img/Yana Kondratovich.jpg")
face_encoding = face_recognition.face_encodings(image)[0]
known_faces = [
    face_encoding,
]
print('2 stage')

face_locations = []
face_encodings = []
face_names = []
face_amount = 0
identified_face_names = []

while True:
    # Берем один кадр из видео
    ret, frame = video_capture.read()

    # Переводим изображение из BGR кодировки(OpenCV использует её) в RGB для face_recognition
    rgb_frame = frame[:, :, ::-1]

    # Находим все лица в кадре
    face_locations = face_recognition.face_locations(rgb_frame)

    # Получаем общее количество лиц в кадре
    if len(face_locations) > face_amount:
        face_amount = len(face_locations)

    # Получаем "развертки" для лиц
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # Проверяем полученные "развертки" на совпадение с имеющимися в базе, если совпадают, даем имя
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
        name = None
        if match[0]:
            name = "Янина Кондратович"
        face_names.append(name)
        # Добавляем опознанных в список
        if name not in identified_face_names and name is not None:
            identified_face_names.append(name)

    # Выводим результат
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            # Для неопознанных лиц рисуем круг вокруг лица
            radius = int((bottom - top) / 2 + 20)
            center_coord = (int(left + (right - left) / 2), int(bottom + (top - bottom) / 2))

            cv2.circle(frame, center_coord, radius, LGRAY_COLOR, 3)
        else:
            # Для опознанных лиц рисуем рамку с подписью вокруг лица
            cv2.rectangle(frame, (left, top), (right, bottom), DGRAY_COLOR, 3)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), DGRAY_COLOR, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), FONT, 0.5, WHITE_COLOR, 1)

    # Рисуем подпись с информацией о выходе
    cv2.rectangle(frame, (0, 20), (150, 0), LGRAY_COLOR, cv2.FILLED)
    cv2.putText(frame, 'press "q" to exit', (6, 14), FONT, 0.5, WHITE_COLOR, 1)
    print('3 stage')

    # Выводим кадр
    cv2.imshow('Recognition', frame)

    # Обработка выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Печатаем результат
print('Максимальное количество найденных лиц в кадре: {}'.format(face_amount))
print('Из них опознано: {}'.format(len(identified_face_names)))
print('Список опознанных лиц: {}'.format(identified_face_names))
# Закрываем использование камеры
video_capture.release()
cv2.destroyAllWindows()
