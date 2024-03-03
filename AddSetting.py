import os

from PyQt5.QtCore import pyqtSignal  # 从PyQt5模块中导入pyqtSignal类，用于创建自定义信号
from PyQt5.QtWidgets import QMainWindow  # 从PyQt5模块中导入QMainWindow类，用于创建应用主窗口
from mutagen.flac import FLAC  # 从mutagen.flac模块中导入FLAC类，用于处理FLAC音频文件的元数据
from mutagen.mp3 import MP3  # 从mutagen.mp3模块中导入MP3类，用于处理MP3音频文件的元数据

from settingUI import Ui_setting  # 从settingUI模块中导入Ui_setting类，用于设置UI界面


class SettingDialog(QMainWindow, Ui_setting):
	save_signal = pyqtSignal(object)  # 创建一个自定义信号，用于在保存设置时发出信号

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)  # 设置UI界面
		self.init_connect()  # 初始化信号槽连接

	def init_connect(self):
		self.save_btn.clicked.connect(self.save)  # 将按钮点击事件连接到保存函数

	def save(self):
		try:
			self.save_signal.emit(True)  # 发射保存信号
		except Exception as e:
			print('save:', e)  # 打印保存过程中出现的异常信息

	def save_song_inf(self, song):
		try:
			title = song.title  # 获取歌曲标题
			artist = song.artist  # 获取歌曲艺术家
			file_path = song.path  # 获取歌曲文件路径
			file_extension = os.path.splitext(file_path)[1].lower()  # 获取文件扩展名并转换为小写

			# 根据文件扩展名选择不同的音频文件处理方式
			if file_extension == '.flac':
				audio = FLAC(file_path)  # 使用mutagen处理FLAC音频文件
			elif file_extension == '.mp3':
				audio = MP3(file_path)  # 使用mutagen处理MP3音频文件
			else:
				print("Unsupported file format")  # 不支持的文件格式
				return

			# 更新元数据
			audio['title'] = [title] if self.SongTitle_edit.text() == '' else [self.SongTitle_edit.text()]
			audio['artist'] = [artist]

			# 保存更改
			audio.save()

		except Exception as e:
			print('save_song_inf:', e)  # 打印保存元数据过程中出现的异常信息
