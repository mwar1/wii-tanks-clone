import pygame, globals
pygame.init()

def splitSpriteSheet(sheet, spriteRects, scale):
    ## Return a list of surfaces, using the 'spriteRects' to take
    ## parts of the original 'sheet'

    output = []
    for rect in spriteRects:
        sprite = pygame.Surface.subsurface(sheet, (rect[0], rect[1], rect[2], rect[3]))
        spriteSize = sprite.get_size()
        sprite = pygame.transform.scale(sprite, (spriteSize[0]*scale, spriteSize[1]*scale))
        output.append(sprite)

    return output
