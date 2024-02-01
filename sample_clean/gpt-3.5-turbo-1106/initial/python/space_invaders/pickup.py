from __future__ import annotations
from typing import Callable, Any, Tuple, List
import copy
import pygame
from pygame.locals import USEREVENT
import space_invaders.spaceship as spaceship
import space_invaders.config as config


class Pickup(pygame.sprite.Sprite):
    def __init__(self, action: Callable[..., Any], args: List[Any], image: pygame.Surface = None, image_file: str = "") -> None:
        if image is not None:
            self._image = image
        else:
            self._image = pygame.image.load(image_file)

        self._rect = self._image.get_rect()
        self._action = action
        self._args = args

    def new_pickup(self) -> Pickup:
        return Pickup(action=self._action, args=self._args, image=copy.copy(self._image))

    def move(self, vec: Tuple[int, int]) -> None:
        self._rect.center = (self._rect.center[0] + vec[0], self._rect.center[1] + vec[1])

    def render(self, window: pygame.Surface) -> None:
        window.blit(self._image, (self._rect.center[0] - self._rect.width//2, self._rect.center[1] - self._rect.height//2))

    @property
    def collider(self) -> pygame.Rect:
        return self._rect

    @property
    def image(self) -> pygame.Surface:
        return self._image

    @property
    def position(self) -> Tuple[int, int]:
        return self._rect.center

    @position.setter
    def position(self, vec: Tuple[int, int]) -> None:
        self._rect.center = vec

    @property
    def action(self) -> Callable[..., Any]:
        return self._action

    @property
    def args(self) -> List[Any]:
        return self._args

    @staticmethod
    def action_heal(entity: Any, amount: int) -> None:
        entity.heal(amount)

    @staticmethod
    def action_give_gun(entity: Any, gun: Any) -> None:
        entity.add_ammo(gun.new_gun())

    @staticmethod
    def action_give_life(entity: Any) -> None:
        entity.add_life()

    @staticmethod
    def action_fire_rate_boost(entity: Any, multiplier: float, duration: int) -> None:
        entity.set_fire_rate_multiplier(multiplier)
        pygame.time.set_timer(RESET_FIRE_RATE, duration)

    @staticmethod
    def action_reset_fire_rate(entity: Any) -> None:
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