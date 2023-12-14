# Example file showing a circle moving on screen
import pygame
from GameEngine import GameEngine

pygame.init()


def main():
    game_engine = GameEngine()
    game_engine.run()


if __name__ == "__main__":
    main()

# TO DO:
# > array of moves - undo button
# > bot moves delay (for imersion (ig))
# addnotation to this -> if there will be a delay on bot move and
# player will spam undo button (which just back 2 last moves)
# he will undo his and bot move but then bot will do next move etc.
# just make player wait for bot to make his move - add (if not bot move) then undo ig guess
