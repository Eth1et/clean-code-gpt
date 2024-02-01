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
        shp = Spaceship([gun.new_gun() for gun in self._guns], self._hp, list(vertex for vertex in self._collider),
                        self._enemy, image=copy.copy(self._image))
        return shp

    def empty_projectiles(self):
        self._projectiles.clear()

    def add_ammo(self, gun):
        for checked in self._guns:
            if checked.type == gun.type:
                checked.add_ammo(gun.ammo)
                return
        self._guns.append(gun)

    # Other methods...

class Gun:
    def __init__(self, fire_rate, projectile, ammo, left_muzzle, right_muzzle, offset,
                 gun_type="default", image=None, image_file=""):
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

    # Other methods...

class Projectile:
    def __init__(self, collider, damage, speed, image_file="", image=None):
        self._image = image if image else pygame.image.load(image_file)
        self._image_rect = self._image.get_rect()
        self._collider = collider
        self._damage = damage
        self._speed = speed

    def new_projectile(self):
        return Projectile(copy.copy(self._collider), self._damage, self._speed, image=copy.copy(self._image))

    # Other methods...

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

# Other constants...