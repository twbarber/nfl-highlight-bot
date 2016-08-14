import urllib.request
import json
from games import Game


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


def get_game_highlights(match: Game):
    highlights = []
    response = urllib.request.urlopen(match.game_center_url())
    string = response.read().decode('utf-8')
    data = json.loads(string)
    in_game_highlights = filter(lambda x: x["clipType"] == "in-game-highlight", data["videos"])
    for video in in_game_highlights:
        highlights.append(Video(video["id"], video["headline"], get_highest_bit_rate_clip(video)))
    return highlights
