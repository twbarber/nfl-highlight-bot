from datetime import datetime, timedelta

GAME_VIDEO_BASE_URL = "http://www.nfl.com/feeds-rs/videos/byGameCenter/{0}.json"
LIVE_UPDATE_BASE_URL = "http://www.nfl.com/liveupdate/game-center/{0}/{0}_gtd.json"


class Game(object):

    def __init__(self, id_, h, v):
        self.id_ = id_
        self.date = self.id_[:-2]
        self.home = h
        self.vis = v

    def is_today(self):
        return self.date == str((datetime.today()).strftime('%Y%m%d'))

    def video_url(self):
        return GAME_VIDEO_BASE_URL.format(self.id_)

    def live_update_url(self):
        return LIVE_UPDATE_BASE_URL.format(self.id_)
