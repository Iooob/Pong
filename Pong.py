import pygame, random, decimal, shelve, os
pygame.init()

run = True
screen = pygame.display.set_mode((400, 400))
def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class paddle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.score = 0
        self.rect = (x, y, w, h)

class ball(object):
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.xvel = speed[0]
        self.yvel = speed[1]

highscore = 0
try:
    save = shelve.open('Pong_SaveData')
    highscore = save['highScore']
    save.close()
except:
    print("Well, shit")
pygame.display.set_caption('Pong')
player = paddle(20, 150, 10, 100)
enemy = paddle(380, 150, 10, 100)
ball = ball(200, 200, 10, (1, 0.5))
ball.rect = pygame.draw.circle(screen, (0,0,0), (ball.x, ball.y), 10)
player.rect = pygame.draw.rect(screen, (0, 0, 0), (player.x, player.y, player.w, player.h))
enemy.rect = pygame.draw.rect(screen, (0, 0, 0), (enemy.x, enemy.y, enemy.w, enemy.h))
font = pygame.font.Font(resourcePath('Font/OstrichSans-Heavy.otf'), 30)
startText1 = font.render('Space to Start', True, (255, 255, 255), (0, 0, 0))
startText2 = font.render('High Score: ' + str(highscore), True, (255, 255, 255), (0, 0, 0))
playText1 = font.render(str(player.score), True, (255, 255, 255), (0, 0, 0))
playText2 = font.render(str(enemy.score), True, (255, 255, 255), (0, 0, 0,))
stRect1 = startText1.get_rect()
stRect1.center = (200, 40)
stRect2 = startText2.get_rect()
stRect2.center = (200, 70)
pRect1 = playText1.get_rect()
pRect1.center = (100, 40)
pRect2 = playText2.get_rect()
pRect2.center = (300, 40)
playing = False
hitObject = False
def drawScreen():
    playText1 = font.render(str(player.score), True, (255, 255, 255), (0, 0, 0))
    playText2 = font.render(str(enemy.score), True, (255, 255, 255), (0, 0, 0,))
    startText2 = font.render('High Score: ' + str(highscore), True, (255, 255, 255), (0, 0, 0))
    pygame.time.delay(3)
    screen.fill((0, 0, 0))
    if playing == False:
        screen.blit(startText1, stRect1)
        screen.blit(startText2, stRect2)
    if playing == True:
        screen.blit(playText1, pRect1)
        screen.blit(playText2, pRect2)
    dPlayer = pygame.draw.rect(screen, (255, 255, 255), (player.x, player.y, player.w, player.h), 1)
    dEnemy = pygame.draw.rect(screen, (255, 255, 255), (enemy.x, enemy.y, enemy.w, enemy.h), 1)
    dBall = pygame.draw.circle(screen, (255, 255, 255), (ball.x, ball.y), ball.size, 2)
    pygame.display.update()

def ballMove():
    ball.x, ball.y = ball.x + ball.xvel, ball.y + ball.yvel
    global hitObject
    global highscore
    if(ball.x > 410):
        player.score += 1
        if highscore < player.score:
            highscore = player.score
        ball.x = 200 
        ball.y = 200
        ball.xvel, ball.yvel = -(ball.xvel) / ball.xvel, float(decimal.Decimal(random.randrange(-5, 5)) / 100)
    if(ball.x < -10):
        enemy.score += 1
        ball.x = 200
        ball.y = 200
        ball.xvel, ball.yvel = ball.xvel / ball.xvel, float(decimal.Decimal(random.randrange(-5, 5)) / 100)
    if(pygame.Rect.colliderect(player.rect, ball.rect) == True) or (pygame.Rect.colliderect(enemy.rect, ball.rect) == True):
        if hitObject == False:
            ball.xvel = -(ball.xvel) + (float(decimal.Decimal(random.randrange(2, 3)) / 100))
            ball.yvel = -(ball.yvel) + (float(decimal.Decimal(random.randrange(-10, 10)) / 10))
            hitObject = True
    elif ball.y < 5 or ball.y > 395:
        if hitObject == False:
            ball.yvel = (-ball.yvel) + (ball.yvel / 100)
            hitObject = True
    else:
        hitObject = False

def enemyMove():
    if (ball.y - 50) > enemy.y and enemy.y < 300:
        enemy.y = enemy.y + 1
    elif ball.y < enemy.y and enemy.y > 0:
        enemy.y = enemy.y - 1


while run == True:
    ball.rect = pygame.draw.circle(screen, (0,0,0), (ball.x, ball.y), 10)
    player.rect = pygame.draw.rect(screen, (0, 0, 0), (player.x, player.y, player.w, player.h))
    enemy.rect = pygame.draw.rect(screen, (0, 0, 0), (enemy.x, enemy.y, enemy.w, enemy.h))
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if playing == True:
                    playing = False
                elif playing == False:
                    playing = True
    if playing == True:
        if key[pygame.K_DOWN] and player.y < 300 or key[pygame.K_s] and player.y < 300:
            player.y += 1
        if key[pygame.K_UP] and player.y > 0 or key[pygame.K_w] and player.y > 0:
            player.y -= 1
        ballMove()
        enemyMove()
    drawScreen()
save = shelve.open('Pong_SaveData')
save['highScore'] = highscore
save.close()
pygame.quit()
