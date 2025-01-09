# Tests modifications

# Libraries
import pygame
from random import randint

# Variables globales
pipewidth = 60
gap_size = 125
pipe_color = (0, 255, 0)
windowWidth = 400
windowHeight = 600
fps = 40  
speed = 3
score = 0
text_color = (0,0,0)
end_game_color = (0,0,0)
bird_angle = 0
clock = pygame.time.Clock()


# Initialisation du module + police
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Times New Roman ',30)
font_fin = pygame.font.SysFont('Diplay',50)
font_fin_2 = pygame.font.SysFont('Diplay',20)

# Creation de l'ecran
screen = pygame.display.set_mode((windowWidth, windowHeight))
screen.fill((255, 255, 255))

# Nom du Jeu + logo
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('flappybird.png')
pygame.display.set_icon(icon)

# Oiseau
birdImg = pygame.image.load('bird (1).png')
birdImg = pygame.transform.scale(birdImg, (55, 40))
birdRect = birdImg.get_rect(center=(50,20))

# Tuyeau
pipeImg_top = pygame.image.load('pipe_down.png')
pipeImg_bottom = pygame.image.load('pipe_up.png')

# Font d'ecran
background_Img = pygame.image.load('background.jpg') 
background_Img = pygame.transform.scale(background_Img, (windowWidth, windowHeight))

# Fonctions
def make_pipe():
    top_pipe_height = randint(100, windowHeight - gap_size - 200)
    top_pipe_rect = pygame.Rect(windowWidth, 0, pipewidth, top_pipe_height)
    bottom_pipe_rect = pygame.Rect(windowWidth, top_pipe_height + gap_size, pipewidth, windowHeight - top_pipe_height - gap_size - 105)
    
    return  top_pipe_rect, bottom_pipe_rect

def starting_screen():
    screen.fill((0, 0, 0))
    start_text = font_fin.render("Flappy Bird", True, (255, 255, 255))
    screen.blit(start_text, (windowWidth // 2 - start_text.get_width() // 2, windowHeight // 2.5))
    starting_text = font_fin_2.render("Appuyer sur 'Enter' pour commencer", True, (255, 255, 255))
    screen.blit(starting_text, (windowWidth // 2 - starting_text.get_width() // 2, windowHeight // 2.5 + 40))

def end_screen():
    screen.fill(end_game_color)
    end_text = font_fin.render(f"Tu as perdu, score: {score}",True,(255,255,255))
    screen.blit(end_text, (windowWidth // 2 - end_text.get_width() // 2, windowHeight // 2.5))
    restart_text = font_fin_2.render("Appuyez sur 'r' pour recommencer", True, (255, 255, 255))
    screen.blit(restart_text, (windowWidth // 2 - restart_text.get_width() // 2, windowHeight // 2.5 + 40))
    
def reset_game(score, birdRect, speed, pipes, checked_pipes, bird_angle):
    score = 0
    speed = 3
    bird_angle = 0
    birdRect = birdImg.get_rect(center=(50, 20))  
    pipes.clear()  
    checked_pipes.clear()  
    
    return score, birdRect, speed, pipes, checked_pipes, bird_angle
    
# Listes pour les tuyeaux
pipes = []
checked_pipes = []

# Boucle principale du jeu
running = True
start = True
while running:
    # Ecran de debut
    while start:
        starting_screen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
    
    # Dessine ecran de fond
    screen.fill((255, 255, 255))
    screen.blit(background_Img, (0, 0))
    
    # Vérifications d'actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed = -6.5
                bird_angle = 45
            if event.key == pygame.K_r:
                reset_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pass
            
    # Gravite de l'oiseau qui augmente (donc difficulte augmente)
    if speed < 100:
        speed += 0.5

    # Mouvement de l'oiseau
    birdRect = birdRect.move((0 ,speed))
    
    # Rotation de l'oiseau grace a gravite
    if bird_angle > -45:
        bird_angle -= 2
    
    # Garde l'oiseau dans l'ecran
    if birdRect.top < 0:
        birdRect.top = 0
    if birdRect.bottom > windowHeight:
        birdRect.bottom = windowHeight
    
    # Creation des tuyeux (intervalle)
    if len(pipes) == 0 or pipes[-1][0].x < windowWidth - 200:
        pipes.append(make_pipe())
        
    # Detection si oiseau touche tuyeau/plafond/sol
    for top_pipe_rect, bottom_pipe_rect in pipes:
        if birdRect.colliderect(top_pipe_rect) or birdRect.colliderect(bottom_pipe_rect) or birdRect.top <= 0 or birdRect.bottom >= windowHeight-105:
            # Ecran de fin
            end_screen()
            pygame.display.update()
        
            # Attend qu'on ferme l'ecran
            running_end_screen = True
            while running_end_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running_end_screen = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  
                            score, birdRect, speed, pipes, checked_pipes, bird_angle = reset_game(score, birdRect, speed, pipes, checked_pipes, bird_angle)
                            running_end_screen = False 
                            
    # Change le score
    for top_pipe_rect, bottom_pipe_rect in pipes:
        if top_pipe_rect.right < birdRect.left and top_pipe_rect not in checked_pipes:
            score += 1
            checked_pipes.append(top_pipe_rect)
    
    # Bouge les tuyeaux
    for top_pipe_rect, bottom_pipe_rect in pipes:
        top_pipe_rect.x -= 4
        bottom_pipe_rect.x -= 4
    
    # Changement de l'angle de l'oiseau + le dessine
    rotated_bird = pygame.transform.rotate(birdImg, bird_angle)
    rotated_rect = rotated_bird.get_rect(center=birdRect.center)
    screen.blit(rotated_bird, rotated_rect)
    
    # Cree les tuyeaux
    for top_pipe_rect, bottom_pipe_rect in pipes:
        top_pipe_img = pygame.transform.scale(pipeImg_top, (pipewidth, top_pipe_rect.height))
        bottom_pipe_img = pygame.transform.scale(pipeImg_bottom, (pipewidth, bottom_pipe_rect.height))
        screen.blit(top_pipe_img, top_pipe_rect)
        screen.blit(bottom_pipe_img, bottom_pipe_rect)
    
    # Met le score sur l'ecran
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (20,20))
    
    # Applique les nouveaux changements a l'ecran
    pygame.display.update()
    
    # Bouge l'ecran
    clock.tick(fps)

# Sort du jeu
pygame.quit()

