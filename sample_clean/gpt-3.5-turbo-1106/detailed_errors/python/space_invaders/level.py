# Refactored code
from enum import Enum, auto
from typing import List, Tuple
import copy

class ActionType(Enum):
    MOVE = auto()
    MOVE_FIRE = auto()
    SHOOT = auto()

class Phase:
    def __init__(self, enemies: List[str], positions: List[Tuple[int, int]], speeds: List[int], actions: List[List[Tuple[str, List]]]):
        self.enemies = enemies
        self.positions = positions
        self.initialized = False
        self.speeds = speeds
        self.actions = copy.deepcopy(actions)
        self.enemies_list = []

    def initialize(self):
        for i in range(len(self.enemies)):
            enemy = spawn_entity(self.enemies[i], self.positions[i], self.speeds[i], self.actions[i])
            if enemy is not None:
                self.enemies_list.append(enemy)
        self.initialized = True

    def create_new(self):
        return Phase(self.enemies, self.positions, self.speeds, copy.deepcopy(self.actions))

    def execute_all_actions(self):
        for enemy in self.enemies_list[:]:
            if enemy.alive() and enemy.image_rect.center[1] < WINDOW_HEIGHT + 100:
                enemy.execute_next_action()
            else:
                self.enemies_list.remove(enemy)

    def is_over(self):
        if self.initialized:
            if len(self.enemies_list) == 0:
                return True
            for enemy in self.enemies_list:
                if enemy.image_rect.center[1] < WINDOW_HEIGHT + 100:
                    return False
            return True
        return False

class Level:
    def __init__(self, phases: List[Phase], player_ship: str, player_spawn_position: Tuple[int, int], player_speed: int, spawned_weapons: List[str], level_text: Tuple[str, str]):
        self.phases = phases
        self.player_ship = player_ship
        self.player_spawn_position = player_spawn_position
        self.player_speed = player_speed
        self.spawned_weapons = spawned_weapons
        self.level_text = level_text

    def create_new(self):
        new_phases = [phase.create_new() for phase in self.phases]
        return Level(new_phases, self.player_ship, self.player_spawn_position, self.player_speed, self.spawned_weapons, self.level_text)

    def spawn_player(self):
        return spawn_entity(self.player_ship, self.player_spawn_position, self.player_speed)

    def execute_phase(self):
        if not self.is_complete():
            if not self.phases[0].initialized:
                self.phases[0].initialize()

            if self.phases[0].is_over():
                self.phases.remove(self.phases[0])
            else:
                self.phases[0].execute_all_actions()

    def is_complete(self):
        return len(self.phases) == 0

def shoot_actions(duration_in_seconds=1/60):
    return [("shoot", [])] * int(60 * duration_in_seconds)

def go_towards_actions(position: Tuple[int, int], target: Tuple[int, int], speed: int, fire: bool = False) -> List[Tuple[str, List]]:
    actions = []
    while abs(position[0] - target[0]) > 0.01 or abs(position[1] - target[1]) > 0.01:
        diff = (target[0] - position[0], target[1] - position[1])
        ease_x = ease_y = move_x = move_y = 0

        if diff[0] < 0:
            ease_x = min(1.0, log2(abs(diff[0])))
            move_x = max(diff[0] / speed, -1.0)
        elif diff[0] > 0:
            ease_x = min(1.0, log2(diff[0]))
            move_x = min(diff[0] / speed, 1.0)

        if diff[1] < 0:
            ease_y = min(1.0, log2(abs(diff[1])))
            move_y = max(diff[1] / speed, -1.0)
        elif diff[1] > 0:
            ease_y = min(1.0, log2(diff[1]))
            move_y = min(diff[1] / speed, 1.0)

        move = (ActionType.MOVE_FIRE.name if fire else ActionType.MOVE.name, [(move_x * ease_x, move_y * ease_y)])
        actions.append(move)
        position = (position[0] + move_x * speed, position[1] + move_y * speed)
    return actions

initialized_arrays = False
enemies, entities = [], []

def initialize_global_arrays(entities_array: List, enemies_array: List):
    global entities, enemies, initialized_arrays
    entities, enemies = entities_array, enemies_array
    initialized_arrays = true

def spawn_entity(ship: str, position: Tuple[int, int], speed: int, actions=None):
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

# Constants defined using the above classes and functions

PHASE_TOKYO_DRIFT = Phase(
    [DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP],
    [(WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//2, -120), (2*WINDOW_WIDTH/3, -130)],
    [5, 5, 5],
    [
        go_towards_actions((WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//3 - 150, 130), 5, False)
        + go_towards_actions((WINDOW_WIDTH//3 - 150, 130), (WINDOW_WIDTH//3 - 50, 200), 5, True)
        + go_towards_actions((WINDOW_WIDTH//3 - 50, 200), (WINDOW_WIDTH//3 - 250, WINDOW_HEIGHT + 200), 5, True),

        go_towards_actions((WINDOW_WIDTH//2, -120), (WINDOW_WIDTH//2, 130), 5, False)
        + go_towards_actions((WINDOW_WIDTH//2, 130), (WINDOW_WIDTH//2, 185), 5, True)
        + go_towards_actions((WINDOW_WIDTH//2, 185), (WINDOW_WIDTH//2, WINDOW_HEIGHT + 200), 5, True),

        go_towards_actions((2*WINDOW_WIDTH/3, -130), (2*WINDOW_WIDTH/3 + 150, 130), 5, False)
        + go_towards_actions((2*WINDOW_WIDTH/3 + 150, 130), (2*WINDOW_WIDTH/3 + 50, 200), 5, True)
        + go_towards_actions((2*WINDOW_WIDTH/3 + 50, 200), (2*WINDOW_WIDTH/3 + 250, WINDOW_HEIGHT + 200), 5, True)
    ]
)

# Other phase constants created in a similar manner