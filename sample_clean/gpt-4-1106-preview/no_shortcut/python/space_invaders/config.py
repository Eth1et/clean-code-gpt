import pygame
import os

# Constants
PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Sound file paths and data
SOUND_FILES = {
    "main_theme": "340452__zagi2__dondolan2-loop.wav",
    "default_gun": "615809__flyingsaucerinvasion__sci-fi-laser-blaster-shot-3.wav",
    "minigun": "156895__halgrimm__a-shot.wav",
    "rocket": "18380__inferno__hvrl.wav",
    "defeat": "277403__landlucky__game-over-sfx-and-voice.wav",
    "victory": "122255__jivatma07__level_complete.wav",
    "enemy_hit": "427409__artembasov__ab_beep_or_blaster_shot.ogg",
    "player_hit": "648200__strangehorizon__glitch_blip.wav",
    "explosion": "565481__jakegwizdak__small-explosion.wav",
    "pickup": "678384__jocabundus__item-pickup-v1.wav",
    "credits": "353775__samueloak89__next-scene.mp3"
}
SOUND_DATA = {key: (os.path.join(PROJECT_DIRECTORY, "Sounds", file), volume, fade_out)
               for key, (file, volume, fade_out) in {
                   "main_theme": (SOUND_FILES["main_theme"], 0.5, 0),
                   "default_gun": (SOUND_FILES["default_gun"], 0.15, 0),
                   "minigun": (SOUND_FILES["minigun"], 0.9, 0),
                   "rocket": (SOUND_FILES["rocket"], 0.6, 0),
                   "defeat": (SOUND_FILES["defeat"], 0.9, 0),
                   "victory": (SOUND_FILES["victory"], 1, 0),
                   "enemy_hit": (SOUND_FILES["enemy_hit"], 0.65, 0),
                   "player_hit": (SOUND_FILES["player_hit"], 0.5, 0),
                   "explosion": (SOUND_FILES["explosion"], 0.4, 0),
                   "pickup": (SOUND_FILES["pickup"], 0.7, 0),
                   "credits": (SOUND_FILES["credits"], 0.7, 0)
               }.items()}

MUSIC_TRACKS = ("main_theme", "credits")

# Font size and font file constants
FONTS = {
    "credits_title": ("AGENCYB.TTF", 35),
    "credits_text": ("AGENCYR.TTF", 27),
    "alien_152": ("Alien Invader.ttf", 152),
    "alien_86": ("Alien Invader.ttf", 86),
    "alien_36": ("Alien Invader.ttf", 36),
    "alien_25": ("Alien Invader.ttf", 25),
    "alien_15": ("Alien Invader.ttf", 15)
}
FONT_DATA = {key: (os.path.join(PROJECT_DIRECTORY, "Fonts", file), size)
             for key, (file, size) in FONTS.items()}

# Gameplay configuration constants
EXPLOSION_DURATION = 4
RESET_SWITCH_DELAY = 200
PICKUP_SPEED = 5
PICKUP_SPAWN_INTERVAL = (4, 8)
score = 0

# Application window constants
LAUNCH_GAME = False
SHOW_COLLIDERS = False
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 950
CAPTION = "Space Invaders"
BACKGROUND_IMAGE = os.path.join(PROJECT_DIRECTORY, "Sprites", "background.png")


def play_sound(sound_key, loops):
    """
    Plays a sound or music based on the given sound_key, and loops it 'loops' times.
    :param sound_key: Key referencing a sound in the SOUND_DATA dictionary.
    :param loops: The number of loops.
    """
    sound_path, volume, fade_out = SOUND_DATA[sound_key]
    if sound_key in MUSIC_TRACKS:
        pygame.mixer_music.load(sound_path)
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.fadeout(fade_out)
        pygame.mixer_music.play(loops=loops)
    else:
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume)
        sound.fadeout(fade_out)
        for i in range(pygame.mixer.get_num_channels()):
            if not pygame.mixer.Channel(i).get_busy():
                pygame.mixer.Channel(i).play(sound, loops=loops)
                break


def get_credits_text():
    """
    Returns the credits string, with the updated score value.
    :return: The credits string.
    """
    return (
        f"CONGRATULATIONS!\n"
        f"YOU HAVE SUCCESSFULLY BEATEN THE GAME!\n"
        f"FINAL SCORE:  {score}\n\n\n"
        "SOUNDS\n"
        "main-theme-song:   https://freesound.org/people/zagi2/sounds/340452/  -  zagi2\n"
        "default-gun-sound:   https://freesound.org/people/flyingsaucerinvasion/sounds/615809/  -  flyingsaucerinvasion\n"
        "minigun-sound:   https://freesound.org/people/Halgrimm/sounds/156895/  -  Halgrimm\n"
        "rocket-sound:   https://freesound.org/people/inferno/sounds/18380/  -  inferno\n"
        "defeat-sound:   https://freesound.org/people/landlucky/sounds/277403/  -  landlucky\n"
        "win-sound:   https://freesound.org/people/jivatma07/sounds/122255/  -  jivatma07\n"
        "hit-positive-sound:   https://freesound.org/people/ArtemBasov/sounds/427409/  -  ArtemBasov\n"
        "hit-negative-sound:   https://freesound.org/people/strangehorizon/sounds/648200/  -  strangehorizon\n"
        "explosion-sound:   https://freesound.org/people/JakeGwizdak/sounds/565481/  -  JakeGwizdak\n"
        "pick-up-sound:   https://freesound.org/people/Jocabundus/sounds/678384/  -  Jocabundus\n"
        "credits-music:   https://freesound.org/people/samueloak89/sounds/353775/  -  samueloak89\n\n"
        "FONTS\n"
        "alien-invader-font:   https://www.dafont.com/alien-invader.font  -  Darrell Flood\n"
        "agency-fb-font:  Builtin Windows Font  -  Bill Gates (I guess)\n\n"
        "ART\n"
        "Bódi Martin (Z9WTNS)\n\n"
        "PROGRAMMING\n"
        "Martin Bódi (h150714)\n\n\n\n\n"
        "--------------~ THE END ~--------------"
    )