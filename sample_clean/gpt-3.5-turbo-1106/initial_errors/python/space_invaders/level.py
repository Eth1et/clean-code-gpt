from space_invaders.entity import Entity, Enemy
from space_invaders.spaceship import DEFAULT_ENEMY_SHIP, DEFAULT_SHIP, MINIGUN, ROCKET_GUN
from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT
import copy

class Phase:
    def __init__(self, phase_enemies, positions, speeds, actions):
        self._enemy_ships = phase_enemies
        self._positions = positions
        self._initialized = False
        self._actions = copy.deepcopy(actions)
        self._speeds = speeds
        self._enemies = []

    @property
    def initialized(self):
        return self._initialized

    def initialize(self):
        for i in range(len(self._enemy_ships)):
            added_enemy = spawn_entity(self._enemy_ships[i], self._positions[i], self._speeds[i], self._actions[i])
            if added_enemy is not None:
                self._enemies.append(added_enemy)

        self._initialized = True

    def create_new(self):
        return Phase(self._enemy_ships, self._positions, self._speeds, copy.deepcopy(self._actions))

    def execute_all_actions(self):
        for enemy in self._enemies[:]:
            if enemy.alive() and enemy.image_rect.center[1] < WINDOW_HEIGHT + 100:
                enemy.execute_next_action()
            else:
                self._enemies.remove(enemy)

    def is_over(self):
        if self._initialized:
            if len(self._enemies) == 0:
                return True
            for enemy in self._enemies:
                if enemy.image_rect.center[1] < WINDOW_HEIGHT + 100:
                    return False
            return True
        return False

class Level:
    def __init__(self, phases, player_ship, player_spawn_position, player_speed, spawned_weapons, level_text):
        self._phases = phases
        self._player_ship = player_ship
        self._player_spawn_position = player_spawn_position
        self._player_speed = player_speed
        self._spawned_weapons = spawned_weapons
        self._level_text = level_text

    @property
    def level_text(self):
        return self._level_text

    @property
    def spawned_weapons(self):
        return self._spawned_weapons

    @property
    def player_spawn_position(self):
        return self._player_spawn_position

    def create_new(self):
        new_phases = [phase.create_new() for phase in self._phases]
        return Level(new_phases, self._player_ship, self._player_spawn_position, self._player_speed, self._spawned_weapons, self._level_text)

    def spawn_player(self):
        return spawn_entity(self._player_ship, self._player_spawn_position, self._player_speed)

    def execute_phase(self):
        if not self.is_complete():
            if not self._phases[0].initialized:
                self._phases[0].initialize()
            if self._phases[0].is_over():
                self._phases.pop(0)
            else:
                self._phases[0].execute_all_actions()

    def is_complete(self):
        return len(self._phases) == 0

def shoot_actions(duration_in_seconds=1/60):
    return [("shoot", [])] * int(60 * duration_in_seconds)

def go_towards_actions(position, target, speed, fire=False):
    actions = []
    while abs(position[0] - target[0]) > 0.01 or abs(position[1] - target[1]) > 0.01:
        diff = (target[0] - position[0], target[1] - position[1])
        ease_x = min(1.0, abs(log2(diff[0])))
        move_x = min(max(diff[0] / speed, -1.0), 1.0) if diff[0] != 0 else 0
        ease_y = min(1.0, abs(log2(diff[1])))
        move_y = min(max(diff[1] / speed, -1.0), 1.0) if diff[1] != 0 else 0
        move = ("move_fire" if fire else "move", [(move_x * ease_x, move_y * ease_y)])
        actions.append(move)
        position = (position[0] + move_x * speed, position[1] + move_y * speed)
    return actions

entities, enemies, initialized_arrays = [], [], False

def initialize_global_arrays(entities_array, enemies_array):
    global entities, enemies, initialized_arrays
    entities, enemies, initialized_arrays = entities_array, enemies_array, True

def spawn_entity(ship, position, speed, actions=None):
    if initialized_arrays:
        if actions is None:
            player = Entity(ship, position, speed)
            entities.append(player)
            return player
        else:
            enemy = Enemy(ship, position, speed, actions)
            entities.append(enemy)
            enemies.append(enemy)
            return enemy

PHASE_TOKYO_DRIFT = Phase(
    [DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP],
    [(WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//2, -120), (2*WINDOW_WIDTH//3, -130)],
    [5, 5, 5],
    [
        go_towards_actions((WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//3 - 150, 130), 5, False)
        + go_towards_actions((WINDOW_WIDTH//3 - 150, 130), (WINDOW_WIDTH//3 - 50, 200), 5, True)
        + go_towards_actions((WINDOW_WIDTH//3 - 50, 200), (WINDOW_WIDTH//3 - 250, WINDOW_HEIGHT + 200), 5, True),
        go_towards_actions((WINDOW_WIDTH//2, -120), (WINDOW_WIDTH//2, 130), 5, False)
        + go_towards_actions((WINDOW_WIDTH//2, 130), (WINDOW_WIDTH//2, 185), 5, True)
        + go_towards_actions((WINDOW_WIDTH//2, 185), (WINDOW_WIDTH//2, WINDOW_HEIGHT + 200), 5, True),
        go_towards_actions((2*WINDOW_WIDTH//3, -130), (2*WINDOW_WIDTH//3 + 150, 130), 5, False)
        + go_towards_actions((2*WINDOW_WIDTH//3 + 150, 130), (2*WINDOW_WIDTH//3 + 50, 200), 5, True)
        + go_towards_actions((2*WINDOW_WIDTH//3 + 50, 200), (2*WINDOW_WIDTH//3 + 250, WINDOW_HEIGHT + 200), 5, True)
    ]
)
# More PHASE_ objects with similar structure and arguments...

LEVEL_ONE = Level(
    [PHASE_SWEEP.create_new(), PHASE_TRIANGLE_TRIO.create_new(), PHASE_CENTER_LINE.create_new(),
        PHASE_SWEEP.create_new(), PHASE_TRIANGLE_TRIO.create_new(), PHASE_DOUBLE_SWEEP.create_new(),
        PHASE_SWEEP.create_new(), PHASE_TOKYO_DRIFT.create_new()],
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20, [],
    ("Level 1", "The Hard Beginning")
)
# More LEVEL_ objects with similar structure and arguments...