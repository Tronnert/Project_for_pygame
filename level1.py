from settings import TILE
from sprite import SpriteObject
from collections import deque 
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32


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
                'side': side
            }, (x, y))
        
    

_ = False
matrix_map = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, _, _, _, _, _, _, _, _, 2, _, _, 2, 2, _, _, _, _, _, _, _, _, _, 2],
    [2, _, _, _, _, _, _, _, _, 2, _, _, _, _, 2, _, _, _, _, _, 2, _, _, 2],
    [2, _, 2, 2, _, _, 2, _, _, 2, 2, _, _, _, _, 2, 2, 2, 2, _, 2, _, 2, 2],
    [2, _, _, _, _, _, 2, _, _, 2, _, _, 2, _, _, _, _, _, _, 2, _, _, _, 2],
    [2, _, _, _, 2, 2, 2, _, _, 2, _, _, 2, _, _, _, _, _, _, _, _, _, 2, 2],
    [2, _, _, _, 2, 2, _, _, 2, _, _, _, _, 2, _, 2, 2, _, _, _, 2, _, _, 2],
    [2, 2, 2, 2, 2, _, _, 2, _, _, 2, _, _, _, 2, _, _, 2, _, 2, 2, _, _, 2],
    [2, _, _, 2, _, _, _, 2, _, _, 2, _, _, 2, _, 2, _, _, _, 2, 2, 2, _, 2],
    [2, _, _, _, _, _, _, 2, 2, 2, _, _, 2, _, _, _, _, _, 2, _, 2, _, _, 2],
    [2, 2, _, _, 2, 2, 2, _, _, _, _, _, 2, _, _, _, 2, 2, _, _, 2, _, _, 2],
    [2, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, 2, _, _, 2, 2, _, _, _, 2],
    [2, _, 2, _, _, _, _, _, 2, 2, _, _, _, _, 2, _, _, _, _, 2, _, _, 2, 2],
    [2, _, _, 2, _, 2, 2, 2, _, _, _, 2, _, _, _, _, 2, 2, _, _, _, 2, _, 2],
    [2, _, _, _, 2, _, _, _, _, _, _, 2, 2, _, _, 2, _, _, 2, _, 2, _, _, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)

collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            world_map[(i * TILE, j * TILE)] = char
