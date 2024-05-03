import pygame
import sys
import math
import os.path
import random
from pygame.locals import *
from sys import exit
from random import randint 

class daButton():
    

    def __init__(self, image, pos, daText, font, daColor, dahoverColor):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.daColor, self.dahoverColor = daColor, dahoverColor
        self.daText = daText
        self.text = self.font.render(self.daText, True, self.daColor)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.daText, True, self.dahoverColor)
        else:
            self.text = self.font.render(self.daText, True, self.daColor)


class Card:

    # this class contains all attributes of a playing card
    def __init__(self, suit, color, label, value):
        self.suit = suit
        self.color = color
        self.label = label
        self.value = value


class Deck:

    # this class contains an array that acts as our 52 card deck
    def __init__(self):
        self.cards = []

    # this method simply creates a deck using the Card class above
    def createDeck(self):
        suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
        for symbol in suits:
            number = 2
            while number < 15:
                if symbol == "Clubs" or symbol == "Spades":
                    suitColor = "Black"
                else:
                    suitColor = "Red"
                value = number
                if number > 10:
                    value = 10
                if number == 14:
                    value = 1
                letter = number
                if number == 11:
                    letter = "J"
                elif number == 12:
                    letter = "Q"
                elif number == 13:
                    letter = "K"
                elif number == 14:
                    letter = "A"
                newCard = Card(symbol, suitColor, letter, value)
                self.cards.append(newCard)
                number += 1

    # this method allows us to shuffle our deck so that it is randomly arranged
    def shuffleDeck(self):
        return random.shuffle(self.cards)

    # this method basically gets the top card of the deck and returns it
    def getCard(self):
        topCard = self.cards[0]
        self.cards.pop(0)
        return topCard


class Dealer:

    # this class contains everything that is within the control of the dealer
    def __init__(self):
        self.deck = Deck()
        self.deck.createDeck()
        self.deck.shuffleDeck()
        self.hand = []
        self.count = 0
        self.x = halfWidth
        self.y = 100

    # this method creates the two-card hand that the dealer starts with
    def createDealerHand(self):
        for i in range(1, 3):
            self.addCard()

    # this method uses the getCard() to deal a card to a player
    def dealCard(self):
        return self.deck.getCard()

    # this method allows the dealer to deal himself a card and also account for the dealer's count
    def addCard(self):
        dealerCard = self.dealCard()
        self.hand.append(dealerCard)
        self.count += dealerCard.value
        self.countAce()

    # this method prints the dealer's hand
    def printDealerHand(self):
        print("")
        print("Dealer's Hand: ")
        for dealerCard in self.hand:
            print("Suit: " + dealerCard.suit + "\nLabel: " + str(dealerCard.label))

    # this method prints the dealer's count
    def printDealerCount(self):
        print("")
        print("Dealer's Count: " + str(self.count))

    # this method considers all aces in a dealer's hand to give them the closest count under 21
    def countAce(self):
        if self.count <= 21:
            for card in self.hand:
                if card.label == "A":
                    self.count += 10
                    if self.count > 21:
                        self.count -= 10
                        break

    # this method will draw all the cards in a hand (13 : 20 Card Dimension Ratio)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for card in self.hand:
            if card == self.hand[1]:
                drawCard = pygame.image.load("BLACKJACK PROJECT\Cards\Backs\back.png")
            else:
                drawCard = pygame.image.load("BLACKJACK PROJECT\Cards" + str(card.suit) + "/" + str(card.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        displayText("DEALER", dafont, surface, nameX, nameY, white)
        deckX = 400 - (0.5 * cardWidth)
        deckY = 100 - (0.5 * cardHeight)
        for card in range(1, 7):
            deckCard = pygame.image.load("BLACKJACK PROJECT\Cards\Backs\back.png")
            backCard = pygame.transform.scale(deckCard, (cardWidth, cardHeight))
            surface.blit(backCard, (deckX, deckY))
            deckX += cardGap


class Player:

    # this class contains everything that is within the control of the player
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.count = 0
        self.blackjack = False
        self.bust = False
        self.bank = 100
        self.bet = 0
        self.roundsWon = 0
        self.x = 0
        self.y = 0
        self.currentTurn = False

    # this method asks the player for their choice of action when it is their turn
    def askChoice(self):
        input = 0
        answered = False
        while answered is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    input = 1
                    answered = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    input = 2
                    answered = True
        return input

    # this method adds a card provided by the dealer to the player's hand
    def addCard(self, card):
        self.hand.append(card)
        self.countCards()
        print(str(self.name) + "'s Count: " + str(self.count))

    # this method prints the player's hand
    def printHand(self):
        print("")
        print(str(self.name) + "'s Hand: ")
        for playerCard in self.hand:
            print("Suit - " + playerCard.suit + "\nLabel - " + str(playerCard.label))

    # this method prints the player's count
    def printCount(self):
        print("")
        print(str(self.name) + "'s Count: " + str(self.count))

    # this method will apply the outcome of the bet to the bank
    # no negative parameter will ever need to passed as we have already subtracted the bet from the bank
    def applyBet(self, factor):
        self.bank += self.bet * factor

    # this method that will reset the bets
    def resetBet(self):
        self.bet = 0

    # this method prints the player's bank
    def printBank(self):
        print("")
        print(str(self.name) + "'s Bank: " + str(self.bank))

    # this method resets the player's hand
    def resetHandAndCount(self):
        self.hand = []
        self.count = 0

    # this method considers all aces in a player's hand to give them the closest count under 21
    def countCards(self):
        self.count = 0
        for card in self.hand:
            self.count += card.value
        for card in self.hand:
            if card.label == "A":
                self.count += 10
                if self.count > 21:
                    self.count -= 10
                    break

    # this method will draw all the cards in a hand (13 : 20 Card Dimension Ratio)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for card in self.hand:
            drawCard = pygame.image.load("BLACKJACK PROJECT\Cards" + str(card.suit) + "/" + str(card.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        nameColor = white
        if self.currentTurn:
            nameColor = blue
            displayText("Hit(H) or Stand(S)", dafont, surface, self.x, self.y - (0.75 * cardHeight), nameColor)
        if self.bust:
            bust = pygame.image.load("BLACKJACK PROJECT\pic\loseHabibi.png")
            bustWidth = bust.get_width()
            bustHeight = bust.get_height()
            surface.blit(bust, (self.x - (0.5 * bustWidth), self.y - (0.5 * bustHeight)))
        if self.blackjack:
            blackjack = pygame.image.load("BLACKJACK PROJECT\pic\winHabibi.png")
            bjWidth = blackjack.get_width()
            bjHeight = blackjack.get_height()
            surface.blit(blackjack, (self.x - (0.5 * bjWidth), self.y - (0.5 * bjHeight)))
        displayText(str(self.name) + "   $" + str(self.bank), dafont, surface, nameX, nameY, nameColor)

    # function to reset everything for the next round
    def resetState(self):
        self.bust = False
        self.blackjack = False
        self.resetBet()
        self.resetHandAndCount()


# Initializes Pygame
pygame.init()
scriptDir = os.path.dirname(os.path.abspath(__file__))
dafont = pygame.font.Font(os.path.join(scriptDir, "font", "CasinoFont.otf"), 40)
def displayText(text, color, x, y):
    textSurface = dafont.render(text, True, color)
    screen.blit(textSurface, (x, y))
# COLORS
backgroundColour = (10, 10, 10)
backgroundColour2 = ( 14, 59, 8)

black, blue, white, orange, red = (0, 0, 0), (51, 235, 255), (255, 255, 255), (255, 165, 0), (255, 0, 0)
# Sets the dimensions of the screen
screenWidth, screenHeight = 1280, 720
screenWidth2, screenHeight2 = 1280, 720
halfWidth = screenWidth / 2
halfHeight = screenHeight / 2

screen = pygame.display.set_mode((screenWidth, screenHeight))
pic = pygame.image.load(os.path.join(scriptDir, "pic", "guy.png")).convert()

# Sets the caption 
pygame.display.set_caption('HABIBI BETS')

# Creates the font for the game
def fontwoo(size): 
    return pygame.font.Font("BLACKJACK PROJECT/font/CasinoFont.otf", size)

balance = 1000
players = []
numPlayers = 0
dealer = Dealer()
startY = 50



# Function for start menu 
def startMenu():
     while True:
        screen.blit(pic, (0, 0))
   
        mouse = pygame.mouse.get_pos()

        menuText = fontwoo(100).render("HABIBI BETS", True, "#b68f40")
        menuRect = menuText.get_rect(center=(640, 100))
        startButton = daButton(image=pygame.image.load("BLACKJACK PROJECT/pic/buttonback.png"), pos=(640, 250), 
                            daText="PLAY", font=fontwoo(75), daColor="#d7fcd4", dahoverColor="White")
        instructionsButton = daButton(image=pygame.image.load("BLACKJACK PROJECT/pic/buttonback.png"), pos=(640, 400), 
                            daText="INSTRUCTION", font=fontwoo(75), daColor="#d7fcd4", dahoverColor="White")
        quitButton = daButton(image=pygame.image.load("BLACKJACK PROJECT/pic/buttonback.png"), pos=(640, 550), 
                            daText="QUIT", font=fontwoo(75), daColor="#d7fcd4", dahoverColor="White")

        screen.blit(menuText, menuRect)

        for button in [startButton,instructionsButton, quitButton]:
            button.changeColor(mouse)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.checkForInput(mouse):
                    bet = getBet()  # Get the bet amount here
                    game(bet) 
                if instructionsButton.checkForInput(mouse):
                    instructions()
                if quitButton.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
 
    
# Function for betting menu 
def instructions():
    while True:
        mousePos = pygame.mouse.get_pos()

        screen.fill(backgroundColour2)
  
        displayText("Goal of the Game:", white, 0, 0)
        displayText("To get the closest to 21 without going over", white, 20, 40)
        displayText("Basic Rules:",  white, 0, 120)
        displayText("Press H to Hit (Gets a card)", white, 20, 160)
        displayText("Press S to Stand (Finishes turn)", white, 20, 200)
        displayText("Betting:",  white, 0, 280)
        displayText("You have $1000 to start the game.",  white, 20, 320)
        displayText("Be careful, because you can go bankrupt", white, 20, 360)
        displayText("If closest to 21 = Earn 2 times your bet",  white, 20, 400)
        displayText("If count is equal to the dealer's = you get bet back", white, 20, 440)
        displayText("Dealer Bust = you earn 2 times your bets.",  white, 20, 480)

       


        #optionsRect = optionsText.get_rect(center=(640, 260))
        #screen.blit(optionsText, optionsRect)

        backButton = daButton(image=None, pos=(640, 600), 
                            daText="BACK", font= fontwoo(75), daColor="White", dahoverColor="Green")

        backButton.changeColor(mousePos)
        backButton.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.checkForInput(mousePos):
                    startMenu()

        pygame.display.update()



def getBet():
    screen.fill(backgroundColour2)
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
        screen.fill(backgroundColour2)
        displayText("Enter your bet (Balance: $"+str(balance)+"): " + bet, white, 20, 100)
        pygame.display.flip()
def game(bet):
    screen.fill(backgroundColour2)
    clock = pygame.time.Clock()  # Create a clock object for controlling the frame rate
    gameActive = True  # Variable to control the game loop

    while gameActive:
        screen.fill(backgroundColour2)
        displayText("Bet:$ " + str(bet), white, screenWidth2 - 250, screenHeight2 - 50)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameActive = False  # Exit the game loop if the user quits

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Cap the frame rate at 60 frames per second

    # When the game loop exits, quit Pygame
    pygame.quit()
    sys.exit()
       

# Start menu and get bet
startMenu()
bet = getBet()
game()



   


gameActive = True
while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False
    
# Quits Pygame
pygame.display.update()
pygame.quit() 