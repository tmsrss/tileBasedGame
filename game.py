import pygame as pg
import random
import sys
from os import path
from settings import *
from sprites import *
from map import *
import pytmx
import pygame_menu as pgm
from random import uniform, choice, randint




def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        # initialise pygame and create window
        pg.mixer.pre_init(44100, -16, 1, 2048)  # used to prevent sound play lag by increasing buffer size
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Mi juego")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        self.paused = False
        self.wave = 0

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        img_folder = path.join(path.dirname(__file__), "img")
        self.map_folder = path.join(path.dirname(__file__), "maps")

        # load font
        self.title_font = path.join(img_folder, "ZOMBIE.TTF")
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')

        # dim screen image
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        #player
        if PLAYER_FOLDER is not False:
            player_folder = path.join(img_folder, PLAYER_FOLDER)
        else:
            player_folder = img_folder
        self.player_img = pg.image.load(path.join(player_folder, PLAYER_IMG))

        #mob
        if MOB_FOLDER is not False:
            mob_folder = path.join(img_folder, MOB_FOLDER)
        else:
            mob_folder = img_folder
        self.mob_img = pg.image.load(path.join(mob_folder, MOB_IMAGE))

        #boss
        if BOSS_FOLDER is not False:
            boss_folder = path.join(img_folder, BOSS_FOLDER)
        else:
            boss_folder = img_folder
        self.boss_img = pg.image.load(path.join(boss_folder, BOSS_IMAGE))

        #wall
        if WALL_FOLDER is not False:
            wall_folder = path.join(img_folder, WALL_FOLDER)
        else:
            wall_folder = img_folder
        self.wall_img = pg.image.load(path.join(wall_folder, WALL_IMG))
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

        # bullet and smoke
        self.bullet_images = {}
        self.bullet_images["lg"] = pg.image.load(path.join(img_folder, BULLET_IMG))
        self.bullet_images["sm"] = pg.transform.scale(self.bullet_images["lg"], (10, 10))
        if SMOKE_FOLDER is not False:
            smoke_folder = path.join(img_folder, SMOKE_FOLDER)
        else:
            smoke_folder = img_folder
        self.gun_flashes = []
        for img in SMOKE:
            self.gun_flashes.append(pg.image.load(path.join(smoke_folder, img)).convert_alpha())

        # Powerups
        if POWERUPS_FOLDER is not False:
            powerups_folder = path.join(img_folder, POWERUPS_FOLDER)
        else:
            powerups_folder = img_folder
        self.powerups_images = {}
        for powerup in POWERUPS_IMAGES:
            self.powerups_images[powerup] = pg.image.load(path.join(powerups_folder, POWERUPS_IMAGES[powerup])).convert_alpha()

        # lighting/night/fog effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        # Death splat
        self.splat = pg.image.load(path.join(img_folder, "splat red.png")).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))

        # Sounds
        snd_folder = path.join(path.dirname(__file__), "snd")
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.game_over_voice = pg.mixer.Sound(path.join(snd_folder, 'game over voice.wav'))

        # Musics
        music_folder = path.join(path.dirname(__file__), "music")
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))

        #  could add zombie moan part 18 15min 10secs

    def new(self):
        # start a new game
        self.hitman_spawn_locations = []
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        # load map
        # self.map = Map(path.join(map_folder, MAP_NAME))  # only needed for txt maps
        self.map = TileMap(path.join(self.map_folder, MAP_NAME))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self, col, row)
        #         elif tile == "P":
        #             self.player = Player(self, col, row)
        #         elif tile == "M":
        #             Mob(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2)
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            elif tile_object.name == "hitman":
                #print("dio can")
                #Mob(self, obj_center.x, obj_center.y)
                self.hitman_spawn_locations.append(pg.Rect(obj_center.x, obj_center.y, 49, 43))
            elif tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            elif tile_object.name == "powerup" :
                choice = random.choice(["health", "shotgun", 'ammo', 'smg'])
                Powerup(self, obj_center, choice)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.effects_sounds["level_start"].play()
        self.paused = False
        self.night = False
        self.countdown_timer = 0
        self.flag = False

    def run(self):
        # game loop
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def new_wave(self):
        used_locations = []
        x = self.wave
        num_hitmen = 20*x
        usable_locations = self.hitman_spawn_locations
        # spawn new hitmen
        camera_rect = self.camera.get_rect()
        unusable_locations = camera_rect.collidelistall(usable_locations)  # returns a list of indexes
        #print(usable_locations)
        for index in sorted(unusable_locations, reverse=True):
            del usable_locations[index]
        #print(usable_locations)
        for y in range(num_hitmen):
            #flag = False
            location = choice(usable_locations)
            location_center_x = location.centerx
            location_center_y = location.centery
            location = [location_center_x, location_center_y]
            if location not in used_locations:
                used_locations.append(location)
                Mob(self, location_center_x, location_center_y)
            else:
                location_center_x = location_center_x+random.randint(40,80)
                location_center_y = location_center_y+random.randint(40,80)
                location = [location_center_x, location_center_y]
                Mob(self, location_center_x, location_center_y)
        Boss(self, 1200, 1200)
        print(self.player.hit_rect.centerx)
        print(self.player.hit_rect.centery)

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.camera.update(self.player)
        # new wave
        if len(self.mobs) == 0:
            if self.flag == False:
                self.countdown_timer = 0
                self.flag = True
            self.countdown_timer -= self.dt
            if self.countdown_timer <= 0:
                self.wave += 1
                self.flag = False
                self.new_wave()

        # player picks up items
        picks = pg.sprite.spritecollide(self.player, self.powerups, False)
        for pick in picks:
            if pick.type == "health" and self.player.health < PLAYER_HEALTH:
                self.effects_sounds["health_up"].play()
                pick.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if pick.type == "shotgun":
                self.effects_sounds['gun_pickup'].play()
                pick.kill()
                if "shotgun" not in self.player.backpack:
                    self.player.backpack.append('shotgun')
            if pick.type == "smg":
                self.effects_sounds['gun_pickup'].play()
                pick.kill()
                if "smg" not in self.player.backpack:
                    self.player.backpack.append('smg')

                # add the shotgun to the self.player.weaponlist
            if pick.type == 'ammo':
                # ammo sound effect
                pick.kill()
                self.player.ammo += AMMO_RELOAD
                pass

        # mob hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random.random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullet hit mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)  #groupcollide returns a dictionary with the number of hits
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]["damage"] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def events(self):
        # game loop events, process input
        for event in pg.event.get():
            if event.type == pg.QUIT:  # check for closing window
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night

    def draw_grid(self):
        pass
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask onto the fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        # game loop draw/render
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))  # used for tmx map
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
                #print(sprite.pos)
                #print(self.mobs)
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug == True:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug == True:
            for wall in self.walls:
                pg.draw.rect(self.screen, MAGENTA, self.camera.apply_rect(wall.rect), 1)
        if self.night == True:
            self.render_fog()

        #pg.draw.rect(self.screen, RED, self.camera.get_rect(), 20)
        #HUD below
        # self.draw_grid()
        draw_player_health(self.screen, 10, 10, self.player.health/PLAYER_HEALTH)
        self.draw_text("Hitmen: {}".format(len(self.mobs)), self.hud_font, 30,
                       WHITE, WIDTH-10, 10, align='ne')
        self.draw_text('AMMO: {}'.format(self.player.ammo), self.hud_font, 25,
                       WHITE, WIDTH/1.1, HEIGHT-40, align='center')
        # -----------------------------------------------------------------------------
        # Draw weapon selection
        # -----------------------------------------------------------------------------
        num_weapons = len(self.player.backpack)
        box_width = num_weapons * 80
        box_start = (WIDTH/2)-(box_width/2)
        for i in range(num_weapons):
            image = self.powerups_images[self.player.backpack[i]]
            locx = box_start+(80*i)
            locy = HEIGHT-40
            self.screen.blit(image, (locx, locy))
            if self.player.backpack[i] == self.player.weapon:
                rect = image.get_rect()
                rect = pg.Rect.move(rect, locx, locy)
                pg.draw.rect(self.screen, MAGENTA, rect, 1)
        # -----------------------------------------------------------------------------
        #   Pause writing
        # -----------------------------------------------------------------------------
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH/2, HEIGHT/2, align="center")
        # -----------------------------------------------------------------------------
        #   Next wave countdown
        # -----------------------------------------------------------------------------
        if self.flag:
            self.draw_text("New wave in: {}".format(int(self.countdown_timer)), self.hud_font, 100, RED, WIDTH / 2,
                           HEIGHT / 8, align="center")

        # flip after drawing everything
        pg.display.flip()

    def show_start_screen(self):
        # start screen
        '''
        self.screen.fill(BLACK)
        self.draw_text("You have discovered great government secrets.",
                       self.hud_font, 20, WHITE, WIDTH/2, HEIGHT/8, align="center")
        self.draw_text("The CIA, FBI, KGB, and INTERPOL are sending waves of hitmen to murder you.",
                       self.hud_font, 20, WHITE, WIDTH/2, HEIGHT/8*2, align="center")
        self.draw_text("Protect yourself and survive as many waves as possible.",
                       self.hud_font, 20, WHITE, WIDTH/2, HEIGHT/8*3, align="center")
        self.draw_text("This is WAR!!!",
                       self.hud_font, 40, WHITE, WIDTH/2, HEIGHT/8*4, align="center")
        pg.display.flip()
        self.wait_key()
        '''
        self.login_menu.disable()
        self.start_menu.run(self)

    def show_over_screen(self):  # game over screen
        self.game_over_voice.play()
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.title_font, 100,
                       GREEN, WIDTH/2, HEIGHT/2, align='center')
        self.draw_text('Press any key to save game', self.title_font, 75,
                       CYAN, WIDTH/2, HEIGHT*3/4, align='center')
        pg.display.flip()
        self.wait_key()

    def wait_key(self):
        pg.event.wait()  # pulls out any event which happened before this
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def stop(self):
        pg.mixer.music.stop()
