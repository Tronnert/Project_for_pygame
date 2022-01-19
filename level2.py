from settings import TILE
from sprite import SpriteObject
from collections import deque
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

_ = False
matrix_map_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# for e in range(len(matrix_map)):
#     for j in range(len(matrix_map[0])):
#         if matrix_map[e][j] == 1:
#             print(e, j)

WORLD_WIDTH_2 = len(matrix_map_2[0]) * TILE
WORLD_HEIGHT_2 = len(matrix_map_2) * TILE
world_map_2 = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)

collision_walls_2 = []
for j, row in enumerate(matrix_map_2):
    for i, char in enumerate(row):
        if char:
            collision_walls_2.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            world_map_2[(i * TILE, j * TILE)] = char

simpl_map_2 = [[0 if not matrix_map_2[j][e] else -1 for e in range(len(matrix_map_2[0]))] for j in range(len(matrix_map_2))]