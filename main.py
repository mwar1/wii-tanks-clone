import pygame, tanks, vector, globals, obstacle
pygame.init()

screen = pygame.display.set_mode((globals.SCREENWIDTH, globals.SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Wii Tanks Clone")

carryOn = True

allTanks = pygame.sprite.Group()
allTanks.add(tanks.Player(400, 400, 20), tanks.Enemy(200, 50, 20, 2))

bullets = pygame.sprite.Group()
bulletTimer = pygame.time.get_ticks()

bombs = pygame.sprite.Group()
bombTimer = pygame.time.get_ticks()

explosions = pygame.sprite.Group()

obstacles = pygame.sprite.Group()
for box in globals.boundingBoxes:
    obstacles.add(obstacle.BoundingBox(box[0], box[1], box[2], box[3]))
for i in range(0, 20, 2):
    obstacles.add(obstacle.Obstacle(i*66, 200))
    obstacles.add(obstacle.BreakableObstacle(i*66, 600))



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
            currentTime = pygame.time.get_ticks()

            if keysPressed[0]:
                ## Shoot a bullet
                if currentTime - bulletTimer > 250 and len(bullets.sprites()) < 5:
                    bulletTimer = pygame.time.get_ticks()
                    mouseToTank = vector.Vector2(mousex - (player.x + player.w/2), mousey - (player.y - player.h/2))
                    mouseToTank.normalise()
                    newBullet = player.shoot(mouseToTank, 0)
                    bullets.add(newBullet)
                    newBullet.updateImage()
            elif keysPressed[2]:
                ## Plant a bomb
                if currentTime - bombTimer > 400 and len(bombs.sprites()) < 2:
                    bombs.add(tanks.Bomb(player.x, player.y, 5000))
            elif keysPressed[1]:
                mouseToTank = vector.Vector2(mousex - player.x, mousey - player.y)
                mouseToTank.normalise()
                newBullet = player.shoot(mouseToTank, 0, isFast=True)
                bullets.add(newBullet)
                newBullet.updateImage()

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
        if not bul.step(dt, obstacles):
            bullets.remove(bul)

    for expl in explosions:
        if not expl.step(dt):
            explosions.remove(expl)

    for bomb in bombs:
        if not bomb.step(dt, bullets, explosions):
            bombs.remove(bomb)
            explosions.add(tanks.Explosion(bomb.x, bomb.y, 50))

    player.updateVelocity(playerMovement)
    for tank in allTanks:
        tank.adjustBarrel(mousex, mousey)
        tank.step(dt, obstacles)
        if tank.isDead(bullets, explosions, allTanks.sprites().index(tank)):
            allTanks.remove(tank)

    for obst in obstacles:
        if obst.breakable and obst.isDead(explosions):
            obstacles.remove(obst)

    screen.fill((0, 0, 0))

    bombs.draw(screen)
    explosions.draw(screen)
    obstacles.draw(screen)
    bullets.draw(screen)
    allTanks.draw(screen)
    s = pygame.Surface([allTanks.sprites()[0].w, allTanks.sprites()[0].h])
    s.set_alpha(100)
    s.fill((0, 255, 0))
    screen.blit(s, (allTanks.sprites()[0].x, allTanks.sprites()[0].y))

    pygame.display.flip()
    clock.tick()

pygame.quit()
