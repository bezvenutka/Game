#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLineEdit, QLabel

from server import rps_server


def run_server():
    print('Server run!!!')
    rps_server.start_server()


class ServerWidget(QWidget):
    def __init__(self, screen_resolution, widget_width=200, widget_height=200):
        super().__init__()
        self.resolution = screen_resolution
        self.width = widget_width
        self.height = widget_height

        self._init_ui()

    def _init_ui(self):
        # Init button to start server
        start_button = QPushButton('Run server!!!', self)
        start_button.clicked.connect(run_server)
        start_button.resize(start_button.sizeHint())
        start_button.setGeometry(20, 150, 160, 30)

        # Init sizes
        label_height = 20
        line_input_height = 30
        elements_width = 160
        elements_x = 20
        host_label_y = 20

        # Init LineInputs
        host_label = QLabel(self)
        host_label.setText('Server host')
        host_label.setGeometry(elements_x, host_label_y, elements_width, label_height)
        host_line_input = QLineEdit(self)
        host_input_y = host_label_y + label_height
        host_line_input.setGeometry(elements_x, host_input_y, elements_width, 30)
        host_line_input.setText('127.0.0.1')

        port_label = QLabel(self)
        port_label.setText('Server port')
        port_label_y = host_input_y + line_input_height
        port_label.setGeometry(elements_x, port_label_y, elements_width, 30)
        port_line_input = QLineEdit(self)
        port_input_y = port_label_y + label_height + 5
        port_line_input.setGeometry(elements_x, port_input_y, elements_width, 30)
        port_line_input.setText('1488')

        # Init self geometry
        x_position = (resolution.width() - self.width) / 2
        y_position = (resolution.height() - self.height) / 2
        self.setGeometry(x_position, y_position, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('RockPaperStone Server')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    resolution = app.desktop().screenGeometry()
    client_widget = ServerWidget(resolution)
    sys.exit(app.exec_())
