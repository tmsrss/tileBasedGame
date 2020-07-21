import pygame as pg
vec = pg.math.Vector2
import random


# colours       https://www.rapidtables.com/web/color/RGB_Color.html
BROWN = (106, 55, 5)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


# window settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
# WIDTH = 2560
# HEIGHT = 1080
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY


# map settings
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
MAP_NAME = "level1.tmx"


# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250  # degrees per second
PLAYER_FOLDER = "Man Blue" #indicates the folder within the img folder, set to False if it is not within a folder
PLAYER_IMG = "manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 40)


# MObs
MOB_FOLDER = "Hitman 1"
MOB_IMAGE = "hitman1_gun.png"
MOB_SPEEDS = [75, 100, 125, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400


# Wall
WALL_FOLDER = "Tiles"
WALL_IMG = "tile_180.png"


# Gun
BULLET_IMG = "bullet.png"
WEAPONS = {}
WEAPONS["pistol"] = {"speed":500,
                     "lifetime":1000,
                     "rate":150,
                     "kickback":200,
                     "spread":5,
                     "damage":10,
                     "size": "lg",
                     "count": 1}
WEAPONS["shotgun"] = {"speed":400,
                       "lifetime":500,
                       "rate":900,
                       "kickback":300,
                       "spread":20,
                       "damage":10,
                       "size": "sm",
                       "count": 12}
WEAPON_SOUNDS = {"pistol":["pistol.wav"],
                 "shotgun":["shotgun.wav"]}
BARREL_OFFSET = vec(30, 10)
SMOKE = ['whitePuff15.png', 'whitePuff16.png',
         'whitePuff17.png', 'whitePuff18.png']
SMOKE_FOLDER = "Smoke"
SMOKE_DURATION = 40
DEFAULT_AMMO = 50
AMMO_RELOAD = 200


# Powerups
POWERUPS_FOLDER = "Powerups"
POWERUPS_IMAGES = {"health":"health_pack.png",
                   "shotgun":"obj_shotgun.png",
                   'ammo':'ammo_pack.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 10
BOB_SPEED = 0.5


# Effects
DAMAGE_ALPHA = [i for i in range(0, 255, 25)]
NIGHT_COLOR = (50, 50, 50)
LIGHT_RADIUS = (1200, 1200)
LIGHT_MASK = "light_350_soft.png"


# Sounds/Musics
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['pistol.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}


# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
POWERUPS_LAYER = 1

