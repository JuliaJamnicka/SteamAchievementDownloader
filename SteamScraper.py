#!/usr/bin/env python3

from Models.Game import Game
from Models.Achievement import Achievement
from Models.Player import Player
from Models.PlayerStats import PlayerStats

import requests
import json
from datetime import datetime
from urllib.parse import quote_plus


class SteamScraper:
    """
    The constructor takes one parameter 'game' of type Models.Game.
    """
    MY_API_KEY = ''         # your Steam API key goes here
    BASE_URL = 'https://api.steampowered.com/ISteamUserStats/'
    MAX_CASES = 1000        # the number of players to download

    def __init__(self, game):
        self.game = game
        self.players = []
        self.achievements = {}
        self.common_achievements = []
        self.cursor = '*'
        self.log_file = open(f'Logs/{game.name}_achievement_logs.csv', 'w')
        self.common_achievements_file = open(f'Logs/{game.name}_common_achievements.json', 'w')
        self.stats_file = open(f'Logs/{game.name}_player_stats.json', 'w')

    def run(self):
        self._get_game_achievements()
        self._get_common_achievements()
        self._get_players()
        self._save()
        self.log_file.close()
        self.common_achievements_file.close()
        self.stats_file.close()

    def _get_game_achievements(self):
        url = f'{self.BASE_URL}GetSchemaForGame/v2/?key={self.MY_API_KEY}&appid={self.game.id}'

        response = requests.get(url)

        if response.ok:
            parsed_json = json.loads(response.content)

            for achievement in parsed_json['game']['availableGameStats']['achievements']:
                name = achievement['displayName']
                self.achievements[achievement['name']] = name.replace(',', '')

    def _get_common_achievements(self):
        url = f'{self.BASE_URL}GetGlobalAchievementPercentagesForApp' \
              f'/v2/?key={self.MY_API_KEY}&gameid={self.game.id}'

        response = requests.get(url)

        if response.ok:
            parsed_json = json.loads(response.content)
            count = 0

            for achievement in parsed_json['achievementpercentages']['achievements']:
                count += 1
                self.common_achievements.append(self.achievements[achievement['name']])

                if count >= 15 or achievement['percent'] < 20:
                    break

            for main_achievement in self.game.main_achievements:
                if main_achievement not in self.common_achievements:
                    self.common_achievements.append(main_achievement)

        json.dump(self.common_achievements, self.common_achievements_file)

    def _get_players(self):
        url = f'https://store.steampowered.com/appreviews/{self.game.id}' \
              f'?json=1&filter=recent&num_per_page=100'

        response = requests.get(url + f'&cursor={self.cursor}')

        while response.ok and len(self.players) < self.MAX_CASES:
            parsed_json = json.loads(response.content)

            if parsed_json['query_summary']['num_reviews'] == 0:
                break

            for review in parsed_json['reviews']:
                new_player = Player(
                    user_id=review['author']['steamid'],
                    playtime=review['author']['playtime_forever'],
                    left_positive_review=review['voted_up'],
                    review=review['review'])

                if any(p.user_id == new_player.user_id
                       for p in self.players):
                    continue

                if self._get_player_achievements(new_player):
                    self.players.append(new_player)

                    if len(self.players) and len(self.players) % 50 == 0:
                        print(f'{len(self.players) / self.MAX_CASES * 100}% downloaded')

            self.cursor = quote_plus(parsed_json['cursor'])
            response = requests.get(url + f'&cursor={self.cursor}')

    def _get_player_achievements(self, player):
        url = f'{self.BASE_URL}GetPlayerAchievements/v0001/?appid={self.game.id}' \
              f'&key={self.MY_API_KEY}&steamid={player.user_id}'

        response = requests.get(url)
        if not response.ok:
            return False

        parsed_data = json.loads(response.content)

        for achievement in parsed_data['playerstats']['achievements']:
            new_achievement = Achievement(
                name=self.achievements[achievement['apiname']],
                unlock_time=datetime.fromtimestamp(achievement['unlocktime']),
                is_achieved=achievement['achieved'])

            player.achievements.append(new_achievement)

        player.collected_all = len(player.achievements) == \
            sum(1 for ach in player.achievements if ach.is_achieved)

        return True

    def _save(self):
        self.log_file.write('CaseId,Activity,Timestamp\n')

        player_stats = {}

        for player in self.players:
            for ach in filter(lambda a: a.is_achieved, player.achievements):
                line = f'{player.user_id},{ach.name},{ach.unlock_time}\n'

                try:
                    self.log_file.write(line)
                except UnicodeEncodeError:
                    continue

            player_stats[player.user_id] = PlayerStats(
                playtime=player.playtime,
                left_positive_review=player.left_positive_review,
                review=player.review,
                collected_all=player.collected_all).__dict__

        json.dump(player_stats, self.stats_file, indent=1)


if __name__ == '__main__':
    scraper = SteamScraper(Game.GRIS)       # make sure the game contains Steam achievements
    scraper.run()
