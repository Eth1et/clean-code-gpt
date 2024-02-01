import pygame
from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT


class Entity(pygame.sprite.Sprite):
    def __init__(self, ship, spawn_position, speed, lives=1, looks_down=True):
        super().__init__()
        self.ship = ship.new_ship()
        self.hp = ship.hp
        self.max_hp = ship.hp
        self.lives = lives
        self.speed = speed
        self.ship.looks_down = looks_down
        self.ship.set_position(spawn_position)

    def render(self, window, show_colliders):
        self.ship.render(window, show_colliders)

    def check_projectile_hit(self, enemies):
        return self.ship.check_projectile_hit(enemies)

    def set_fire_rate_multiplier(self, multiplier):
        return self.ship.set_fire_rate_multiplier(multiplier)

    @property
    def collider(self):
        return self.ship.collider

    @property
    def image_rect(self):
        return self.ship.image_rect

    def add_ammo(self, gun):
        self.ship.add_ammo(gun)

    def next_gun(self):
        if not self.alive():
            return
        self.ship.next_gun()

    def shoot(self):
        if not self.alive():
            return
        self.ship.shoot()

    def alive(self):
        return self.hp > 0

    def add_life(self, amount=1):
        if self.alive():
            self.lives += amount

    def heal(self, amount):
        if self.alive() and amount > 0:
            self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, amount):
        if not self.alive() or not self.in_bounds() or amount <= 0:
            return

        self.hp = max(0, self.hp - amount)

        if self.hp == 0:
            self.lives -= 1
            if self.lives == 0:
                self.die()
            else:
                self.hp = self.max_hp

    def move(self, vec, clamp=True):
        if not self.alive():
            return
        
        if clamp and vec[0] != 0 and vec[1] != 0:
            diagonal_len = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)
            vec = (vec[0] / diagonal_len, vec[1] / diagonal_len)

        vec = (vec[0] * self.speed, vec[1] * self.speed)
        self.ship.move(vec)
    
    def in_bounds(self):
        position = self.ship.image_rect.center
        return 0 <= position[0] < WINDOW_WIDTH and 0 <= position[1] < WINDOW_HEIGHT

    def die(self):
        pass


class Enemy(Entity):
    def __init__(self, ship, spawn_position, speed, actions):
        super().__init__(ship, spawn_position, speed, lives=1, looks_down=True)
        self.actions = actions

    def execute_next_action(self):
        if len(self.actions) > 0:
            action, arg = self.actions[0]
            if action == "shoot":
                self.shoot()
            elif action == "move":
                self.move(arg[0], clamp=False)
            elif action == "move_fire":
                self.shoot()
                self.move(arg[0], clamp=False)
            self.actions.pop(0)