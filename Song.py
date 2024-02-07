from datetime import datetime

class Song:
    def __init__(self, title, path,ChangeTime):
        self.title = title
        self.path = path
        self.ChangeTime=datetime.fromtimestamp(ChangeTime)
