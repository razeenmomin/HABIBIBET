import os.path
import pygame
from sys import exit
from random import randint, choice

pygame.init()
scriptDir = os.path.dirname(os.path.abspath(__file__))

screen = pygame.display.set_mode((1280,640))
pygame.display.set_caption("HABIBI BETS")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite): #inheriting Sprite class
    def __init__(self): #constructor
        super().__init__()
         
#def startgame():   
def button(x,y,w,h):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0] > x and pos[0] < x + w and pos[1] > y and pos[1] < y + h:
       if click[0] == 1:
         startgame()
    pygame.draw.rect(screen, color, (x,y,w,h))
def menu():

 while True:

    surface.blit(background, (0, 0))


    button(x,y,w,h)

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
    pygame.display.update()
    
        
while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    
    
    color = (30, 92, 58)
    screen.fill(color)  # Fill the display with a solid color

   

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
