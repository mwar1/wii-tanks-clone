import pygame, tanks, vector, globals
pygame.init()

screen = pygame.display.set_mode((globals.SCREENWIDTH, globals.SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Wii Tanks Clone")

carryOn = True

allTanks = pygame.sprite.Group()
allTanks.add(tanks.Player(400, 400, 20), tanks.Enemy(200, 200, 20, 2))

bullets = pygame.sprite.Group()
bulletTimer = pygame.time.get_ticks()

bombs = pygame.sprite.Group()
bombs.add(tanks.Bomb(100, 500, 2000))

explosions = pygame.sprite.Group()

while carryOn:
    dt = clock.get_time()/100
    player = allTanks.sprites()[0]
    playerMovement = vector.Vector2(0, 0)
    mousex, mousey = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[27]:
            carryOn = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            keysPressed = pygame.mouse.get_pressed()
            if keysPressed[0]:
                ## Shoot a bullet
                player = allTanks.sprites()[0]
                currentTime = pygame.time.get_ticks()

                if currentTime - bulletTimer > 250 and len(bullets.sprites()) < 5:
                    bulletTimer = pygame.time.get_ticks()
                    mouseToTank = vector.Vector2(mousex - player.x, mousey - player.y)
                    mouseToTank.normalise()
                    newBullet = player.shoot(mouseToTank, 0)
                    bullets.add(newBullet)
            elif keysPressed[1]:
                ## Plant a bomb
                pass

    if pygame.key.get_pressed()[pygame.K_w]:
        playerMovement.add(vector.Vector2(0, -1))
    if pygame.key.get_pressed()[pygame.K_d]:
        playerMovement.add(vector.Vector2(1, 0))
    if pygame.key.get_pressed()[pygame.K_s]:
        playerMovement.add(vector.Vector2(0, 1))
    if pygame.key.get_pressed()[pygame.K_a]:
        playerMovement.add(vector.Vector2(-1, 0))

    if pygame.key.get_pressed()[pygame.K_b]:
        bombs.add(tanks.Bomb(mousex, mousey, 4000))

    for bul in bullets.sprites():
        if not bul.step(dt):
            bullets.remove(bul)

    for expl in explosions:
        if not expl.step(dt):
            explosions.remove(expl)

    for bomb in bombs:
        if not bomb.step(dt):
            bombs.remove(bomb)
            explosions.add(tanks.Explosion(bomb.x, bomb.y, 50))

    player.updateVelocity(playerMovement)
    for tank in allTanks:
        tank.adjustBarrel(mousex, mousey)
        tank.step(dt)
        if tank.isDead(bullets, explosions, allTanks.sprites().index(tank)):
            allTanks.remove(tank)

    screen.fill((0, 0, 0))
    for box in globals.boundingBoxes:
        pygame.draw.rect(screen, (125, 62, 0), box)
    allTanks.draw(screen)
    bullets.draw(screen)
    bombs.draw(screen)
    explosions.draw(screen)

    pygame.display.flip()
    clock.tick()

pygame.quit()
