import pygame

SCREENWIDTH = 1320
SCREENHEIGHT = 990
TANK_SCALE = 6
BULLET_SCALE = 2
BOMB_SCALE = 3
EXPLOSION_SCALE = 2
BLOCK_SCALE = 3

boundingBoxes = [
                pygame.rect.Rect(0, 0, SCREENWIDTH, 2),
                pygame.rect.Rect(SCREENWIDTH-2, 0, 2, SCREENHEIGHT),
                pygame.rect.Rect(0, SCREENHEIGHT-2, SCREENWIDTH, 2),
                pygame.rect.Rect(0, 0, 2, SCREENHEIGHT)
                ]
