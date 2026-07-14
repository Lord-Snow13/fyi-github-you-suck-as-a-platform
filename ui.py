import pygame
import sys
import game_logic
from settings import Settings
from units import EnemyUnit, FriendlyUnit, EnemyBullet, Pipe
from settings import AttackDistance
from level import Level




# you need to figure out tomorow how to initialze the next wave not just the first calc if all enemys are gone then spwan the new wave and put it on timer

pygame.init()
screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
pygame.display.set_caption(Settings.TITLE)

clock = pygame.time.Clock()

game = game_logic.Game()
game.initialize()


def draw_grid():
    for row in range(1, Settings.ROWS + 1):
        for col in range(1, Settings.COLS + 1):
            rect = pygame.Rect(
                col * Settings.GRID_BLOCK_SIZE,
                row * Settings.GRID_BLOCK_SIZE-Settings.ROW_OFFSET,
                Settings.GRID_BLOCK_SIZE,
                Settings.GRID_BLOCK_SIZE
            )
            pygame.draw.rect(screen, Settings.COLOR_BLUE, rect, 1)


def draw_unit(unit):
    x = unit.coords[0]  # this coord is the x coord
    y = unit.coords[1]  # this one is the y coord
    unit.sprite = pygame.image.load(unit.image_path).convert_alpha() # needs to be convert_alpha
    unit.sprite = pygame.transform.scale(unit.sprite, (Settings.GRID_BLOCK_SIZE,Settings.GRID_BLOCK_SIZE))
    screen.blit(unit.sprite, (x, y))


def draw_all_units():
    for unit in game.friendly_units_on_screen:
        draw_unit(unit)
    for unit in game.enemy_units_on_screen:
        if unit.invisible == False:
            draw_unit(unit)
    for unit in game.bullets_on_screen:
        draw_unit(unit)


def assign_targets():
    for unit in game.enemy_units_on_screen:
        unit.calc_speed(unit.x_distance(game.friendly_units_on_screen[0]),unit.y_distance(game.friendly_units_on_screen[0]))


def assign_shooting_targets():
    for unit in game.bullets_on_screen:
        unit.calc_speed(unit.x_distance(game.friendly_units_on_screen[0]),unit.y_distance(game.friendly_units_on_screen[0]))  #temporu


def move_all_enemies(): # under matanice need to add a basic move right to left
    for unit in game.enemy_units_on_screen:
        unit.move()


def move_all_bullets(): # under matanice need to add a basic move right to left
    for unit in game.bullets_on_screen:
        unit.move()


def shooting(frame):
    for unit in game.friendly_units_on_screen:
        if unit.is_shooter:
            if frame - unit.last_frame_shot == unit.shooting_speed:
                bullet = unit.shoot(frame)
                game.bullets_on_screen.append(bullet)
    c = 0
    x = 0
    test = set()
    for unit in game.enemy_units_on_screen:
        if unit.is_shooter:
            test.add(unit)
            if (frame - unit.last_frame_shot) % unit.shooting_speed == 0:
                bullet = unit.shoot(frame)
                game.bullets_on_screen.append(bullet)
    # print(test)
    for unit in test:
        # print(unit.name, unit.last_frame_shot)
        pass

def detecthits():
    mybigdict = dict()
    bullets_to_remove = []
    for bullet in game.bullets_on_screen:
        for friendly_unit in game.friendly_units_on_screen:
            if bullet.shooter is not friendly_unit:
                was_it_hit = bullet.hit(friendly_unit)
            if was_it_hit and bullet.shooter is friendly_unit:
                bullets_to_remove.append(bullet)
                if isinstance(bullet, EnemyUnit):
                    pass
                else:
                    if isinstance(friendly_unit, Pipe):
                        friendly_unit.activate()
                        if friendly_unit.openings["L"]:
                            if bullet.shooter.coords[0] < friendly_unit.coords[0]:
                                friendly_unit.balls_went_in_here["L"] = True
                                # print(friendly_unit.balls_went_in_here)
                        if friendly_unit.openings["R"]:
                            if bullet.shooter.coords[0] > friendly_unit.coords[0]: # need to change coords
                                friendly_unit.balls_went_in_here["R"] = True
                        if friendly_unit.openings["U"]:
                            if bullet.shooter.coords[1] < friendly_unit.coords[1]: # need to change coords
                                friendly_unit.balls_went_in_here["U"] = True
                        if friendly_unit.openings["D"]:
                            if bullet.shooter.coords[1] > friendly_unit.coords[1]: # need to change coords
                                friendly_unit.balls_went_in_here["D"] = True

    for bullet in bullets_to_remove:
       game.bullets_on_screen.remove(bullet)

current_wave = 1
current_frame = 0
total_frames = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEWHEEL: # a test for invisible enemeis to show with mousewheel
        #     for enemy in game.enemy_units_on_screen:
        #         if enemy.invisible:
        #             enemy.invisible = False

    screen.fill(Settings.COLOR_BLACK)
    draw_grid()
    assign_targets()
    move_all_enemies()
    # d = game.enemy_units_on_screen[1].check_distance(game.enemy_units_on_screen[1], game.friendly_units_on_screen[1])
    # print(game.enemy_units_on_screen[1].coords, game.enemy_units_on_screen[1].is_in_range(d, attack_distance_type=AttackDistance.SHORT))
    detecthits()
    shooting(total_frames)
    assign_shooting_targets()
    move_all_bullets()
    draw_all_units()
    pygame.display.flip()
    clock.tick(Settings.FPS)
    current_frame += 1
    total_frames += 1
    if current_frame == Settings.FPS:
        current_wave += 1
        current_frame = 0
        game.initialize_the_wave(current_wave)

pygame.quit()
sys.exit()

# load basic sprits