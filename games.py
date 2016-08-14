import xml.etree.ElementTree
import urllib.request
import json
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


class Video:

    def __init__(self, id_, desc, url):
        self.id_ = id_
        self.desc = desc
        self.url = url

    def __str__(self):
        return self.id_ + " - " + self.desc + "\n" + self.url


def get_highest_bit_rate_clip(clips):
    bit_rated = sorted(clips["videoBitRates"], key=lambda video: video["bitrate"], reverse=True)
    return bit_rated[0]["videoPath"]


def get_game_index_xml(source=NFL_LIVE_GAME_INDEX_URL):
    if is_remote_url(source):
        response_xml = urllib.request.urlopen(source).read()
    else:
        response_xml = open(source).read()

    return xml.etree.ElementTree.fromstring(response_xml).find("gms").findall("g")


def is_remote_url(url: str):
    return url.startswith("http://")


def get_highlight_list():

    games = []
    for entry in get_game_index_xml("data/ss.xml"):
        games.append(Game(entry.get("eid"), entry.get("h"), entry.get("v")))
    highlights = []

    for game in (date for date in games if date.was_yesterday()):
        response = urllib.request.urlopen(game.game_center_url())
        string = response.read().decode('utf-8')
        data = json.loads(string)
        in_game_highlights = filter(lambda x: x["clipType"] == "in-game-highlight", data["videos"])
        for video in in_game_highlights:
            highlights.append(Video(video["id"], video["headline"], get_highest_bit_rate_clip(video)))

    return highlights
