import os
import sqlite3

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

from Song import Song


class SongLoadingThread(QThread):
	songsLoaded = pyqtSignal()

	def __init__(self, folder_path, is_folder, parent=None):
		super().__init__(parent)
		self.folder_path = folder_path
		self.is_folder = is_folder
		self.parent = parent

	def run(self):
		# 在线程中处理加载歌曲
		self.parent.load_songs_from_folder_logic(self.folder_path, self.is_folder)
		self.songsLoaded.emit()


class MusicList(QObject):
	updated = pyqtSignal(object)  # 当音乐列表更新时发射信号

	def __init__(self):
		super().__init__()
		self.songs = []  # 存储音乐文件的列表
		self.init_db()

	def init_db(self):
		# 初始化数据库，创建表结构
		with sqlite3.connect('music_library.sqlite') as conn:
			cursor = conn.cursor()
			cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                 (id INTEGER PRIMARY KEY,
                  title TEXT,
                  artist TEXT,
                  modification_time TEXT,
                  path TEXT,
                  bitrate INTEGER DEFAULT 0)''')
			cursor.execute("CREATE INDEX IF NOT EXISTS idx_path ON songs (path)")
			conn.commit()

	def add_song(self, song):
		"""添加单曲到音乐列表和数据库"""
		# 连接到 SQLite 数据库
		with sqlite3.connect('music_library.sqlite') as conn:
			cursor = conn.cursor()
			# 标准化歌曲路径
			normalized_path = os.path.normpath(song.path)
			# 查询数据库中是否已存在相同路径的歌曲
			cursor.execute("SELECT id, bitrate FROM songs WHERE path = ?", (normalized_path,))
			result = cursor.fetchone()
			if result is not None:  # 如果歌曲已存在
				old_bitrate = result[1]
				if old_bitrate != song.bitrate:  # 如果现有的比特率与新歌曲的比特率不同
					# 更新数据库中的比特率信息
					cursor.execute("UPDATE songs SET bitrate = ? WHERE path = ?", (song.bitrate, normalized_path))
					conn.commit()  # 提交事务
					# 更新音乐列表中对应歌曲的比特率信息
					for i, s in enumerate(self.songs):
						if s.path == song.path:
							self.songs[i].bitrate = song.bitrate
			else:  # 如果歌曲不存在
				# 将新歌曲信息插入到数据库中
				cursor.execute(
					"INSERT INTO songs (title, artist, modification_time, path, bitrate) VALUES (?, ?, ?, ?, ?)",
					(song.title, song.artist, song.modification_time, normalized_path, song.bitrate))
				conn.commit()  # 提交事务
				# 将新歌曲添加到音乐列表中
				self.songs.append(song)

	def load_songs_from_folder(self, path_or_paths, is_folder):
		"""启动异步加载"""
		self.loadingThread = SongLoadingThread(path_or_paths, is_folder, self)
		self.loadingThread.songsLoaded.connect(self.on_songs_loaded)
		self.loadingThread.start()

	def on_songs_loaded(self):
		"""加载完成后的处理"""
		try:
			self.load_songs_from_db()
			self.updated.emit(100)
		except Exception as e:
			print(f"on_songs_loaded: {e}")

	def load_songs_from_folder_logic(self, path_or_paths, is_folder):
		"""处理音乐文件的加载，无论是从文件夹还是从单个/多个文件"""
		supported_formats = ('.mp3', '.wav', '.flac')
		if is_folder:
			for entry in os.scandir(path_or_paths):
				if entry.is_file() and entry.name.lower().endswith(supported_formats):
					self.process_single_file(entry.path)
		else:
			for file_path in path_or_paths:
				if file_path.lower().endswith(supported_formats):
					self.process_single_file(file_path)

	def process_single_file(self, file_path):
		"""处理单个文件的加载"""
		song_metadata = self.get_song_metadata(file_path)
		# 检查元数据是否存在且有效
		# print(song_metadata[2])
		if song_metadata:
			if song_metadata[0] is not None:
				title = song_metadata[0]
			else:
				title = self.parse_file_name(os.path.basename(file_path))[0]
			if song_metadata[1] is not None:

				artist = song_metadata[1]
			else:
				artist = self.parse_file_name(os.path.basename(file_path))[1]
			bitrate = song_metadata[2]
		else:
			title, artist = self.parse_file_name(os.path.basename(file_path))
			bitrate = 0
		# if song_metadata and not (song_metadata[0] in [None, "未知歌手"] or song_metadata[1] in [None, "未知歌手"]):
		# 	title, artist, bitrate = song_metadata
		# else:
		# 	# 如果元数据不存在或不完整，从文件名解析
		# 	title, artist = self.parse_file_name(os.path.basename(file_path))

		mod_time = os.path.getmtime(file_path)
		normalized_path = os.path.normpath(file_path)
		song = Song(title=title, artist=artist, modification_time=mod_time, path=normalized_path, bitrate=bitrate)
		self.add_song(song)

	def load_songs_from_db(self):
		"""从数据库加载所有歌曲并更新歌曲列表"""
		try:
			with sqlite3.connect('music_library.sqlite') as conn:
				cursor = conn.cursor()
				cursor.execute(
					"SELECT title, artist, modification_time, path,bitrate FROM songs ORDER BY modification_time "
					"DESC")
				self.songs = [Song(title=row[0], artist=row[1], modification_time=row[2], path=row[3], bitrate=row[
					4])
				              for
				              row in
				              cursor.fetchall()]
				print(f"从数据库加载了{len(self.songs)}首歌曲")
		except Exception as e:
			print(f"load_songs_from_db: {e}")

	def delete_song_by_path(self, song_path):
		"""通过路径删除数据库中的歌曲，并更新内存中的列表"""
		with sqlite3.connect('music_library.sqlite') as conn:
			cursor = conn.cursor()
			cursor.execute("DELETE FROM songs WHERE path = ?", (song_path,))
			conn.commit()
			self.songs = [song for song in self.songs if song.path != song_path]
			self.updated.emit('删除单曲')

	def delete_music_list(self):
		try:
			"""删除数据库中的所有歌曲，并更新内存中的列表"""
			with sqlite3.connect('music_library.sqlite') as conn:
				cursor = conn.cursor()
				cursor.execute("DELETE FROM songs")
				conn.commit()
				self.songs = []
				self.updated.emit('删除所有歌曲')
		except Exception as e:
			print(f"删除音乐列表时出错: {e}")

	def parse_file_name(self, file_name):
		"""从文件名解析歌名和艺术家"""
		file_name_without_extension = os.path.splitext(file_name)[0]
		parts = file_name_without_extension.split('-', 1)
		return (parts[0].strip(), parts[1].strip()) if len(parts) > 1 else (file_name_without_extension, '未知')

	def get_song_metadata(self, file_path):
		supported_formats = {
			'.mp3': {'class': MP3, 'metadata_keys': {'title': 'TIT2', 'artist': 'TPE1'}},
			'.flac': {'class': FLAC, 'metadata_keys': {'title': 'title', 'artist': 'artist'}}
		}
		"""尝试从音乐文件的元数据中读取歌曲信息"""
		file_extension = file_path[file_path.rfind('.'):].lower()
		if file_extension in supported_formats:
			format_info = supported_formats[file_extension]
			try:
				audio = format_info['class'](file_path)
				metadata_keys = format_info['metadata_keys']
				title = audio[metadata_keys['title']][0] if metadata_keys['title'] in audio else None
				artist = audio[metadata_keys['artist']][0] if metadata_keys['artist'] in audio else None
				bitrate = audio.info.bitrate if hasattr(audio.info, 'bitrate') else 0
				return title, artist, bitrate
			except Exception as e:
				raise Exception(f"读取音乐文件元数据时出错: {e}")
		else:
			return None
