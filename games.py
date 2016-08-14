import xml.etree.ElementTree
import urllib.request
import json
from datetime import datetime, timedelta

NFL_LIVE_GAME_INDEX_URL = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
NFL_VIDEO_BASE_URL = "http://www.nfl.com/feeds-rs/videos/byGameCenter/{0}.json"


class Video:

    def __init__(self, id_, desc, url):
        self.id_ = id_
        self.desc = desc
        self.url = url

    def __str__(self):
        return '<' + self.url + '|' + self.desc + '>'


def game_is_today(game_id):
    return str(game_id[:-2]) == str((datetime.today() - timedelta(1)).strftime('%Y%m%d'))


def get_highest_bitrate_clip(clips):
    bitrated = sorted(clips["videoBitRates"], key=lambda video: video["bitrate"], reverse=True)
    return bitrated[0]["videoPath"]


def get_highlight_list():

    highlights = []

    response_xml = urllib.request.urlopen(NFL_LIVE_GAME_INDEX_URL).read()

    games = xml.etree.ElementTree.fromstring(response_xml).find("gms").findall("g")

    for game in (x for x in games if game_is_today(x.get("eid"))):
        response = urllib.request.urlopen(NFL_VIDEO_BASE_URL.format(game.get("eid")))
        string = response.read().decode('utf-8')
        data = json.loads(string)
        in_game_highlights = filter(lambda x: x["clipType"] == "in-game-highlight", data["videos"])
        for video in in_game_highlights:
            highlights.append(Video(video["id"], video["headline"], get_highest_bitrate_clip(video)))

    return highlights
