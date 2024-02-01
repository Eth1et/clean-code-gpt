import random
import pygame
from pygame.locals import K_w, K_a, K_s, K_d, K_SPACE, K_LSHIFT, USEREVENT
from shapely.geometry import Polygon
from space_invaders.entity import Entity
from space_invaders.pickup import (
    PICKUP_LIFE, PICKUP_MINIGUN, PICKUP_REPAIR, PICKUP_ROCKET_GUN, PICKUP_SMALL_HEAL, PICKUP_MEDIUM_HEAL,
    PICKUP_FIRE_RATE_BOOSTER, Pickup, RESET_FIRE_RATE, PICKUP_DEFAULT_GUN
)
from space_invaders.spaceship import ROCKET_GUN, MINIGUN
from space_invaders.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, play_sound, PICKUP_SPEED, PICKUP_SPAWN_INTERVAL, SOUND_CREDITS_DATA, SOUND_EXPLOSION_DATA, 
    SOUND_MAIN_THEME_DATA, SOUND_DEFEAT_DATA, SOUND_VICTORY_DATA, SOUND_ENEMY_HIT_DATA, SOUND_PLAYER_HIT_DATA, SHOW_COLLIDERS, 
    get_credits_text, EXPLOSION_DURATION, RESET_SWITCH_DELAY, FONT_CREDITS_TEXT_DATA, FONT_CREDITS_TITLE_DATA, FONT_BIG_DATA, 
    FONT_MEDIUM_DATA, FONT_SMALL_DATA, FONT_EXTRA_SMALL_DATA, CHANNEL_COUNT, CAPTION, BACKGROUND_IMAGE, SOUND_PICKUP_DATA, LAUNCH_GAME
)
import space_invaders.config as config
import space_invaders.level as level_module


def move_pickups():
    global pickups, window, player
    player_shape = Polygon(player.collider)

    for pickup in pickups[:]:
        if pickup.position[1] > WINDOW_HEIGHT + 55:
            pickups.remove(pickup)
        else:
            pickup_shape = Polygon([pickup.collider.topleft, pickup.collider.topright,
                                    pickup.collider.bottomright, pickup.collider.bottomleft])
            if pickup_shape.intersects(player_shape):
                play_sound(SOUND_PICKUP_DATA, 0)
                pickup.apply(player, *pickup.args)
                pickups.remove(pickup)
            else:
                pickup.move((0, PICKUP_SPEED))
                pickup.render(window)
                if SHOW_COLLIDERS:
                    pygame.draw.rect(window, (255, 0, 255), pickup.collider, 1)


def create_pickup():
    global pickups, current_level

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

    spawn_position = (random.randint(50, WINDOW_WIDTH - 50), -60)
    new_pickup = pickup_type.new_pickup()
    new_pickup.position = spawn_position
    pickups.append(new_pickup)


def setup_pickup_spawn():
    pygame.time.set_timer(SPAWN_PICKUP, random.randint(
        int(PICKUP_SPAWN_INTERVAL[0]*1000), int(PICKUP_SPAWN_INTERVAL[1]*1000)
    ))


def fetch_gun_image(gun):
    return {
        "rocket": PICKUP_ROCKET_GUN.image,
        "minigun": PICKUP_MINIGUN.image
    }.get(gun.weapon_type, PICKUP_DEFAULT_GUN.image)


def show_hud():
    global player, enemies, window

    for enemy_ in enemies:
        position = (enemy_.image_rect.center[0], enemy_.image_rect.center[1] - 18)
        health_width = 90
        bar_height = 15
        bar_shift = 37
        
        pygame.draw.rect(window, (255, 50, 50), (position[0] - health_width/2, position[1] - bar_height//2 - bar_shift, health_width, bar_height))
        pygame.draw.rect(window, (50, 255, 50), (position[0] - health_width/2, position[1] - bar_height//2 - bar_shift,
                                                 health_width * enemy_.hp / enemy_.max_hp, bar_height))
        hp_rendered = FONT_EXTRA_SMALL.render(f"{enemy_.hp}", True, (25, 25, 20))
        window.blit(hp_rendered, (position[0] - bar_height//2, position[1] - bar_height//2 - bar_shift))

    # Player health and lives
    render_player_states(player, window)

    # Player ammo
    render_player_ammo(player, window)

    # Player Score
    show_score(config.score, window)


def show_credits():
    global window
    
    stop_music_start_sound(SOUND_CREDITS_DATA)
    scroll_images(window, clock, get_credits_text())

    pygame.time.wait(1500)
    fade_out(window, clock)
    quit_game()


def end_level():
    global LEVELS, LEVEL_OVER, level_index
    
    display_end_text()
    reset_level_end_state()

    if player.alive():
        proceed_to_next_level()
    else:
        load_first_level()


def check_collisions(ent1, ent_list):
    shape1 = Polygon(ent1.collider)

    for ent in ent_list:
        shape2 = Polygon(ent.collider)
        if shape1.intersects(shape2):
            handle_collision(ent1, ent)


def process_input(ent: Entity, max_x, max_y):
    global CAN_SWITCH, RESET_SWITCH
    perform_movement(ent, max_x, max_y)
    handle_other_inputs(ent)


def load_level(level):
    global current_level, player, entities, enemies, pickups, explosions
    reset_level_state()

    current_level = load_or_reset_player(level)
    display_level_info()

    return player, current_level


if LAUNCH_GAME:
    initialize()
    player, current_level = load_next_level()

    if player and current_level:
        queue_pickup_spawn()

        game_loop()