import pygame, globals, vector, sprite
from math import atan, pi
pygame.init()

bulletImg = pygame.image.load("res/images/bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (30, 30))
bulletImgW = bulletImg.get_width()
bulletImgH = bulletImg.get_height()

tanksSheet = pygame.image.load("res/images/tanks.png")
tankParts = sprite.splitSpriteSheet(tanksSheet, [(0, 0, 12, 7), (0, 7, 9, 5),    ## Red tank
                                                 (12, 0, 12, 7), (12, 7, 9, 5),  ## Green tank
                                                 (24, 0, 12, 7), (24, 7, 9, 5),  ## Grey tank
                                                 (36, 0, 12, 7), (36, 7, 9, 5),  ## White tank
                                                 (48, 0, 12, 7), (48, 7, 9, 5)]) ## Blue tank

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.bounces = 1
        self.lastCollision = -1

        self.image = pygame.Surface([bulletImgW, bulletImgH])
        self.image.set_colorkey((0, 0, 0))

        self.image.fill((0, 0, 0))
        newImg = pygame.transform.rotate(bulletImg, -1*atan(self.direction.y/self.direction.x) * 180/pi)
        self.image.blit(newImg, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def step(self, dt):
        self.x += self.speed * self.direction.x * dt
        self.y += self.speed * self.direction.y * dt
        self.rect.x = self.x
        self.rect.y = self.y

        for i in range(0, len(globals.boundingBoxes)):
            if self.rect.colliderect(globals.boundingBoxes[i]):
                if self.bounces > 0:
                    if i != self.lastCollision:
                        self.direction.x *= -1 if (i % 2 == 1) else 1
                        self.direction.y *= -1 if (i % 2 == 0) else 1
                        self.bounces -= 1
                        self.lastCollision = i

                    self.updateImage()
                else:
                    return False
        return True

    def updateImage(self):
        self.image.fill((0, 0, 0))
        newImg = pygame.transform.rotate(bulletImg, -1*atan(self.direction.y/self.direction.x) * 180/pi)
        self.image.blit(newImg, (0, 0))

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, tankType):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.tankType = tankType
        self.velocity = vector.Vector2(0, 0)
        self.alive = True

        self.image = pygame.Surface([14*globals.TANK_SCALE+10, 7*globals.TANK_SCALE+10])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.image.blit(tankParts[self.tankType*2], (0, 0))
        self.image.blit(tankParts[self.tankType*2+1], (3*globals.TANK_SCALE, 1*globals.TANK_SCALE))

    def shoot(self, direction):
        return Bullet(self.x, self.y, 75, direction)

    def updateVelocity(self, delta):
        self.velocity = vector.set(delta)

    def step(self, dt):
        self.x += self.velocity.x * self.speed * dt
        self.y += self.velocity.y * self.speed * dt
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self, barrelImg):
        self.image.fill((0, 0, 0))
        self.image.blit(tankParts[self.tankType*2], (0, 0))
        self.image.blit(barrelImg, (3*globals.TANK_SCALE, 1*globals.TANK_SCALE))

class Player(Tank):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, 4)

    def adjustBarrel(self, mousex, mousey):
        mouseToTank = vector.Vector2(mousex - self.x, mousey - self.y)
        if mouseToTank.x != 0:
            rotatedBarrel = pygame.transform.rotate(tankParts[self.tankType*2+1], -1*atan(mouseToTank.y/mouseToTank.x) * 180/pi)
        else:
            rotatedBarrel = tankParts[self.tankType*2+1]
        self.updateImage(rotatedBarrel)

class Enemy(Tank):
    def __init__(self, x, y, speed, tankType):
        super().__init__(x, y, speed, tankType)

    def adjustBarrel(self, mousex, mousey):
        pass
