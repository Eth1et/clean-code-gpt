import copy
import pygame
from pygame.locals import USEREVENT
import space_invaders.spaceship as spaceship
import space_invaders.config as config


class Pickup(pygame.sprite.Sprite):
    """Represents objects that the player can pick up and gain bonuses from them"""
    def __init__(self, action, args, image=None, image_file=""):
        super().__init__()
        if image:
            self.image = image
        else:
            self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.action = action
        self.args = args

    def new_pickup(self):
        return Pickup(action=self.action, args=self.args, image=copy.copy(self.image))

    def move(self, vec):
        self.rect.center = (self.rect.center[0] + vec[0], self.rect.center[1] + vec[1])

    def render(self, window):
        window.blit(self.image, (self.rect.centerx - self.rect.width//2, self.rect.centery - self.rect.height//2))

    @property
    def collider(self):
        return self.rect

    @property
    def position(self):
        return self.rect.center

    @position.setter
    def position(self, vec):
        self.rect.center = vec

    @staticmethod
    def action_heal(entity, amount):
        entity.heal(amount)

    @staticmethod
    def action_give_gun(entity, gun):
        entity.add_ammo(gun.new_gun())

    @staticmethod
    def action_give_life(entity):
        entity.add_life()

    @staticmethod
    def action_fire_rate_boost(entity, multiplier, duration):
        entity.set_fire_rate_multiplier(multiplier)
        pygame.time.set_timer(RESET_FIRE_RATE, duration)

    @staticmethod
    def action_reset_fire_rate(entity):
        entity.set_fire_rate_multiplier(1)


RESET_FIRE_RATE = USEREVENT + 1

PICKUP_REPAIR = Pickup(
    action=Pickup.action_heal,
    image_file=config.get_path("Sprites", "repair.png"),
    args=[1000000]
)
PICKUP_SMALL_HEAL = Pickup(
    action=Pickup.action_heal,
    image_file=config.get_path("Sprites", "small_heal.png"),
    args=[5]
)
PICKUP_MEDIUM_HEAL = Pickup(
    action=Pickup.action_heal,
    image_file=config.get_path("Sprites", "medium_heal.png"),
    args=[10]
)
PICKUP_DEFAULT_GUN = Pickup(
    action=Pickup.action_give_gun,
    image_file=config.get_path("Sprites", "default_gun_pickup.png"),
    args=[spaceship.DEFAULT_GUN]
)
PICKUP_MINIGUN = Pickup(
    action=Pickup.action_give_gun,
    image_file=config.get_path("Sprites", "minigun_pickup.png"),
    args=[spaceship.MINIGUN]
)
PICKUP_ROCKET_GUN = Pickup(
    action=Pickup.action_give_gun,
    image_file=config.get_path("Sprites", "rocket_gun_pickup.png"),
    args=[spaceship.ROCKET_GUN]
)
PICKUP_LIFE = Pickup(
    action=Pickup.action_give_life,
    image_file=config.get_path("Sprites", "life.png"),
    args=[]
)
PICKUP_FIRE_RATE_BOOSTER = Pickup(
    action=Pickup.action_fire_rate_boost,
    image_file=config.get_path("Sprites", "fire_rate_booster.png"),
    args=[0.5, 5000]
)