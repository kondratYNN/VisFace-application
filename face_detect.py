# Импорт библиотек и константы
import cv2
import face_recognition
LGRAY_COLOR = (80, 80, 80)
WHITE_COLOR = (255, 255, 255)
FONT = cv2.FONT_ITALIC


# Получаем доступ к камере ноутбука
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

face_locations = []
amount = 0

while True:
    # Берем один кадр из видео
    ret, frame = video_capture.read()

    # Переводим изображение из BGR кодировки(OpenCV использует её) в RGB для face_recognition
    rgb_frame = frame[:, :, ::-1]

    # Находим все лица в кадре
    face_locations = face_recognition.face_locations(rgb_frame)

    # Получаем общее количество лиц в кадре
    if len(face_locations) > amount:
        amount = len(face_locations)

    # Выводим обработанный кадр
    for top, right, bottom, left in face_locations:
        # Рисуем круг вокруг лица
        radius = int((bottom - top) / 2 + 20)
        center_coord = (int(left + (right - left) / 2), int(bottom + (top - bottom) / 2))

        cv2.circle(frame, center_coord, radius, LGRAY_COLOR, 3)

    # Рисуем подпись с информацией о выходе
    cv2.rectangle(frame, (0, 20), (150, 0), LGRAY_COLOR, cv2.FILLED)
    cv2.putText(frame, 'press "q" to exit', (6, 14), FONT, 0.5, WHITE_COLOR, 1)

    # Выводим кадр
    cv2.imshow('Detector', frame)

    # Обработка выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('Максимальное количество найденных лиц в кадре: {}'.format(amount))
# Закрываем использование камеры
video_capture.release()
cv2.destroyAllWindows()
