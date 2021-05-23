import getch
import time
import pygame
import sys


pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(0)

screen_width = 1250
screen_height = 750
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.SCALED)

sentence = 'This is a sentence which has a number of words'
symbol = ''
words = sentence.split()
wpm = 0
car_movement = 0
progress = 0
error = 0


class RaceCar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 100, 100))


car = RaceCar(100, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.unicode != "":
                symbol = event.unicode

    pygame.display.flip()
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
    car.x = 100 + (100 * car_movement)
    car.update()
    clock.tick(60)

    if progress < len(sentence):
        if symbol == sentence[progress]:
            if progress == 0:
                start_time = time.time()
            if sentence[progress] == ' ':
                car_movement += 1
            print(symbol, end='')
            progress += 1
        else:
            error += 1

    end_time = time.time()

    if car_movement == len(words):
        wpm = len(words) * (60 / (end_time - start_time))
        print('  errors: ' + str(error))
        print('  words per minute: ' + str(wpm))
