import pygame
from collections import deque
import math
from settings import Settings
#from player import Player
from sprite import SpriteObject
from rays import ray_casting_walls
from level1 import collision_walls, world_map, matrix_map, simpl_map
from level2 import collision_walls_2, world_map_2, matrix_map_2, simpl_map_2
#from drawing import Drawing
from wave import get_path

class Portal(SpriteObject):
    def __init__(self, x, y, scale, sh, side):
        super().__init__({
                'sprite': pygame.image.load('sprites/portal/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': sh,
                'scale': scale,
                'animation': [],
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'side': side,
                'anim_dir': 0
            }, (x, y))
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
    #
    # def object_locate(self, x, y, angle):
    #     # print(pygame.Rect(x, y, 1, 1).collidelistall([self.rect]), self.rect, x, y)
    #     # if len(pygame.Rect(x, y, 1, 1).collidelistall([self.rect])):
    #     #     level.__init__([], [], [], collision_walls_2, world_map_2, matrix_map_2, min_map_col, simpl_map_2)
    #     #     return False
    #     return super().object_locate(x, y, angle)


class Win(SpriteObject):
    def __init__(self, x, y, scale, sh, side):
        super().__init__({
                'sprite': pygame.image.load('sprites/win/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': sh,
                'scale': scale,
                'animation': [],
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'side': side,
                'anim_dir': 0
            }, (x, y))


class Enemy(SpriteObject):
    def __init__(self, x, y, scale, sh, side, hp):
        super().__init__({
                'sprite': pygame.image.load('sprites/enemy/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': sh,
                'scale': scale,
                'animation': deque(
                    [pygame.image.load(f'sprites/enemy/noth/{i}.png').convert_alpha() for i in range(1, 5)]),
                'animation_dist': 800,
                'animation_speed': 20,
                'blocked': True,
                'side': side,
                'anim_dir': -1
            }, (x, y))
        self.player_hp = hp
        self.noth_an = deque([pygame.image.load(f'sprites/enemy/noth/{i}.png').convert_alpha() for i in range(1, 5)])
        self.att_an = deque([pygame.image.load(f'sprites/enemy/attack/{i}.png').convert_alpha() for i in range(1, 6)])
        self.dam_an = deque([pygame.image.load(f'sprites/enemy/damaged/{i}.png').convert_alpha() for i in range(1, 3)])
        self.death_an = deque([pygame.image.load(f'sprites/enemy/death/{i}.png').convert_alpha() for i in range(1, 6)])
        self.walk_an = deque([pygame.image.load(f'sprites/enemy/walk/{i}.png').convert_alpha() for i in range(1, 6)])
        self.hp = 100
        self.dam = 10
        self.go_death = False
        self.death = False
        self.att = False
        self.an = 0
        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)
        self.way = []

    def attacked(self, dam):
        if not self.go_death:
            self.att = False
            self.hp -= dam
            if self.hp <= 0:
                self.animation = self.death_an
                self.go_death = True
                self.an = 5
            else:
                self.animation = self.dam_an.copy()
                self.an = 2

    def object_locate(self, x, y, angle):
        # print(x, y, " ", self.x, self.y)
        x2, y2 = int(x / setin.TILE), int(y / setin.TILE)
        x1, y1 = int(self.x / setin.TILE), int(self.y / setin.TILE)
        if not self.animation_count < self.animation_speed:
            self.an -= 1
            if self.att and self.an == 0:
                self.att = False
                if ((x2 == x1 and y2 == y1) or (x2 - 1 == x1 and y2 == y1) or (x2 + 1 == x1 and y2 == y1)
                    or (x2 == x1 and y2 - 1 == y1) or (x2 == x1 and y2 + 1 == y1)):
                    # print(1, 1, 1, 1, 1, 1, sep="\n")
                    # print()
                    self.att = False
                    self.player_hp.get_dam(setin.ENEMY_DAM)
        if self.an <= 0 and not self.att:
            self.att = False
            self.animation = self.noth_an
            if self.way:
                self.animation = self.walk_an
                dx = self.way[0][0] * setin.TILE - (self.x - self.side // 2)
                dy = self.way[0][1] * setin.TILE - (self.y - self.side // 2)
                # print(dx, dy, self.x, self.y, self.way)
                # print(dx, dy, dx / ((abs(dx) ** 2 + abs(dy) ** 2) * 0.5), dy / ((abs(dx) ** 2 + abs(dy) ** 2) * 0.5))
                if abs(dx) <= setin.SPEED and abs(dy) <= setin.SPEED:
                    #print("hhhh", self.way[1:])
                    self.x, self.y = self.way[0][0] * setin.TILE, self.way[0][1] * setin.TILE
                    self.way = self.way[1:]
                    dx = self.way[0][0] * setin.TILE - (self.x - self.side // 2)
                    dy = self.way[0][1] * setin.TILE - (self.y - self.side // 2)
                if abs(dx) >= setin.SPEED:
                    self.x += setin.SPEED * (dx // abs(dx))
                    #print("x", 10 * (dx // abs(dx)), self.x, self.y)
                if abs(dy) >= setin.SPEED:
                    self.y += setin.SPEED * (dy // abs(dy))
                    #print("y", 10 * (dy // abs(dy)), self.x, self.y)
                #print("ll", self.x, self.y)
                # self.x += dx / ((abs(dx) ** 2 + abs(dy) ** 2) * 0.5) * 200
                # self.y += dy / ((abs(dx) ** 2 + abs(dy) ** 2) * 0.5) * 200
                # # self.x = round(self.x + (self.way[0][0] - self.x / TILE) * TILE / 10, 2)
                # # self.y = round(self.y + (self.way[0][1] - self.y / TILE) * TILE / 10, 2)
                # print(self.x, self.y, self.way)
                # if (round(self.x / TILE, 2), round(self.y / TILE, 2)) == tuple(map(float, self.way[0])):
                #     self.way = self.way[1:]
            if self.go_death:
                self.death = True
        self.pos = (self.x - self.side // 2, self.y - self.side // 2)
        #print(self.pos, (x, y), self.way)
        if self.death:
            return (False,)
        return super().object_locate(x, y, angle)

    def move(self, pos):
        #print(pos, self.x, self.y, "#########################################")
        x2, y2 = int(pos[0] / setin.TILE), int(pos[1] / setin.TILE)
        x1, y1 = int(self.x / setin.TILE), int(self.y / setin.TILE)
        self.way = get_path(x1, y1, x2, y2, level.simple_map)
        if ((x2 == x1 and y2 == y1) or (x2 - 1 == x1 and y2 == y1) or (x2 + 1 == x1 and y2 == y1)
                or (x2 == x1 and y2 - 1 == y1) or (x2 == x1 and y2 + 1 == y1)) and not self.att and not self.go_death and not self.way and self.an <= 0:
            self.an = 5
            self.att = True
            self.animation = self.att_an.copy()
        # else:
        #     print("not")
        #print(x1, y1, "))))))))))")

        #print(self.way)


class Ball(SpriteObject):
    def __init__(self, x, y, scale, sh, side, angle):
        super().__init__({
                'sprite': pygame.image.load('sprites/ball/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': sh,
                'scale': scale,
                'animation': deque(
                    [pygame.image.load(f'sprites/ball/anim/{i}.png').convert_alpha() for i in range(4)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': False,
                'side': side,
                'anim_dir': -1
            }, (x, y))
        self.angle = angle
        self.rect = pygame.Rect(*self.pos, self.side, self.side)
        self.sp = 10
        self.death = False

    def move(self):
        if self.death:
            return
        next_rect = self.rect.copy()
        dx, dy = self.sp * math.cos(self.angle), self.sp * math.sin(self.angle)
        next_rect.move_ip(dx, dy)
        #print(next_rect)
        hit_indexes = next_rect.collidelistall(level.collision_list)
        if len(hit_indexes):
            #print(hit_indexes, blocked)
            for hit_index in hit_indexes:
                if hit_index > len(level.collision_walls) - 1:
                    if isinstance(level.blocked[hit_index - len(level.collision_walls)], Enemy):
                        level.blocked[hit_index - len(level.collision_walls)].attacked(setin.DAMAGE)
            self.death = True
        self.x += dx  # 0 1 2 3 4 5
        self.y += dy
        self.rect.center = self.x, self.y

    def object_locate(self, x, y, angle):
        if self.death:
            return (False, )
        return super().object_locate(x, y, angle)


def detect_collision(dx, dy, rect):
    next_rect = rect.copy()
    next_rect.move_ip(dx, dy)
    hit_indexes = next_rect.collidelistall(level.collision_list)
    if len(hit_indexes):
        # print(hit_indexes)
        delta_x, delta_y = 0, 0
        for hit_index in hit_indexes:
            hit_rect = level.collision_list[hit_index]
            if hit_index > len(level.collision_walls) - 1:
                if isinstance(level.blocked[hit_index - len(level.collision_walls)], Portal):
                    level.__init__([Win(5.5, 5.5, 1, -0.2, 100)], [], [], collision_walls_2, world_map_2, matrix_map_2, min_map_col, simpl_map_2)
                    flag[0] = True
                    return 0, 0
                elif isinstance(level.blocked[hit_index - len(level.collision_walls)], Win):
                    flag[1] = True
                    return 0, 0
            if dx > 0:
                delta_x += next_rect.right - hit_rect.left
            else:
                delta_x += hit_rect.right - next_rect.left
            if dy > 0:
                delta_y += next_rect.bottom - hit_rect.top
            else:
                delta_y += hit_rect.bottom - next_rect.top
        if abs(delta_x - delta_y) < 50:
            dx, dy = 0, 0
        elif delta_x > delta_y:
            dy = 0
        elif delta_y > delta_x:
            dx = 0
        # print(dx, dy, delta_x, delta_y)
    return dx, dy
    # self.x += dx
    # self.y += dy


def menu():
    pygame.mouse.set_visible(True)
    # text1 = font.render("Начать", True, (255, 255, 255))
    # text2 = font.render("Статистика", True, (255, 255, 255))
    # text3 = font.render("Выйти", True, (255, 255, 255))
    anim = deque([pygame.image.load(f'sprites/pedestal/anim/{i}.png').convert_alpha() for i in range(1, 7)])
    x, y = 100, 100
    rects_of_butt = [pygame.Rect(x, y + e * 100, 160, 40) for e in range(1, 4)]
    a = 0
    leave = False
    while True:
        if leave:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if click[0]:
            hit_indexes = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelistall(rects_of_butt)
            if hit_indexes:
                if hit_indexes[0] == 0:
                    pygame.mouse.set_pos(setin.HALF_WIDTH, setin.HALF_HEIGHT)
                    leave = True
                if hit_indexes[0] == 2:
                    exit()
                if hit_indexes[0] == 1:
                    history()
        a += 1
        if a > 4:
            anim.rotate(-1)
            a = 0
        sc.fill(setin.DARKGRAY)
        for e in range(1, 4):
            sc.blit(textures['butt' + str(e)], (x, y + 100 * e))

        sc.blit(pygame.transform.scale(anim[0], (66 * 4, 103 * 4)), (300, 200))
        sc.blit(pygame.transform.scale(anim[0], (66 * 4, 103 * 4)), (600, 200))
        sc.blit(pygame.transform.scale(anim[0], (66 * 4, 103 * 4)), (900, 200))
        if leave:
            sc.blit(textures['load'], (0, 0))
        pygame.display.flip()
        clock.tick(setin.FPS)
    pygame.mouse.set_visible(False)


def death():
    w = open("stats.txt", mode="r")
    text = w.read()
    text += "\n" + "/".join(list(map(str, count)) + ["смерть"])
    w = open("stats.txt", mode="w")
    w.write(text)
    count[:] = [0, 0]
    sc.blit(textures['death'], (0, 0))
    x = 0
    while x < setin.FPS * 5:
        x += 1
        pygame.display.flip()
        clock.tick(setin.FPS)

def win():
    w = open("stats.txt", mode="r")
    text = w.read()
    text += "\n" + "/".join(list(map(str, count)) + ["победа!"])
    w = open("stats.txt", mode="w")
    w.write(text)
    count[:] = [0, 0]
    sc.blit(textures['win'], (0, 0))
    x = 0
    while x < setin.FPS * 5:
        x += 1
        pygame.display.flip()
        clock.tick(setin.FPS)


def history():
    w = open("stats.txt", mode="r")
    text = w.readlines()
    print(text)
    da = [font.render(e.strip(), True, (255, 255, 255)) for e in text]
    rects_of_butt_1 = [pygame.Rect(100, 100, 160, 40)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        click = pygame.mouse.get_pressed()
        if click[0]:
            #print("kkk", click)
            hit_indexes = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelistall(rects_of_butt_1)
            #print(hit_indexes )
            if hit_indexes:
                #print("88")
                return
        sc.fill(setin.BLACK)
        sc.blit(textures['butt3'], (100, 100))
        for e in range(len(da)):
            sc.blit(da[e], (400, 100 + 75 * e))
        pygame.display.flip()
        clock.tick(setin.FPS)


class Now:
    def __init__(self, other_spr, enemies, balls, collision_walls, world_map, matrix_map, min_map_col, simple_map):
        self.other_spr = other_spr
        self.enemies = enemies
        self.balls = balls
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  other_spr + enemies + balls if obj.blocked]
        self.blocked = [e for e in other_spr + enemies + balls if e.blocked]
        self.collision_list = collision_walls + self.collision_sprites
        self.collision_walls = collision_walls
        self.world_map = world_map
        self.matrix_map = matrix_map
        self.min_map_col = min_map_col
        self.simple_map = simple_map

    def check_death(self):
        x = len(self.enemies)
        self.enemies = [e for e in self.enemies if not e.death]
        count[0] += x - len(self.enemies)
        x = len(self.balls)
        self.balls = [e for e in self.balls if not e.death]
        count[1] += x - len(self.balls)
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.other_spr + self.enemies + self.balls if obj.blocked]
        self.blocked = [e for e in self.other_spr + self.enemies + self.balls if e.blocked]
        self.collision_list = self.collision_walls + self.collision_sprites

    def all_spr(self):
        return self.other_spr + self.enemies + self.balls

    def update(self):
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.other_spr + self.enemies + self.balls if obj.blocked]
        self.collision_list = self.collision_walls + self.collision_sprites


class HP:
    def __init__(self):
        self.hp = 100

    def get_dam(self, dam):
        self.hp -= dam

    def check_death(self):
        return self.hp <= 0

setin = Settings()
hp = HP()

pygame.init()
sc = pygame.display.set_mode((setin.WIDTH, setin.HEIGHT))

pygame.mouse.set_visible(False)

barrels = [
    # Barrel(7.1, 2.1, 0.4, 1.8, 40),
    # Barrel(5.9, 2.1, 0.4, 1.8, 40),
    # Barrel(1.2, 1.2, 0.6, 1, 60),
]
enemies_args = [(6.5, 2.1, 1.2, -0.1, 60), (7.5, 5.5, 1.2, -0.1, 60), (2.5, 11.5, 1.2, -0.1, 60),
                (11.5, 10.5, 1.2, -0.1, 60), (21.5, 2.5, 1.2, -0.1, 60), (10.5, 5.5, 1.2, -0.1, 60),
                (15.5, 5.5, 1.2, -0.1, 60), (22.5, 9.5, 1.2, -0.1, 60), (16.5, 11.5, 1.2, -0.1, 60)]
enemies = [Enemy(*e, hp) for e in enemies_args]

balls = []

other_spr = [Portal(22.5, 1.5, 1, -0.2, 100)]

# sprites = Sprites()
clock = pygame.time.Clock()
x, y = setin.player_pos
# print(x, y)

rect = pygame.Rect(*setin.player_pos, setin.SIDE, setin.SIDE)
# collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
#                                   all_spr if obj.blocked]
# blocked = [e for e in all_spr if e.blocked]
# collision_list = collision_walls + collision_sprites
min_map_col = {2: setin.BLACK, False: setin.WHITE, 1: setin.BLACK}
level = Now(other_spr, enemies, balls, collision_walls, world_map, matrix_map, min_map_col, simpl_map)
#player = Player(sprites)
#drawing = Drawing(sc, sc_map)
# print(get_path(2, 1, 5, 2, level.simple_map))
flag = [False, False]
textures = {1: pygame.image.load('img/wall_2_1.png').convert(),
            2: pygame.image.load('img/wall_2_2.png').convert(),
            #3: pygame.image.load('img/wall5.png').convert(),
            #4: pygame.image.load('img/wall6.png').convert(),
            'S': pygame.image.load('img/sky2.png').convert(),
            'butt1': pygame.image.load('img/butt1.png').convert(),
            'butt2': pygame.image.load('img/butt2.png').convert(),
            'butt3': pygame.image.load('img/butt3.png').convert(),
            'load': pygame.image.load('img/load.png').convert(),
            'death': pygame.image.load('img/death.png').convert(),
            'win': pygame.image.load('img/win.png').convert(),
            }

font = pygame.font.SysFont('arial', 50)

count = [0, 0]

attack_loc = 60
max_attacl_loc = attack_loc
attack_loc -= 1

menu()

while True:
    level.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sin_a = math.sin(setin.player_angle)
    cos_a = math.cos(setin.player_angle)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_ESCAPE]:
        menu()
        attack_loc = max_attacl_loc - 1
    if keys[pygame.K_w]:
        dx = setin.player_speed * cos_a
        dy = setin.player_speed * sin_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_s]:
        dx = -setin.player_speed * cos_a
        dy = -setin.player_speed * sin_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_a]:
        dx = setin.player_speed * sin_a
        dy = -setin.player_speed * cos_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_d]:
        dx = -setin.player_speed * sin_a
        dy = setin.player_speed * cos_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_LEFT]:
        setin.player_angle -= 0.02
    if keys[pygame.K_RIGHT]:
        setin.player_angle += 0.02
    if pygame.mouse.get_focused():
        difference = pygame.mouse.get_pos()[0] - setin.HALF_WIDTH
        pygame.mouse.set_pos((setin.HALF_WIDTH, setin.HALF_HEIGHT))
        setin.player_angle += difference * setin.SENS
    if flag[0]:
        flag[0] = False
        x, y = 1.5 * setin.TILE, 1.5 * setin.TILE

    click = pygame.mouse.get_pressed()
    if click[0] and attack_loc == max_attacl_loc:
        level.balls.append(Ball(x / setin.TILE, y / setin.TILE, 0.7, 0, 30, setin.player_angle))
        # for e in enemies:
        #     e.attacked(10)
        attack_loc -= 1
    if attack_loc < max_attacl_loc:
        attack_loc -= 1
        if attack_loc < 0:
            attack_loc = max_attacl_loc
    rect.center = x, y
    setin.player_angle %= setin.DOUBLE_PI

    level.check_death()

    # player.movement()wwwwwwwwwwwwwwwww
    sc.fill(setin.BLACK)

    sky_offset = -10 * math.degrees(setin.player_angle) % setin.WIDTH
    sc.blit(textures['S'], (sky_offset, 0))
    sc.blit(textures['S'], (sky_offset - setin.WIDTH, 0))
    sc.blit(textures['S'], (sky_offset + setin.WIDTH, 0))
    pygame.draw.rect(sc, setin.DARKGRAY, (0, setin.HALF_HEIGHT, setin.WIDTH, setin.HALF_HEIGHT))
    # drawing.background(player.angle)
    walls = ray_casting_walls((x, y), setin.player_angle, textures, level.world_map)
    located = [obj.object_locate(x, y, setin.player_angle) for obj in level.all_spr()]
    #print(walls)
    for obj in sorted(walls + located, key=lambda n: n[0], reverse=True):
        if obj[0]:
            _, object, object_pos = obj
            sc.blit(object, object_pos)
    # drawing.world(walls + [obj.object_locate(x, y, player_angle) for obj in all_spr])
    # drawing.fps(clock)
    # drawing.mini_map(player)
    for e in range(len(level.matrix_map[0])):
        for j in range(len(level.matrix_map)):
            pygame.draw.rect(sc, level.min_map_col[level.matrix_map[j][e]], (setin.WIDTH - 10 * len(level.matrix_map[0]) + 10 * e,
                                                                 10 * j, 10, 10), 0)
            #pygame.draw.re
    pygame.draw.rect(sc, setin.GRAY, (setin.WIDTH + int(x / setin.TILE) * 10 - 10 * len(level.matrix_map[0]), int(y / setin.TILE) * 10, 10, 10), 0)
    pygame.draw.rect(sc, setin.BLACK, (10, setin.HEIGHT - 60, 305, 45), 5)
    pygame.draw.rect(sc, setin.RED, (15, setin.HEIGHT - 55, hp.hp * 3 - 5, 35), 0)
    #print(hp.hp)
    for e in level.balls:
        e.move()
    for e in level.enemies:
        e.move((x, y))
    if hp.check_death():
        death()
        setin.__init__()
        enemies = [Enemy(*e, hp) for e in enemies_args]
        hp = HP()
        x, y = setin.player_pos
        rect = pygame.Rect(*setin.player_pos, setin.SIDE, setin.SIDE)
        level.__init__(other_spr, enemies, balls, collision_walls, world_map, matrix_map, min_map_col, simpl_map)
        attack_loc = 60
        max_attacl_loc = attack_loc
        attack_loc -= 1
        menu()
    if flag[1]:
        flag[1] = False
        win()
        setin.__init__()
        enemies = [Enemy(*e, hp) for e in enemies_args]
        hp = HP()
        x, y = setin.player_pos
        rect = pygame.Rect(*setin.player_pos, setin.SIDE, setin.SIDE)
        level.__init__(other_spr, enemies, balls, collision_walls, world_map, matrix_map, min_map_col, simpl_map)
        attack_loc = 60
        max_attacl_loc = attack_loc
        attack_loc -= 1
        menu()

    # all_spr = [e for e in all_spr if not e.death]
    # balls = [e for e in balls if not e.death]
    # #print(all_spr)
    # walls_rect = [e[1].get_rect().move(*e[2]) for e in walls]
    # for e in range(len(all_spr)):
    #     if isinstance(all_spr[e], Enemy):
    #         if located[e][0]:
    #             print(located[e][1].get_rect().move(*located[e][2]), walls_rect)
    #             if len(located[e][1].get_rect().move(*located[e][2]).collidelistall(walls_rect)) == 0 and 0 <= :
    #                 all_spr[e].move(player_pos)
    #print((int(x / TILE) * 10, int(y / TILE) * 10, 10, 10))
    #print(WIDTH + int(x / TILE) * 10 - 10 * len(matrix_map[0]), int(y / TILE) * 10)
    pygame.display.flip()
    clock.tick(setin.FPS)

