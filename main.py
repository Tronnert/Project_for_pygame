import pygame
from collections import deque
from settings import *
#from player import Player
from sprite import SpriteObject
from rays import ray_casting_walls
from level1 import collision_walls, world_map, matrix_map
#from drawing import Drawing


class Barrel(SpriteObject):
    def __init__(self, x, y, scale, sh, side):
        super().__init__({
                'sprite': pygame.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': sh,
                'scale': scale,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'side': side,
                'anim_dir': 1
            }, (x, y))


class Enemy(SpriteObject):
    def __init__(self, x, y, scale, sh, side):
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
        self.noth_an = deque([pygame.image.load(f'sprites/enemy/noth/{i}.png').convert_alpha() for i in range(1, 5)])
        self.att_an = deque([pygame.image.load(f'sprites/enemy/attack/{i}.png').convert_alpha() for i in range(1, 6)])
        self.dam_an = deque([pygame.image.load(f'sprites/enemy/damaged/{i}.png').convert_alpha() for i in range(1, 3)])
        self.death_an = deque([pygame.image.load(f'sprites/enemy/death/{i}.png').convert_alpha() for i in range(1, 6)])
        self.walk_an = deque([pygame.image.load(f'sprites/enemy/walk/{i}.png').convert_alpha() for i in range(1, 6)])
        self.hp = 100
        self.dam = 10
        self.go_death = False
        self.death = False
        self.an = 0
        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)

    def attacked(self, dam):
        if not self.go_death:
            self.hp -= dam
            if self.hp <= 0:
                self.animation = self.death_an
                self.go_death = True
                self.an = 5
            else:
                self.animation = self.dam_an.copy()
                self.an = 2

    def object_locate(self, x, y, angle):
        if not self.animation_count < self.animation_speed:
            self.an -= 1
        if self.an == 0:
            self.animation = self.noth_an
            if self.go_death:
                self.death = True
        if self.death:
            return (False,)
        return super().object_locate(x, y, angle)

    def move(self, pos):
        print(pos)


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
        hit_indexes = next_rect.collidelistall(collision_list)
        if len(hit_indexes):
            #print(hit_indexes, blocked)
            for hit_index in hit_indexes:
                if hit_index > len(collision_walls) - 1:
                    if isinstance(blocked[hit_index - len(collision_walls)], Enemy):
                        blocked[hit_index - len(collision_walls)].attacked(DAMAGE)
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
    hit_indexes = next_rect.collidelistall(collision_list)
    if len(hit_indexes):
        # print(hit_indexes)
        delta_x, delta_y = 0, 0
        for hit_index in hit_indexes:
            hit_rect = collision_list[hit_index]
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if click[0]:
            hit_indexes = pygame.Rect(*pygame.mouse.get_pos(), 1, 1).collidelistall(rects_of_butt)
            if hit_indexes:
                if hit_indexes[0] == 0:
                    pygame.mouse.set_pos(HALF_WIDTH, HALF_WIDTH)
                    break
                if hit_indexes[0] == 2:
                    exit()
        a += 1
        if a > 4:
            anim.rotate(-1)
            a = 0
        sc.fill(DARKGRAY)
        for e in range(1, 4):
            sc.blit(textures['butt' + str(e)], (x, y + 100 * e))

        sc.blit(pygame.transform.scale(anim[0], (66 * 4, 103 * 4)), (300, 200))
        sc.blit(pygame.transform.scale(anim[0], (66 * 4, 103 * 4)), (600, 200))
        sc.blit(pygame.transform.scale(anim[0], (66 * 4, 103 * 4)), (900, 200))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.mouse.set_visible(False)


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

barrels = [
    # Barrel(7.1, 2.1, 0.4, 1.8, 40),
    # Barrel(5.9, 2.1, 0.4, 1.8, 40),
    # Barrel(1.2, 1.2, 0.6, 1, 60),
]
enemies = [Enemy(6.5, 2.1, 1.2, -0.1, 60)]

balls = []

all_spr = barrels + enemies

# sprites = Sprites()
clock = pygame.time.Clock()
x, y = player_pos
# print(x, y)

rect = pygame.Rect(*player_pos, SIDE, SIDE)
collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  all_spr if obj.blocked]
blocked = [e for e in all_spr if e.blocked]
collision_list = collision_walls + collision_sprites

#player = Player(sprites)
#drawing = Drawing(sc, sc_map)

textures = {1: pygame.image.load('img/wall3.png').convert(),
            2: pygame.image.load('img/wall_2_2.png').convert(),
            #3: pygame.image.load('img/wall5.png').convert(),
            #4: pygame.image.load('img/wall6.png').convert(),
            'S': pygame.image.load('img/sky2.png').convert(),
            'butt1': pygame.image.load('img/butt1.png').convert(),
            'butt2': pygame.image.load('img/butt2.png').convert(),
            'butt3': pygame.image.load('img/butt3.png').convert(),
            }

font = pygame.font.SysFont('arial', 50)

min_map_col = {2: BLACK, False: WHITE}

attack_loc = 60
max_attacl_loc = attack_loc
attack_loc -= 1

menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_ESCAPE]:
        menu()
        attack_loc = max_attacl_loc - 1
    if keys[pygame.K_w]:
        dx = player_speed * cos_a
        dy = player_speed * sin_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_s]:
        dx = -player_speed * cos_a
        dy = -player_speed * sin_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_a]:
        dx = player_speed * sin_a
        dy = -player_speed * cos_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_d]:
        dx = -player_speed * sin_a
        dy = player_speed * cos_a
        dx, dy = detect_collision(dx, dy, rect)
        x += dx
        y += dy
    if keys[pygame.K_LEFT]:
        player_angle -= 0.02
    if keys[pygame.K_RIGHT]:
        player_angle += 0.02
    if pygame.mouse.get_focused():
        difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
        pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
        player_angle += difference * SENS
    click = pygame.mouse.get_pressed()
    if click[0] and attack_loc == max_attacl_loc:
        balls.append(Ball(x / TILE, y / TILE, 0.7, 0, 30, player_angle))
        # for e in enemies:
        #     e.attacked(10)
        attack_loc -= 1
    if attack_loc < max_attacl_loc:
        attack_loc -= 1
        if attack_loc < 0:
            attack_loc = max_attacl_loc
    rect.center = x, y
    player_angle %= DOUBLE_PI
    #player.movement()wwwwwwwwwwwwwwwww
    sc.fill(BLACK)

    sky_offset = -10 * math.degrees(player_angle) % WIDTH
    sc.blit(textures['S'], (sky_offset, 0))
    sc.blit(textures['S'], (sky_offset - WIDTH, 0))
    sc.blit(textures['S'], (sky_offset + WIDTH, 0))
    pygame.draw.rect(sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
    # drawing.background(player.angle)
    walls = ray_casting_walls((x, y), player_angle, textures, world_map)
    located = [obj.object_locate(x, y, player_angle) for obj in all_spr + balls]
    #print(walls)
    for obj in sorted(walls + located, key=lambda n: n[0], reverse=True):
        if obj[0]:
            _, object, object_pos = obj
            sc.blit(object, object_pos)
    # drawing.world(walls + [obj.object_locate(x, y, player_angle) for obj in all_spr])
    # drawing.fps(clock)
    # drawing.mini_map(player)
    for e in range(len(matrix_map[0])):
        for j in range(len(matrix_map)):
            pygame.draw.rect(sc, min_map_col[matrix_map[j][e]], (WIDTH - 10 * len(matrix_map[0]) + 10 * e,
                                                                 10 * j, 10, 10), 0)
            #pygame.draw.re
    pygame.draw.rect(sc, GRAY, (WIDTH + int(x / TILE) * 10 - 10 * len(matrix_map[0]), int(y / TILE) * 10, 10, 10), 0)
    for e in balls:
        e.move()
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
    clock.tick(FPS)