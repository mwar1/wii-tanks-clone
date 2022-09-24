import pygame, globals
pygame.init()

woodBlockImg = pygame.image.load("res/images/wood_block.png")
blockSize = woodBlockImg.get_size()
woodBlockImg = pygame.transform.scale(woodBlockImg, (blockSize[0] * globals.BLOCK_SCALE, blockSize[1] * globals.BLOCK_SCALE))
blockSize = woodBlockImg.get_size()

breakableImg = pygame.image.load("res/images/breakable_block.png")
blockSize = breakableImg.get_size()
breakableImg = pygame.transform.scale(breakableImg, (blockSize[0] * globals.BLOCK_SCALE, blockSize[1] * globals.BLOCK_SCALE))
blockSize = breakableImg.get_size()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.w = blockSize[0]
        self.h = blockSize[1]
        self.breakable = False

        self.image = pygame.Surface([self.w, self.h])
        self.image.set_colorkey((0, 0, 0))

        self.image.fill((0, 0, 0))
        self.image.blit(woodBlockImg, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class BoundingBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.breakable = False

        self.image = pygame.Surface([self.w, self.h])

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.image.fill((125, 62, 0))

class BreakableObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.breakable = True

        self.image.fill((0, 0, 0))
        self.image.blit(breakableImg, (0, 0))

    def isDead(self, explosions):
        for e in explosions:
            for side in [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]:
                if (side[0] - e.centre.x)**2 + (side[1] - e.centre.y)**2 < e.radius**2:
                    return True
        return False

class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.Surface([blockSize[0], blockSize[1]])
        self.image.set_colorkey((0, 0, 0))

        self.image.fill((0, 0, 0))
        pygame.draw.ellipse(self.image, (0, 0, 0), (0, 0, blockSize[0], blockSize[1]))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
