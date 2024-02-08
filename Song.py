from datetime import datetime

class Song:
    def __init__(self, title='未知', path='', modification_time=0, artist='未知'):
        self.title = title
        self.path = path
        # 检查modification_time是否为整数或浮点数类型的时间戳
        if isinstance(modification_time, (int, float)):
            # 如果是整数或浮点数，假设它是时间戳，并转换为ISO8601格式的字符串
            self.modification_time = datetime.fromtimestamp(modification_time).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(modification_time, str):
            # 如果已经是字符串，直接使用
            self.modification_time = modification_time
        else:
            # 如果modification_time既不是整数/浮点数也不是字符串，或为了处理其他类型
            self.modification_time = "1970-01-01 00:00:00"  # 或其他合适的默认值
        self.artist = artist
