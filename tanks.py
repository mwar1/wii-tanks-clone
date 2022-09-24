import pygame, globals, vector, sprite
from math import atan, pi
pygame.init()

bulletImg = pygame.image.load("res/images/bullet.png")
bulletImgW = bulletImg.get_width()
bulletImgH = bulletImg.get_height()
bulletImg = pygame.transform.scale(bulletImg, (bulletImgW * globals.BULLET_SCALE, bulletImgH * globals.BULLET_SCALE))
bulletImgW = bulletImg.get_width()
bulletImgH = bulletImg.get_height()

bombsSheet = pygame.image.load("res/images/bomb.png")
bombParts = sprite.splitSpriteSheet(bombsSheet, [(0, 0, 17, 10),
                                                 (0, 10, 17, 10)],
                                    globals.BOMB_SCALE)

tanksSheet = pygame.image.load("res/images/tanks.png")
tankParts = sprite.splitSpriteSheet(tanksSheet, [(0, 0, 12, 7), (0, 7, 9, 5),    ## Red tank
                                                 (12, 0, 12, 7), (12, 7, 9, 5),  ## Green tank
                                                 (24, 0, 12, 7), (24, 7, 9, 5),  ## Grey tank
                                                 (36, 0, 12, 7), (36, 7, 9, 5),  ## White tank
                                                 (48, 0, 12, 7), (48, 7, 9, 5)], ## Blue tank
                                    globals.TANK_SCALE)

explosionSheet = pygame.image.load("res/images/bomb_explosion.png")
explParts = sprite.splitSpriteSheet(explosionSheet, [(0, 0, 44, 41),
                                                     (44, 0, 34, 42),
                                                     (78, 0, 38, 41),
                                                     (116, 0, 26, 41)],
                                    globals.EXPLOSION_SCALE)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, delay):
        super().__init__()

        self.x = x
        self.y = y
        self.frames = explParts
        self.delay = delay

        self.timer = delay
        self.frameIndex = 0
        self.w = 0
        self.h = 0

        for frame in self.frames:
            dim = frame.get_size()
            if dim[0] > self.w:
                self.w = dim[0]
            if dim[1] > self.h:
                self.h = dim[1]

        # TODO: Adjust radius properly so appropriate tanks die
        self.radius = self.w / 2 if self.w > self.h else self.h / 2
        self.radius += 35
        self.centre = vector.Vector2(self.x + self.radius, self.y + self.radius)
        #self.centre.x -= 50
        #self.centre.y -= 50

        self.image = pygame.Surface([self.w, self.h])
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.image.fill((0, 0, 0))
        self.image.blit(self.frames[self.frameIndex], (0, 0))

    def step(self, dt):
        dt *= 100
        self.timer -= dt

        if self.timer <= 0:
            if self.frameIndex < len(self.frames) - 1:
                self.frameIndex += 1
                self.timer = self.delay

                self.image.fill((0, 0, 0))
                self.image.blit(self.frames[self.frameIndex], (0, 0))
            else:
                return False
        return True

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, timer):
        super().__init__()

        self.x = x
        self.y = y
        self.timer = timer
        self.delay = 300
        self.interTimer = self.delay
        self.state = 0

        self.image = pygame.Surface([17*globals.BOMB_SCALE, 10*globals.BOMB_SCALE])
        self.image.set_colorkey((0, 0, 0))

        self.image.fill((0, 0, 0))
        self.image.blit(bombParts[self.state], (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def step(self, dt):
        dt *= 100
        self.timer -= dt
        self.interTimer -= dt
        if self.interTimer <= 0:
            self.changeState((self.state + 1) % 2)
            self.interTimer = self.delay


        if self.timer <= 1500:
            self.delay = 100

        if self.timer <= 0:
            return False
        return True

    def changeState(self, newState):
        ## Change colour to red if 1, green if 0
        self.state = newState
        self.image.fill((0, 0, 0))
        if newState == 0:
            self.image.blit(bombParts[0], (0, 0))
        elif newState == 1:
            self.image.blit(bombParts[1], (0, 0))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction, owner):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.owner = owner

        self.bounces = 3
        self.lastCollision = pygame.time.get_ticks()
        self.lastBox = -1

        self.dim = bulletImgW if bulletImgW > bulletImgH else bulletImgH
        self.image = pygame.Surface([self.dim, self.dim])
        self.image.set_colorkey((0, 0, 0))

        self.image.fill((0, 0, 0))
        newImg = pygame.transform.rotate(bulletImg, -1*atan(self.direction.y/self.direction.x) * 180/pi)
        self.image.blit(newImg, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def step(self, dt, levelBoxes):
        collision = False
        currentTime = pygame.time.get_ticks()

        ## Move in the x-direction
        self.x += self.speed * self.direction.x * dt
        self.rect.x = self.x
        #print(currentTime, self.lastCollision)
        for box in levelBoxes:
            if currentTime - self.lastCollision > 5:
                if self.rect.colliderect(box.rect) and self.bounces > 0 and self.lastBox != box:
                    self.direction.x *= -1
                    self.lastBox = box
                    self.updateImage()
                    collision = True
                    self.lastCollision = currentTime

        ## Move in the y-direction
        self.y += self.speed * self.direction.y * dt
        self.rect.y = self.y
        for box in levelBoxes:
            if currentTime - self.lastCollision > 5:
                if self.rect.colliderect(box.rect) and self.bounces > 0 and self.lastBox != box:
                    self.direction.y *= -1
                    self.lastBox = box
                    self.updateImage()
                    collision = True
                    self.lastCollision = currentTime

        if collision:
            self.bounces -= 1
            self.lastCollision = currentTime
        return self.bounces > 0

    def updateImage(self):
        self.image.fill((0, 0, 0))
        angle = vector.angle(self.direction, vector.Vector2(1, 0))
        if self.direction.y > 0:
            angle *= -1
        newImg = pygame.transform.rotate(bulletImg, angle * 180/pi)
        self.image.blit(newImg, (0, 0))

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, tankType):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = speed
        self.tankType = tankType
        self.velocity = vector.Vector2(0, 0)
        self.turretDirection = vector.Vector2(0, 0)
        self.bodyDirection = vector.Vector2(0, 0)
        self.bodyImg = tankParts[self.tankType*2]
        self.barrelImg = tankParts[self.tankType*2+1]
        self.alive = True

        self.image = pygame.Surface([14*globals.TANK_SCALE+10, 7*globals.TANK_SCALE+10])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.image.blit(tankParts[self.tankType*2], (0, 0))
        self.image.blit(tankParts[self.tankType*2+1], (3*globals.TANK_SCALE, 1*globals.TANK_SCALE))

    def shoot(self, direction, index):
        return Bullet(self.x, self.y, 45, direction, index)

    def updateVelocity(self, delta):
        self.velocity = vector.set(delta)
        self.bodyDirection = delta
        self.bodyDirection.normalise()
        if self.bodyDirection.x != 0:
            self.bodyImg = pygame.transform.rotate(tankParts[self.tankType*2], -1*atan(self.bodyDirection.y/self.bodyDirection.x) * 180/pi)
        else:
            self.bodyImg = tankParts[self.tankType*2]
        self.updateImage()

    def step(self, dt, obstacles):
        ## Move in x-direction
        self.x += self.velocity.x * self.speed * dt
        self.rect.x = self.x
        for box in obstacles:
            if self.rect.colliderect(box.rect):
                if self.rect.x < box.rect.x:
                    self.rect.right = box.rect.left
                else:
                    self.rect.left = box.rect.right
                self.x = self.rect.x

        ## Move in y-direction
        self.rect.y = self.y
        self.y += self.velocity.y * self.speed * dt
        for box in obstacles:
            if self.rect.colliderect(box.rect):
                if self.rect.y < box.rect.y:
                    self.rect.bottom = box.rect.top
                else:
                    self.rect.top = box.rect.bottom
                self.y = self.rect.y

    def updateImage(self):
        self.image.fill((0, 0, 0))
        self.image.blit(self.bodyImg, (0, 0))
        self.image.blit(self.barrelImg, (3*globals.TANK_SCALE, 1*globals.TANK_SCALE))

    def isDead(self, bullets, explosions, index):
        # TODO: Should be able to kill self, only after bullet has left,
        # Offset bullet so it never collides in the first place?
        for bul in bullets:
            if self.rect.colliderect(bul.rect) and bul.owner != index:
                self.alive = False
                return True

        for e in explosions:
            for side in [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]:
                if (side[0] - e.centre.x)**2 + (side[1] - e.centre.y)**2 < e.radius**2:
                    return True

        return False

class Player(Tank):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, 4)

    def adjustBarrel(self, mousex, mousey):
        mouseToTank = vector.Vector2(mousex - self.x, mousey - self.y)
        if mouseToTank.x != 0:
            self.barrelImg = pygame.transform.rotate(tankParts[self.tankType*2+1], -1*atan(mouseToTank.y/mouseToTank.x) * 180/pi)
        else:
            self.barrelImg = tankParts[self.tankType*2+1]
        self.updateImage()

class Enemy(Tank):
    def __init__(self, x, y, speed, tankType):
        super().__init__(x, y, speed, tankType)

    def adjustBarrel(self, mousex, mousey):
        pass
