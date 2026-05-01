from level import Level
from units import *  # hard coded fix it so we can inherit the whole unit shabang


class Game:
    def __init__(self):
        self.level = Level(1, 'test')
        # self.friendly_units = dict() # maybe not neccery
        # self.enemy_units = dict()
        self.enemy_units_on_screen = list()
        self.friendly_units_on_screen = list()

    def initialize(self): # i want to not hard coded the stuff below
        self.level.initialize()  # hard coded
        self.friendly_units_on_screen.append(Wall(1, 'wall', 'glory hole', 5, [500, 600], 1, 1, 1, Settings.BASIC_NERD_IMAGE))  # change this to read from settings
        # self.enemy_units_on_screen[1] = BasicEnemy(1, 'wall', 'glory hole', 5, 1, [100, 200], 1, 1,1)  # change this to coded
        # make a placment feture for the freindly units
        self.initialize_the_wave(1)



    def initialize_the_wave(self,wave_number):
        for wave, alist in self.level.enemies.items():  # this needs to be mutable instaed of wave 1 this also needs to turn into an function
            if wave == wave_number:
                for enemy in alist:
                    self.enemy_units_on_screen.append(enemy)