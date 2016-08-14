import xml.etree.ElementTree
import urllib.request
import json
from datetime import datetime

NFL_LIVE_GAME_INDEX_URL = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
NFL_VIDEO_BASE_URL = "http://www.nfl.com/feeds-rs/videos/byGameCenter/{0}.json"


def game_is_today(game_id):
    return str(game_id[:-2]) == str(datetime.today().strftime('%Y%m%d'))

response = urllib.request.urlopen(NFL_LIVE_GAME_INDEX_URL)
response_xml = response.read()

e = xml.etree.ElementTree.fromstring(response_xml).find("gms")

game_ids = e.findall("g")

for game in game_ids:
    game_id = game.get("eid")
    if game_is_today(game_id):
        response = urllib.request.urlopen(NFL_VIDEO_BASE_URL.format(game_id))
        string = response.read().decode('utf-8')
        data = json.loads(string)
        for video in data["videos"]:
            print(str(video["headline"]))
            bitrated = sorted(video["videoBitRates"], key=lambda video: video["bitrate"], reverse=True)
            print(bitrated[0]["videoPath"])

