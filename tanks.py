import pygame
pygame.init()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.image.fill((255, 0, 0))

    def step(self, dt):
        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt
        self.rect.x = self.x
        self.rect.y = self.y

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.alive = True

        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.image.fill((0, 255, 0))

    def shoot(self, direction):
        return Bullet(self.x, self.y, 1, direction)
