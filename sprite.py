import pygame
import sys
import random
import os
vec = pygame.math.Vector2


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("Bullet.wav")

    def shoot(self):
        self.gunshot.play()
        hits = pygame.sprite.spritecollide(crosshair, target_group, False)
        for hit in hits:
            hit.death = True

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, images, pos_x, pos_y):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.pos = vec(pos_x, pos_y)
        self.rect.center = self.pos
        self.dir = -1
        self.image_count = 0
        self.current_image = 0
        self.death = False
        self.death_count = 0

    def update(self):
        self.image_count += 1
        if self.image_count >= 10:
            self.current_image += 1
            if self.current_image >= 3:
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.image_count = 0
        self.pos.y += 10 * self.dir
        if self.pos.y - 96 >= screen_height:
            self.kill()
        if self.pos.y + 96 <= 0:
            self.kill()
        self.rect.center = self.pos
        if self.death:
            self.dir = 0
            image = pygame.image.load("duck_hurt.png")
            self.image = pygame.transform.scale(image, (90, 90))
            self.death_count += 1
            if self.death_count >= 30:
                image = pygame.image.load("duck_fall.png")
                self.image = pygame.transform.scale(image, (45, 90))
                self.dir = 2


pygame.init()
clock = pygame.time.Clock()


screen_width = 1250
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
image_sky = pygame.image.load("onlysky.png").convert_alpha()
image_foreground = pygame.image.load("ducknobg.png").convert_alpha()

surface_sky = pygame.Surface((screen_width, screen_height))
surface_foreground = pygame.Surface((screen_width, screen_height))

pygame.mouse.set_visible(False)

# pygame.transform.scale(background,(screen_width,screen_height))
surface_sky.blit(image_sky, (0, 0))

# pygame.transform.scale(background2,(screen_width,screen_height))
surface_foreground.blit(image_foreground, (0, 0))


crosshair = Crosshair("crosshair_red_large.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

target_group = pygame.sprite.Group()
for target in range(2):
    images = []
    for i in range(1, 4):
        image_path = "duck"
        image = pygame.image.load(image_path + str(i) + ".png")
        image = pygame.transform.scale(image, (96, 93))
        images.append(image)
    new_target = Target(images, random.randrange(0,
                                                 screen_width),
                        screen_height - 48)
    target_group.add(new_target)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

    pygame.display.flip()
    screen.blit(surface_sky, (0, 0))
    # screen.blit(surface_foreground,(0, 0))
    target_group.draw(screen)
    target_group.update()
    crosshair_group.draw(screen)
    crosshair_group.update()
    if len(target_group) == 0:
        for target in range(2):
            images = []
            for i in range(1, 4):
                image = pygame.image.load("duck" + str(i) + ".png")
                image = pygame.transform.scale(image, (96, 93))
                images.append(image)
            new_target = Target(images, random.randrange(0,
                                                         screen_width),
                                screen_height - 48)
            target_group.add(new_target)

    clock.tick(60)
