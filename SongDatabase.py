import sqlite3

from Song import Song


def create_db_and_table():
    conn = sqlite3.connect('playlist.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS playlist
                 (title TEXT, path TEXT, ChangeTime REAL)''')
    conn.commit()
    conn.close()

def save_playlist_to_db(music_list):
    conn = sqlite3.connect('playlist.db')
    c = conn.cursor()
    c.execute('DELETE FROM playlist')  # 清空旧数据
    for song in music_list.songs:
        c.execute('INSERT INTO playlist (title, path, ChangeTime) VALUES (?, ?, ?)',
                  (song.title, song.path, song.ChangeTime))
    conn.commit()
    conn.close()

def load_playlist_from_db(music_list):
    conn = sqlite3.connect('playlist.db')
    c = conn.cursor()
    for row in c.execute('SELECT title, path, ChangeTime FROM playlist'):
        song = Song(title=row[0], path=row[1], ChangeTime=row[2])
        music_list.add_song(song)
    conn.close()
