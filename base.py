# libraries
import pygame
from random import randint

# Variables globales
windowWidth = 400
windowHeight = 600
fps = 3
speed = 1
clock = pygame.time.Clock()

# fonctions

def make_pipe():
    """
    Makes pipes
    """


# Initialisation du module
pygame.init()  # intiates all the modules of pygame

# sets the resolution of the window
screen = pygame.display.set_mode((windowWidth, windowHeight))
screen.fill((255, 255, 255))  # background colour

pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('flappybird.png')
pygame.display.set_icon(icon)

# Oiseau
birdImg = pygame.image.load('bird.png')
birdImg = pygame.transform.scale(birdImg, (55, 40))
birdRect = birdImg.get_rect(center=(50,50))

running = True
while running:
    spacePressed = False
    # Vérifications d'actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed += 1
                pass
            
    # Oiseau
    birdRect = birdRect.move((4,speed))
    
    # Images
    screen.blit(birdImg, birdRect) # Oiseau
    pygame.display.update()  # to update the display
    clock.tick(fps)

pygame.quit()



