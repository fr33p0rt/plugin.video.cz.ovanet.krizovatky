# -*- coding: utf-8 -*-

# Author/Copyright: fr33p0rt
# License: GPLv3 https://www.gnu.org/copyleft/gpl.html

import sys

from urllib import urlencode
from urlparse import parse_qsl

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.crossings import Crossings


def get_url(**kwargs):
    return '{0}?{1}'.format(_addon_url_, urlencode(kwargs))


def list_root():
    crossings = Crossings()
    xbmcplugin.setPluginCategory(_addon_handle_, _addon_id_)
    xbmcplugin.setContent(_addon_handle_, 'videos')

    for crossing in crossings.get_crossings():
        list_item = xbmcgui.ListItem(label=crossing['title'])
        list_item.setInfo('video', {'title': crossing['title'], 'genre': crossing['title'], 'mediatype': 'video'})

        url = get_url(action='crossing', id=crossing['id'])
        xbmcplugin.addDirectoryItem(_addon_handle_, url, list_item, True)
    xbmcplugin.addSortMethod(_addon_handle_, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_addon_handle_)


def list_crossing(direction_id):
    crossings = Crossings()
    xbmcplugin.setPluginCategory(_addon_handle_, _addon_id_)
    xbmcplugin.setContent(_addon_handle_, 'videos')

    for cam in crossings.get_cams(direction_id):
        title = 'směr ' + cam['title']
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title, 'genre': title, 'mediatype': 'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='stream', id=cam['id'])
        xbmcplugin.addDirectoryItem(_addon_handle_, url, list_item, False)
    xbmcplugin.addSortMethod(_addon_handle_, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_addon_handle_)


def play_video(stream_id):
    crossings = Crossings()
    video = crossings.get_stream(stream_id)
    if video:
        play_item = xbmcgui.ListItem(path=video)
        xbmcplugin.setResolvedUrl(_addon_handle_, True, listitem=play_item)
    else:
        xbmcgui.Dialog().ok('Chyba', 'Stream nenalezen')


_addon_version_ = '0.1.0'
if __name__ == '__main__':
    _addon_url_ = sys.argv[0]
    _addon_id_ = _addon_url_.replace('plugin://', '').replace('/', '')
    _addon_handle_ = int(sys.argv[1])

    p = dict(parse_qsl(sys.argv[2][1:]))
    if p:
        if p['action'] == 'crossing':
            list_crossing(int(p['id']))
        if p['action'] == 'stream':
            play_video(int(p['id']))
    else:
        list_root()
