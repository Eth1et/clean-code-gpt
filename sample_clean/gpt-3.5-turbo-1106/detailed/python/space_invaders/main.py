class PickupSpawner:
    def __init__(self, pickups, current_level):
        self.pickups = pickups
        self.current_level = current_level

    def update_pickups(self):
        player_poly = Polygon(self.current_level.player.collider)

        for pickup in self.pickups[:]:
            if pickup.position[1] > WINDOW_HEIGHT + 55:
                self.pickups.remove(pickup)
            else:
                pickup_poly = Polygon([pickup.collider.topleft, pickup.collider.topright,
                                       pickup.collider.bottomright, pickup.collider.bottomleft])
                if pickup_poly.intersects(player_poly):
                    play_sound(SOUND_PICKUP_DATA, 0)
                    pickup.action(self.current_level.player, *pickup.args)
                    self.pickups.remove(pickup)
                else:
                    pickup.move((0, PICKUP_SPEED))
                    pickup.render(window)
                    if SHOW_COLLIDERS:
                        pygame.draw.rect(window, (255, 0, 255), pickup.collider, 1)

    def spawn_pickup(self):
        rnd = random.randint(0, 100)
        pickup_type = None
        if rnd > 96:
            pickup_type = PICKUP_LIFE
        elif rnd > 87:
            pickup_type = PICKUP_REPAIR
        # ... (continued from the original code)

    def spawn_at_random_interval(self):
        pygame.time.set_timer(SPAWN_PICKUP, random.randint(int(PICKUP_SPAWN_INTERVAL[0]*1000), int(PICKUP_SPAWN_INTERVAL[1]*1000)))


def get_pickup_image_by_gun(gun):
    if gun.type == "rocket":
        return PICKUP_ROCKET_GUN.image
    elif gun.type == "minigun":
        return PICKUP_MINIGUN.image
    else:
        return PICKUP_DEFAULT_GUN.image


class HUD:
    def __init__(self, player, enemies, window):
        self.player = player
        self.enemies = enemies
        self.window = window

    def display_hud(self):
        for enemy_ in self.enemies:
            # ... (continued from the original code)

    def display_credits(self):
        # ... (continued from the original code)

    def level_over(self):
        # ... (continued from the original code)


class GameLoop:
    def __init__(self, level, player):
        self.current_level = level
        self.player = player

    def load_level(self, level):
        # ... (continued from the original code, with minor changes)

    def handle_player_input(self):
        # ... (continued from the original code, with minor changes)

    def run_game_loop(self):
        # ... (continued from the original code)