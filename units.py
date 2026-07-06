from settings import Settings
from settings import AttackDistance

class Unit:
    def __init__(self, unit_type, name, hp, coords, zaxis, modifiers, image_path):
        self.unit_type = unit_type
        self.is_shooter = False
        self.name = name
        self.hp = hp
        self.coords = coords
        self.zaxis = zaxis
        self.modifiers = modifiers
        self.sprite = None
        self.image_path = image_path
        self.sound_path = None
        self.sound_level = 11  # why 11 because its one louder than 10 soo if i need that extra umf i can go one louder
        self.invisible = False
        self.hitbox = coords[0],coords[1],coords[0] + Settings.GRID_BLOCK_SIZE,coords[1] + Settings.GRID_BLOCK_SIZE
    def __str__(self):
        return (f"unit type:{self.unit_type} name:{self.name} hp:{self.hp} "
                f"coords:{self.coords} zaxis:{self.zaxis} modifiers:{self.modifiers} "
                f"image_path:{self.image_path} sound_path:{self.sound_path} sound_level:{self.sound_level}")

    def x_distance(self, other_point):
        return other_point.coords[0] - self.coords[0]  # x is the 0 of chords

    def y_distance(self, other_point):
        return other_point.coords[1] - self.coords[1]   # y is the 1 of chords

    def place(self, x, y):
        self.coords[0] = x
        self.coords[1] = y


    # def hit_scan(self,other):
    #     ALL CODE AND NO PLAY MAKES LIOR A LONLEY BOY
    #     ALL CODE AND NO PLAY MAKES LIOR A LONLEY BOY
    #     REDRUM
    #     REDRUM
    #     REDRUM

class Dangerous:
    def __init__(self, dmg, pulse):
        self.dmg = dmg
        self.pulse = pulse

    @staticmethod
    def attack(attacker, target, attack_distance_type=AttackDistance.MELEE):  # unfinished class method
        target.hp -= attacker.dmg
        print(attacker.name, 'attacking', target.name, 'causing dmg:', attacker.dmg)

    @staticmethod
    def check_distance(attacker, target):
        xd = abs(attacker.coords[0] - target.coords[0])  # the coords 0 is the X axis
        yd = abs(attacker.coords[1] - target.coords[1])  # coords 1 is Y axis
        d = (xd **2 + yd **2)**0.5
        print("distance:", d)
        return d

    @staticmethod
    def is_in_range(distance, attack_distance_type):
        attack_distance = -1
        if attack_distance_type == AttackDistance.MELEE:
            attack_distance = Settings.MELEE_DISTANCE
        if attack_distance_type == AttackDistance.SHORT:
            attack_distance = Settings.SHORT_RANGE_DISTANCE
        if attack_distance_type == AttackDistance.LONG:
            attack_distance = Settings.LONG_RANGE_DISTANCE
        print(distance <= attack_distance)
        return distance <= attack_distance


class Movable:
    def __init__(self, speed):
        self.speed = speed * Settings.BASE_SPEED
        self.h_speed = 0
        self.v_speed = 0

    def calc_speed(self, x_distance, y_distance):
        if y_distance == 0:
            abs_v_speed = 0
            abs_h_speed = self.speed

        elif x_distance == 0:
            abs_h_speed = 0
            abs_v_speed = self.speed
        else:
            ratio = abs(x_distance / y_distance)
            abs_v_speed = (self.speed**2/(ratio+1))**0.5
            abs_h_speed = ratio * abs_v_speed
            abs_d_speed = (abs_h_speed**2 + abs_v_speed**2)**0.5
            x = self.speed/abs_d_speed
            abs_v_speed *= x
            abs_h_speed *= x
        self.v_speed = abs_v_speed if y_distance > 0 else -abs_v_speed
        self.h_speed = abs_h_speed if x_distance > 0 else -abs_h_speed
        return [self.h_speed, self.v_speed]

    def move(self):  # NOT FINISHED
        self.place(self.coords[0] + self.h_speed, self.coords[1] + self.v_speed)


class Env(Unit):
    def __init__(self, unit_type, name, hp, coords, zaxis, modifiers, image_path):
        super().__init__(unit_type, name, hp, coords, zaxis, modifiers, image_path)


class Projectile(Unit, Dangerous, Movable):
    def __init__(self, unit_type, name, dmg, pulse, hp, coords, speed, zaxis, modifiers, image_path, shooter):
        Unit.__init__(self,unit_type, name, hp, coords, zaxis, modifiers, image_path)
        Dangerous.__init__(self, dmg, pulse)
        Movable.__init__(self, speed)
        self.shooter = shooter


class FriendlyUnit(Unit):
    def __init__(self, price, unit_type, name, hp, coords, zaxis, modifiers, image_path):
        super().__init__(unit_type, name, hp, coords, zaxis, modifiers, image_path)
        self.price = price


class EnemyUnit(Unit, Dangerous, Movable):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path):
        Unit.__init__(self, unit_type, name, hp, coords, zaxis, modifiers, image_path)
        Dangerous.__init__(self, dmg, pulse)
        Movable.__init__(self, speed)

    def attack(self, target):
        super().attack(self, target)


class Shooting:
    def __init__(self,shooting_speed,is_shooter=True):
        self.last_frame_shot = 0
        self.shooting_speed = shooting_speed
        self.is_shooter = is_shooter

    def shoot(self, frame):
        self.last_frame_shot = frame
        if isinstance(self, FriendlyUnit):
            bullet = FriendlyBullet("f_bullet", "bb", 1, 1, 1,
                            [self.coords[0],self.coords[1]], 3, 1,
                            None , Settings.BASIC_BULLET_IMAGE, self)
        else:
            bullet = EnemyBullet("e_bullet", "bb", 1, 1, 1,
                            [self.coords[0], self.coords[1]], 3, 1,
                            None, Settings.BASIC_BULLET_IMAGE, self)

        # print(f"i am shooting{frame}")
        return bullet
# WE WANT TO FLIP IMAGES THATS PART ONE AND FLIP HIT DETECTION MAYBE LIOR CAN DO THIS BYHIMSELF MAKE THE BULLETS A CIRCLE AND NO NEED TO FLIP
# WHEN THE SHOOTER LOCKS ON TO THE TARGET THEN THE MATHS OF THE HITBOX AND TARGET FOR THE BULLET SHOULD BE MADE

class Modifier:
    pass


class BasicChick(EnemyUnit):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path):
        super().__init__(dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path)


class ToughChick(EnemyUnit):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path):
        super().__init__(dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path)


class ToughChickSuper(EnemyUnit):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path):
        super().__init__(dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path)


class InvisibleChick(EnemyUnit):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path):
        super().__init__(dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path)
        self.invisible = True


class ShootingChick(EnemyUnit, Shooting):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path, shooting_speed):
        EnemyUnit.__init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path,)
        Shooting.__init__(self, 45)  # this should be loaded from settings

    def str(self):
        return f"word{self.last_frame_shot}"


class BossChick(EnemyUnit):
    def __init__(self, dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path):
        super().__init__(dmg, pulse, unit_type, name, hp, coords, speed, zaxis, modifiers, image_path)


class Mine(Env):
    def __init__(self, capacity, ttm, name, hp, coords, zaxis, modifiers, image_path):  # ttm "time to mine"
        super().__init__('Mine', name, hp, coords, zaxis, modifiers, image_path)
        self.capacity = capacity
        self.ttm = ttm


class Tree(Env):
    def __init__(self, name, hp, coords, zaxis, modifiers, image_path):
        super().__init__('Tree', name, hp, coords, zaxis, modifiers, image_path)


class Miner(FriendlyUnit, Movable):
    def __init__(self, price, name, hp, coords, speed, zaxis, modifiers, image_path):
        FriendlyUnit.__init__(self, price, 'Miner', name, hp, coords, zaxis, modifiers, image_path)
        Movable.__init__(self, speed)


class Pipe(FriendlyUnit, Movable, Shooting):
    def __init__(self, price, unit_type, name, hp, coords,speed, zaxis, modifiers, image_path, openings={'L':False,'R':False,'U':False,'D':False}, shooting_speed=Settings.PIPE_1_S_SPEED):
        FriendlyUnit.__init__(self, price, unit_type, name, hp, coords, zaxis, modifiers, image_path)
        Movable.__init__(self, speed)
        Shooting.__init__(self, shooting_speed,False)
        self.openings = openings.copy()
        self.balls_went_in_here = {'L':False,
                       'R':False,
                       'U':False,
                       'D':False}

    def set_opening(self, opening):
        self.openings[opening] = True


class Nerd(FriendlyUnit, Shooting):
    def __init__(self, price, unit_type, name, hp, coords,speed, zaxis, modifiers, image_path):
        FriendlyUnit.__init__(self, price, unit_type, name, hp, coords, zaxis, modifiers, image_path)
        Shooting.__init__(self, 45)  # this should be loaded from settings

class Grid(FriendlyUnit):
    def __init__(self, price, unit_type, name, hp, coords, zaxis, modifiers, image_path):
        super().__init__(price, unit_type, name, hp, coords, zaxis, modifiers, image_path)


class Bullet(Projectile):
    def __init__(self, unit_type, name, dmg, pulse, hp, coords, speed, zaxis, modifiers, image_path, shooter):
        super().__init__(unit_type, name, dmg, pulse, hp, coords, speed, zaxis, modifiers, image_path, shooter)

    def hit(self, target):
        bulletx = self.coords[0] + Settings.GRID_BLOCK_SIZE / 2
        bullety = self.coords[1] + Settings.GRID_BLOCK_SIZE / 2
        target_left_x = target.coords[0]
        target_right_x = target.coords[0] + Settings.GRID_BLOCK_SIZE / 2
        target_up_y = target.coords[1]
        target_down_y = target.coords[1] + Settings.GRID_BLOCK_SIZE / 2

        # if target_left_x < bulletx < target_right_x and target_up_y < bullety < target_down_y:
        #     return True

        target_x_the_closer_one = target_left_x if (abs(bulletx - target_left_x) <
                                                    abs(bulletx - target_right_x)) else target_right_x
        target_y_the_closer_one = target_down_y if (abs(bullety - target_down_y) <
                                                    abs(bullety - target_up_y)) else target_up_y

        x_distance = abs(bulletx - target_x_the_closer_one)
        y_distance = abs(bullety - target_y_the_closer_one)

        if target_down_y < bullety < target_up_y:
            # IF THE BULLET COMES FROM BLUE QUADRANTS (COMING TOWARDS THE LEFT OR RIGHT SIDES)
            c_distance_from_target = x_distance
        elif target_left_x < bulletx < target_right_x:
            # IF THE BULLET COMES FROM GREEN QUADRANTS (COMING TOWARDS THE UP OR DOWN SIDE)
            c_distance_from_target = y_distance
        else:
            # IF THE BULLET COMES FROM RED QUADRANTS (COMING TOWARDS THE VERTICES)
            c_distance_from_target = (x_distance ** 2 + y_distance ** 2) ** 0.5

        return c_distance_from_target < Settings.GRID_BLOCK_SIZE / 4  # <- HARDCODED! WORKS IF THE BULLET IMAGE SIZE IS HALF OF THE GRID SIZE


class FriendlyBullet(Bullet, FriendlyUnit):
    pass


class EnemyBullet(Bullet, EnemyUnit):
    pass

if __name__ == '__main__':
    eu = EnemyUnit(1, 1, 'enemy', 'black punisher', 1, [0, 0], 60, 1, 1, "assets/basic_chick.png")
    print(eu)

    w = Pipe(1, 'wall', 'glory hole', 5, [100, 0], 1, 1, 1,"./assets/basic_friendly_unit.png")
    print(w)
    eu.attack(w)
    print(w)
    eu.attack(w)
    print(w)

    d = eu.check_distance(eu, w)
    eu.is_in_range(d, attack_distance_type=AttackDistance.MELEE)
    x_distance = eu.x_distance(w)
    y_distance = eu.y_distance(w)
    print(w.coords)
    print(eu.coords)
    eu.calc_speed(x_distance, y_distance)
    eu.move()
    print(eu.coords)
    eu.is_in_range(d, attack_distance_type=AttackDistance.MELEE)
    print(w.coords)

# TO DO keep changing the speed thing
# y_distance = starting_point.y_distance(ending_point)
# x_distance = starting_point.x_distance(ending_point)