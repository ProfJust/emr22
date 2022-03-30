#!/usr/bin/env python3
# --- ur5_gazebo_qt_slider.py ------
# Qt-Gui with Slider to move UR5 in Gazebo
# Version vom 30.3.2022 by OJ
# ----------------------------

import sys
import rospy

# Qt -------------------------------
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QPushButton, QVBoxLayout,
                             QHBoxLayout, QApplication,
                             QLabel)
from std_msgs.msg import Float64


class UIClass(QWidget):
    def __init__(self):  # Konstrukor
        # Konstruktor der Elternklasse aufrufen
        super(UIClass, self).__init__()
        self.initUI()

        self.wrist1_msg = Float64()
        rospy.init_node('ur5_gazebo_qt_slider', anonymous=True)
        self.pos_wrist1_pub = rospy.Publisher('/wrist_1_joint_position_controller/command',
                                              Float64, queue_size=10)
        self.rate = rospy.Rate(10)

    def initUI(self):
        # Instanziierung der Widgets
        LCDstartWert = 0
        self.lcdX = QLCDNumber(self)
        self.lcdX.display(LCDstartWert)

        self.sldX = QSlider(Qt.Horizontal, self)
        self.sldX.setMaximum(6)
        self.sldX.setMinimum(-6)
        self.sldX.setValue(LCDstartWert)
        self.pbLessX = QPushButton('<')
        self.pbMoreX = QPushButton('>')

        self.pbGo = QPushButton(' Go Home ')
        self.lblInfoX = QLabel('Wrist 1  * 10')
        self.lblStatus = QLabel('Status - Ausgabe')

        # BOX-Layout mit Widgets füllen
        vbox = QVBoxLayout()
        #  0.Reihe - Label
        hbox = QHBoxLayout()
        hbox.addWidget(self.lblInfoX)
        vbox.addLayout(hbox)
        # 1.Reihe
        hbox = QHBoxLayout()
        hbox.addWidget(self.lcdX)
        vbox.addLayout(hbox)
        # 2.Reihe
        hbox = QHBoxLayout()
        hbox.addWidget(self.sldX)
        vbox.addLayout(hbox)

        # 3.Reihe
        hbox = QHBoxLayout()
        hbox.addWidget(self.pbLessX)
        hbox.addWidget(self.pbMoreX)
        vbox.addLayout(hbox)

        # 4.Reihe
        hbox = QHBoxLayout()
        hbox.addWidget(self.pbGo)
        vbox.addLayout(hbox)

        # 5.Reihe
        hbox = QHBoxLayout()
        hbox.addWidget(self.lblStatus)
        vbox.addLayout(hbox)

        # Alle Boxen ins Window setzen
        self.setLayout(vbox)

        # Fenster Konfigurieren
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('EMR22 - UR5 - Gazebo Steering')
        self.show()

        # Signal und Slot verbinden
        self.sldX.valueChanged.connect(self.lcdX.display)
        self.sldX.valueChanged.connect(self.SlotPublish)  # publish to ROS
        self.pbLessX.clicked.connect(self.SlotKlickX)
        self.pbMoreX.clicked.connect(self.SlotKlickX)
        self.pbGo.clicked.connect(self.SlotGo)
        self.pbStop.clicked.connect(self.SlotStop)

    def SlotKlickX(self):
        sender = self.sender()
        self.lblStatus.setText(' X ' + sender.text() + ' was pressed')
        if sender.text() == '<':
            wert = self.sldX.value()
            wert = wert-1
            self.sldX.setValue(wert)
        else:
            wert = self.sldX.value()
            wert = wert+1
            self.sldX.setValue(wert)

    def SlotGo(self):
        self.lblStatus.setText(' Go Home Button klicked ')
        self.wrist1_msg = self.sldX.value()
        self.pos_wrist1_pub.publish(float(self.wrist1_msg)/10.0)

    def SlotPublish(self):
        self.wrist1_msg = self.sldX.value()
        self.pos_wrist1_pub.publish(float(self.wrist1_msg)/10.0)

    def SlotStop(self):
        self.lblStatus.setText(' Stop Button klicked ')
        self.timer.stop()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ui = UIClass()
        sys.exit(app.exec_())

    except rospy.ROSInterruptException:
        pass
