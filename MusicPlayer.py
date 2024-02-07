import pygame
from PyQt5.QtCore import QObject, QThread, QMutex, pyqtSignal
from PlayTask import PlayTask

class MusicPlayer(QObject):
    # 信号定义，用于更新播放状态和进度
    statusChanged = pyqtSignal(str)
    progressUpdated = pyqtSignal(object)  # 参数为当前播放时间和总时长
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.play_task = None
        self.thread = None  # 线程用于播放音乐
        self.mutex = QMutex()  # 互斥锁保证线程安全

    def play_song(self, song_path,start_position=0):
        self.mutex.lock()
        try:
            self._ensure_previous_task_stopped()
            self._setup_new_play_task(song_path,start_position)
        except Exception as e:
            print(f"play_song: {e}")
        finally:
            self.mutex.unlock()

    def _ensure_previous_task_stopped(self):
        if self.play_task:
            self.play_task.stop()
            self._disconnect_play_task_signals()
            self._wait_for_thread_to_finish()
            self.play_task.deleteLater()
            self.play_task = None

    def _disconnect_play_task_signals(self):
        # 断开与play_task相关的信号连接
        self.play_task.finished.disconnect()
        self.play_task.progressUpdated.disconnect()

    def _wait_for_thread_to_finish(self):
        if self.thread:
            self.thread.quit()
            self.thread.wait()
            self.thread = None

    def _setup_new_play_task(self, song_path,start_position=0):
        self.play_task = PlayTask(song_path,start_position)
        self.thread = QThread()
        self.play_task.moveToThread(self.thread)

        # 连接新的信号
        self.thread.started.connect(self.play_task.run)
        self.play_task.finished.connect(self.on_finished)
        self.play_task.progressUpdated.connect(self.on_progress_updated)

        self.thread.start()

    def on_finished(self):
        # 处理播放完成逻辑
        self.finished.emit()

    def on_progress_updated(self, progress_info):
        # 更新播放进度
        self.progressUpdated.emit(progress_info)


    def pause_song(self):
        if self.play_task:
            try:
                self.play_task.pause()
            except Exception as e:
                print(f"pause_song: {e}")

    def unpause_song(self):
        if self.play_task:
            try:
                self.play_task.unpause()
            except Exception as e:
                print(f"unpause_song: {e}")

    def stop_song(self):
        if self.play_task:
            try:
                self.play_task.stop()
            except Exception as e:
                print(f"stop_song: {e}")

    def TurnDownVolume(self):
        if self.play_task:
            try:
                self.play_task.adjustVolume(-0.1)
            except Exception as e:
                print(f"TurnDownVolume: {e}")

    def TurnUpTheVolume(self):
        if self.play_task:
            try:
                self.play_task.adjustVolume(0.1)
            except Exception as e:
                print(f"TurnUpTheVolume: {e}")

    def setVolume(self, Volume):
        if self.play_task:
            try:
                self.play_task.setVolume(Volume)
            except Exception as e:
                print(f"SetVolume: {e}")
    def get_total_duration(self):
        if self.play_task:
            try:
                return self.play_task.get_total_duration()
            except Exception as e:
                print(f"get_total_duration: {e}")

    def seek_to(self, time):
        if self.play_task:
            self.play_task.seek_to(time)

    def get_current_pos(self):
        if self.play_task:
            try:
                return self.play_task.get_current_pos()
            except Exception as e:
                print(f"get_current_pos: {e}")
