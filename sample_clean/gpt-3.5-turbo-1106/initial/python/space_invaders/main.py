def update_pickups(pickups, window, player):
    for pickup in pickups[:]:
        if pickup.position[1] > WINDOW_HEIGHT + 55:
            pickups.remove(pickup)
        else:
            if pickup.collider.colliderect(player.collider):
                play_sound(SOUND_PICKUP_DATA, 0)
                pickup.action(player, *pickup.args)
                pickups.remove(pickup)
            else:
                pickup.move((0, PICKUP_SPEED))
                pickup.render(window)
                if SHOW_COLLIDERS:
                    pygame.draw.rect(window, (255, 0, 255), pickup.collider, 1)


def spawn_pickup(pickups, current_level):
    rnd = random.randint(0, 100)
    # ... (unchanged)
    pickups.append(spawned_pickup)


def get_pickup_image_by_gun(gun):
    if gun.type == "rocket":
        return PICKUP_ROCKET_GUN.image
    elif gun.type == "minigun":
        return PICKUP_MINIGUN.image
    else:
        return PICKUP_DEFAULT_GUN.image


def display_hud(player, enemies, window):
    # ... (unchanged)


def display_credits(window):
    # ... (unchanged)


def level_over(player, entities, level_index, LEVELS):
    if player.alive():
        play_sound(SOUND_VICTORY_DATA, 0)
        # ... (unchanged)
    else:
        play_sound(SOUND_DEFEAT_DATA, 0)
        # ... (unchanged)


def check_entity_collision(player_entity, enemy_entities):
    # ... (unchanged)


def handle_player_input(player_entity, max_x, max_y):
    # ... (unchanged)


def load_level(level):
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
    title = FONT152.render(current_level.level_text[0], True, (0, 255, 255))
    # ... (unchanged)
    return player, current_level


if LAUNCH_GAME:
    # INITIALIZATIONS
    # ... (unchanged)

    while True:
        if LEVEL_OVER:
            level_over(player, entities, level_index, LEVELS)
        # ... (unchanged)
        handle_player_input(player, WINDOW_WIDTH, WINDOW_HEIGHT)
        current_level.execute_phase()
        check_entity_collision(player, enemies)
        # ... (unchanged)