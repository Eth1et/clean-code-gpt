class PickupType:
    LIFE = 96
    REPAIR = 87
    ROCKET_GUN = 80
    MINIGUN = 70
    FIRE_RATE_BOOSTER = 60
    MEDIUM_HEAL = 30

def spawn_pickup_type():
    rnd = random.randint(0, 100)
    if rnd > PickupType.LIFE:
        return PICKUP_LIFE
    elif rnd > PickupType.REPAIR:
        return PICKUP_REPAIR
    elif rnd > PickupType.ROCKET_GUN and ROCKET_GUN in current_level.spawned_weapons:
        return PICKUP_ROCKET_GUN
    elif rnd > PickupType.MINIGUN and MINIGUN in current_level.spawned_weapons:
        return PICKUP_MINIGUN
    elif rnd > PickupType.FIRE_RATE_BOOSTER:
        return PICKUP_FIRE_RATE_BOOSTER
    elif rnd > PickupType.MEDIUM_HEAL:
        return PICKUP_MEDIUM_HEAL
    else:
        return PICKUP_SMALL_HEAL

def update_pickups():
    global pickups, window, player
    player_poly = Polygon(player.collider)

    for pickup in list(pickups):
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

def check_entity_collision(player_entity, enemy_entities):
    player_poly = Polygon(player_entity.collider)
    for enemy in enemy_entities:
        enemy_poly = Polygon(enemy.collider)
        if player_poly.intersects(enemy_poly):
            play_sound(SOUND_ENEMY_HIT_DATA, 0)
            play_sound(SOUND_PLAYER_HIT_DATA, 0)
            enemy_hp = enemy.hp
            enemy.take_damage(player_entity.hp)
            player_entity.take_damage(enemy_hp)

def handle_player_input(player_entity: Entity, max_x, max_y):
    global CAN_SWITCH_GUN
    pressed_keys = pygame.key.get_pressed()
    vec = [0, 0]

    if pressed_keys[K_w]:
        vec[1] -= 0.65
    if pressed_keys[K_s]:
        vec[1] += 0.65
    if pressed_keys[K_a]:
        vec[0] -= 1
    if pressed_keys[K_d]:
        vec[0] += 1

    player_entity.move(vec)

    if player_entity.image_rect.left < 0:
        player_entity.move((-player_entity.image_rect.left/player_entity.speed, 0))
    elif player_entity.image_rect.right > max_x:
        player_entity.move(((max_x - player_entity.image_rect.right)/player_entity.speed, 0))
    if player_entity.image_rect.top < 0:
        player_entity.move((0, -player_entity.image_rect.top/player_entity.speed))
    elif player_entity.image_rect.bottom > max_y:
        player_entity.move((0, (max_y - player_entity.image_rect.bottom)/player_entity.speed))

    if pressed_keys[K_LSHIFT] and CAN_SWITCH_GUN:
        CAN_SWITCH_GUN = False
        player_entity.next_gun()
        pygame.time.set_timer(RESET_CAN_SWITCH, RESET_SWITCH_DELAY)
    if pressed_keys[K_SPACE]:
        player_entity.shoot()

def load_level(level):
    global current_level, player, entities, enemies, pickups, explosions
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
    title_shadow = FONT152.render(current_level.level_text[0], True, (255, 0, 255))
    text = FONT86.render(current_level.level_text[1], True, (200, 200, 200))
    text_shadow = FONT86.render(current_level.level_text[1], True, (50, 50, 50))

    window.fill((8, 8, 8))
    window.blit(title_shadow, (154, 255))
    window.blit(title, (150, 250))
    window.blit(text_shadow, (154, 424))
    window.blit(text, (150, 420))

    pygame.display.update()
    pygame.time.wait(2000)

    return player, current_level