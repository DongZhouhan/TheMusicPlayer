import os
import sqlite3
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC

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
                  path TEXT)''')
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_path ON songs (path)")
            conn.commit()

    def add_song(self, song):
        """添加单曲到音乐列表和数据库"""
        with sqlite3.connect('music_library.sqlite') as conn:
            cursor = conn.cursor()
            normalized_path = os.path.normpath(song.path)
            cursor.execute("SELECT id FROM songs WHERE path = ?", (normalized_path,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO songs (title, artist, modification_time, path) VALUES (?, ?, ?, ?)",
                               (song.title, song.artist, song.modification_time, normalized_path))
                conn.commit()
                self.songs.append(song)

    def load_songs_from_folder(self, path_or_paths, is_folder):
        """启动异步加载"""
        self.loadingThread = SongLoadingThread(path_or_paths, is_folder, self)
        self.loadingThread.songsLoaded.connect(self.on_songs_loaded)
        self.loadingThread.start()

    def on_songs_loaded(self):
        """加载完成后的处理"""
        self.load_songs_from_db()
        self.updated.emit(100)

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
        title, artist = song_metadata if song_metadata else self.parse_file_name(os.path.basename(file_path))
        mod_time = os.path.getmtime(file_path)
        normalized_path = os.path.normpath(file_path)
        song = Song(title=title, artist=artist, modification_time=mod_time, path=normalized_path)
        self.add_song(song)

    def load_songs_from_db(self):
        """从数据库加载所有歌曲并更新歌曲列表"""
        with sqlite3.connect('music_library.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, artist, modification_time, path FROM songs ORDER BY modification_time DESC")
            self.songs = [Song(title=row[0], artist=row[1], modification_time=row[2], path=row[3]) for row in cursor.fetchall()]
            print(f"从数据库加载了{len(self.songs)}首歌曲")

    def delete_song_by_path(self, song_path):
        """通过路径删除数据库中的歌曲，并更新内存中的列表"""
        with sqlite3.connect('music_library.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM songs WHERE path = ?", (song_path,))
            conn.commit()
            self.songs = [song for song in self.songs if song.path != song_path]
            self.updated.emit('删除单曲')

    def parse_file_name(self, file_name):
        """从文件名解析歌名和艺术家"""
        file_name_without_extension = os.path.splitext(file_name)[0]
        parts = file_name_without_extension.split(' - ', 1)
        return (parts[0], parts[1]) if len(parts) > 1 else (file_name_without_extension, '未知歌手')

    def get_song_metadata(self, file_path):
        """尝试从音乐文件的元数据中读取歌曲信息"""
        try:
            if file_path.endswith('.mp3'):
                audio = EasyID3(file_path)
            elif file_path.endswith('.flac'):
                audio = FLAC(file_path)
            else:
                return None
            title = audio['title'][0] if 'title' in audio else os.path.splitext(os.path.basename(file_path))[0]
            artist = audio['artist'][0] if 'artist' in audio else '未知歌手'
            return title, artist
        except Exception as e:
            print(f"读取音乐文件元数据时出错: {e}")
            return None
