import copy
import pygame
from shapely.geometry import Polygon
import space_invaders.config as config

class Spaceship:
    def __init__(self, gun, hp, collider, enemy, image_file="", image=None):
        self._image = image if image else pygame.image.load(image_file)
        self._guns = gun if isinstance(gun, list) else [gun]
        self._active_gun = 0
        self._hp = hp
        self._image_rect = self._image.get_rect()
        self._collider_relative_vertices = copy.copy(collider)
        self._collider = collider
        self._enemy = enemy
        self._fire_rate_multiplier = 1
        self._projectiles = []

    def new_ship(self):
        new_guns = [gun.new_gun() for gun in self._guns]
        shp = Spaceship(new_guns, self._hp, list(vertex for vertex in self._collider), self._enemy, image=copy.copy(self._image))
        return shp

    def empty_projectiles(self):
        self._projectiles.clear()

    def add_ammo(self, gun):
        for checked in self._guns:
            if checked.type == gun.type:
                checked.add_ammo(gun.ammo)
                return
        self._guns.append(gun)

    def set_fire_rate_multiplier(self, multiplier):
        self._fire_rate_multiplier = multiplier

    def set_position(self, vec):
        self._image_rect.center = vec
        for i, vertex in enumerate(self._collider_relative_vertices):
            self._collider[i] = (vertex[0] + vec[0], vertex[1] + vec[1])
        for gun in self._guns:
            gun.set_position(vec)

    def move(self, vec):
        self._image_rect.move_ip(vec[0], vec[1])
        for i, vertex in enumerate(self._collider_relative_vertices):
            self._collider[i] = (self._image_rect.center[0] + vertex[0], self._image_rect.center[1] + vertex[1])
        for gun in self._guns:
            gun.move(vec)

    def next_gun(self):
        self._active_gun += 1
        self._active_gun %= len(self._guns)
        self._guns[self._active_gun].set_position(self._image_rect.center)

    def shoot(self):
        new_projectile = self._guns[self._active_gun].shoot(self._fire_rate_multiplier)
        if new_projectile:
            self._projectiles.append(new_projectile)

    def render(self, window, show_colliders):
        self._guns[self._active_gun].render(window)
        window.blit(self._image, (self._image_rect.center[0] - self._image_rect.width//2, self._image_rect.center[1] - self._image_rect.height//2))
        self.render_projectiles(window, show_colliders)
        if show_colliders:
            self._render_colliders(window)

    def _render_colliders(self, window):
        pygame.draw.rect(window, (255, 255, 0), self._image_rect, 1)
        pygame.draw.circle(window, (255, 0, 0), self._image_rect.center, 3)
        pygame.draw.polygon(window, (255, 0, 255), self._collider, 1)

    def check_projectile_hit(self, enemies):
        explosions = []
        for projectile in self._projectiles:
            hit_count = 0
            p_poly = Polygon([projectile.collider.topleft, projectile.collider.topright,
                              projectile.collider.bottomright, projectile.collider.bottomleft])

            for enemy in enemies:
                enemy_poly = Polygon(enemy.collider)
                if p_poly.intersects(enemy_poly):
                    enemy.take_damage(projectile.damage)
                    hit_count += 1
                    if self._enemy:
                        config.score -= 15

            if hit_count > 0:
                self._handle_explosions(explosions, projectile)

        return explosions

    def _handle_explosions(self, explosions, projectile):
        config.play_sound(config.SOUND_PLAYER_HIT_DATA if self._enemy else config.SOUND_ENEMY_HIT_DATA, 0)
        self._projectiles.remove(projectile)
        explosions.append([pygame.image.load(config.get_path("Sprites", "explosion.png")), projectile.image_rect.center, config.EXPLOSION_DURATION])

    def check_projectiles(self):
        for projectile in list(self._projectiles):
            projectile.move_forward(self._enemy)
            if projectile.check_if_out():
                self._projectiles.remove(projectile)

    def render_projectiles(self, window, show_colliders):
        self.check_projectiles()
        for projectile in self._projectiles:
            projectile.render(window)
            if show_colliders:
                self._render_projectile_colliders(window, projectile)

    def _render_projectile_colliders(self, window, projectile):
        pygame.draw.rect(window, (255, 255, 0), projectile.image_rect, 1)
        pygame.draw.circle(window, (255, 0, 0), projectile.image_rect.center, 3)
        pygame.draw.rect(window, (255, 0, 255), projectile.collider, 1)

    @property
    def guns(self):
        return self._guns

    @property
    def active_gun(self):
        return self._active_gun

    @property
    def image(self):
        return self._image

    @property
    def hp(self):
        return self._hp

    @property
    def image_rect(self):
        return self._image_rect

    @property
    def fire_rate_multiplier(self):
        return self._fire_rate_multiplier

    @property
    def collider(self):
        return self._collider

class Gun:
    def __init__(self, fire_rate, projectile, ammo, left_muzzle, right_muzzle, offset, gun_type="default", image=None,
                 image_file=""):
        self._image = image if image else pygame.image.load(image_file)
        self._rect = self._image.get_rect()
        self._fire_rate = fire_rate
        self._projectile = projectile
        self._ammo = ammo
        self._left_muzzle = left_muzzle
        self._right_muzzle = right_muzzle
        self._offset = offset
        self._time_since_last_shot = 0
        self._type = gun_type

    def new_gun(self):
        return Gun(self._fire_rate, self._projectile, self._ammo, self._left_muzzle, self._right_muzzle, self._offset,
                   image=copy.copy(self._image), gun_type=self._type)

    def set_position(self, vec):
        self._rect.center = (vec[0] + self._offset[0], vec[1] + self._offset[1])

    def move(self, vec):
        self._rect.move_ip(vec[0], vec[1])

    def render(self, window):
        window.blit(self._image, (self._rect.center[0] - self._rect.width//2, self._rect.center[1] - self._rect.height//2))

    @property
    def image(self):
        return self._image

    @property
    def type(self):
        return self._type

    @property
    def rect(self):
        return self._rect

    @property
    def ammo(self):
        return self._ammo

    def add_ammo(self, amount):
        self._ammo += max(0, amount)

    def shoot(self, fire_rate_multiplier):
        current_time = pygame.time.get_ticks()
        if self._ammo != 0 and current_time - self._time_since_last_shot > self._fire_rate * fire_rate_multiplier:
            config.play_sound(get_sound_by_projectile(self._projectile), 0)
            projectile = self.spawn_projectile(self._left_muzzle if self._ammo % 2 == 0 else self._right_muzzle)
            self._ammo -= 1
            self._time_since_last_shot = current_time
            return projectile
        return None

    def spawn_projectile(self, relative_position):
        position = (self._rect.center[0] + relative_position[0], self._rect.center[1] + relative_position[1])
        new_projectile = self._projectile.new_projectile()
        new_projectile.set_position(position)
        return new_projectile

class Projectile:
    def __init__(self, collider, damage, speed, image_file="", image=None):
        self._image = image if image else pygame.image.load(image_file)
        self._image_rect = self._image.get_rect()
        self._collider = collider
        self._damage = damage
        self._speed = speed

    def set_position(self, position):
        self._collider.center = position
        self._image_rect.center = position

    def new_projectile(self):
        return Projectile(copy.copy(self._collider), self._damage, self._speed, image=copy.copy(self._image))

    @property
    def speed(self):
        return self._speed

    @property
    def damage(self):
        return self._damage

    @property
    def image(self):
        return self._image

    @property
    def image_rect(self):
        return self._image_rect

    @property
    def collider(self):
        return self._collider

    def render(self, window):
        window.blit(self._image, (self._image_rect.center[0] - self._image_rect.width//2, self._image_rect.center[1] - self._image_rect.height//2))

    def move_forward(self, enemy):
        diff = self._speed if enemy else -self._speed
        self._collider.center = (self._collider.center[0], self._collider.center[1] + diff)
        self._image_rect.center = (self._image_rect.center[0], self._image_rect.center[1] + diff)

    def check_if_out(self):
        return self._collider.bottom < -100 or self._collider.top > config.WINDOW_HEIGHT + 100

def get_sound_by_projectile(projectile):
    if projectile in (DEFAULT_PROJECTILE, DEFAULT_ENEMY_PROJECTILE):
        return config.SOUND_DEFAULT_GUN_DATA
    if projectile == MINIGUN_PROJECTILE:
        return config.SOUND_MINIGUN_DATA
    return config.SOUND_ROCKET_DATA

# Constants for different types of projectiles, guns, and ships
DEFAULT_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 30, 60), 2, 20, image_file=config.get_path("Sprites", "default_projectile.png")
)
DEFAULT_GUN = Gun(
    170, DEFAULT_PROJECTILE, -1,
    (-58, -55), (58, -55), (0, 0),
    image_file=config.get_path("Sprites", "default_gun.png")
)
DEFAULT_SHIP_collider = [
    (-100, -50), (-20, -100), (20, -100), (99, -50), (99, 80), (60, 99), (-60, 99), (-100, 80)
]
DEFAULT_SHIP = Spaceship(
    DEFAULT_GUN, 25, DEFAULT_SHIP_collider, False, image_file=config.get_path("Sprites", "default_ship.png")
)

MINIGUN_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 15, 35), 1, 20, image_file=config.get_path("Sprites", "minigun_projectile.png")
)
MINIGUN = Gun(
    60, MINIGUN_PROJECTILE, 140,
    (-58, -55), (58, -55), (0, 0),
    gun_type="minigun", image_file=config.get_path("Sprites", "minigun.png")
)

ROCKET_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 50, 50), 10, 22, image_file=config.get_path("Sprites", "rocket_projectile.png")
)
ROCKET_GUN = Gun(
    300, ROCKET_PROJECTILE, 15,
    (-58, -55), (58, -55), (0, 0),
    gun_type="rocket", image_file=config.get_path("Sprites", "rocket_gun.png")
)

DEFAULT_ENEMY_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 20, 40), 1, 22, image_file=config.get_path("Sprites", "default_enemy_projectile.png")
)
DEFAULT_ENEMY_GUN = Gun(
    250, DEFAULT_ENEMY_PROJECTILE, -1,
    (-20, 50), (20, 50), (0, 0),
    image_file=config.get_path("Sprites", "default_enemy_gun.png")
)
DEFAULT_ENEMY_SHIP_collider = [
    (-90, -80), (-60, -100), (60, -100), (90, -80), (99, 0), (90, 80), (60, 99), (-60, 99), (-80, 90), (-100, 0)
]
DEFAULT_ENEMY_SHIP = Spaceship(
    DEFAULT_ENEMY_GUN, 10, DEFAULT_ENEMY_SHIP_collider, True,
    image_file=config.get_path("Sprites", "default_enemy_ship.png")
)