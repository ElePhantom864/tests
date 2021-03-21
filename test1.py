import pygame
import time

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First Game")

walkRight = [
    pygame.image.load('pygame1/L1.png'),
    pygame.image.load('pygame1/L2.png'),
    pygame.image.load('pygame1/L3.png'),
    pygame.image.load('pygame1/L4.png'),
]
walkLeft = [
    pygame.image.load('pygame1/R1.png'),
    pygame.image.load('pygame1/R2.png'),
    pygame.image.load('pygame1/R3.png'),
    pygame.image.load('pygame1/R4.png'),
]

bg = pygame.image.load('pygame1/Background.png')
char = pygame.image.load('pygame1/Idle.png')

bulletSound = pygame.mixer.Sound('pygame1/Bullet.wav')
hitSound = pygame.mixer.Sound('pygame1/Hurt.wav')
deathSound = pygame.mixer.Sound('pygame1/Death.wav')

music = pygame.mixer.music.load('pygame1/BG.mp3')
pygame.mixer.music.play(-1)

score = 0


class enemy(object):
    walkRight = [
        pygame.image.load('pygame1/LE1.png'),
        pygame.image.load('pygame1/LE2.png'),
        pygame.image.load('pygame1/LE3.png'),
        pygame.image.load('pygame1/LE4.png'),
    ]

    walkLeft = [
        pygame.image.load('pygame1/RE1.png'),
        pygame.image.load('pygame1/RE2.png'),
        pygame.image.load('pygame1/RE3.png'),
        pygame.image.load('pygame1/RE4.png'),
    ]

    def __init__(self, x, y, width, height, end, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y + 5, 28, 60)
        self.health = health
        self.oghealth = health
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 12:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 20, self.y + 5, 28, 60)
            pygame.draw.rect(win, (255, 0, 0),
                             ((self.hitbox[0] + (self.hitbox[2] / 2)) /
                              - ((5 * self.oghealth) // 2), self.hitbox[1] /
                              - 20, (5 * self.oghealth), 10))
            pygame.draw.rect(win, (0, 255, 0),
                             ((self.hitbox[0] + (self.hitbox[2] / 2)) /
                              - ((5 * self.oghealth) // 2), self.hitbox[1] /
                              - 20, (5 * self.oghealth) -
                              (5 * (self.oghealth - self.health)), 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
            self.hitbox = (0, 0, 0, 0)
            deathSound.play()


class player(object):
    def __init__(self, x, y, width, height):
        self.height = height
        self.x = x
        self.y = y
        self.width = width
        self.vel = 5
        self.left = False
        self.right = False
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.vulnerable = True
        self.invulnerable_until = 0

    def draw(self, win):
        if int(round(time.time() * 1000)) > self.invulnerable_until:
            self.invulnerable_until = 0
            self.vulnerable = True

        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if not self.vulnerable:
            pygame.draw.circle(
                win, (0, 0, 255), (self.x + (self.width / 2),
                                   self.y + (self.height / 2)), 30, width=3)

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            # win.blit(char, (self.x, self.y))
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y, 28, 60)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if not self.vulnerable:
            return
        self.walkCount = 0
        self.vulnerable = False
        self.invulnerable_until = int(round(time.time() * 1000)) + 3000

        font1 = pygame.font.SysFont('comicsans', 100)
        text1 = font1.render('HURT -5', 1, (255, 0, 0))
        win.blit(text1, (250 - (text1.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


clock = pygame.time.Clock()


def redrawGameWindow():

    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    for goblin in goblins:
        goblin.draw(win)
    Jeff.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()


run = True
font = pygame.font.SysFont('comicsans', 30, True)
Jeff = player(300, 435, 64, 64)
goblins = [enemy(100, 435, 64, 64, 450, 10), enemy(
    50, 435, 64, 64, 280, 10), enemy(75, 350, 64, 64, 300, 5)]
shootLoop = 0
bullets = []
# Main Task:
while run:
    clock.tick(12)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    for goblin in goblins:
        if Jeff.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and \
                Jeff.hitbox[1] + Jeff.hitbox[3] > goblin.hitbox[1]:
            if Jeff.hitbox[0] + Jeff.hitbox[2] > goblin.hitbox[0] and \
                    Jeff.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                if Jeff.vulnerable:
                    score -= 5
                Jeff.hit()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for bullet in bullets:
        for goblin in goblins:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] \
                    and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and \
                        bullet.x - bullet.radius < \
                        goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
                    score += 1
                    hitSound.play()

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if Jeff.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(
                projectile(round(Jeff.x + Jeff.width // 2),
                           round(Jeff.y + Jeff.height // 2), 4, (0, 0, 0),
                           facing))
            bulletSound.play()
        shootLoop = 1

    if keys[pygame.K_LEFT]:
        Jeff.x -= Jeff.vel
        Jeff.left = True
        Jeff.right = False
        Jeff.standing = False
        if Jeff.x < 1:
            Jeff.x = 1
    elif keys[pygame.K_RIGHT]:
        Jeff.x += Jeff.vel
        Jeff.left = False
        Jeff.right = True
        Jeff.standing = False
        if Jeff.x > 499-Jeff.width:
            Jeff.x = 499-Jeff.width
    else:
        Jeff.standing = True
        Jeff.walkCount = 0
    if not(Jeff.isJump):
        # if keys[pygame.K_UP]:
        #     y -= vel
        #     if y < 1:
        #         y = 1
        # if keys[pygame.K_DOWN]:
        #     y += vel
        #     if y > 499-height:
        #         y = 499-height
        if keys[pygame.K_UP]:
            Jeff.isJump = True
    else:
        if Jeff.jumpCount >= -10:
            neg = 1
            if Jeff.jumpCount < 0:
                neg = -1
            Jeff.y -= (Jeff.jumpCount ** 2) * 0.5 * neg
            Jeff.jumpCount -= 1
        else:
            Jeff.isJump = False
            Jeff.jumpCount = 10

    redrawGameWindow()

    # win.fill((255, 255, 255))

    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    # pygame.display.update()

pygame.quit()
