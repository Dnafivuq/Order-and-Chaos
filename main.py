# Example file showing a circle moving on screen
import pygame
from GameEngine import GameEngine

pygame.init()


def main():
    game_engine = GameEngine()
    game_engine.run()
    pygame.quit()


if __name__ == "__main__":
    main()
