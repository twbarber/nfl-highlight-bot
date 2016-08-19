import unittest
from nflh.gcd import GameCenterDaemon


class GameCenterDaemonTest(unittest.TestCase):

    def test_local_index(self):
        local_index = "../data/ss.xml"
        test = GameCenterDaemon(local_index)
        self.assertEqual(local_index, test.index)

    def test_local_games(self):
        local_index = "../data/ss.xml"
        local_game_eids = {
            '2016081152', '2016081151', '2016081153', '2016081155',
            '2016081154', '2016081156', '2016081252', '2016081253',
            '2016081254', '2016081255', '2016081256', '2016081351',
            '2016081354', '2016081353', '2016081352', '2016081451'
        }
        test = GameCenterDaemon(local_index)
        self.assertEqual(local_game_eids, set(test.get_active_games().keys()))

    def test_check_game_updates_populates_active_games(self):
        local_index = "../data/ss.xml"
        test = GameCenterDaemon(local_index)
        test.check_games_for_updates()

if __name__ == '__main__':
    unittest.main()
