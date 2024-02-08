# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from ClickableSlider import ClickableSlider


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1164, 666)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(18)
        Form.setFont(font)
        Form.setStyleSheet("")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.OpenFolder_btn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.OpenFolder_btn.setFont(font)
        self.OpenFolder_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.OpenFolder_btn.setObjectName("OpenFolder_btn")
        self.verticalLayout.addWidget(self.OpenFolder_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FilterMusic = QtWidgets.QLineEdit(Form)
        self.FilterMusic.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.FilterMusic.setClearButtonEnabled(True)
        self.FilterMusic.setObjectName("FilterMusic")
        self.horizontalLayout.addWidget(self.FilterMusic)
        self.ClearSearch_btn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.ClearSearch_btn.setFont(font)
        self.ClearSearch_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ClearSearch_btn.setObjectName("ClearSearch_btn")
        self.horizontalLayout.addWidget(self.ClearSearch_btn)
        self.RandomPlay_btn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.RandomPlay_btn.setFont(font)
        self.RandomPlay_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RandomPlay_btn.setObjectName("RandomPlay_btn")
        self.horizontalLayout.addWidget(self.RandomPlay_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(39)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(49)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.MusicTitle = QtWidgets.QLabel(Form)
        self.MusicTitle.setMaximumSize(QtCore.QSize(506, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.MusicTitle.setFont(font)
        self.MusicTitle.setText("")
        self.MusicTitle.setObjectName("MusicTitle")
        self.horizontalLayout_5.addWidget(self.MusicTitle)
        self.Additional_btn = QtWidgets.QPushButton(Form)
        self.Additional_btn.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Additional_btn.setFont(font)
        self.Additional_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Additional_btn.setObjectName("Additional_btn")
        self.horizontalLayout_5.addWidget(self.Additional_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.SongLyrics = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.SongLyrics.setFont(font)
        self.SongLyrics.setFocusPolicy(QtCore.Qt.NoFocus)
        self.SongLyrics.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.SongLyrics.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.SongLyrics.setProperty("showDropIndicator", False)
        self.SongLyrics.setObjectName("SongLyrics")
        self.verticalLayout_2.addWidget(self.SongLyrics)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.current_pos = QtWidgets.QLabel(Form)
        self.current_pos.setMinimumSize(QtCore.QSize(75, 0))
        self.current_pos.setMaximumSize(QtCore.QSize(75, 16777215))
        self.current_pos.setObjectName("current_pos")
        self.horizontalLayout_6.addWidget(self.current_pos)
        self.SongProgressBar = ClickableSlider(Form)
        self.SongProgressBar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.SongProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.SongProgressBar.setObjectName("SongProgressBar")
        self.horizontalLayout_6.addWidget(self.SongProgressBar)
        self.total_length = QtWidgets.QLabel(Form)
        self.total_length.setMinimumSize(QtCore.QSize(75, 0))
        self.total_length.setMaximumSize(QtCore.QSize(75, 16777215))
        self.total_length.setObjectName("total_length")
        self.horizontalLayout_6.addWidget(self.total_length)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 10)
        self.horizontalLayout_6.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LastSong = QtWidgets.QPushButton(Form)
        self.LastSong.setFocusPolicy(QtCore.Qt.NoFocus)
        self.LastSong.setObjectName("LastSong")
        self.horizontalLayout_2.addWidget(self.LastSong)
        self.ControlMusicPlayback_btn = QtWidgets.QPushButton(Form)
        self.ControlMusicPlayback_btn.setObjectName("ControlMusicPlayback_btn")
        self.horizontalLayout_2.addWidget(self.ControlMusicPlayback_btn)
        self.NextSong = QtWidgets.QPushButton(Form)
        self.NextSong.setFocusPolicy(QtCore.Qt.NoFocus)
        self.NextSong.setObjectName("NextSong")
        self.horizontalLayout_2.addWidget(self.NextSong)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.TurnDownVolume_btn = QtWidgets.QPushButton(Form)
        self.TurnDownVolume_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.TurnDownVolume_btn.setObjectName("TurnDownVolume_btn")
        self.horizontalLayout_3.addWidget(self.TurnDownVolume_btn)
        self.VolumeSlider = ClickableSlider(Form)
        self.VolumeSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.VolumeSlider.setMaximum(100)
        self.VolumeSlider.setProperty("value", 100)
        self.VolumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.VolumeSlider.setObjectName("VolumeSlider")
        self.horizontalLayout_3.addWidget(self.VolumeSlider)
        self.TurnUpTheVolume_btn = QtWidgets.QPushButton(Form)
        self.TurnUpTheVolume_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.TurnUpTheVolume_btn.setObjectName("TurnUpTheVolume_btn")
        self.horizontalLayout_3.addWidget(self.TurnUpTheVolume_btn)
        self.MusicMode_btn = QtWidgets.QPushButton(Form)
        self.MusicMode_btn.setObjectName("MusicMode_btn")
        self.horizontalLayout_3.addWidget(self.MusicMode_btn)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.OpenFolder_btn.setText(_translate("Form", "打开"))
        self.ClearSearch_btn.setText(_translate("Form", "清除"))
        self.RandomPlay_btn.setText(_translate("Form", "随机"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "名字"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "修改时间"))
        self.Additional_btn.setText(_translate("Form", "..."))
        self.current_pos.setText(_translate("Form", "00:00"))
        self.total_length.setText(_translate("Form", "00:00"))
        self.LastSong.setText(_translate("Form", "上一首"))
        self.ControlMusicPlayback_btn.setText(_translate("Form", "播放"))
        self.ControlMusicPlayback_btn.setShortcut(_translate("Form", "Space"))
        self.NextSong.setText(_translate("Form", "下一首"))
        self.TurnDownVolume_btn.setText(_translate("Form", "-"))
        self.TurnUpTheVolume_btn.setText(_translate("Form", "+"))
        self.MusicMode_btn.setText(_translate("Form", "随机"))
