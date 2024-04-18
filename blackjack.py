import pygame
import sys
import os.path
from sys import exit
from random import randint 
# Initializes Pygame
pygame.init()
scriptDir = os.path.dirname(os.path.abspath(__file__))

# COLORS
backgroundColour = (10, 10, 10)
backgroundColour2 = ( 14, 59, 8)
white = (255, 255, 255)
black = (0, 0, 0)

# Sets the dimensions of the screen
screenWidth, screenHeight = 1000, 1000
screenWidth2, screenHeight2 = 1000, 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Sets the caption 
pygame.display.set_caption('HABIBI BETS')

# Creates the font for the game
font = pygame.font.Font(os.path.join(scriptDir, "font", "CasinoFont.otf"), 40)

# User set balance
balance = 1000

# Function to display the texts on the screen
def displayText(text, color, x, y):
    textSurface = font.render(text, True, color)
    screen.blit(textSurface, (x, y))

# Function for start menu 
def startMenu():
    screen.fill(backgroundColour)
    displayText("WELCOME TO HABIBI BETS BLACKJACK", white, 80, 70)
    displayText("Press SPACE to start", white, 250, 700)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
# Function for betting menu 

def getBet():
    screen.fill(backgroundColour)
    displayText("Enter your bet (Balance: $"+str(balance)+"):", white, 20, 100)
    pygame.display.flip()
    bet = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if bet.isdigit() and int(bet) <= balance:
                        return int(bet)
                elif event.key == pygame.K_BACKSPACE:
                    bet = bet[:-1]
                elif event.unicode.isdigit():
                    bet += event.unicode
        screen.fill(backgroundColour)
        displayText("Enter your bet (Balance: $"+str(balance)+"): " + bet, white, 20, 100)
        pygame.display.flip()

# Start menu and get bet
startMenu()
bet = getBet()

# Closes the window for start menu and betting
pygame.display.quit()

# Creates a new window for the main game
screen = pygame.display.set_mode((screenWidth2, screenHeight2))

# Main game loop
screen.fill(backgroundColour2)
displayText("Bet: " + str(bet), white, screenWidth2- 200 , screenHeight2-50 )
pygame.display.flip()

gameActive = True
while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False

# Quits Pygame
pygame.quit()

