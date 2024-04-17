import pygame
import sys
import os.path
from sys import exit
from random import randint 
# Initialize Pygame
pygame.init()
scriptDir = os.path.dirname(os.path.abspath(__file__))

# Define colours
backgroundColour = (10, 10, 10)
backgroundColour2 = ( 14, 59, 8)
white = (255, 255, 255)
black = (0, 0, 0)

# Set the dimensions of the screen
screenWidth, screenHeight = 700, 500
screenWidth2, screenHeight2 = 1000, 1000
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Set the caption of the screen
pygame.display.set_caption('HABIBI BETS')

# Create font objects
font = pygame.font.Font(os.path.join(scriptDir, "font", "CasinoFont.ttf"), 40)

# User balance
balance = 1000

# Function to display text on the screen
def displayText(text, color, x, y):
    textSurface = font.render(text, True, color)
    screen.blit(textSurface, (x, y))

# Function for start menu and bet input
def startMenu():
    screen.fill(backgroundColour)
    displayText("Press SPACE to start", white, 50, 100)
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

def get_bet():
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
bet = get_bet()

# Close the previous window
pygame.display.quit()

# Create a new window for the main game
screen = pygame.display.set_mode((screenWidth2, screenHeight2))

# Main game loop
screen.fill(backgroundColour2)
displayText("WELCOME TO HABIBI BETS BLACKJACK", white, 50, 50)
displayText("Bet: " + str(bet), white, screenWidth2- 180 , screenHeight2-50 )
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
