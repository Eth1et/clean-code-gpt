class SoundData:
    def __init__(self, sound_path, volume, fadeout):
        self.sound_path = sound_path
        self.volume = volume
        self.fadeout = fadeout


class CreditsFontData:
    def __init__(self, font_path, font_size):
        self.font_path = font_path
        self.font_size = font_size


class Config:
    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.MUSICS = (SOUND_MAIN_THEME_DATA, SOUND_CREDITS_DATA)
        self.EXPLOSION_DURATION = 4
        self.RESET_SWITCH_DELAY = 200
        self.PICKUP_SPEED = 5
        self.PICKUP_SPAWN_INTERVAL = (4, 8)
        self.score = 0
        self.LAUNCH_GAME = False
        self.SHOW_COLLIDERS = False
        self.WINDOW_WIDTH = 1400
        self.WINDOW_HEIGHT = 950
        self.CAPTION = "Space Invaders"
        self.BACKGROUND_IMAGE = get_path("Sprites", "background.png")

        self.FONT_CREDITS_TITLE_DATA = CreditsFontData(get_path("Fonts", "AGENCYB.TTF"), 35)
        self.FONT_CREDITS_TEXT_DATA = CreditsFontData(get_path("Fonts", "AGENCYR.TTF"), 27)
        self.FONT152_DATA = CreditsFontData(get_path("Fonts", "Alien Invader.ttf"), 152)
        self.FONT86_DATA = CreditsFontData(get_path("Fonts", "Alien Invader.ttf"), 86)
        self.FONT36_DATA = CreditsFontData(get_path("Fonts", "Alien Invader.ttf"), 36)
        self.FONT25_DATA = CreditsFontData(get_path("Fonts", "Alien Invader.ttf"), 25)
        self.FONT15_DATA = CreditsFontData(get_path("Fonts", "Alien Invader.ttf"), 15)

    def get_path(self, *args):
        return os.path.join(self.PATH, *args)

    def play_sound(self, sound_data, loops):
        if sound_data in self.MUSICS:
            pygame.mixer_music.load(sound_data.sound_path)
            pygame.mixer_music.set_volume(sound_data.volume)
            pygame.mixer_music.fadeout(sound_data.fadeout)
            pygame.mixer_music.play(loops=loops)
            return

        sound = pygame.mixer.Sound(sound_data.sound_path)
        sound.set_volume(sound_data.volume)
        sound.fadeout(sound_data.fadeout)
        for i in range(pygame.mixer.get_num_channels()):
            if not pygame.mixer.Channel(i).get_busy():
                pygame.mixer.Channel(i).play(sound, loops=loops)
                break

    def get_credits_text(self):
        return f"""CONGRATULATIONS!
YOU HAVE SUCCESSFULLY BEATEN THE GAME!
FINAL SCORE:  {self.score}



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