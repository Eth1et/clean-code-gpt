import copy
import pygame
from shapely.geometry import Polygon
import space_invaders.config as config


class Spaceship:
    """
    Represents spaceships with a weapon
    """
    def __init__(self, guns, hp, collider, enemy, image_file="", image=None):
        """
        Either the image_file or the image must be set, if both set, the image is used
        @param guns a list of gun constants chosen from spaceship module
        @param hp the health points that the ship has
        @param collider a list of 2D tuple points that describe the polygon collider of the ship, must be convex
        @param enemy True if the ship is an enemy ship, false otherwise
        @param image_file source of an image file used as image for the ship
        @param image a pygame Surface (image) that is copied to be the image of the ship
        """
        self._image = image if image is not None else pygame.image.load(image_file)
        self._guns = guns if isinstance(guns, list) else [guns]
        self._active_gun = 0
        self._hp = hp
        self._image_rect = self._image.get_rect()
        self._collider_relative_vertices = copy.copy(collider)
        self._collider = collider
        self._enemy = enemy
        self._fire_rate_multiplier = 1
        self._projectiles = []

    def new_ship(self):
        """
        Creates a new instance of this ship with the same data but new references
        @return: the new instance
        """
        guns = [gun.new_gun() for gun in self._guns]
        shp = Spaceship(guns, self._hp, list(vertex for vertex in self._collider),
                        self._enemy, image=copy.copy(self._image))
        return shp

    def empty_projectiles(self):
        """Clears the projectiles list of the ship"""
        self._projectiles.clear()

    def add_ammo(self, gun):
        """
        Adds the gun to the gun collection of the ship, if already has a gun with the same type, then it adds the
        ammo count to the current ammo count
        @param gun a gun constant chosen from spaceship module
        """
        for checked in self._guns:
            if checked.type == gun.type:
                checked.add_ammo(gun.ammo)
                return
        self._guns.append(gun)

    def set_fire_rate_multiplier(self, multiplier):
        """@param multiplier the new multiplier, the smaller, the faster it shoots"""
        self._fire_rate_multiplier = multiplier

    def set_position(self, vec):
        """
        Sets the position of the ship to the given vector
        @param vec the new position (center)
        """
        self._image_rect.center = vec
        for i, vertex in enumerate(self._collider_relative_vertices):
            self._collider[i] = (vertex[0] + vec[0],
                                 vertex[1] + vec[1])
        for gun in self._guns:
            gun.set_position(vec)

    def move(self, vec):
        """
        Moves the ship by the given vector
        @param vec the move
        """
        self._image_rect.move_ip(vec[0], vec[1])
        for i, vertex in enumerate(self._collider_relative_vertices):
            self._collider[i] = (self._image_rect.center[0] + vertex[0],
                                 self._image_rect.center[1] + vertex[1])
        for gun in self._guns:
            gun.move(vec)

    def next_gun(self):
        """Cycles the selected gun to be the next available one"""
        self._active_gun += 1
        self._active_gun %= len(self._guns)
        self._guns[self._active_gun].set_position(self._image_rect.center)

    def shoot(self):
        """Creates a new projectile and stores it in the list of the ship's projectiles"""
        new_projectile = self._guns[self._active_gun].shoot(self._fire_rate_multiplier)
        if new_projectile is not None:
            self._projectiles.append(new_projectile)

    # ... (remaining methods and properties unchanged)