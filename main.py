import pygame
from collections import deque
from settings import *
#from player import Player
from sprite import SpriteObject
from rays import ray_casting_walls
from level1 import collision_walls, world_map
#from drawing import Drawing


class Barrel(SpriteObject):
    def __init__(self, x, y):
        super().__init__({
                'sprite': pygame.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            }, (x, y))


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

        if abs(delta_x - delta_y) < 20:
            dx, dy = 0, 0
        elif delta_x > delta_y:
            dy = 0
        elif delta_y > delta_x:
            dx = 0
        # print(dx, dy, delta_x, delta_y)
    return dx, dy
    # self.x += dx
    # self.y += dy


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

all_spr = [
    Barrel(7.1, 2.1),
    Barrel(5.9, 2.1)
]

#sprites = Sprites()
clock = pygame.time.Clock()
x, y = player_pos

rect = pygame.Rect(*player_pos, SIDE, SIDE)
collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  all_spr if obj.blocked]
collision_list = collision_walls + collision_sprites

#player = Player(sprites)
#drawing = Drawing(sc, sc_map)

textures = {#1: pygame.image.load('img/wall3.png').convert(),
            2: pygame.image.load('img/wall4.png').convert(),
            #3: pygame.image.load('img/wall5.png').convert(),
            #4: pygame.image.load('img/wall6.png').convert(),
            'S': pygame.image.load('img/sky2.png').convert()
            }

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_ESCAPE]:
        exit()
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
    rect.center = x, y
    player_angle %= DOUBLE_PI
    #player.movement()
    sc.fill(BLACK)

    sky_offset = -10 * math.degrees(player_angle) % WIDTH
    sc.blit(textures['S'], (sky_offset, 0))
    sc.blit(textures['S'], (sky_offset - WIDTH, 0))
    sc.blit(textures['S'], (sky_offset + WIDTH, 0))
    pygame.draw.rect(sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
    # drawing.background(player.angle)
    walls = ray_casting_walls((x, y), player_angle, textures, world_map)
    for obj in sorted(walls + [obj.object_locate(x, y, player_angle) for obj in all_spr], key=lambda n: n[0], reverse=True):
        if obj[0]:
            _, object, object_pos = obj
            sc.blit(object, object_pos)
    # drawing.world(walls + [obj.object_locate(x, y, player_angle) for obj in all_spr])
    # drawing.fps(clock)
    # drawing.mini_map(player)

    pygame.display.flip()
    clock.tick(FPS)