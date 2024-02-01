def display_credits():
    global window
    SPACES_TO_FAST_FORWARD = {pygame.K_SPACE, pygame.K_w, pygame.K_s}
    credits_text = get_credits_text()
    shift = 0
    while shift < int(window.get_height() * 3.05):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if any(pygame.key.get_pressed()[key] for key in SPACES_TO_FAST_FORWARD):
            shift += 10
        render_credits(window, credits_text, shift)
        shift += 1

    pygame.time.wait(1500)
    fade_window(window)
    pygame.time.wait(500)
    pygame.quit()
    exit()

def render_credits(window, credits_text, shift):
    window.fill((11, 11, 11))
    i = 0
    for line in credits_text.split('\n'):
        data = FONT_CREDITS_TITLE if line.isupper() else FONT_CREDITS_TEXT
        text = data.render(line, True, (255, 0, 255) if line.isupper() else (0, 255, 255))
        window.blit(text, (window.get_width() // 2 - text.get_width() // 2, window.get_height() + i * 70 - shift))
        i += 1
    pygame.display.update()
    clock.tick(60)

def get_pickup_image_by_gun(gun):
    match gun.type:
        case "rocket":
            return PICKUP_ROCKET_GUN.image
        case "minigun":
            return PICKUP_MINIGUN.image
        case _:
            return PICKUP_DEFAULT_GUN.image