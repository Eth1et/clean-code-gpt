import pygame
import os

# Configuration file containing globally used constants and functions

# Get the absolute path based on where the project is installed
PATH = os.path.dirname(os.path.abspath(__file__))

def get_path(*args):
    return os.path.join(PATH, *args)

# Define sound and music data
SOUND_MAIN_THEME_DATA = (get_path("Sounds", "340452__zagi2__dondolan2-loop.wav"), 0.5, 0)
SOUND_CREDITS_DATA = (get_path("Sounds", "353775__samueloak89__next-scene.mp3"), 0.7, 0)

MUSICS = (SOUND_MAIN_THEME_DATA, SOUND_CREDITS_DATA)

# Play sound or music based on the given data 
def play_sound(sound_data, loops):
    if sound_data in MUSICS:
        pygame.mixer_music.load(sound_data[0])
        pygame.mixer_music.set_volume(sound_data[1])
        pygame.mixer_music.fadeout(sound_data[2])
        pygame.mixer_music.play(loops=loops)
        return

    sound = pygame.mixer.Sound(sound_data[0])
    sound.set_volume(sound_data[1])
    sound.fadeout(sound_data[2])
    for i in range(pygame.mixer.get_num_channels()):
        if not pygame.mixer.Channel(i).get_busy():
            pygame.mixer.Channel(i).play(sound, loops=loops)
            break


# Define font data
def get_font_data(font_name, font_size):
    return (get_path("Fonts", font_name), font_size)

FONT_CREDITS_TITLE_DATA = get_font_data("AGENCYB.TTF", 35)
FONT_CREDITS_TEXT_DATA = get_font_data("AGENCYR.TTF", 27)
FONT152_DATA = get_font_data("Alien Invader.ttf", 152)
FONT86_DATA = get_font_data("Alien Invader.ttf", 86)
FONT36_DATA = get_font_data("Alien Invader.ttf", 36)
FONT25_DATA = get_font_data("Alien Invader.ttf", 25)
FONT15_DATA = get_font_data("Alien Invader.ttf", 15)

# Define other constants
EXPLOSION_DURATION = 4
RESET_SWITCH_DELAY = 200
PICKUP_SPEED = 5
PICKUP_SPAWN_INTERVAL = (4, 8)
score = 0
LAUNCH_GAME = False
SHOW_COLLIDERS = False
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 950
CAPTION = "Space Invaders"
BACKGROUND_IMAGE = get_path("Sprites", "background.png")

# Returns the credits string, with the updated score value
def get_credits_text():
    return f"""CONGRATULATIONS!
YOU HAVE SUCCESSFULLY BEATEN THE GAME!
FINAL SCORE:  {score}



SOUNDS
main-theme-song:   https://freesound.org/people/zagi2/sounds/340452/  -  zagi2
credits-music:   https://freesound.org/people/samueloak89/sounds/353775/  -  samueloak89

FONTS
alienvader-font:   https://www.dafont.com/alien-invader.font  -  Darrell Flood
agency-fb-font:  Builtin Windows Font  -  Bill Gates (I guess)

ART
Bódi Martin (Z9WTNS)

PROGRAMMING
Martin Bódi (h150714)
\n\n\n\n\n
--------------~ THE END ~--------------"""