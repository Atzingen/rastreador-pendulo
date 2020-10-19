import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QPushButton, QFileDialog, QStyle, QListWidgetItem
from PyQt5 import uic
import numpy as np
import cv2

''''
TODO

* Arrumar enable disable visual - não parece habilidado realmente apenas com set enable


'''


def hhmmss(ms):
    h, r = divmod(ms, 36000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)
        # Cria os connect's
        self.pushButton_playPause.clicked.connect(self.BtnPlay)
        self.pushButton_playPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.pushButton_stop.clicked.connect(self.BtnStop)
        self.pushButton_stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.pushButton_add_item.clicked.connect(self.add_item_dialog)
        self.pushButton_dell_item.clicked.connect(self.remove_listItem)
        self.listWidget.itemSelectionChanged.connect(self.movieSelected)
        self.horizontalSlider_video.valueChanged[int].connect(self.slider_video)
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        #self.pushButton_processar.clicked.connect(self.processar)
        self.horizontalSlider_blur.valueChanged[int].connect(self.processar)
        self.horizontalSlider_hmin.valueChanged[int].connect(self.processar)
        self.horizontalSlider_hmax.valueChanged[int].connect(self.processar)
        self.horizontalSlider_rmin.valueChanged[int].connect(self.processar)
        self.horizontalSlider_rmax.valueChanged[int].connect(self.processar)
        # flags
        self.can_play = True
        self.enable_play(True)

    def processar(self):
        # self.can_play = not self.can_play
        # print(self.can_play)
        # self.enable_play(self.can_play)
        blur = self.horizontalSlider_blur.value()
        hmin = self.horizontalSlider_hmin.value()
        hmax = self.horizontalSlider_hmax.value()
        rmin = self.horizontalSlider_rmin.value()
        hmax = self.horizontalSlider_rmax.value()
        self.label_blur.setText(str(blur))
        self.label_hmin.setText(str(hmin))
        self.label_hmax.setText(str(hmax))
        self.label_rmin.setText(str(rmin))
        self.label_rmax.setText(str(hmax))

    def enable_play(self, state):
        self.pushButton_playPause.setEnabled(state)
        self.pushButton_stop.setEnabled(state)
        self.horizontalSlider_video.setEnabled(state)
        self.label_play.setEnabled(state)
        self.label_play.setEnabled(state)
        self.comboBox.setEnabled(state)

    def movieSelected(self):
        self.selected_item()

    def BtnPlay(self):
        listItem = self.listWidget.currentItem()
        if listItem:
            if self.player.state() == 1:    
                self.player.pause()
                self.pushButton_playPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            else:
                self.player.play()
                self.pushButton_playPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def BtnStop(self):
        self.player.stop()
        self.pushButton_playPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def update_duration(self, duration):
        print("update_duration ", duration)
        print("update_duration ", self.player.duration())
        self.horizontalSlider_video.setMaximum(duration)
        if duration >= 0:
            self.label_total.setText(hhmmss(duration))

    def update_position(self, position):
        print("update_position ", position)
        if position >= 0:
            self.label_play.setText(hhmmss(position))
            self.horizontalSlider_video.blockSignals(True)
            self.horizontalSlider_video.setValue(position)
            self.horizontalSlider_video.blockSignals(False)

    def slider_video(self, value):
        # print(f'slider = {value}') 
        self.player.setPosition(value)

    def remove_listItem(self):
        listItems = self.listWidget.selectedItems()
        if not listItems: 
            return        
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))

    def add_item_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            item = QListWidgetItem(fileName)
            self.listWidget.addItem(item)
            self.listWidget.setCurrentItem(item)
            self.selected_item()
    
    def selected_item(self):
        listItem = self.listWidget.currentItem()
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(listItem.text())))
        self.player.setVideoOutput(self.widget)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()