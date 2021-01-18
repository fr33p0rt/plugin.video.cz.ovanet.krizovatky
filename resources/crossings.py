# -*- coding: utf-8 -*-

# Author/Copyright: fr33p0rt
# License: GPLv3 https://www.gnu.org/copyleft/gpl.html

import requests


class Crossings():

    url_list = 'https://krizovatky.ovanet.cz/function/seznam_krizovatek.php'
    url_cam = 'https://stream.ovanet.cz/player/api/embed-live.js?stream=camera{}'

    def get_crossings(self):
        r = requests.get(self.url_list)
        j = r.json()
        c = []
        # id, title
        for i in j:
            c.append({'id': i['cam_id'], 'title': i['title']})
        return c

    def get_cams(self, id):
        r = requests.get(self.url_list)
        j = r.json()
        c = []
        # id, title
        for i1 in j:
            if i1['cam_id'] == id:
                for i2 in i1['cam_ids']:
                    c.append({'id': i2['cam_id'], 'title': i2['title']})
        return c

    def get_stream(self, id):
        r = requests.get(self.url_cam.format(id))
        u = None
        for line in r.iter_lines():
            if '"https://' in line:
                u = line.split('"')[1]
                break
        return u
