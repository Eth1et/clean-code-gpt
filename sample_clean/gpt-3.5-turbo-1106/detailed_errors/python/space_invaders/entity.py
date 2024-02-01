class Alien(Entity):
    """A special Entity that has only 1 life and executes a series of predefined actions"""

    def __init__(self, ship, spawn_position, speed, actions):
        super().__init__(ship, spawn_position, speed, lives=1, looks_down=True)
        self._actions = actions

    def execute_next_action(self):
        if self._actions:
            action = self._actions.pop(0)
            if action[0] == "shoot":
                self.shoot()
            elif action[0] == "move":
                self.move(action[1][0], clamp=False)
            elif action[0] == "move_fire":
                self.shoot()
                self.move(action[1][0], clamp=False)