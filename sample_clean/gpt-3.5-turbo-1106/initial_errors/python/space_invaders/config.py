import pygame
import os

class Configuration:
    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.MUSICS = ()
        self.score = 0
        self.LAUNCH_GAME = False
        self.SHOW_COLLIDERS = False
        self.WINDOW_WIDTH = 1400
        self.WINDOW_HEIGHT = 950
        self.EXPLOSION_DURATION = 4
        self.RESET_SWITCH_DELAY = 200
        self.PICKUP_SPEED = 5
        self.PICKUP_SPAWN_INTERVAL = (4, 8)
        self.CAPTION = "Space Invaders"
        self.BACKGROUND_IMAGE = self.get_path("Sprites", "background.png")

    def get_path(self, *args):
        return os.path.join(self.PATH, *args)

    def play_sound(self, sound_data, loops):
        if sound_data in self.MUSICS:
            pygame.mixer_music.load(sound_data[0], "muzsika")
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

    def get_credits_text(self):
        return (f"CONGRATULATIONS!\n"
                f"YOU HAVE SUCCESSFULLY BEATEN THE GAME!\n"
                f"FINAL SCORE:  {self.score}\n"
                f"\n"
                f"\n"
                f"SOUNDS\n"
                f"main-theme-song:   https://freesound.org/people/zagi2/sounds/340452/  -  zagi2\n"
                f"default-gun-sound:   https://freesound.org/people/flyingsaucerinvasion/sounds/615809/  -  flyingsaucerinvasion\n"
                f"minigun-sound:   https://freesound.org/people/Halgrimm/sounds/156895/  -  Halgrimm\n"
                f"rocket-sound:   https://freesound.org/people/inferno/sounds/18380/  -  inferno\n"
                f"defeat-sound:   https://freesound.org/people/landlucky/sounds/277403/  -  landlucky\n"
                f"win-sound:   https://freesound.org/people/jivatma07/sounds/122255/  -  jivatma07\n"
                f"hit-positive-sound:   https://freesound.org/people/ArtemBasov/sounds/427409/  -  ArtemBasov\n"
                f"hit-negative-sound:   https://freesound.org/people/strangehorizon/sounds/648200/  -  strangehorizon\n"
                f"explosion-sound:   https://freesound.org/people/JakeGwizdak/sounds/565481/  -  JakeGwizdak\n"
                f"pick-up-sound:   https://freesound.org/people/Jocabundus/sounds/678384/  -  Jocabundus\n"
                f"credits-music:   https://freesound.org/people/samueloak89/sounds/353775/  -  samueloak89\n"
                f"\n"
                f"FONTS\n"
                f"alien-invader-font:   https://www.dafont.com/alien-invader.font  -  Darrell Flood\n"
                f"agency-fb-font:  Builtin Windows Font  -  Bill Gates (I guess)\n"
                f"\n"
                f"ART\n"
                f"Bódi Martin (Z9WTNS)\n"
                f"\n"
                f"PROGRAMMING\n"
                f"Martin Bódi (h150714)\n"
                f"\n\n\n\n\n"
                f"--------------~ THE END ~--------------"
        )