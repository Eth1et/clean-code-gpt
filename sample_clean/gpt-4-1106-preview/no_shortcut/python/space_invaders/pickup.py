import copy
import pygame
import space_invaders.spaceship as spaceship
import space_invaders.config as config

class Pickup(pygame.sprite.Sprite):
    def __init__(self, trigger_effect, effect_args, image=None, image_file_path=""):
        super().__init__()
        self.image = image if image else pygame.image.load(image_file_path)
        self.rect = self.image.get_rect()
        self.trigger_effect = trigger_effect
        self.effect_args = effect_args

    def duplicate(self):
        return Pickup(action=self.trigger_effect, args=self.effect_args, image=copy.copy(self.image))

    def move(self, offset):
        self.rect.move_ip(offset)

    def render(self, surface):
        surface.blit(self.image, self.rect.topleft)

    @property
    def collider(self):
        return self.rect

    @property
    def position(self):
        return self.rect.center

    @position.setter
    def position(self, new_pos):
        self.rect.center = new_pos

    @property
    def action(self):
        return self.trigger_effect

    @property
    def args(self):
        return self.effect_args

    @staticmethod
    def heal_action(target, heal_amount):
        target.heal(heal_amount)

    @staticmethod
    def give_weapon_action(target, weapon_type):
        target.add_ammo(weapon_type.new_gun())

    @staticmethod
    def give_extra_life_action(target):
        target.add_life()

    @staticmethod
    def boost_fire_rate_action(target, multiplier, duration):
        target.set_fire_rate_multiplier(multiplier)
        pygame.time.set_timer(RESET_FIRE_RATE, duration)

    @staticmethod
    def reset_fire_rate_action(target):
        target.set_fire_rate_multiplier(1)

RESET_FIRE_RATE = pygame.locals.USEREVENT + 1

PICKUP_REPAIR = Pickup(
    trigger_effect=Pickup.heal_action,
    image_file_path=config.get_path("Sprites", "repair.png"),
    effect_args=[1000000]
)
PICKUP_SMALL_HEAL = Pickup(
    trigger_effect=Pickup.heal_action,
    image_file_path=config.get_path("Sprites", "small_heal.png"),
    effect_args=[5]
)
PICKUP_MEDIUM_HEAL = Pickup(
    trigger_effect=Pickup.heal_action,
    image_file_path=config.get_path("Sprites", "medium_heal.png"),
    effect_args=[10]
)
PICKUP_DEFAULT_GUN = Pickup(
    trigger_effect=Pickup.give_weapon_action,
    image_file_path=config.get_path("Sprites", "default_gun_pickup.png"),
    effect_args=[spaceship.DEFAULT_GUN]
)
PICKUP_MINIGUN = Pickup(
    trigger_effect=Pickup.give_weapon_action,
    image_file_path=config.get_path("Sprites", "minigun_pickup.png"),
    effect_args=[spaceship.MINIGUN]
)
PICKUP_ROCKET_GUN = Pickup(
    trigger_effect=Pickup.give_weapon_action,
    image_file_path=config.get_path("Sprites", "rocket_gun_pickup.png"),
    effect_args=[spaceship.ROCKET_GUN]
)
PICKUP_LIFE = Pickup(
    trigger_effect=Pickup.give_extra_life_action,
    image_file_path=config.get_path("Sprites", "life.png"),
    effect_args=[]
)
PICKUP_FIRE_RATE_BOOSTER = Pickup(
    trigger_effect=Pickup.boost_fire_rate_action,
    image_file_path=config.get_path("Sprites", "fire_rate_booster.png"),
    effect_args=[0.5, 5000]
)