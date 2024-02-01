import pygame

from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT


class Entity(pygame.sprite.Sprite):
    def __init__(self, spaceship, spawn_position, speed, lives=1, looks_down=True):
        super().__init__()
        self._ship = spaceship.new_ship()
        self._hp = spaceship.hp
        self._max_hp = spaceship.hp
        self._lives = lives
        self._speed = speed
        self._ship.looks_down = looks_down
        self._ship.set_position(spawn_position)

    def render(self, window, show_colliders):
        self._ship.render(window, show_colliders)

    def check_projectile_hit(self, enemies):
        return self._ship.check_projectile_hit(enemies)

    def set_fire_rate_multiplier(self, multiplier):
        self._ship.set_fire_rate_multiplier(multiplier)

    @property
    def collider(self):
        return self._ship.collider

    @property
    def image_rect(self):
        return self._ship.image_rect

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def speed(self):
        return self._speed

    def in_bounds(self):
        return 0 <= self._ship.image_rect.center[0] < WINDOW_WIDTH and 0 <= self._ship.image_rect.center[1] < WINDOW_HEIGHT

    def add_ammo(self, gun):
        self._ship.add_ammo(gun)

    def next_gun(self):
        if self.alive():
            self._ship.next_gun()

    def shoot(self):
        if self.alive():
            self._ship.shoot()

    def alive(self):
        return self._hp > 0

    @property
    def ship(self):
        return self._ship

    @property
    def lives(self):
        return self._lives

    def add_life(self, amount=1):
        if self.alive():
            self._lives += amount

    def heal(self, amount):
        if self.alive() and amount > 0:
            self._hp = min(self._hp + amount, self._max_hp)

    def take_damage(self, amount):
        if not self.alive() or not self.in_bounds() or amount <= 0:
            return

        self._hp = max(0, self._hp - amount)

        if self._hp == 0:
            if self._lives == 0:
                self.die()
            else:
                self._lives -= 1
                self._hp = self._max_hp

    def move(self, vec, clamp=True):
        if not self.alive():
            return

        if clamp and vec[0] != 0 and vec[1] != 0:
            diagonal_len = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)
            vec = (vec[0] / diagonal_len, vec[1] / diagonal_len)

        vec = (vec[0] * self._speed, vec[1] * self._speed)
        self._ship.move(vec)

    def die(self):
        del self


class Enemy(Entity):
    def __init__(self, spaceship, spawn_position, speed, actions):
        super().__init__(spaceship, spawn_position, speed, lives=1, looks_down=True)
        self._actions = actions

    def execute_next_action(self):
        if len(self._actions) > 0:
            action = self._actions[0]
            match action[0]:
                case "shoot":
                    self.shoot()
                case "move":
                    self.move(action[1][0], clamp=False)
                case "move_fire":
                    self.shoot()
                    self.move(action[1][0], clamp=False)

            self._actions.remove(action)