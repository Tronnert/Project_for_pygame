from settings import TILE
from sprite import SpriteObject
from collections import deque
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32
    

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

# for e in range(len(matrix_map)):
#     for j in range(len(matrix_map[0])):
#         if matrix_map[e][j] == 1:
#             print(e, j)


WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)

collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            world_map[(i * TILE, j * TILE)] = char

simpl_map = [[0 if not matrix_map[j][e] else -1 for e in range(len(matrix_map[0]))] for j in range(len(matrix_map))]
