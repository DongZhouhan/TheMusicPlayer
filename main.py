# 导入必要的库
import json
import math
import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, QPropertyAnimation, QSize, QTimer, Qt, QEvent
from PyQt5.QtGui import QColor, QFont, QIcon, QTextCursor
from PyQt5.QtWidgets import QApplication, QFileDialog, QHeaderView, QMenu, QMessageBox, QSystemTrayIcon, \
	QTableWidgetItem, QWidget

from ClickableSlider import ClickableSlider
from LyricsManager import LyricsManager
from MusicList import MusicList
from MusicPlayer import MusicPlayer
from untitled import Ui_form


# 定义主页面类
class MainPage(QWidget, Ui_form):
	# 初始化函数
	def __init__(self):
		super().__init__()
		self.pre_path = ''
		self.start_position = 0
		self.setupUi(self)
		self.MusicList = MusicList()
		self.music_player = MusicPlayer()
		self.PlayMode = 0
		self.index = -1
		self.folder_path = ''
		self.lyrics_data = []  # 存储歌词数据
		self.user_is_interacting_with_lyrics = False  # 用户是否正在滑动歌词
		# 初始化定时器
		self.lyrics_scroll_timer = QTimer(self)
		self.lyrics_scroll_timer.setSingleShot(True)  # 设置定时器只触发一次
		self.lyrics_scroll_timer.timeout.connect(self.reset_lyrics_auto_scroll)

		# 添加用户交互标志
		self.user_is_interacting = False
		self.PreviousSong = []
		self.lyrics_manager = LyricsManager()
		self.filtered_song_indices = []
		self.initUI()
		self.init_connect()
		self.init_data()
		self.initTrayIcon()

	# 初始化UI设置
	def initUI(self):
		self.tableWidget.setColumnWidth(0, 250)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		self.SongLyrics.verticalScrollBar().valueChanged.connect(self.on_lyrics_scroll)
		self.tableWidget.installEventFilter(self)
		self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)  # 支持扩展选择（包括多选）

	# 连接UI元素和相应的函数
	def init_connect(self):
		self.OpenFolder_btn.clicked.connect(self.loadSongs)
		self.MusicList.updated.connect(self.on_music_list_updated)
		self.RandomPlay_btn.clicked.connect(self.random_play)
		self.music_player.progressUpdated.connect(self.update_progress)
		self.music_player.finished.connect(self.next_song)
		self.ControlMusicPlayback_btn.clicked.connect(self.ControlMusicPlayback)
		self.tableWidget.itemDoubleClicked.connect(self.on_double_click)
		self.TurnDownVolume_btn.clicked.connect(self.TurnDownVolume)
		self.TurnUpTheVolume_btn.clicked.connect(self.TurnUpTheVolume)
		self.VolumeSlider.valueChanged.connect(self.setVolume)
		self.NextSong.clicked.connect(self.next_song)
		self.FilterMusic.textChanged.connect(self.search_song)
		self.SongProgressBar.sliderPressed.connect(self.on_slider_pressed)
		self.SongProgressBar.sliderReleased.connect(self.on_slider_released)
		self.SongProgressBar.valueChanged.connect(self.on_slider_moved)
		self.LastSong.clicked.connect(self.previous_song)
		self.MusicMode_btn.clicked.connect(self.change_MusicMode)
		self.SongLyrics.itemDoubleClicked.connect(self.on_lyric_double_clicked)
		self.DeleteSong_btn.clicked.connect(self.delete_selected_songs)

	# 初始化数据，如配置文件读取
	def init_data(self):
		try:
			data = self.read_data()

			self.PlayMode = data.get('PlayMode', -1)
			self.index = data.get('index', -1)
			self.start_position = data.get('current_pos', 0)
			self.pre_path = data.get('pre_path', '')

			self.MusicList.on_songs_loaded()

			if self.PlayMode == 0:
				self.MusicMode_btn.setText('随机')
			elif self.PlayMode == 1:
				self.MusicMode_btn.setText('单曲')
			else:
				self.MusicMode_btn.setText('列表')
		except Exception as e:
			print('init_data', e)

	# 初始化系统托盘图标
	def initTrayIcon(self):
		self.trayIcon = QSystemTrayIcon(self)
		self.trayIcon.setIcon(QIcon("src/img.png"))
		self.trayMenu = QMenu()
		restoreAction = self.trayMenu.addAction("还原")
		quitAction = self.trayMenu.addAction("退出")
		restoreAction.triggered.connect(self.showNormal)
		quitAction.triggered.connect(self.close)
		self.trayIcon.activated.connect(self.trayIconActivated)
		self.trayIcon.setContextMenu(self.trayMenu)
		self.trayIcon.show()

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.ContextMenu and source is self.tableWidget:
			contextMenu = QMenu(self)
			delete_current = contextMenu.addAction("删除")
			action = contextMenu.exec_(event.globalPos())
			if action == delete_current:
				self.delete_song()
			return True
		return super().eventFilter(source, event)

	# 从配置文件读取数据
	def read_data(self):
		try:
			with open('config.json', 'r') as file:
				return json.load(file)
		except IOError:
			print("read_data: 配置文件不存在")
			return {}

	# 将数据写入配置文件
	def write_data(self, data):
		try:
			with open('config.json', 'w') as file:
				json.dump(data, file, indent=4)
		except IOError:
			print("write_data: 写入配置数据异常")

	# 加载歌曲功能
	def loadSongs(self):
		# 创建一个消息框实例
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Question)
		msgBox.setText("加载音乐")
		msgBox.setInformativeText("请选择加载方式：")
		msgBox.setWindowTitle("加载音乐")

		# 添加按钮，设置角色并接收返回值
		folderButton = msgBox.addButton("文件夹", QMessageBox.ActionRole)
		fileButton = msgBox.addButton("文件", QMessageBox.ActionRole)
		cancelButton = msgBox.addButton("取消", QMessageBox.RejectRole)

		# 显示消息框
		msgBox.exec_()

		# 根据用户的选择执行操作
		if msgBox.clickedButton() == folderButton:
			# 用户选择加载文件夹
			folder_path = QFileDialog.getExistingDirectory(self, "选择音乐文件夹")
			if folder_path:
				self.MusicList.load_songs_from_folder(folder_path, is_folder=True)
		elif msgBox.clickedButton() == fileButton:
			# 用户选择加载单个或多个文件
			file_paths, _ = QFileDialog.getOpenFileNames(self, "选择音乐文件", "", "音乐文件 (*.mp3 *.wav *.flac)")
			if file_paths:
				self.MusicList.load_songs_from_folder(file_paths, is_folder=False)
		# 如果点击了取消按钮，不需要执行任何操作，因为操作已经被取消了
		# 无论加载文件夹还是单个文件，都执行搜索以更新UI显示
		self.search_song(self.FilterMusic.text())

	# 当音乐列表更新时的处理逻辑
	def on_music_list_updated(self, obj):
		try:
			# self.load_songs_to_table()
			self.search_song(self.FilterMusic.text())
			print(obj,self.index)
			if obj == 100 and self.index != -1:
				# print(self.MusicList.songs[self.index])
				print(1)
				print(self.pre_path, self.MusicList.songs[self.index].path)
				if self.index>=len(self.MusicList.songs) or self.pre_path != self.MusicList.songs[self.index].path:
					self.index = -1
					self.start_position=0

				else:
					self.play_song(self.MusicList.songs[self.index], self.start_position)
					self.music_player.pause_song()
			elif obj == 100 and self.index == -1 and self.MusicList.songs:
				if self.PlayMode == 0:
					self.random_play()
				elif self.PlayMode == 1:
					self.single_loop()
				else:
					self.list_loop()
		except Exception as e:
			print('on_music_list_updated', e)

	def delete_selected_songs(self):
		# 获取所有选中的行，返回的是 QModelIndex 列表
		selectedRows = set()  # 使用集合避免重复的行号
		for index in self.tableWidget.selectionModel().selectedIndexes():
			selectedRows.add(index.row())
		# 对行号进行排序并逆序，确保从最后一个开始删除
		for row in sorted(selectedRows, reverse=True):
			self.delete_song(row)

	def delete_song(self,currentRow=-1):
		if currentRow == -1:
			currentRow = self.tableWidget.currentRow()
		if currentRow >= 0:
			songPath = self.MusicList.songs[currentRow].path  # 假设每个歌曲对象都有一个路径属性
			# reply = QMessageBox.question(self, '确认删除', '你确定要删除这首歌吗？',
			#                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

			# if reply == QMessageBox.Yes:
			if True:
				# 检查是否删除的是当前播放的歌曲
				if self.index == currentRow:
					self.music_player.stop_song()  # 停止当前歌曲的播放
					self.MusicList.delete_song_by_path(songPath)  # 删除歌曲
					self.tableWidget.removeRow(currentRow)
					self.MusicList.songs.pop(currentRow)  # 也从内存中的歌曲列表中删除

					# 如果有其他歌曲，播放下一首；否则重置播放器状态
					if len(self.MusicList.songs) > 0:
						nextRow = currentRow if currentRow < len(self.MusicList.songs) else 0
						self.play_song(self.MusicList.songs[nextRow])
					else:
						# 重置播放器UI等
						# self.reset_player_ui()
						pass
				else:
					# 如果删除的不是当前播放的歌曲，直接删除即可
					self.MusicList.delete_song_by_path(songPath)  # 删除歌曲
					self.tableWidget.removeRow(currentRow)
					self.MusicList.songs.pop(currentRow)  # 也从内存中的歌曲列表中删除

	# 随机播放音乐
	def random_play(self):
		# print(1)
		if self.MusicList.songs:
			random_song = random.choice(self.MusicList.songs)
			# print(self.MusicList.songs.index(random_song))
			self.play_song(random_song)

	# 单曲循环逻辑
	def single_loop(self):
		if self.MusicList.songs:
			self.play_song(self.MusicList.songs[self.index])

	# 列表循环逻辑
	def list_loop(self):
		if self.MusicList.songs:
			self.index = (self.index + 1) % len(self.MusicList.songs)
			self.play_song(self.MusicList.songs[self.index])

	# 播放选定音乐的逻辑
	def play_song(self, song, start_position=0):
		print(song.title, song.artist, song.path, start_position)
		try:
			self.index = self.MusicList.songs.index(song)
			self.MusicTitle.setText(f'{song.title} - {song.artist}')
			self.lyrics_data = self.lyrics_manager.load_lyrics(song.path)
			self.display_lyrics()
			self.music_player.play_song(song.path, start_position)
		except Exception as e:
			print('play_song', e)

	def reset_lyrics_auto_scroll(self):
		# 当定时器超时时，重置用户互动标志并更新当前播放的歌词位置
		self.user_is_interacting_with_lyrics = False
		if self.music_player.play_task:
			current_time = self.music_player.get_current_pos()
			self.update_lyrics_display(current_time)

	def on_lyrics_scroll(self):
		# 用户开始滑动时调用
		self.user_is_interacting_with_lyrics = True
		self.lyrics_scroll_timer.start(1000)

	# 显示歌词的逻辑
	def display_lyrics(self):

		try:
			self.SongLyrics.clear()
			self.SongLyrics.setStyleSheet(
				"QListWidget::item { padding-top: 10px; padding-bottom: 10px; max-width: 200px; }")
			self.SongLyrics.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
			for lyric in self.lyrics_data:
				item = QtWidgets.QListWidgetItem(lyric['text'])
				item.setTextAlignment(QtCore.Qt.AlignCenter)
				item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
				item.setForeground(QtGui.QColor('black'))
				item.setBackground(QtGui.QColor('white'))
				self.SongLyrics.addItem(item)
		except Exception as e:
			print('display_lyrics', e)

	# 更新歌词显示逻辑
	def update_lyrics_display(self, current_time):
		if self.user_is_interacting_with_lyrics:
			# 如果用户正在滑动歌词，不自动更新当前播放位置
			return
		current_line_index = -1
		for i, lyric in enumerate(self.lyrics_data):
			item = self.SongLyrics.item(i)
			item.setBackground(QtGui.QColor('white'))
			if current_time >= lyric['time']:
				current_line_index = i
		if current_line_index != -1:
			self.SongLyrics.item(current_line_index).setBackground(QtGui.QColor('pink'))
			self.SongLyrics.setCurrentRow(current_line_index)
			self.SongLyrics.scrollToItem(self.SongLyrics.item(current_line_index),
			                             QtWidgets.QAbstractItemView.PositionAtCenter)

	def on_lyric_double_clicked(self, item):
		# 找到被双击的歌词对应的时间戳
		for lyric in self.lyrics_data:
			if lyric['text'] == item.text():
				target_time = lyric['time']
				self.music_player.seek_to(target_time)  # 跳转到该时间点
				break

	# 播放下一首音乐逻辑
	def next_song(self):
		if self.PlayMode != 1:
			if len(self.PreviousSong) >= 50:
				self.PreviousSong.pop(0)
			self.PreviousSong.append(self.index)
		if self.PlayMode == 0:
			self.random_play()
		elif self.PlayMode == 1:
			self.single_loop()
		else:
			self.list_loop()

	# 播放上一首音乐逻辑
	def previous_song(self):
		if self.PreviousSong == []:
			pass
		else:
			if len(self.PreviousSong) >= 50:
				self.PreviousSong.pop(0)
			self.index = self.PreviousSong.pop()
			self.play_song(self.MusicList.songs[self.index])

	# 控制音乐播放和暂停逻辑
	def ControlMusicPlayback(self):
		if self.music_player.play_task and self.music_player.play_task.is_paused:
			self.music_player.unpause_song()
			self.ControlMusicPlayback_btn.setText('暂停')
		else:
			self.music_player.pause_song()
			self.ControlMusicPlayback_btn.setText('播放')

	# 处理双击音乐列表中的项目逻辑
	def on_double_click(self, item):
		print(item.row(), len(self.filtered_song_indices))
		if item.row() < len(self.filtered_song_indices):
			self.index = self.filtered_song_indices[item.row()]
			self.play_song(self.MusicList.songs[self.index])

	# 减小音量逻辑
	def TurnDownVolume(self):
		new_volume = max(0, self.VolumeSlider.value() - 10)
		self.VolumeSlider.setValue(new_volume)
		self.music_player.TurnDownVolume()

	# 增大音量逻辑
	def TurnUpTheVolume(self):
		new_volume = min(100, self.VolumeSlider.value() + 10)
		self.VolumeSlider.setValue(new_volume)
		self.music_player.TurnUpTheVolume()

	# 设置音量逻辑
	def setVolume(self, volume):
		# print(self.VolumeSlider.value())
		self.music_player.setVolume(volume / 100)

	# 搜索音乐逻辑
	def search_song(self, search_text):
		self.filtered_song_indices.clear()

		self.tableWidget.setRowCount(0)
		for index, song in enumerate(self.MusicList.songs):
			if search_text.lower() in song.title.lower():
				self.filtered_song_indices.append(index)
				row_count = self.tableWidget.rowCount()
				self.tableWidget.insertRow(row_count)
				item=QTableWidgetItem(song.title)
				item.setTextAlignment(Qt.AlignCenter)
				self.tableWidget.setItem(row_count, 0, item)
				item = QTableWidgetItem(song.artist)
				item.setTextAlignment(Qt.AlignCenter)
				self.tableWidget.setItem(row_count, 1, item)

	# 处理系统托盘图标的点击事件逻辑
	def trayIconActivated(self, reason):
		if reason == QSystemTrayIcon.Trigger or reason == QSystemTrayIcon.DoubleClick:
			self.restore()

	# 还原窗口并激活它逻辑
	def restore(self):
		self.showNormal()
		self.activateWindow()

	# 处理窗口状态的改变事件逻辑
	def changeEvent(self, event):
		if event.type() == QEvent.WindowStateChange:
			if self.isMinimized():
				self.hide()
				self.trayIcon.showMessage("运行中", "应用程序正在后台运行。")

	# 处理窗口关闭事件，并保存配置数据逻辑
	def closeEvent(self, event):
		data = {
			'PlayMode': self.PlayMode,
			'index': self.index,
			'current_pos': self.get_current_pos(),
			'pre_path':self.MusicList.songs[self.index].path
		}
		if self.folder_path:
			data['folder_path'] = self.folder_path
		self.write_data(data)
		QApplication.quit()

	# 用户按下进度条逻辑
	def on_slider_pressed(self):
		self.user_is_interacting = True

	# 用户释放进度条后更新歌曲播放位置逻辑
	def on_slider_released(self):
		self.user_is_interacting = False
		self.update_song_position_from_slider()
		current_time = self.music_player.get_current_pos()
		self.update_lyrics_display(current_time)

	# 计算目标时间并跳转逻辑
	def update_song_position_from_slider(self):
		slider_position = self.SongProgressBar.value()
		total_duration = self.music_player.get_total_duration()
		target_time = total_duration * slider_position / self.SongProgressBar.maximum()
		self.music_player.seek_to(target_time)

	# 更新进度条的逻辑
	def update_progress(self, time):
		try:
			self.update_lyrics_display(time[0])
		except Exception as e:
			print(e)
		if self.ControlMusicPlayback_btn.text() == '播放':
			self.ControlMusicPlayback_btn.setText('暂停')
		if not self.user_is_interacting:
			current_pos, total_length, percentage = time
			self.SongProgressBar.setMaximum(math.ceil(self.music_player.get_total_duration()))
			self.SongProgressBar.setValue(int(current_pos))
			current_pos_str = f'{int(current_pos) // 60:02d}:{int(current_pos) % 60:02d}'
			total_length_str = f'{math.ceil(total_length) // 60:02d}:{math.ceil(total_length) % 60:02d}'
			self.current_pos.setText(current_pos_str)
			self.total_length.setText(total_length_str)

	# 当用户移动进度条逻辑
	def on_slider_moved(self):
		current_pos = self.SongProgressBar.value()
		self.current_pos.setText(f'{int(current_pos) // 60:02d}:{int(current_pos) % 60:02d}')

	# 获取当前播放位置逻辑
	def get_current_pos(self):
		return self.music_player.get_current_pos()



	# 改变音乐播放模式逻辑
	def change_MusicMode(self):
		self.PlayMode = (self.PlayMode + 1) % 3
		if self.PlayMode == 0:
			self.MusicMode_btn.setText('随机')
		elif self.PlayMode == 1:
			self.MusicMode_btn.setText('单曲')
		else:
			self.MusicMode_btn.setText('列表')


# 主程序入口
if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	window = MainPage()
	window.show()
	sys.exit(app.exec_())
