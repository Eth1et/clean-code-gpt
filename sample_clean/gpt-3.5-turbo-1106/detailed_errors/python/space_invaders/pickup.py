import copy
import pygame
from pygame.locals import USEREVENT
import space_invaders.spaceship as spaceship
import space_invaders.config as config


class Pickup(pygame.sprite.Sprite):
    def __init__(self, action, args, image=None, image_file=""):
        super().__init__()
        self._image = image if image is not None else pygame.image.load(image_file)
        self._rect = self._image.get_rect()
        self._action = action
        self._args = args

    def new_pickup(self):
        return Pickup(action=self._action, args=self._args, image=copy.copy(self._image))

    def move(self, vec):
        self._rect.center = (self._rect.center[0] + vec[0], self._rect.center[1] + vec[1])

    def render(self, window):
        window.blit(self._image, (self._rect.center[0] - self._rect.width//2, self._rect.center[1] - self._rect.height//2))

    @property
    def collider(self):
        return self._rect

    @property
    def image(self):
        return self._image

    @property
    def position(self):
        return self._rect.center

    @position.setter
    def position(self, vec):
        self._rect.center = vec

    @property
    def action(self):
        return self._action

    @property
    def args(self):
        return self._args


class Action:
    @staticmethod
    def heal(entity, amount):
        entity.heal(amount)

    @staticmethod
    def give_gun(entity, gun):
        entity.add_ammo(gun.new_gun())

    @staticmethod
    def give_life(entity):
        entity.add_life()

    @staticmethod
    def fire_rate_boost(entity, multiplier, duration):
        entity.set_fire_rate_multiplier(multiplier)
        pygame.time.set_timer(RESET_FIRE_RATE, duration)

    @staticmethod
    def reset_fire_rate(entity):
        entity.set_fire_rate_multiplier(1)


RESET_FIRE_RATE = USEREVENT + 1

PICKUP_REPAIR = Pickup(
    action=Action.heal,
    image_file=config.get_path("Sprites", "repair.png"),
    args=[1000000]
)
PICKUP_SMALL_HEAL = Pickup(
    action=Action.heal,
    image_file=config.get_path("Sprites", "small_heal.png"),
    args=[5]
)
PICKUP_MEDIUM_HEAL = Pickup(
    action=Action.heal,
    image_file=config.get_path("Sprites", "medium_heal.png"),
    args=[10]
)
PICKUP_DEFAULT_GUN = Pickup(
    action=Action.give_gun,
    image_file=config.get_path("Sprites", "default_gun_pickup.png"),
    args=[spaceship.DEFAULT_GUN]
)
PICKUP_MINIGUN = Pickup(
    action=Action.give_gun,
    image_file=config.get_path("Sprites", "minigun_pickup.png"),
    args=[spaceship.MINIGUN]
)
PICKUP_ROCKET_GUN = Pickup(
    action=Action.give_gun,
    image_file=config.get_path("Sprites", "rocket_gun_pickup.png"),
    args=[spaceship.ROCKET_GUN]
)
PICKUP_LIFE = Pickup(
    action=Action.give_life,
    image_file=config.get_path("Sprites", "life.png"),
    args=[]
)
PICKUP_FIRE_RATE_BOOSTER = Pickup(
    action=Action.fire_rate_boost,
    image_file=config.get_path("Sprites", "fire_rate_booster.png"),
    args=[0.5, 5000]
)