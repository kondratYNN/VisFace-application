from face_proc import FaceProc


def detection():
    process_object = FaceProc()
    process_object.set_capture('BASE')
    process_object.start()
    process_object.close()


def recognition():
    process_object = FaceProc(function='Recognition', count=True)
    process_object.set_capture('BASE')
    process_object.set_face_base()
    process_object.start()
    process_object.close()


if __name__ == '__main__':
    pass


# process_object = FaceProc(count=True)
# process_object.set_capture('BASE')
# process_object.start()

#повториение куска кода при рисовании рамок
