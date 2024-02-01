class Phase:
    def __init__(self, enemy_ships, positions, speeds, actions):
        self._enemy_ships = enemy_ships
        self._positions = positions
        self._initialized = False
        self._actions = copy.deepcopy(actions)
        self._speeds = speeds
        self._enemies = []

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

    def execute_phase(self):
        if not self.is_complete():
            if not self._phases[0].initialized:
                self._phases[0].initialize()
            if self._phases[0].is_over():
                self._phases.pop(0)
            else:
                self._phases[0].execute_all_actions()

    # ... (same as before)

def go_towards_actions(start, target, speed, fire=False):
    actions = []
    while abs(start[0] - target[0]) > 0.01 or abs(start[1] - target[1]) > 0.01:
        diff = (target[0] - start[0], target[1] - start[1])
        ease_x = log2(abs(diff[0])) if diff[0] != 0 else 0
        move_x = min(diff[0] / speed, 1) if diff[0] > 0 else max(diff[0] / speed, -1)
        ease_y = log2(abs(diff[1])) if diff[1] != 0 else 0
        move_y = min(diff[1] / speed, 1) if diff[1] > 0 else max(diff[1] / speed, -1)
        move_type = "move_fire" if fire else "move"
        actions.append((move_type, [(move_x * ease_x, move_y * ease_y)]))
        start = (start[0] + move_x * speed, start[1] + move_y * speed)
    return actions

# ... (same as before)

def initialize_global_arrays(entities_array, enemies_array):
    global entities, enemies, initialized_arrays
    entities, enemies = entities_array, enemies_array
    initialized_arrays = True

def spawn_entity(ship, position, speed, actions=None):
    if initialized_arrays:
        new_entity = Entity(ship, position, speed) if actions is None else Enemy(ship, position, speed, actions)
        entities.append(new_entity)
        if isinstance(new_entity, Enemy):
            enemies.append(new_entity)
        return new_entity

# ... (same as before)