import pygame, tanks
pygame.init()

SCREENWIDTH = SCREENHEIGHT = 950
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Wii Tanks Clone")

carryOn = True

allTanks = pygame.sprite.Group()
allTanks.add(tanks.Tank(50, 50))

bullets = pygame.sprite.Group()

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[27]:
            carryOn = False
        elif pygame.key.get_pressed()[32]:
            newBullet = allTanks.sprites()[0].shoot((1, 10))
            bullets.add(newBullet)

    dt = clock.get_time()/100
    for bul in bullets.sprites():
        bul.step(dt)


    screen.fill((0, 0, 0))
    allTanks.draw(screen)
    bullets.draw(screen)

    pygame.display.flip()
    clock.tick()

pygame.quit()
