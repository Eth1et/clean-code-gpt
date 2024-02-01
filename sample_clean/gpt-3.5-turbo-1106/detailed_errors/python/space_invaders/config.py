SOUND_SPECS = {
    "main_theme": (get_path("Sounds", "340452__zagi2__dondolan2-loop.wav"), 0.5, 0),
    "default_gun": (get_path("Sounds", "615809__flyingsaucerinvasion__sci-fi-laser-blaster-shot-3.wav"), 0.15, 0),
    "minigun": (get_path("Sounds", "156895__halgrimm__a-shot.wav"), 0.9, 0),
    "rocket": (get_path("Sounds", "18380__inferno__hvrl.wav"), 0.6, 0),
    "defeat": (get_path("Sounds", "277403__landlucky__game-over-sfx-and-voice.wav"), 0.9, 0),
    "victory": (get_path("Sounds", "122255__jivatma07__level_complete.wav"), 1, 0),
    "enemy_hit": (get_path("Sounds", "427409__artembasov__ab_beep_or_blaster_shot.ogg"), 0.65, 0),
    "player_hit": (get_path("Sounds", "648200__strangehorizon__glitch_blip.wav"), 0.5, 0),
    "explosion": (get_path("Sounds", "565481__jakegwizdak__small-explosion.wav"), 0.4, 0),
    "pickup": (get_path("Sounds", "678384__jocabundus__item-pickup-v1.wav"), 0.7, 0),
    "credits": (get_path("Sounds", "353775__samueloak89__next-scene.mp3"), 0.7, 0)
}

MUSICS = (SOUND_SPECS["main_theme"], SOUND_SPECS["credits"])

# ...

FONT_SPECS = {
    "credits_title": (get_path("Fonts", "AGENCYB.TTF"), 35),
    "credits_text": (get_path("Fonts", "AGENCYR.TTF"), 27),
    "alien_invader_152": (get_path("Fonts", "Alien Invader.ttf"), 152),
    "alien_invader_86": (get_path("Fonts", "Alien Invader.ttf"), 86),
    "alien_invader_36": (get_path("Fonts", "Alien Invader.ttf"), 36),
    "alien_invader_25": (get_path("Fonts", "Alien Invader.ttf"), 25),
    "alien_invader_15": (get_path("Fonts", "Alien Invader.ttf"), 15)
}

# ...

def play_sound(sound_data, loops):
    """
    Plays a sound or music based on the given sound_data, and loops it 'loops' times
    @param sound_data the sound_data tuple that is selected from the constants defined in config
    @param loops the number of loops
    """
    if sound_data in MUSICS:
        music = pygame.mixer_music
        music.load(sound_data[0])
        music.set_volume(sound_data[1])
        music.fadeout(sound_data[2])
        music.play(loops=loops)
        return

    sound = pygame.mixer.Sound(sound_data[0])
    sound.set_volume(sound_data[1])
    sound.fadeout(sound_data[2])
    channels = pygame.mixer.get_num_channels()
    for i in range(channels):
        channel = pygame.mixer.Channel(i)
        if not channel.get_busy():
            channel.play(sound, loops=loops)
            break

# ...