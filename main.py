import pygame
from GameEngine import GameEngine


def main():
    pygame.init()
    game_engine = GameEngine()
    game_engine.run()
    pygame.quit()


if __name__ == "__main__":
    main()
