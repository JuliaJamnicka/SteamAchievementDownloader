#!/usr/bin/env python3


class Player:
    def __init__(self, user_id, playtime,
                 left_positive_review, review):
        self.user_id = user_id
        self.playtime = playtime
        self.left_positive_review = left_positive_review
        self.review = review
        self.achievements = []
        self.collected_all = False
