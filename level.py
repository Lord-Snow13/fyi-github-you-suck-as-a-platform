from settings import Settings
import units

class Level:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.waves = 0
        self.enemies_dbug = dict()
        self.enemies = dict()

    def initialize(self):
        with open(f'levels\\level_{self.number}_enemies', 'r') as f:
            all_rows = f.read().split('\n')
        for row in all_rows:
            row_length = len(row.rstrip())
            if row_length > self.waves:
                self.waves = row_length
        for wave_number in range(1, self.waves + 1):
            self.enemies_dbug[wave_number] = ''
            self.enemies[wave_number] = []
        x = 0
        for wave_index in range(self.waves):
            wave_number = wave_index + 1
            for row_index in range(Settings.ROWS):
                if wave_index < len(all_rows[row_index]):
                    self.enemies_dbug[wave_number] += all_rows[row_index][wave_index]
                    if all_rows[row_index][wave_index] == Settings.BASIC_CHICK_UNIT:
                        enemy = units.BasicChick(1, 1, 'enemy', 'goth mama', 1, [Settings.WIDTH+1,row_index * Settings.GRID_BLOCK_SIZE], 1, 1, 1,
                                                 Settings.BASIC_CHICK_IMAGE)
                        self.enemies[wave_number].append(enemy)
                    elif all_rows[row_index][wave_index] == Settings.SHOOTING_CHICK_UNIT:
                        enemy = units.ShootingChick(1, 1, 'enemy', f"shooting_chick_number {x}", 1, [Settings.WIDTH+1,row_index * Settings.GRID_BLOCK_SIZE], 1, 1, 1,
                                                 Settings.SHOOTING_CHICK_IMAGE, 20)
                        x += 1
                        self.enemies[wave_number].append(enemy)
                else:
                    self.enemies_dbug[wave_number] += ' '


# if __name__ == '__main__':
#     level1 = Level(1, 'test')
#     level1.initialize()
#     for wave,alist in level1.enemies.items():
#         if wave == 1:
#             print(wave)
#             for enemy in alist:
#                 print(enemy.coords)
#     print(level1.enemies_dbug)

