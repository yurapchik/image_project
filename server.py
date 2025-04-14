import socket
import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFrame, QLabel, QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QPainter, QColor, QPixmap


class Server(QWidget):
    def __init__(self,ip,port):
        super().__init__()
        self.ip = ip
        self.port = port

        self.initUI()
    def initUI(self):
        self.setWindowTitle("Сервер")
        self.setFixedSize(500,800)
        self.image_lbl = QLabel("Ожидаю картинку")
        self.image_lbl.setScaledContents(True)
        self.file_btn = QPushButton("Выбрать и отправить файл", self)
        self.start_btn = QPushButton("получить файл", self)
        self.file_btn.clicked.connect(self.send_file)
        self.start_btn.clicked.connect(self.start_server)
        layout = QVBoxLayout()
        layout.addWidget(self.image_lbl)
        layout.addWidget(self.file_btn)
        layout.addWidget(self.start_btn)
        self.setLayout(layout)
    def start_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.bind((self.ip,self.port))
                server.listen(1)
                con, addr = server.accept()
                with con:
                    with open("image_client.jpg","wb") as file:
                        while True:
                            data = con.recv(1000024)
                            if data:
                                file.write(data)
                                break
                self.display_image("image_client.jpg")
        except Exception as e:
            print(e)
    def display_image(self,image_name):
        pixmap = QPixmap(image_name)
        self.image_lbl.setPixmap(pixmap)
    def send_file(self):
        try:
            ip, ok = QInputDialog.getText(self,"Введите IP","Введите IP")
            port, ok = QInputDialog.getText(self,"Введите порт","Введите порт")

            file_name, _ = QFileDialog.getOpenFileName(self,"Выберете файл")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.connect((ip,int(port)))
                with open(file_name, "rb") as file:
                    data = file.read()
                    server.sendall(data)
        except Exception as e:
            print(e)




if __name__ == "__main__":
    app = QApplication([])
    server = Server("localhost",10000)
    server.show()
    sys.exit(app.exec())



