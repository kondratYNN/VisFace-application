import os
import shutil
import sqlite3
import sys
from xlsxwriter.workbook import Workbook

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QLabel, QMessageBox, QDesktopWidget, QFrame, \
    QLineEdit, QFileDialog, QTableWidgetItem, QTableWidget, QHeaderView

from core import detection, recognition


class RecognitionWindow(QWidget):
    __BUTTON_STYLESHEET = """
                            QPushButton:hover { background-color: #FFBB74}
                            QPushButton:!hover { background-color: #6EC9E7}
                            QPushButton:pressed { background-color: #FFA241}
                            """
    __identified_face_names = []

    def __init__(self):
        super().__init__()
        self.initUI()
        self.parent_window = None

    def initUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#099ECF"))
        self.setPalette(palette)
        self.setFixedSize(1200, 1000)
        self.center()
        self.setWindowTitle('Face Recognition')
        self.setWindowIcon(QIcon('view_elements/icon.png'))

        title_lbl = QLabel(self)
        title_lbl.setText('VisFace Recognition')
        title_lbl.setFont(QFont('Kaufmann BT', 40))
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.move(350, 70)

        main_menu_btn = QPushButton('Go back', self)
        main_menu_btn.setFont(QFont('SansSerif', 10))
        main_menu_btn.setGeometry(0, 0, 100, 50)
        main_menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        main_menu_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        main_menu_btn.clicked.connect(self.close)

        main_menu_btn = QPushButton('Info', self)
        main_menu_btn.setFont(QFont('SansSerif', 10))
        main_menu_btn.setGeometry(100, 0, 100, 50)
        main_menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        main_menu_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        main_menu_btn.clicked.connect(self.show_info)

        start_btn = QPushButton('Start camera', self)
        start_btn.setFont(QFont('SansSerif', 12))
        start_btn.setToolTip('Launch camera frame <b>recognition</b>')
        start_btn.setGeometry(200, 200, 800, 50)
        start_btn.setCursor(QCursor(Qt.PointingHandCursor))
        start_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        start_btn.clicked.connect(self.recognition_wrap)

        self.amount_lbl = QLabel(self)
        self.amount_lbl.setGeometry(QRect(200, 270, 800, 40))
        self.amount_lbl.setText('Maximum number of faces found in the frame: ')
        self.amount_lbl.setFont(QFont('SansSerif', 12))

        self.rec_amount_lbl = QLabel(self)
        self.rec_amount_lbl.setGeometry(QRect(200, 310, 800, 40))
        self.rec_amount_lbl.setText('Number of identified: ')
        self.rec_amount_lbl.setFont(QFont('SansSerif', 12))

        name_lbl = QLabel(self)
        name_lbl.setGeometry(QRect(200, 350, 800, 40))
        name_lbl.setText('List of identified individuals:')
        name_lbl.setFont(QFont('SansSerif', 12))

        self.qttable = QTableWidget(self)
        self.qttable.setGeometry(200, 390, 800, 350)
        self.qttable.setFont(QFont('SansSerif', 10))

        txt_save_btn = QPushButton('Save results(.txt)', self)
        txt_save_btn.setFont(QFont('SansSerif', 12))
        txt_save_btn.setToolTip('Save results  to <b>txt file</b>')
        txt_save_btn.setGeometry(200, 750, 395, 70)
        txt_save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        txt_save_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        txt_save_btn.clicked.connect(self.save_results_txt)

        xlsx_save_btn = QPushButton('Save results(.xlsx)', self)
        xlsx_save_btn.setFont(QFont('SansSerif', 12))
        xlsx_save_btn.setToolTip('Save results  to <b>xlsx file</b>')
        xlsx_save_btn.setGeometry(605, 750, 395, 70)
        xlsx_save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        xlsx_save_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        xlsx_save_btn.clicked.connect(self.save_results_xlsx)

    def recognition_wrap(self):
        face_amount, self.__identified_face_names = recognition()
        amount = self.amount_lbl.text() + str(face_amount)
        self.amount_lbl.setText(amount)
        identified_amount = self.rec_amount_lbl.text() + str(len(self.__identified_face_names))
        self.rec_amount_lbl.setText(identified_amount)
        self.fillQTable(self.__identified_face_names)

    def save_results_txt(self):
        fname, ok = QFileDialog.getSaveFileName(self, 'Save', '/home/results.txt', 'All Files(*.txt)')
        if not fname:
            return
        my_file = open(fname, "w+")
        result = self.amount_lbl.text() + '\n' + self.rec_amount_lbl.text() + '\n' + \
                 'List of identified individuals: ' + '; '.join(self.__identified_face_names)
        my_file.write(result)
        my_file.close()
        QMessageBox.information(self, 'Success', f"File saved successfully: \n{fname}", QMessageBox.Ok, QMessageBox.Ok)

    def save_results_xlsx(self):
        fname, ok = QFileDialog.getSaveFileName(self, "Save", "/home/results.xlsx", "All Files(*.xlsx)")
        if not fname:
            return
        _list = []
        model = self.qttable.model()
        for row in range(model.rowCount()):
            _r = []
            for column in range(model.columnCount()):
                _r.append("{}".format(model.index(row, column).data() or ""))
            _list.append(_r)

        workbook = Workbook(fname)
        worksheet = workbook.add_worksheet()

        for r, row in enumerate(_list):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        workbook.close()
        QMessageBox.information(self, 'Success', f"File saved successfully: \n{fname}", QMessageBox.Ok, QMessageBox.Ok)

    def fillQTable(self, identified_face_names):
        data = self.getData(identified_face_names)
        rowCount = len(data)
        colCount = 3
        self.qttable.setRowCount(rowCount)
        self.qttable.setColumnCount(colCount)
        self.qttable.verticalHeader().setVisible(False)
        self.qttable.setHorizontalHeaderLabels(('Full Name', 'Status', 'Img path'))
        self.qttable.horizontalHeader().setVisible(True)
        for s in range(colCount):
            self.qttable.horizontalHeaderItem(s).setTextAlignment(Qt.AlignLeft)
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                if j == 2:
                    pic = QPixmap(col)
                    label = QLabel(self)
                    pixmap_resize = pic.scaled(60, 60, Qt.KeepAspectRatio)
                    label.setPixmap(pixmap_resize)
                    self.qttable.setCellWidget(i, j, label)
                else:
                    item = QTableWidgetItem(col)
                    self.qttable.setItem(i, j, item)
        header = self.qttable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def getData(self, value_names_list):
        conn = sqlite3.connect('personality.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS person(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        image_path TEXT NOT NULL);
                    ''')
        conn.commit()
        cur.execute("select name, status, image_path from person WHERE name=?", tuple(value_names_list))
        raw_data = cur.fetchall()
        conn.commit()
        conn.close()
        return raw_data

    def center(self):
        pos = QDesktopWidget().rect().center() - self.rect().center()
        self.move(pos)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
                                     "Are you sure to go to the main menu?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.parent_window = MainMenu()
            self.parent_window.show()
        else:
            event.ignore()

    def show_info(self):
        msg = "Please, push the 'Start camera' button, after this will appear camera frame, to quit it" \
              " you have to press the 'q' key. After this you will see results of recognition.\nAlso you can " \
              "save this results in txt or xlsx file."
        QMessageBox.information(self, 'Info', msg, QMessageBox.Ok, QMessageBox.Ok)


class DatabaseWindow(QWidget):
    __BUTTON_STYLESHEET = """
                        QPushButton:hover { background-color: #FFBB74}
                        QPushButton:!hover { background-color: #6EC9E7}
                        QPushButton:pressed { background-color: #FFA241}
                        """

    def __init__(self):
        super().__init__()
        self.initUI()
        self.parent_window = None

    def fillQTable(self):
        data = self.getData()
        rowCount = len(data)
        colCount = 3
        self.qttable.setRowCount(rowCount)
        self.qttable.setColumnCount(colCount)
        self.qttable.verticalHeader().setVisible(False)
        self.qttable.setHorizontalHeaderLabels(('Full Name', 'Status', 'Img path'))
        self.qttable.horizontalHeader().setVisible(True)
        for s in range(colCount):
            self.qttable.horizontalHeaderItem(s).setTextAlignment(Qt.AlignLeft)
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                if j == 2:
                    pic = QPixmap(col)
                    label = QLabel(self)
                    pixmap_resize = pic.scaled(60, 60, Qt.KeepAspectRatio)
                    label.setPixmap(pixmap_resize)
                    self.qttable.setCellWidget(i, j, label)
                else:
                    item = QTableWidgetItem(col)
                    self.qttable.setItem(i, j, item)
        header = self.qttable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def getData(self):
        conn = sqlite3.connect('personality.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS person(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        image_path TEXT NOT NULL);
                    ''')
        conn.commit()
        cur.execute("select name, status, image_path from person")
        raw_data = cur.fetchall()
        conn.commit()
        conn.close()
        return raw_data

    def initUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#099ECF"))
        self.setPalette(palette)
        self.setFixedSize(1200, 1000)
        self.center()
        self.setWindowTitle('Face Database')
        self.setWindowIcon(QIcon('view_elements/icon.png'))

        title_lbl = QLabel(self)
        title_lbl.setText('VisFace Database')
        title_lbl.setFont(QFont('Kaufmann BT', 40))
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.move(370, 30)

        name_lbl = QLabel(self)
        name_lbl.setGeometry(QRect(180, 150, 120, 40))
        name_lbl.setText('Full name:')
        name_lbl.setFont(QFont('SansSerif', 12))

        self.name_edl = QLineEdit(self)
        self.name_edl.setGeometry(QRect(310, 150, 250, 40))
        self.name_edl.setFont(QFont('SansSerif', 12))

        status_lbl = QLabel(self)
        status_lbl.setGeometry(QRect(580, 150, 150, 40))
        status_lbl.setText('Person status:')
        status_lbl.setFont(QFont('SansSerif', 12))

        self.status_edl = QLineEdit(self)
        self.status_edl.setGeometry(QRect(750, 150, 250, 40))
        self.status_edl.setFont(QFont('SansSerif', 12))

        path_lbl = QLabel(self)
        path_lbl.setGeometry(QRect(180, 220, 150, 40))
        path_lbl.setText('File path:')
        path_lbl.setFont(QFont('SansSerif', 12))

        self.path_edl = QLineEdit(self)
        self.path_edl.setGeometry(QRect(310, 220, 490, 40))
        self.path_edl.setFont(QFont('SansSerif', 8))

        chpath_btn = QPushButton('Choose path', self)
        chpath_btn.setFont(QFont('SansSerif', 12))
        chpath_btn.setToolTip('Open window to select a file')
        chpath_btn.setGeometry(850, 220, 150, 40)
        chpath_btn.setCursor(QCursor(Qt.PointingHandCursor))
        chpath_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        chpath_btn.clicked.connect(self.choose_pic_dialog)

        preview_lbl = QLabel(self)
        preview_lbl.setGeometry(QRect(700, 300, 100, 40))
        preview_lbl.setText('Preview:')
        preview_lbl.setFont(QFont('SansSerif', 12))

        self.for_pic_lbl = QLabel(self)
        self.for_pic_lbl.setGeometry(QRect(800, 300, 200, 200))
        self.for_pic_lbl.setText('File')
        self.for_pic_lbl.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#E9F9FF'))
        self.for_pic_lbl.setPalette(palette)
        self.for_pic_lbl.setAlignment(Qt.AlignCenter)
        self.for_pic_lbl.setFont(QFont('SansSerif', 12))

        add_person_btn = QPushButton('Add to database', self)
        add_person_btn.setFont(QFont('SansSerif', 12))
        add_person_btn.setGeometry(180, 300, 500, 100)
        add_person_btn.setCursor(QCursor(Qt.PointingHandCursor))
        add_person_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        add_person_btn.clicked.connect(self.add_person_to_db)

        self.qttable = QTableWidget(self)
        self.qttable.setGeometry(180, 510, 830, 390)
        self.qttable.setFont(QFont('SansSerif', 10))
        self.fillQTable()

        main_menu_btn = QPushButton('Go back', self)
        main_menu_btn.setFont(QFont('SansSerif', 10))
        main_menu_btn.setGeometry(0, 0, 100, 50)
        main_menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        main_menu_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        main_menu_btn.clicked.connect(self.close)

        main_menu_btn = QPushButton('Info', self)
        main_menu_btn.setFont(QFont('SansSerif', 10))
        main_menu_btn.setGeometry(100, 0, 100, 50)
        main_menu_btn.setCursor(QCursor(Qt.PointingHandCursor))
        main_menu_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        main_menu_btn.clicked.connect(self.show_info)

        del_name_lbl = QLabel(self)
        del_name_lbl.setGeometry(QRect(180, 410, 150, 40))
        del_name_lbl.setText('Name to delete:')
        del_name_lbl.setFont(QFont('SansSerif', 10))

        self.del_name_edl = QLineEdit(self)
        self.del_name_edl.setGeometry(QRect(340, 410, 340, 40))
        self.del_name_edl.setFont(QFont('SansSerif', 10))

        delete_person_btn = QPushButton('Delete from base', self)
        delete_person_btn.setFont(QFont('SansSerif', 12))
        delete_person_btn.setToolTip('Delete person with this full name from database')
        delete_person_btn.setGeometry(180, 460, 500, 40)
        delete_person_btn.setCursor(QCursor(Qt.PointingHandCursor))
        delete_person_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        delete_person_btn.clicked.connect(self.delete_person_from_db)

    def delete_person_from_db(self):
        name = self.del_name_edl.text()
        conn = sqlite3.connect('personality.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS person(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        image_path TEXT NOT NULL);
                    ''')
        conn.commit()
        cur.execute("SELECT image_path from person WHERE name=?;", (name,))
        file_path_to_delete = cur.fetchone()
        cur.execute('DELETE from person WHERE name=?;', (name,))
        conn.commit()
        conn.close()
        os.remove(file_path_to_delete[0])
        self.del_name_edl.setText('')
        self.fillQTable()

    def add_person_to_db(self):
        name = self.name_edl.text()
        status = self.status_edl.text()
        path = self.path_edl.text()
        new_path = 'face_img/' + name + '.jpg'
        shutil.copy(path, new_path)
        conn = sqlite3.connect('personality.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS person(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        image_path TEXT NOT NULL);
                    ''')
        conn.commit()
        user = (name, status, new_path)
        cur.execute("INSERT INTO person(name, status, image_path) VALUES(?, ?, ?);", user)
        conn.commit()
        conn.close()
        self.name_edl.setText('')
        self.path_edl.setText('')
        self.status_edl.setText('')
        self.for_pic_lbl.setText('Person added')
        self.fillQTable()

    def choose_pic_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose picture', './')
        self.path_edl.setText(fname[0])
        pixmap = QPixmap(fname[0])
        pixmap_resize = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.for_pic_lbl.setPixmap(pixmap_resize)

    def center(self):
        pos = QDesktopWidget().rect().center() - self.rect().center()
        self.move(pos)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
                                     "Are you sure to go to the main menu?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.parent_window = MainMenu()
            self.parent_window.show()
        else:
            event.ignore()

    def show_info(self):
        msg = "1. If you want to add person in database, please, fill next fields: Full name, Person status and File " \
              "path. After this push the button 'Add to database.'" \
              "<br>2. If you want to delete person from database, please, fill 'Name to delete'(It must be full " \
              "name) field and push the button 'Delete from base'. Current data in database given in the table."
        QMessageBox.information(self, 'Info', msg, QMessageBox.Ok, QMessageBox.Ok)


class MainMenu(QWidget):
    __BUTTON_STYLESHEET = """
                            QPushButton:hover { background-color: #FFBB74}
                            QPushButton:!hover { background-color: #6EC9E7}
                            QPushButton:pressed { background-color: #FFA241}
                            """


    def __init__(self):
        super().__init__()
        self.initUI()
        self.child_window = None
        self.__exit_flag = 1

    def show_info(self):
        link = 'https://www.linkedin.com/in/kondratynn/'
        msg = "Hi there! This program can detect and recognize faces. Have a nice day, user!" \
              "<br><br>Program written by Yanina Kondratovich in 2021.<br>Her <a href='%s'>LinkedIn</a>." % link
        QMessageBox.information(self, 'Info', msg, QMessageBox.Ok, QMessageBox.Ok)

    def create_db_win(self):
        self.__exit_flag = 0
        self.close()
        self.child_window = DatabaseWindow()
        self.child_window.show()

    def create_recognition_win(self):
        self.__exit_flag = 0
        self.close()
        # QCoreApplication.instance().quit()
        self.child_window = RecognitionWindow()
        self.child_window.show()

    def closeEvent(self, event):
        if self.__exit_flag == 1:
            reply = QMessageBox.question(self, 'Exit',
                                        "Are you sure to quit?", QMessageBox.Yes |
                                        QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept

    def initUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#099ECF"))
        self.setPalette(palette)
        self.setFixedSize(1200, 1000)
        self.center()
        self.setWindowTitle('Main menu')
        self.setWindowIcon(QIcon('view_elements/icon.png'))
        QToolTip.setFont(QFont('SansSerif', 8))

        title_lbl = QLabel(self)
        title_lbl.setText('VisFace')
        title_lbl.setFont(QFont('Kaufmann BT', 60))
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.move(445, 65)

        frame = QFrame(self)
        frame.setGeometry(QRect(385, 200, 425, 710))
        frame.setAutoFillBackground(False)
        frame.setFrameShape(QFrame.Box)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setLineWidth(2)

        face_detect_btn = QPushButton('Face detection', self)
        face_detect_btn.setFont(QFont('SansSerif', 18))
        face_detect_btn.setToolTip('Open window to <b>detect</b> persons in camera capture')
        face_detect_btn.resize(400, 100)
        face_detect_btn.move(400, 220)
        face_detect_btn.setCursor(QCursor(Qt.PointingHandCursor))
        face_detect_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        face_detect_btn.clicked.connect(detection)

        face_bd_btn = QPushButton('Face database', self)
        face_bd_btn.setFont(QFont('SansSerif', 18))
        face_bd_btn.setToolTip('Open face database window')
        face_bd_btn.resize(400, 100)
        face_bd_btn.move(400, 350)
        face_bd_btn.setCursor(QCursor(Qt.PointingHandCursor))
        face_bd_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        face_bd_btn.clicked.connect(self.create_db_win)

        face_rec_btn = QPushButton('Face recognition', self)
        face_rec_btn.setFont(QFont('SansSerif', 18))
        face_rec_btn.setToolTip('Open window to <b>recognize</b> persons in camera capture')
        face_rec_btn.resize(400, 100)
        face_rec_btn.move(400, 480)
        face_rec_btn.setCursor(QCursor(Qt.PointingHandCursor))
        face_rec_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        face_rec_btn.clicked.connect(self.create_recognition_win)

        info_btn = QPushButton('About program', self)
        info_btn.setFont(QFont('SansSerif', 18))
        info_btn.setToolTip('<b>Information sheet</b>')
        info_btn.resize(400, 100)
        info_btn.move(400, 610)
        info_btn.setCursor(QCursor(Qt.PointingHandCursor))
        info_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        info_btn.clicked.connect(self.show_info)

        esc_btn = QPushButton('Exit', self)
        esc_btn.setFont(QFont('SansSerif', 18))
        esc_btn.resize(400, 100)
        esc_btn.move(400, 790)
        esc_btn.setCursor(QCursor(Qt.PointingHandCursor))
        esc_btn.setStyleSheet(self.__BUTTON_STYLESHEET)
        esc_btn.clicked.connect(self.close)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        pos = QDesktopWidget().rect().center() - self.rect().center()
        self.move(pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec_())

# Вопрос с выходом как обыграть
