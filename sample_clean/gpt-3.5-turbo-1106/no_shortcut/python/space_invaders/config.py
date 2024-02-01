import pygame
import os

path = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(*relative_path):
    return os.path.join(path, *relative_path)


channel_count = 30
sound_main_theme_data = (get_absolute_path("Sounds", "340452__zagi2__dondolan2-loop.wav"), 0.5, 0)
sound_default_gun_data = (get_absolute_path("Sounds", "615809__flyingsaucerinvasion__sci-fi-laser-blaster-shot-3.wav"), 0.15, 0)
sound_minigun_data = (get_absolute_path("Sounds", "156895__halgrimm__a-shot.wav"), 0.9, 0)
sound_rocket_data = (get_absolute_path("Sounds", "18380__inferno__hvrl.wav"), 0.6, 0)
sound_defeat_data = (get_absolute_path("Sounds", "277403__landlucky__game-over-sfx-and-voice.wav"), 0.9, 0)
sound_victory_data = (get_absolute_path("Sounds", "122255__jivatma07__level_complete.wav"), 1, 0)
sound_enemy_hit_data = (get_absolute_path("Sounds", "427409__artembasov__ab_beep_or_blaster_shot.ogg"), 0.65, 0)
sound_player_hit_data = (get_absolute_path("Sounds", "648200__strangehorizon__glitch_blip.wav"), 0.5, 0)
sound_explosion_data = (get_absolute_path("Sounds", "565481__jakegwizdak__small-explosion.wav"), 0.4, 0)
sound_pickup_data = (get_absolute_path("Sounds", "678384__jocabundus__item-pickup-v1.wav"), 0.7, 0)
sound_credits_data = (get_absolute_path("Sounds", "353775__samueloak89__next-scene.mp3"), 0.7, 0)

musics = (sound_main_theme_data, sound_credits_data)


def play_sound(sound_data, loops):
    if sound_data in musics:
        pygame.mixer.music.load(sound_data[0])
        pygame.mixer.music.set_volume(sound_data[1])
        pygame.mixer.music.fadeout(sound_data[2])
        pygame.mixer.music.play(loops=loops)
        return

    sound = pygame.mixer.Sound(sound_data[0])
    sound.set_volume(sound_data[1])
    sound.fadeout(sound_data[2])
    for i in range(pygame.mixer.get_num_channels()):
        if not pygame.mixer.Channel(i).get_busy():
            pygame.mixer.Channel(i).play(sound, loops=loops)
            break


font_credits_title_data = (get_absolute_path("Fonts", "AGENCYB.TTF"), 35)
font_credits_text_data = (get_absolute_path("Fonts", "AGENCYR.TTF"), 27)
font152_data = (get_absolute_path("Fonts", "Alien Invader.ttf"), 152)
font86_data = (get_absolute_path("Fonts", "Alien Invader.ttf"), 86)
font36_data = (get_absolute_path("Fonts", "Alien Invader.ttf"), 36)
font25_data = (get_absolute_path("Fonts", "Alien Invader.ttf"), 25)
font15_data = (get_absolute_path("Fonts", "Alien Invader.ttf"), 15)

explosion_duration = 4
reset_switch_delay = 200
pickup_speed = 5
pickup_spawn_interval = (4, 8)
score = 0

launch_game = False

show_colliders = False
window_width = 1400
window_height = 950
caption = "Space Invaders"
background_image = get_absolute_path("Sprites", "background.png")


def get_credits_text():
    return f"""CONGRATULATIONS!
YOU HAVE SUCCESSFULLY BEATEN THE GAME!
FINAL SCORE:  {score}



SOUNDS
main-theme-song:   https://freesound.org/people/zagi2/sounds/340452/  -  zagi2
default-gun-sound:   https://freesound.org/people/flyingsaucerinvasion/sounds/615809/  -  flyingsaucerinvasion
minigun-sound:   https://freesound.org/people/Halgrimm/sounds/156895/  -  Halgrimm
rocket-sound:   https://freesound.org/people/inferno/sounds/18380/  -  inferno
defeat-sound:   https://freesound.org/people/landlucky/sounds/277403/  -  landlucky
win-sound:   https://freesound.org/people/jivatma07/sounds/122255/  -  jivatma07
hit-positive-sound:   https://freesound.org/people/ArtemBasov/sounds/427409/  -  ArtemBasov
hit-negative-sound:   https://freesound.org/people/strangehorizon/sounds/648200/  -  strangehorizon
explosion-sound:   https://freesound.org/people/JakeGwizdak/sounds/565481/  -  JakeGwizdak
pick-up-sound:   https://freesound.org/people/Jocabundus/sounds/678384/  -  Jocabundus
credits-music:   https://freesound.org/people/samueloak89/sounds/353775/  -  samueloak89

FONTS
alien-invader-font:   https://www.dafont.com/alien-invader.font  -  Darrell Flood
agency-fb-font:  Builtin Windows Font  -  Bill Gates (I guess)

ART
Bódi Martin (Z9WTNS)

PROGRAMMING
Martin Bódi (h150714)
\n\n\n\n\n
--------------~ THE END ~--------------"""