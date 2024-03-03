from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from mutagen.flac import FLAC

from settingUI import Ui_setting


class SettingDialog(QMainWindow, Ui_setting):
	save_signal = pyqtSignal(object)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.init_connect()

	def init_connect(self):
		self.save_btn.clicked.connect(self.save)

	def save(self):
		try:
			self.save_signal.emit(True)
		except Exception as e:
			print('save:', e)

	def sava_song_inf(self, song):
		try:
			# print(song.path,song.title,song.artist)
			# title = self.SongTitle
			# artist = self.SongSinger
			title = song.title
			artist = song.artist
			# audio = ID3(song.path)

			audio = FLAC(song.path)
			audio['title'] = title
			audio['artist'] = artist
			if self.SongTitle_edit.text() != '':
				audio['title'] = self.SongTitle_edit.text()
			# audio['APIC'] = APIC(  # 插入专辑图片
			# 	# encoding=3,
			# 	# mime='image/jpeg',
			# 	# type=3,
			# 	# desc=u'Cover',
			# )
			# audio['TIT2'] = TIT2(  # 插入歌名
			# 	encoding=3,
			# 	text=[title]
			# )
			# audio['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
			# 	encoding=3,
			# 	text=[artist]
			# )
			# audio['TALB'] = TALB(  # 插入专辑名称
			# 	# encoding=3,
			# 	# text=[songalbum]
			# )
			audio.save()  # 记得要保存


		except Exception as e:
			print('sava_song_inf:', e)
