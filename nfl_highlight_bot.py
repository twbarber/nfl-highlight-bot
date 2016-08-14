import games
import videos
from games import Game


def get_highlight_list():

    matchups = []
    for entry in games.get_game_index_xml("data/ss.xml"):
        matchups.append(Game(entry.get("eid"), entry.get("h"), entry.get("v")))

    highlights = []
    for game in (date for date in matchups if date.was_yesterday()):
        highlights += videos.get_game_highlights(game)

    return highlights
