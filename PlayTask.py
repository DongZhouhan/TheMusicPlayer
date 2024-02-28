import pygame
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class PlayTask(QObject):
    # 定义用于通信的信号
    finished = pyqtSignal()  # 播放完成
    errorOccurred = pyqtSignal(str)  # 错误发生
    playbackStarted = pyqtSignal()  # 开始播放
    playbackPaused = pyqtSignal()  # 暂停播放
    playbackStopped = pyqtSignal()  # 停止播放
    progressUpdated = pyqtSignal(object)  # 播放进度更新

    def __init__(self, song_path, start_position=0):
        super().__init__()
        self.song_path = song_path  # 歌曲文件路径
        self.is_paused = False  # 暂停状态标志
        self.total_length = 0
        self.seeking = False  # 新增标志来指示是否正在进行跳转
        self.current_pos = 0
        self.start_position = start_position
        self.current_seek_position = start_position  # 新增变量跟踪跳转位置

        try:
            pygame.init()
            pygame.mixer.init()  # 初始化pygame的mixer模块
        except Exception as e:
            self.errorOccurred.emit(f"Pygame初始化错误: {str(e)}")

    def run(self):
        try:
            pygame.mixer.music.load(self.song_path)  # 加载音乐文件
            pygame.mixer.music.set_volume(1)  # 设置初始音量
            pygame.mixer.music.play(start=self.start_position)  # 开始播放
            self.playbackStarted.emit()

            sound = pygame.mixer.Sound(self.song_path)
            total_length = sound.get_length()  # 获取音乐总长度
            self.total_length = total_length

            # 循环以更新播放进度
            while pygame.mixer.music.get_busy():
                current_pos, total_length, percentage = self.get_current_playback_info()
                self.progressUpdated.emit([current_pos, total_length, percentage])  # 发射播放进度信号
                QThread.msleep(100)  # 稍微等待一会，避免过度占用CPU

                # 处理暂停逻辑
                if self.is_paused:
                    while self.is_paused:
                        QThread.msleep(100)

            if not self.is_paused and not self.seeking:
                self.finished.emit()  # 仅在非暂停且非跳转状态时发射完成信号

        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号

    def get_current_playback_info(self):
        """
        获取当前播放信息：播放位置、总长度和播放百分比
        """
        current_pos = (pygame.mixer.music.get_pos() / 1000.0) + self.current_seek_position
        self.current_pos = current_pos
        if current_pos > self.total_length:  # 确保当前位置不超过歌曲总长
            current_pos = self.total_length
        percentage = (current_pos / self.total_length) * 100
        return current_pos, self.total_length, percentage

    def seek_to(self, time):
        self.seeking = True  # 在跳转开始时设置标志
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=time)
            self.current_seek_position = time  # 更新跳转位置
            self.playbackStarted.emit()
        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号
        finally:
            self.seeking = False  # 跳转完成后重置标志

    def pause(self):
        # 暂停播放音乐
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.is_paused = True
                self.playbackPaused.emit()
        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号

    def unpause(self):
        # 恢复播放音乐
        try:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.playbackStarted.emit()
        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号

    def stop(self):
        # 停止播放音乐
        try:
            pygame.mixer.music.stop()
            self.is_paused = False
            self.playbackStopped.emit()
        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号

    def adjustVolume(self, change):
        # 调整音量，确保在0到1的范围内
        try:
            volume = max(0.0, min(pygame.mixer.music.get_volume() + change, 1.0))
            pygame.mixer.music.set_volume(volume)

        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号

    def setVolume(self, volume):
        # 直接设置音量，确保在0到1的范围内
        try:
            pygame.mixer.music.set_volume(volume)

        except Exception as e:
            self.errorOccurred.emit(str(e))  # 发射其他错误信号

    def get_total_duration(self):
        return self.total_length

    def get_current_pos(self):
        return self.current_pos
