import runpy
import space_invaders.config as config


def launch_game():
    print("3.. 2.. 1.. LAUNCH!")
    config.LAUNCH_GAME = True
    runpy.run_module("space_invaders.main")


if __name__ == '__main__':
    launch_game()