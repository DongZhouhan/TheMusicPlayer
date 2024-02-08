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
        # 在线程中创建新的数据库连接来加载歌曲
        self.parent.load_songs_from_folder_logic(self.folder_path, self.is_folder, new_thread=True)
        self.songsLoaded.emit()

class MusicList(QObject):
    updated = pyqtSignal(object)  # 当音乐列表更新时发射信号

    def __init__(self):
        super().__init__()
        self.songs = []  # 存储音乐文件的列表
        # 初始化数据库结构，不在这里创建连接
        self.init_db()

    def init_db(self):
        # 创建数据库和表结构，但不保持打开的连接
        connection = sqlite3.connect('music_library.sqlite')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS songs
             (id INTEGER PRIMARY KEY,
              title TEXT,
              artist TEXT,
              modification_time TEXT,
              path TEXT)''')
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_path ON songs (path)")
        connection.commit()
        connection.close()

    def add_song(self, song, cursor):
        """添加单曲到音乐列表和数据库"""
        try:
            # 使用os.path.normpath确保路径格式一致
            normalized_path = os.path.normpath(song.path)
            cursor.execute("SELECT id FROM songs WHERE path = ?", (normalized_path,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO songs (title, artist, modification_time, path) VALUES (?, ?, ?, ?)",
                               (song.title, song.artist, song.modification_time, normalized_path))
                self.songs.append(song)
            else:
                pass
        except Exception as e:
            print(f"添加歌曲时出错: {e}")

    def load_songs_from_folder(self, path_or_paths, is_folder):
        """启动异步加载"""
        self.loadingThread = SongLoadingThread(path_or_paths, is_folder, self)
        self.loadingThread.songsLoaded.connect(self.on_songs_loaded)
        self.loadingThread.start()

    def on_songs_loaded(self):
        """加载完成后的处理"""
        self.load_songs_from_db()  # 确保列表与数据库同步
        self.updated.emit(100)  # 发射更新信号

    def load_songs_from_folder_logic(self, path_or_paths, is_folder, new_thread=False):
        """处理音乐文件的加载，无论是从文件夹还是从单个/多个文件"""
        supported_formats = ('.mp3', '.wav', '.flac')  # 支持的文件格式
        if new_thread:
            # 在新线程中创建数据库连接
            connection = sqlite3.connect('music_library.sqlite')
            cursor = connection.cursor()
        else:
            cursor = self.db_cursor  # 如果不是新线程，使用原有的cursor

        try:
            if is_folder:
                # 处理文件夹路径
                for entry in os.scandir(path_or_paths):
                    if entry.is_file() and entry.name.lower().endswith(supported_formats):
                        self.process_single_file(entry.path, cursor)
            else:
                # 处理单个或多个文件路径
                for file_path in path_or_paths:
                    if file_path.lower().endswith(supported_formats):
                        self.process_single_file(file_path, cursor)
                    else:
                        print("不支持的文件格式:", os.path.basename(file_path))
            if new_thread:
                connection.commit()  # 确保在新线程中提交事务
                connection.close()  # 并关闭连接
        except Exception as e:
            print(f"加载音乐时出错: {e}")
            if new_thread:
                connection.rollback()
                connection.close()

        # 发射更新信号
        if not new_thread:
            self.updated.emit(100)

    def process_single_file(self, file_path, cursor):
        """处理单个文件的加载"""
        song_metadata = self.get_song_metadata(file_path)
        if song_metadata:
            title, artist = song_metadata
        else:
            title, artist = self.parse_file_name(os.path.basename(file_path))
        mod_time = os.path.getmtime(file_path)
        normalized_path = os.path.normpath(file_path)
        song = Song(title=title, artist=artist, modification_time=mod_time, path=normalized_path)
        self.add_song(song, cursor)

    def load_songs_from_db(self):
        """从数据库加载所有歌曲并更新歌曲列表"""
        connection = sqlite3.connect('music_library.sqlite')
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT title, artist, modification_time, path FROM songs ORDER BY modification_time DESC")
            self.songs.clear()
            for row in cursor.fetchall():
                song = Song(title=row[0], artist=row[1], modification_time=row[2], path=row[3])
                self.songs.append(song)
            print(f"从数据库加载了{len(self.songs)}首歌曲")
            self.updated.emit(100)
        except Exception as e:
            print(f"从数据库加载歌曲时出错: {e}")
        finally:
            connection.close()
    def delete_song_by_path(self, song_path):
        """通过路径删除数据库中的歌曲，并更新内存中的列表"""
        try:
            self.db_cursor.execute("DELETE FROM songs WHERE path = ?", (song_path,))
            self.db_connection.commit()  # 提交变更
            self.songs = [song for song in self.songs if song.path != song_path]  # 更新内存列表
            self.updated.emit('删除单曲')  # 发射更新信号
        except Exception as e:
            print(f"删除歌曲时出错: {e}")
    def close(self):
        """关闭数据库连接"""
        self.db_connection.close()

    # 这里添加了从文件名解析歌名和艺术家的函数和从音乐文件元数据中获取信息的函数
    def parse_file_name(self,file_name):
        """从文件名解析歌名和艺术家"""
        file_name_without_extension = os.path.splitext(file_name)[0]
        if ' - ' in file_name_without_extension:
            title, artist = file_name_without_extension.split('-', 1)
        else:
            title = file_name_without_extension
            artist = '未知歌手'
        return title.strip(), artist.strip()

    def get_song_metadata(self, file_path):
        """尝试从音乐文件的元数据中读取歌曲信息。如果标题或艺术家为空，则使用默认值或文件名。"""
        try:
            title = None
            artist = None
            if file_path.endswith('.mp3'):
                audio = EasyID3(file_path)
            elif file_path.endswith('.flac'):
                audio = FLAC(file_path)
            else:
                return None

            if 'title' in audio and audio['title']:
                title = audio['title'][0]
            if 'artist' in audio and audio['artist']:
                artist = audio['artist'][0]

            # 如果标题为空，使用文件名（不包含扩展名）作为标题
            if not title:
                title = os.path.splitext(os.path.basename(file_path))[0]

            # 如果艺术家为空，使用默认值
            if not artist:
                artist = '未知歌手'

            return title, artist
        except Exception as e:
            print(f"读取音乐文件元数据时出错: {e}")
            # 如果无法读取元数据，同样使用文件名作为标题，艺术家为未知
            title = os.path.splitext(os.path.basename(file_path))[0]
            artist = '未知歌手'
            return title, artist
