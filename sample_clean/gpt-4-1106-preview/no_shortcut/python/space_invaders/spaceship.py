import copy
import pygame
from shapely.geometry import Polygon
import space_invaders.config as config


class Spaceship:
    def __init__(self, weapons, health, collider_shape, is_enemy, image_file=None, image_surface=None):
        self.image = image_surface if image_surface is not None else pygame.image.load(image_file)
        self.weapons = weapons if isinstance(weapons, list) else [weapons]
        self.active_weapon_index = 0
        self.health = health
        self.image_rect = self.image.get_rect()
        self.collider_vertices_relative = copy.copy(collider_shape)
        self.collider_absolute = collider_shape
        self.is_enemy = is_enemy
        self.fire_rate_multiplier = 1
        self.projectiles = []

    def clone(self):
        clone = Spaceship(
            [weapon.clone() for weapon in self.weapons],
            self.health,
            [vertex for vertex in self.collider_absolute],
            self.is_enemy,
            image_surface=copy.copy(self.image)
        )
        return clone

    def clear_projectiles(self):
        self.projectiles.clear()

    def add_weapon(self, new_weapon):
        for weapon in self.weapons:
            if weapon.weapon_type == new_weapon.weapon_type:
                weapon.replenish_ammo(new_weapon.ammo)
                return
        self.weapons.append(new_weapon)

    def modify_fire_rate(self, new_multiplier):
        self.fire_rate_multiplier = new_multiplier

    def update_position(self, new_position):
        self.image_rect.center = new_position
        for i, vertex in enumerate(self.collider_vertices_relative):
            self.collider_absolute[i] = (vertex[0] + new_position[0], vertex[1] + new_position[1])
        for weapon in self.weapons:
            weapon.set_position(new_position)

    def shift_position(self, shift_vector):
        self.image_rect.move_ip(shift_vector)
        for i, vertex in enumerate(self.collider_vertices_relative):
            self.collider_absolute[i] = (self.image_rect.center[0] + vertex[0],
                                         self.image_rect.center[1] + vertex[1])
        for weapon in self.weapons:
            weapon.move(shift_vector)

    def cycle_active_weapon(self):
        self.active_weapon_index = (self.active_weapon_index + 1) % len(self.weapons)
        self.weapons[self.active_weapon_index].set_position(self.image_rect.center)

    def fire(self):
        projectile = self.weapons[self.active_weapon_index].fire(self.fire_rate_multiplier)
        if projectile:
            self.projectiles.append(projectile)

    def draw(self, surface, debug_mode=False):
        self.weapons[self.active_weapon_index].draw(surface)
        surface.blit(self.image, self.image_rect.topleft)
        self.draw_projectiles(surface, debug_mode)
        if debug_mode:
            self.draw_debug_elements(surface)

    def check_projectile_collisions(self, targets):
        explosions = []
        for projectile in self.projectiles[:]:
            projectile_poly = Polygon([
                projectile.collider.topleft, projectile.collider.topright,
                projectile.collider.bottomright, projectile.collider.bottomleft
            ])
            for target in targets:
                target_poly = Polygon(target.collider_absolute)
                if projectile_poly.intersects(target_poly):
                    target.apply_damage(projectile.damage)
                    self.projectiles.remove(projectile)
                    if self.is_enemy:
                        config.score -= 15
                    break
            if projectile not in self.projectiles:
                config.play_sound(config.SOUND_PLAYER_HIT_DATA if self.is_enemy else config.SOUND_ENEMY_HIT_DATA, 0)
                explosion_center = projectile.image_rect.center
                explosion_duration = config.EXPLOSION_DURATION
                explosion_image = pygame.image.load(config.get_path("Sprites", "explosion.png"))
                explosions.append([explosion_image, explosion_center, explosion_duration])
        return explosions

    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.advance(self.is_enemy)
            if projectile.is_out_of_bounds():
                self.projectiles.remove(projectile)

    def draw_projectiles(self, surface, debug_mode):
        self.update_projectiles()
        for projectile in self.projectiles:
            projectile.draw(surface)
            if debug_mode:
                self.draw_projectile_debug(projectile, surface)

    def draw_debug_elements(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.image_rect, 1)
        pygame.draw.circle(surface, (255, 0, 0), self.image_rect.center, 3)
        pygame.draw.polygon(surface, (255, 0, 255), self.collider_absolute, 1)

    def draw_projectile_debug(self, projectile, surface):
        pygame.draw.rect(surface, (255, 255, 0), projectile.image_rect, 1)
        pygame.draw.circle(surface, (255, 0, 0), projectile.image_rect.center, 3)
        pygame.draw.rect(surface, (255, 0, 255), projectile.collider, 1)


class Gun:
    def __init__(self, cooldown, projectile_type, ammo, muzzle_left, muzzle_right, adjustment, weapon_type="default", image_surface=None, image_file=None):
        self.image = image_surface if image_surface is not None else pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.cooldown = cooldown
        self.projectile_type = projectile_type
        self.ammo = ammo
        self.muzzle_left = muzzle_left
        self.muzzle_right = muzzle_right
        self.adjustment = adjustment
        self.last_fire_time = 0
        self.weapon_type = weapon_type

    def clone(self):
        return Gun(
            self.cooldown,
            self.projectile_type,
            self.ammo,
            self.muzzle_left,
            self.muzzle_right,
            self.adjustment,
            weapon_type=self.weapon_type,
            image_surface=copy.copy(self.image)
        )

    def set_position(self, new_position):
        self.rect.center = (new_position[0] + self.adjustment[0], new_position[1] + self.adjustment[1])

    def move(self, shift_vector):
        self.rect.move_ip(shift_vector)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def replenish_ammo(self, amount):
        self.ammo = max(self.ammo + amount, 0)

    def fire(self, rate_multiplier):
        if pygame.time.get_ticks() - self.last_fire_time > self.cooldown * rate_multiplier and self.ammo != 0:
            projectile = self.create_projectile()
            self.last_fire_time = pygame.time.get_ticks()
            self.ammo -= 1 if self.ammo > 0 else 0
            config.play_sound(get_sound_by_projectile_type(self.projectile_type), 0)
            return projectile
        return None

    def create_projectile(self):
        muzzle = self.muzzle_left if self.ammo % 2 == 0 else self.muzzle_right
        muzzle_position = (self.rect.center[0] + muzzle[0], self.rect.center[1] + muzzle[1])
        projectile = self.projectile_type.clone()
        projectile.set_position(muzzle_position)
        return projectile


class Projectile:
    def __init__(self, hitbox, damage, velocity, image_file=None, image_surface=None):
        self.image = image_surface if image_surface is not None else pygame.image.load(image_file)
        self.image_rect = self.image.get_rect()
        self.collider = hitbox
        self.damage = damage
        self.velocity = velocity

    def set_position(self, new_center):
        self.collider.center = new_center
        self.image_rect.center = new_center

    def clone(self):
        return Projectile(
            copy.copy(self.collider),
            self.damage,
            self.velocity,
            image_surface=copy.copy(self.image)
        )

    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)

    def advance(self, is_enemy_direction):
        offset = self.velocity if is_enemy_direction else -self.velocity
        self.collider.centery += offset
        self.image_rect.centery += offset

    def is_out_of_bounds(self):
        return (self.collider.top > config.WINDOW_HEIGHT + 100) or (self.collider.bottom < -100)


def get_sound_by_projectile_type(projectile):
    if projectile in (DEFAULT_PROJECTILE, DEFAULT_ENEMY_PROJECTILE):
        return config.SOUND_DEFAULT_GUN_DATA
    elif projectile == MINIGUN_PROJECTILE:
        return config.SOUND_MINIGUN_DATA
    else:
        return config.SOUND_ROCKET_DATA


# Constants using the new class and parameter names with "_" removed for clarity
DEFAULT_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 30, 60), 2, 20, image_file=config.get_path("Sprites", "default_projectile.png")
)
DEFAULT_GUN = Gun(
    170, DEFAULT_PROJECTILE, -1, (-58, -55), (58, -55), (0, 0), image_file=config.get_path("Sprites", "default_gun.png")
)
SHIP_COLLIDER = [
    (-100, -50), (-20, -100), (20, -100), (99, -50), (99, 80), (60, 99), (-60, 99), (-100, 80)
]
DEFAULT_SHIP = Spaceship(
    DEFAULT_GUN, 25, SHIP_COLLIDER, is_enemy=False, image_file=config.get_path("Sprites", "default_ship.png")
)
# Define other constants in a similar fashion as above.