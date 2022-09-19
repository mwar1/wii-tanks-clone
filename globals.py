import pygame

SCREENWIDTH = SCREENHEIGHT = 950
TANK_SCALE = 6
BOMB_SCALE = 3
EXPLOSION_SCALE = 2

boundingBoxes = [
                pygame.rect.Rect(0, 0, SCREENWIDTH, 2),
                pygame.rect.Rect(SCREENWIDTH-2, 0, 2, SCREENHEIGHT),
                pygame.rect.Rect(0, SCREENHEIGHT-2, SCREENWIDTH, 2),
                pygame.rect.Rect(0, 0, 2, SCREENHEIGHT)
                ]
