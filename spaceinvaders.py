import pygame
import random

pygame.init()

WIDTH = 512
HEIGHT = 512
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")

run = True
clock = pygame.time.Clock()

BG = pygame.image.load("pygame1/BG.png")


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.spacePic = pygame.image.load("pygame1/Sample.png")
        self.standing = True
        self.left = False
        self.right = False
        self.bullets = []

    def draw(self, win):
        for bullet in self.bullets:
            if bullet.y > 0:
                bullet.y -= bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))
            bullet.draw(win)

        win.blit(self.spacePic, (self.x, self.y))

    def handle_events(self, keys):
        if keys[pygame.K_SPACE]:
            if len(self.bullets) < 1:
                x = round(Ship.x + Ship.width // 2)
                y = round(Ship.y + Ship.height // 2)
                projectile1 = projectile(x, y, radius=4, color=(0, 0, 0))
                self.bullets.append(projectile1)

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            if self.x < 1:
                self.x = 1

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            if self.x >= WIDTH - self.width:
                self.x = WIDTH - self.width


class enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemyPic = pygame.image.load("pygame1/Sample.png")

    def draw(self, win):
        win.blit(self.enemyPic, (self.x, self.y))


class EnemyController(object):
    def __init__(self):
        self.enemybullets = []
        self.enemy_width = 16
        self.enemy_height = 16
        self.enemies = []
        self.direction = 1
        self.velocity = 16
        self.timeLoop = 0
        self.timeInterval = 4
        self.Visible = True
        pos_x = 16
        for i in range(10):
            enemy1 = enemy(pos_x, 10)
            self.enemies.append(enemy1)
            pos_x += self.enemy_width + 16

    def draw(self, win):
        direction = self.direction
        move_down = False

        for enemybullet in self.enemybullets:
            if enemybullet.y < HEIGHT:
                enemybullet.y += enemybullet.vel
            else:
                self.enemybullets.pop(self.enemybullets.index(enemybullet))
            enemybullet.draw(win)

        for bullet in Ship.bullets:
            for enemy in self.enemies:
                if bullet.y - bullet.radius < enemy.y + self.enemy_height\
                        and bullet.y + bullet.radius > enemy.y:
                    if bullet.x - bullet.radius < enemy.x \
                        + self.enemy_width and bullet.x +\
                            bullet.radius > enemy.x:
                        self.enemies.pop(self.enemies.index(enemy))
                        Ship.bullets.pop(Ship.bullets.index(bullet))

        if self.timeLoop >= 0:
            self.timeLoop += 1
        if self.timeLoop == self.timeInterval:
            self.timeLoop = 0

        for enemy in self.enemies:
            if self.timeLoop == 0:
                enemy.x += self.velocity * direction
                if enemy.x >= WIDTH - self.enemy_width:
                    enemy.x = WIDTH - self.enemy_width
                    self.direction = self.direction * -1
                    move_down = True
                if enemy.x <= 0:
                    enemy.x = 0
                    self.direction = self.direction * -1
                    move_down = True
            enemy.draw(win)

        if move_down:
            for enemy in self.enemies:
                enemy.y += self.enemy_height

        random_enemies = random.choices(self.enemies, k=3)

        for enemy in random_enemies:
            if random.randrange(1, 101) == 1:
                x = round(enemy.x + self.enemy_width // 2)
                y = round(enemy.y + self.enemy_height // 2)
                self.enemybullets.append(projectile(
                    x, y, radius=4, color=(0, 0, 0)))


class projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class shield(object):
    pass


def redrawGameWindow():
    # win.blit(BG, (0, 0))
    pygame.draw.rect(win, (255, 255, 255), (0, 0, WIDTH, HEIGHT))
    Ship.draw(win)
    enemy_controller.draw(win)
    pygame.display.update()


Ship = player(120, 491, 16, 16)
enemy_controller = EnemyController()

while run:
    clock.tick(12)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    Ship.handle_events(keys)

    redrawGameWindow()
