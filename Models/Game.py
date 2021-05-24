#!usr/bin/env python3

from enum import Enum


class Game(Enum):
    GRIS = 683320
    HADES = 1145360
    PER_ASPERA = 803050
    BLACK_MIRROR = 581300
    TIS_100 = 370360
    FRIDAY_THE_13TH = 438740
    OXYGEN_NOT_INCLUDED = 457140
    WITCHER_3 = 292030

    @property
    def id(self):
        return self.value

    @property
    def end_achievement(self):
        if self == Game.GRIS:
            return 'The End'
        elif self == Game.HADES:
            return 'The Family Secret'
        elif self == Game.PER_ASPERA:
            return 'Terraformer V'
        elif self == Game.BLACK_MIRROR:
            return 'Chapter V completed'
        elif self == Game.TIS_100:
            return '100_PERCENT_V1'
        elif self == Game.WITCHER_3:
            return 'Passed the Trial'
        elif self == Game.OXYGEN_NOT_INCLUDED:
            return 'Home Sweet Home'
        else:
            return ''

    @property
    def main_achievements(self):
        if self == Game.GRIS:
            return ['Red', 'Green', 'Blue',
                    'Yellow', 'The End']
        elif self == Game.HADES:
            return ['Escaped Tartarus', 'Escaped Asphodel', 'Escaped Elysium',
                    'Is There No Escape?', 'The Family Secret']
        elif self == Game.PER_ASPERA:
            return ['Terraformer I', 'Terraformer II', 'Terraformer III',
                    'Terraformer IV', 'Terraformer V']
        elif self == Game.BLACK_MIRROR:
            return ['Chapter I completed', 'Chapter II completed', 'Chapter III completed',
                    'Chapter IV completed', 'Chapter V completed']
        elif self == Game.WITCHER_3:
            return ['Lilac and Gooseberries', 'Family Counselor', 'A Friend in Need', 'Necromancer',
                    'Something More', 'Xenonaut', 'The King is Dead', 'Passed the Trial']
        else:
            return []
