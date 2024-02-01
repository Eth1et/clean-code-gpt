import pygame
from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT

class GameEntity(pygame.sprite.Sprite):
    def __init__(self, spaceship_factory, position, speed, health=1, aims_down=True):
        super().__init__()
        self.spaceship = spaceship_factory()
        self.health = self.max_health = spaceship_factory.health
        self.lives = health
        self.speed = speed
        self.spaceship.aims_down = aims_down
        self.spaceship.set_position(position)

    def render(self, window, debug_colliders):
        self.spaceship.render(window, debug_colliders)

    def detect_projectile_collision(self, targets):
        return self.spaceship.detect_projectile_collision(targets)

    def change_fire_rate(self, rate_multiplier):
        self.spaceship.change_fire_rate(rate_multiplier)

    def is_within_game_bounds(self):
        pos = self.spaceship.image_rect.center
        return 0 <= pos[0] < WINDOW_WIDTH and 0 <= pos[1] < WINDOW_HEIGHT

    def add_ammo_type(self, ammo_type):
        self.spaceship.add_ammo_type(ammo_type)

    def select_next_weapon(self):
        if self.is_alive():
            self.spaceship.select_next_weapon()

    def fire(self):
        if self.is_alive():
            self.spaceship.fire()

    def is_alive(self):
        return self.health > 0

    def gain_life(self, extra_lives=1):
        if self.is_alive():
            self.lives += extra_lives

    def recover_health(self, recovery_amount):
        if self.is_alive() and recovery_amount > 0:
            self.health = min(self.health + recovery_amount, self.max_health)

    def receive_damage(self, damage):
        if not self.is_alive() or not self.is_within_game_bounds() or damage <= 0:
            return

        self.health = max(0, self.health - damage)

        if self.health == 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = self.max_health
            else:
                self.destroy()

    def move_by(self, direction, normalize=True):
        if not self.is_alive():
            return

        if normalize and direction[0] and direction[1]:
            direction_magnitude = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            direction = (direction[0] / direction_magnitude, direction[1] / direction_magnitude)

        adjusted_direction = (direction[0] * self.speed, direction[1] * self.speed)
        self.spaceship.move_by(adjusted_direction)

    def destroy(self):
        del self

class Enemy(GameEntity):
    def __init__(self, spaceship_factory, position, speed, behavior):
        super().__init__(spaceship_factory, position, speed, health=1, aims_down=True)
        self.behavior = behavior

    def perform_next_action(self):
        if self.behavior:
            action, args = self.behavior[0]
            match action:
                case "shoot":
                    self.fire()
                case "move":
                    self.move_by(args[0], normalize=False)
                case "move_fire":
                    self.fire()
                    self.move_by(args[0], normalize=False)
            self.behavior.pop(0)