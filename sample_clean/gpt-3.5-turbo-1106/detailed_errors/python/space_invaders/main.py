# Refactored code with clean code principles

# Import statements remain unchanged

# Function to update pickups
def update_pickups(player, pickups, window):
    player_poly = Polygon(player.collider)

    for pickup in pickups[:]:
        if pickup.position[1] > WINDOW_HEIGHT + 55:
            pickups.remove(pickup)
        else:
            pickup_poly = Polygon([
                pickup.collider.topleft, pickup.collider.topright,
                pickup.collider.bottomright, pickup.collider.bottomleft
            ])
            if pickup_poly.intersects(player_poly):
                play_sound(SOUND_PICKUP_DATA, 0)
                pickup.action(player, *pickup.args)
                pickups.remove(pickup)
            else:
                pickup.move((0, PICKUP_SPEED))
                pickup.render(window)
                if SHOW_COLLIDERS:
                    pygame.draw.rect(window, (255, 0, 255), pickup.collider, 1)


# Function to spawn pickup
def spawn_pickup(pickups, current_level):
    rnd = random.randint(0, 100)
    if rnd > 96:
        pickup_type = PICKUP_LIFE
    elif rnd > 87:
        pickup_type = PICKUP_REPAIR
    elif rnd > 80 and ROCKET_GUN in current_level.spawned_weapons:
        pickup_type = PICKUP_ROCKET_GUN
    elif rnd > 70 and MINIGUN in current_level.spawned_weapons:
        pickup_type = PICKUP_MINIGUN
    elif rnd > 60:
        pickup_type = PICKUP_FIRE_RATE_BOOSTER
    elif rnd > 30:
        pickup_type = PICKUP_MEDIUM_HEAL
    else:
        pickup_type = PICKUP_SMALL_HEAL

    spawn_location = (random.randint(50, WINDOW_WIDTH - 50), -60)
    spawned_pickup = pickup_type.new_pickup()
    spawned_pickup.position = spawn_location
    pickups.append(spawned_pickup)


# Function to handle player input
def handle_player_input(player_entity, max_x, max_y):
    global CAN_SWITCH_GUN, RESET_CAN_SWITCH
    pressed_keys = pygame.key.get_pressed()
    vec = [0, 0]
    # remaining logic remains unchanged


# Function to load level
def load_level(level):
    global entities, enemies, pickups, explosions, current_level, player, level_index
    entities = []
    enemies = []
    pickups = []
    explosions = []
    level.initialize_global_arrays(entities, enemies)

    previous_level = current_level
    current_level = level.create_new()
    if previous_level is None or not player.alive():
        player = current_level.spawn_player()
    else:
        entities.append(player)
        player.ship.empty_projectiles()
        player.heal(200000)
        player.ship.set_position(level.player_spawn_position)

    # Rendering text shown before the level starts
    # remaining logic remains unchanged
    return player, current_level


# Main game loop
if LAUNCH_GAME:
    # remaining logic remains unchanged