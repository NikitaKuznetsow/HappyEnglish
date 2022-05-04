import sqlite3
from urllib.request import urlopen
import json
from urllib.error import HTTPError
import re

COUNT_OF_LOADED_VIDEO = 10

con = sqlite3.connect('./subtitles.db')
cur = con.cursor()


def create_database():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    if not tables or 'subtitles' not in tables[0]:
        cur.execute('''
                    CREATE TABLE subtitles
                        (videoId integer, link text, duration integer, content text, startOfParagraph integer, startTime integer)
                        ''')


def get_subtitles_from_video(video_id, ted_url):
    ted_json = ted_url.read().decode('utf8')
    ted_list = json.loads(ted_json)['captions']
    rows = []
    link_on_video = get_link(video_id)
    for item in ted_list:
        rows.append([video_id, link_on_video] + list(item.values()))
    print(rows)
    return rows


def get_link(video_id):
    page = urlopen(f'https://www.ted.com/talks/{video_id}').read().decode('utf8')
    vidlinks = re.findall(r'https://py.tedcdn(.*)\.mp4', page)  # find all between the two parts in the data
    return f'https://py.tedcdn{vidlinks[0]}.mp4'


def fill_database():
    for video_id in range(1, COUNT_OF_LOADED_VIDEO):
        try:
            page = urlopen(f'https://www.ted.com/talks/subtitles/id/{video_id}/lang/en')

            rows = get_subtitles_from_video(video_id,
                                            page
                                            )
        except HTTPError:
            rows = None
        if rows:
            cur.executemany('insert into subtitles values (?, ?, ?, ?, ?, ?)', rows)
            con.commit()


create_database()
fill_database()
con.close()
