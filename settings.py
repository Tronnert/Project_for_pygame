import math

class Settings:
    def __init__(self):


        # game settings
        self.WIDTH = 1200
        self.HEIGHT = 600
        self.HALF_WIDTH = self.WIDTH // 2
        self.HALF_HEIGHT = self.HEIGHT // 2
        self.PENTA_HEIGHT = 5 * self.HEIGHT
        self.DOUBLE_HEIGHT = 2 * self.HEIGHT
        self.FPS = 30
        self.TILE = 100
        self.FPS_POS = (self.WIDTH - 65, 5)

        # ray casting settings
        self.FOV = math.pi / 3
        self.HALF_FOV = self.FOV / 2
        self.NUM_RAYS = 300
        self.MAX_DEPTH = 800
        self.DELTA_ANGLE = self.FOV / self.NUM_RAYS
        self.DIST = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV))
        self.PROJ_COEFF = 3 * self.DIST * self.TILE
        self.SCALE = self.WIDTH // self.NUM_RAYS

        # sprite settings
        self.DOUBLE_PI = math.pi * 2
        self.CENTER_RAY = self.NUM_RAYS // 2 - 1
        self.FAKE_RAYS = 100
        self.FAKE_RAYS_RANGE = self.NUM_RAYS - 1 + 2 * self.FAKE_RAYS

        # Grahics
        self.GRAPHICS = 1

        # texture settings (1200 x 1200)
        self.TEXTURE_WIDTH = 1200
        self.TEXTURE_HEIGHT = 1200
        self.TEXTURE_SCALE = self.TEXTURE_WIDTH // self.TILE // self.GRAPHICS

        # player settings
        self.player_pos = (2.5 * self.TILE, 1.5 * self.TILE)
        # print(player_pos, HALF_WIDTH, HALF_HEIGHT)
        self.player_angle = 0
        self.player_speed = 2.5
        self.SENS = 0.004
        self.SIDE = 50

        self.DAMAGE = 50

        # Enemy settings
        self.DETECT_RAD = 5
        self.SPEED = 4
        self.ENEMY_DAM = 10

        # colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (220, 0, 0)
        self.GREEN = (0, 80, 0)
        self.BLUE = (0, 0, 255)
        self.DARKGRAY = (40, 40, 40)
        self.PURPLE = (120, 0, 120)
        self.SKYBLUE = (0, 186, 255)
        self.YELLOW = (220, 220, 0)
        self.SANDY = (244, 164, 96)
        self.DARKBROWN = (97, 61, 25)
        self.DARKORANGE = (255, 140, 0)

WIDTH = 1200
HEIGHT = 600
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = 2 * HEIGHT
FPS = 30
TILE = 100
FPS_POS = (WIDTH - 65, 5)


# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# sprite settings
DOUBLE_PI = math.pi * 2
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS

#Grahics
GRAPHICS = 1

# texture settings (1200 x 1200)
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE // GRAPHICS

# player settings
player_pos = (2.5 * TILE, 1.5 * TILE)
#print(player_pos, HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 2.5
SENS = 0.004
SIDE = 50

DAMAGE = 50


# Enemy settings
DETECT_RAD = 5
SPEED = 4
ENEMY_DAM = 10

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)
DARKBROWN = (97, 61, 25)
DARKORANGE = (255, 140, 0)
