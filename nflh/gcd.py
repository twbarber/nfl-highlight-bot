import _thread
import urllib.request
import xml.etree.ElementTree

from nflh.games import Game

NFL_LIVE_GAME_INDEX_URL = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"


class GameCenterDaemon:

    def __init__(self, index=NFL_LIVE_GAME_INDEX_URL):
        self.index = index
        self.active_games = self.get_active_games()

    def get_active_games(self):
        games = {}
        for game in self.get_game_index_xml():
            eid = game.get("eid")
            games[eid] = Game(eid, game.get("h"), game.get("v"))
        return games

    def check_game_for_update(self, game: Game):
        return True

    def check_games_for_updates(self):
        i = 0
        for game in self.active_games:
            _thread.start_new_thread(self.check_game_for_update, (game, ))
            i += 1
        return

    @staticmethod
    def is_remote_url(url: str):
        return url.startswith("http://")

    def get_game_index_xml(self):
        response_xml = ""
        if self.is_remote_url(self.index):
            try:
                response_xml = urllib.request.urlopen(self.index).read()
            except ConnectionError:
                print("Unable to load game index.")
        else:
            with open(self.index,'r') as f:
                response_xml = f.read()
        return xml.etree.ElementTree.fromstring(response_xml).find("gms").findall("g")

    def index(self):
        return self.index
