class Settings:

    @classmethod
    def initialize(cls):
        with open('settings.txt', 'r') as f:
            settings_string = f.read().split('\n')
        settings = dict()
        for settings_row in settings_string:
            setting, value = settings_row.split('=')
            if value.isnumeric():
                settings[setting] = int(value)
            elif setting in {
                'TITLE',
                'BASIC_CHICK_UNIT',
                'SHOOTING_CHICK_UNIT',
                'BASIC_NERD_UNIT',
                'BASIC_NERD_IMAGE',
                'BASIC_CHICK_IMAGE',
                'SHOOTING_CHICK_IMAGE',
                'BASIC_BULLET_UNIT',
                'BASIC_BULLET_IMAGE'
            }:
                settings[setting] = value

            elif len(setting) >= 5:
                if setting[:5] == 'COLOR':
                    red, green, blue = value.split(',')
                    red = int(red)
                    green = int(green)
                    blue = int(blue)
                    settings[setting] = (red, green, blue)
        for setting, value in settings.items():
            if setting == 'GRID_BLOCK_SIZE':
                cls.GRID_BLOCK_SIZE = value
            elif setting == 'ROWS':
                cls.ROWS = value
            elif setting == 'COLS':
                cls.COLS = value
            elif setting == 'FPS':
                cls.FPS = value
            elif setting == 'BASE_SPEED':
                cls.BASE_SPEED = value * cls.GRID_BLOCK_SIZE / cls.FPS
            elif setting == 'MELEE_DISTANCE':
                cls.MELEE_DISTANCE = value * cls.GRID_BLOCK_SIZE
            elif setting == 'SHORT_RANGE_DISTANCE':
                cls.SHORT_RANGE_DISTANCE = value * cls.GRID_BLOCK_SIZE
            elif setting == 'LONG_RANGE_DISTANCE':
                cls.LONG_RANGE_DISTANCE = value * cls.GRID_BLOCK_SIZE
            elif setting == 'TITLE':
                cls.TITLE = value
            elif setting == "BASIC_NERD_UNIT":
                cls.BASIC_NERD_UNIT = value
            elif setting == "BASIC_CHICK_UNIT":
                cls.BASIC_CHICK_UNIT = value
            elif setting == "SHOOTING_CHICK_UNIT":
                cls.SHOOTING_CHICK_UNIT = value
            elif setting == "BASIC_BULLET_UNIT":
                cls.BASIC_BULLET_UNIT = value
            elif setting == "BASIC_BULLET_IMAGE":
                cls.BASIC_BULLET_IMAGE = value
            elif setting == "BASIC_NERD_IMAGE":
                cls.BASIC_NERD_IMAGE = value
            elif setting == "BASIC_CHICK_IMAGE":
                cls.BASIC_CHICK_IMAGE = value
            elif setting == "SHOOTING_CHICK_IMAGE":
                cls.SHOOTING_CHICK_IMAGE = value
            elif setting == 'COLOR_BLACK':
                cls.COLOR_BLACK = value
            elif setting == 'COLOR_BLUE':
                cls.COLOR_BLUE = value
            elif setting == 'COLOR_PASO':
                cls.COLOR_PASO = value
            elif setting == 'COLOR_RED':
                cls.COLOR_RED = value

        cls.WIDTH = cls.COLS * cls.GRID_BLOCK_SIZE
        cls.HEIGHT = cls.ROWS * cls.GRID_BLOCK_SIZE

class AttackDistance:

    @classmethod
    def initialize(cls):
        cls.MELEE = Settings.MELEE_DISTANCE * Settings.GRID_BLOCK_SIZE
        cls.SHORT = Settings.SHORT_RANGE_DISTANCE * Settings.GRID_BLOCK_SIZE
        cls.LONG = Settings.LONG_RANGE_DISTANCE * Settings.GRID_BLOCK_SIZE


class UnitType:
    TURRET = 1
    PROJECTILE = 2
    WALL = 3
    ENEMY = 4
    GRID = 5
    MINE = 6
    MINER = 7
    PORTAL = 8


class AttackType:
    PHYSICAL = 1
    FOOD = 2
    FIRE = 3
    ICE = 4


Settings.initialize()
AttackDistance.initialize()
