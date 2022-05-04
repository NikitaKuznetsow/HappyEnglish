import sqlite3


class FinderPhrases:
    def __init__(self):
        pass

    def get_phrases(self, word, count_phrases):
        con = sqlite3.connect('subtitles.db')
        cur = con.cursor()
        usage_dict = cur.execute(
            f'''select link, content, startTime, duration from subtitles
               where content like '%{word}%'
               order by random()
               limit({count_phrases})
            '''
        ).fetchall()
        links_and_contents = []
        for elem in usage_dict:
            temp_dict = {'link' : self._get_reel(link_video=elem[0], start=elem[2], end=elem[2] + elem[3]),
                         'caption' : elem[1]
            }
            links_and_contents.append(temp_dict)

        return links_and_contents

    def _get_reel(self, link_video, start, end):
        return f'{link_video}#t={start / 1000},{end / 1000}'
