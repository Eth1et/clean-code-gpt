import copy
from math import log2
from space_invaders.entity import Enemy
import space_invaders.spaceship as spaceship
from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT


class Phase:
    def __init__(self, enemies, positions, speeds, actions):
        self.enemies = enemies
        self.positions = positions
        self.initialized = False
        self.actions = copy.deepcopy(actions)
        self.speeds = speeds
        self.active_enemies = []

    def initialize(self):
        for i in range(len(self.enemies)):
            enemy = self._spawn_enemy(i)
            if enemy:
                self.active_enemies.append(enemy)
        self.initialized = True

    def _spawn_enemy(self, index):
        return spawn_entity(self.enemies[index], self.positions[index], self.speeds[index], self.actions[index])

    def execute_actions(self):
        for enemy in self.active_enemies[:]:
            if enemy.alive() and enemy.y_position < WINDOW_HEIGHT + 100:
                enemy.execute_next_action()
            else:
                self.active_enemies.remove(enemy)

    def is_complete(self):
        if not self.initialized:
            return False
        return all(enemy.y_position >= WINDOW_HEIGHT + 100 for enemy in self.active_enemies)


class Level:
    def __init__(self, phases, player_ship, spawn_position, speed, weapon_types, introduction):
        self.phases = phases
        self.player_ship = player_ship
        self.spawn_position = spawn_position
        self.player_speed = speed
        self.weapon_types = weapon_types
        self.introduction = introduction

    def spawn_player(self):
        return spawn_entity(self.player_ship, self.spawn_position, self.player_speed)

    def update(self):
        current_phase = self.phases[0]
        if not current_phase.initialized:
            current_phase.initialize()
        if current_phase.is_complete():
            self.phases.pop(0)
        else:
            current_phase.execute_actions()

    def is_complete(self):
        return not self.phases


def shoot(duration=1 / 60):
    return [("shoot", [])] * int(60 * duration)


def navigate_to(position, target, speed, shoot_while_moving=False):
    actions = []
    while not _positions_almost_equal(position, target):
        move = _calculate_move(position, target, speed)
        action = ("move_fire", move) if shoot_while_moving else ("move", move)
        actions.append(action)
        position = (position[0] + move[0] * speed, position[1] + move[1] * speed)
    return actions


def _positions_almost_equal(pos1, pos2, threshold=0.01):
    return abs(pos1[0] - pos2[0]) < threshold and abs(pos1[1] - pos2[1]) < threshold


def _calculate_move(from_pos, to_pos, speed):
    x_diff, y_diff = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
    ease_x, ease_y = _ease_value(x_diff), _ease_value(y_diff)
    move_x, move_y = speed * ease_x * _direction(x_diff), speed * ease_y * _direction(y_diff)

    return move_x, move_y


def _ease_value(diff):
    return min(1.0, log2(abs(diff)))


def _direction(value):
    return (value > 0) - (value < 0)


global_entities_initialized = False
entities, enemies = [], []


def initialize_global_entities(entities_list, enemies_list):
    global entities, enemies, global_entities_initialized
    entities, enemies = entities_list, enemies_list
    global_entities_initialized = True


def spawn_entity(ship, position, speed, actions=None):
    if not global_entities_initialized:
        return None
    entity_type = Enemy if actions else spaceship.Entity
    entity = entity_type(ship, position, speed, actions)
    entities.append(entity)
    if actions:
        enemies.append(entity)
    return entity


# Phase and Level instances can now be instantiated as needed using the defined classes and functions.
# Specific examples have been omitted here, but the `Phase` and `Level` objects can be created similarly
# to the original code, leveraging the classes and helper functions provided.