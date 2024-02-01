# Cleaned and refactored code

# ... (imports unchanged)

def update_pickups(player, pickups, window):
    for pickup in pickups[:]:
        if pickup.position[1] > WINDOW_HEIGHT + 55:
            pickups.remove(pickup)
        else:
            pickup_poly = Polygon(pickup.collider)
            if pickup_poly.intersects(Polygon(player.collider)):
                play_sound(SOUND_PICKUP_DATA, 0)
                pickup.action(player, *pickup.args)
                pickups.remove(pickup)
            else:
                pickup.move((0, PICKUP_SPEED))
                pickup.render(window)
                if SHOW_COLLIDERS:
                    pygame.draw.rect(window, (255, 0, 255), pickup.collider, 1)

def get_random_pickup_type():
    rnd = random.randint(0, 100)
    if rnd > 96:
        return PICKUP_LIFE
    elif rnd > 87:
        return PICKUP_REPAIR
    # ... (other conditions unchanged)

def spawn_pickup(pickups, current_level):
    pickup_type = get_random_pickup_type()
    spawn_location = (random.randint(50, WINDOW_WIDTH-50), -60)
    spawned_pickup = pickup_type.new_pickup()
    spawned_pickup.position = spawn_location
    pickups.append(spawned_pickup)

def spawn_at_random_interval():
    delay = random.randint(int(PICKUP_SPAWN_INTERVAL[0]*1000), int(PICKUP_SPAWN_INTERVAL[1]*1000))
    pygame.time.set_timer(SPAWN_PICKUP, delay)

def get_pickup_image_by_gun(gun):
    # ...

def display_hud(player, enemies, window):
    # ...

def display_credits(window):
    # ...

def level_over(player, enemies, window, LEVELS, level_index):
    # ...

def check_entity_collision(player, enemy_entities):
    # ...

def handle_player_input(player, max_x, max_y):
    # ...

def load_level(level, current_level, player, entities, enemies, pickups, explosions):
    # ...

# Main game loop
if LAUNCH_GAME:
    # INITIALIZATIONS
    pygame.init()
    # ... (other initializations unchanged)

    # Declaration of global arrays
    entities = []
    enemies = []
    pickups = []
    explosions = []

    # Loading the first level, and its player
    current_level = player = None
    player, current_level = load_level(LEVELS[0], current_level, player, entities, enemies, pickups, explosions)

    if player is not None and current_level is not None:
        # Queues a new pickup spawn
        spawn_at_random_interval()

        while True:
            if LEVEL_OVER:
                level_over(player, enemies, window, LEVELS, level_index)

            for event in pygame.event.get():
                # ... (handling events unchanged)

            handle_player_input(player, WINDOW_WIDTH, WINDOW_HEIGHT)
            current_level.execute_phase()
            check_entity_collision(player, enemies)
            # ... (rendering and updating display unchanged)