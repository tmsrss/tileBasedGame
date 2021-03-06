import pygame as pg
from settings import *
from random import uniform, choice, randint
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2


def collide_hit_rect(player, wall):
    return player.hit_rect.colliderect(wall.rect)


def collide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width/2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height/2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.backpack = ["pistol"]
        self.weapon = "pistol"
        self.damaged = False
        self.ammo = DEFAULT_AMMO
        self.kill_count = 0

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]  or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            self.shoot()
        if keys[pg.K_1] or keys[pg.K_KP1]:
            self.weapon = self.backpack[0]
        if keys[pg.K_2] or keys[pg.K_KP2]:
            try:
                self.weapon = self.backpack[1]
            except:
                pass
        if keys[pg.K_3] or keys[pg.K_KP3]:
            try:
                self.weapon = self.backpack[2]
            except:
                pass

    def shoot(self):
        now = pg.time.get_ticks()
        if self.ammo > 0:
            if now - self.last_shot > WEAPONS[self.weapon]["rate"]:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)  # this is position of barrel end
                self.vel = vec(-WEAPONS[self.weapon]["kickback"], 0).rotate(-self.rot)
                for i in range(WEAPONS[self.weapon]["count"]):
                    spread = uniform(-WEAPONS[self.weapon]["spread"], WEAPONS[self.weapon]["spread"])
                    Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                    snd = choice(self.game.weapon_sounds[self.weapon])
                    if snd.get_num_channels() > 2:
                        snd.stop()
                    snd.play()
                self.ammo -= 1
                MuzzleFlash(self.game, pos)

    def update(self):
        self.get_keys()
        self.rot = (self.rot +self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health >= PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def get_kills(self):
        return self.kill_count


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
         self.groups = game.all_sprites, game.mobs
         pg.sprite.Sprite.__init__(self, self.groups)
         self.game = game
         self.image = game.mob_img.copy()
         self.rect = self.image.get_rect()
         self.rect.center = (x, y)
         self.hit_rect = MOB_HIT_RECT.copy()
         self.hit_rect.center = self.rect.center
         self.pos = vec(x, y)
         self.vel = vec(0, 0)
         self.acc = vec(0, 0)
         self.rect.center = self.pos
         self.rot = 0
         self.health = MOB_HEALTH
         self.speed = choice(MOB_SPEEDS)
         self.target = game.player
         self.image_file = self.game.mob_img

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if dist == 0:
                    positionx = mob.pos.x
                    positiony = mob.pos.y
                    #mob.pos = vec(positionx+(random.randrange(600, 2000, 600, Type=int), positiony+(random.randrange(600, 2000, 600, Type=int))))
                    mob.pos = vec(1020, 400)
                    dist = self.pos - mob.pos
                if 0.1 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()
        for wall in self.game.walls:
            dist = self.pos - wall.pos
            if 0.1 < dist.length() < AVOID_RADIUS:
                self.acc += dist.normalize()

    def update(self, *args):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.image_file, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            #self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel+= self.acc *self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, "x")
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, "y")
            self.rect.center = self.hit_rect.center
        else:
            pass  # need to add code for hitmen to wonder around
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.target.kill_count+=1
            print(self.target.kill_count)

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health/MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Boss(Mob):
    def __init__(self, game, x, y):
        Mob.__init__(self, game, x, y)
        self.image = game.boss_img.copy()
        self.image_file = self.game.boss_img


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.rect.x = x
        self.rect.y = y


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]["size"]]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * WEAPONS[game.player.weapon]["speed"] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self._layer = BULLET_LAYER
        self.damage = damage

    def update(self):
         self.pos += self.vel * self.game.dt
         self.rect.center = self.pos
         if pg.sprite.spritecollideany(self, self.game.walls):
             self.kill()
         if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]["lifetime"]:
             self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y *TILESIZE


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self, *args):
        if pg.time.get_ticks() - self.spawn_time > SMOKE_DURATION:
            self.kill()


class Powerup(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = POWERUPS_LAYER
        self.game = game
        self.type = type
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.powerups_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = pos
        self.pos = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step/BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1


class WaveCounter(pg.sprite.Sprite):
    def __init__(self, game, time_until):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect(topleft=(10, 10))
        game.draw_text(f'new wave in {time_until}', game.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        self.timer = time_until * 1000
        self.game = game

    def update(self):
        self.timer -= self.game.dt
        self.game.draw_text(f'new wave in {int(self.timer / 1000) + 1}', self.game.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        if self.timer <= 0:
            self.game.new_wave()
            self.kill()


'''
class Button():
	def __init__(self, color, x, y, width, height, text=""):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw(self, surf, outline=None):
		if outline:
			pygame.draw.rect(surf, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
		pygame.draw.rect(surf, self.color, (self.y, self.width, self.height, 0))
		if self.text != "":
			font = pygame.font.SysFont('comicsans', 60)
			text = font.render(self.text, 1, (0, 0, 0))
			surf.blit(text, (sef.x + (self.width/2 - text.get_width()/2),
			                 self.y + (self.height/2 - text.get_height()/2)))

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x+self.width:
			if pos[1] > self.y and pos{1} < self.y+self.height:
				return True
		return False
'''
