import os
import re

class LyricsManager:
    def __init__(self):
        # 初始化 LyricsManager 实例
        pass

    def load_lyrics(self, song_path):
        """
        从指定的歌曲路径加载歌词。
        :param song_path: 歌曲文件的路径。
        :return: 格式化后的歌词或提示信息。
        """
        # 获取歌曲所在目录
        song_dir = os.path.dirname(song_path)
        # 获取不带扩展名的歌曲文件名
        base_name = os.path.splitext(os.path.basename(song_path))[0]
        # 构造歌词文件的完整路径
        lyrics_path = os.path.join(song_dir, 'lyrics', base_name + '.lrc')

        if os.path.exists(lyrics_path):
            with open(lyrics_path, 'r', encoding='utf-8') as file:
                lyrics_lines = file.readlines()
            return self.parse_lyrics(lyrics_lines)
        else:
            return [{'time': 0, 'text': "歌词不存在"}]

    def parse_lyrics(self, lyrics_lines):
        """
        解析歌词文件中的每一行。
        :param lyrics_lines: 歌词文件的所有行组成的列表。
        :return: 格式化后的歌词字符串。
        """
        formatted_lyrics = ""
        # 歌词时间标记的正则表达式
        # time_pattern = re.compile(r'\[(\d{2}):(\d{2}\.\d{2})\](.*)')
        # 歌词元数据的正则表达式
        # metadata_pattern = re.compile(r'\[(\w+):(.*)\]')
        time_pattern = re.compile(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)')
        lyrics_data = []
        for line in lyrics_lines:
            time_match = time_pattern.match(line)
            # metadata_match = metadata_pattern.match(line)

            if time_match:
                # 处理歌词行
                minutes, seconds, millis, lyrics_text = time_match.groups()
                # print(minutes, seconds, millis)
                total_seconds = int(minutes) * 60 + int(seconds) + int(millis) / 100
                parts = lyrics_text.split(' / ')
                original = parts[0]
                translation = parts[1] if len(parts) > 1 else ""
                # formatted_lyrics = f"<p style='text-align:center;'>{original}</p>"
                # if translation:
                #     formatted_lyrics = f"<p style='text-align:center;'>{original}</p>"
                lyrics_data.append({'time': total_seconds, 'text': original})

            # elif metadata_match:
                # 处理元数据行
                # pass
        # print(lyrics_data)
        return lyrics_data
