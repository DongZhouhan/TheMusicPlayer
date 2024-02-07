import os
from Song import Song  # Song 类用于表示音乐文件
from PyQt5.QtCore import QObject, pyqtSignal

class MusicList(QObject):
    updated = pyqtSignal(object)  # 当音乐列表更新时发射信号

    def __init__(self):
        super().__init__()
        self.songs = []  # 存储音乐文件的列表

    # 添加单曲到音乐列表
    def add_song(self, song):
        try:
            self.songs.append(song)
            self.updated.emit('添加单曲')  # 发射更新信号，通知播放列表已更新
        except Exception as e:
            print(f"add_song: {e}")

    # 从指定文件夹加载音乐文件
    def load_songs_from_folder(self, folder_path):
        try:
            supported_formats = ('.mp3', '.wav', '.flac')  # 支持的音乐文件格式
            # 使用 os.scandir() 获取目录条目的迭代器
            with os.scandir(folder_path) as entries:
                # 创建一个列表来保存文件和它们的修改时间
                files_with_mod_time = [(entry.name, entry.path, entry.stat().st_mtime) for entry in entries if
                                       entry.is_file() and entry.name.endswith(supported_formats)]

            # 根据修改时间对文件列表进行排序，以便最新的文件排在前面
            files_with_mod_time.sort(key=lambda x: x[2], reverse=True)

            # 遍历排序后的文件列表，为每个文件创建 Song 实例并添加到音乐列表
            songs=[]
            for name, path, mod_time in files_with_mod_time:
                song = Song(title=os.path.splitext(name)[0], path=path, ChangeTime=mod_time)
                songs.append(song)
            self.songs=songs

            # 发射信号，通知播放列表已加载完成
            self.updated.emit(100)
        except Exception as e:
            print(f"load_songs_from_folder: {e}")
