import runpy

from space_invaders import config


def launch_space_invaders():
    """
    Launch Space Invaders game by running the main module.
    Sets the LAUNCH_GAME flag to True to enable the game's execution.
    """
    print("3.. 2.. 1.. LAUNCH!")
    config.LAUNCH_GAME = True
    runpy.run_module("space_invaders.main")


if __name__ == '__main__':
    launch_space_invaders()