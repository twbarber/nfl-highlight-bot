import xml.etree.ElementTree
import urllib.request
from datetime import datetime, timedelta

NFL_LIVE_GAME_INDEX_URL = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"


class Game:

    NFL_VIDEO_BASE_URL = "http://www.nfl.com/feeds-rs/videos/byGameCenter/{0}.json"

    def __init__(self, id_, h, v):
        self.id_ = id_
        self.date = self.id_[:-2]
        self.home = h
        self.vis = v

    def is_today(self):
        return self.date == str((datetime.today()).strftime('%Y%m%d'))

    def was_yesterday(self):
        return self.date == str((datetime.today() - timedelta(1)).strftime('%Y%m%d'))

    def game_center_url(self):
        return self.NFL_VIDEO_BASE_URL.format(self.id_)


def is_remote_url(url: str):
    return url.startswith("http://")


def get_game_index_xml(source=NFL_LIVE_GAME_INDEX_URL):
    if is_remote_url(source):
        response_xml = urllib.request.urlopen(source).read()
    else:
        response_xml = open(source).read()

    return xml.etree.ElementTree.fromstring(response_xml).find("gms").findall("g")

