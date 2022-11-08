import pygame
from pygame.locals import *
import random
import math
import sys

#Defines
XSPACING = 20
YSPACING = 20
TOPBAR = 100
CLRX = 80
CLRY = 80


#Helper functions
def CheckTounching(pos1, pos2, size):
    if ((pos1[0] >= pos2[0] and pos1[0] <= pos2[0] + size[0]) and (pos1[1] >= pos2[1] and pos1[1] <= pos2[1] + size[1])):
        return True
    else:
        return False

class ColourBlock:
    def __init__(self, pos):
        self.pos = pos
        self.isDifferent = False
        self.colour = (0,0,0)
    
    def SetColour(self, colour):
        self.colour = colour
    
    def GetColour(self):
        return self.colour


class AShadeDifferent:
    def __init__(self, setUp):
        self.xSquares = setUp[0]
        self.ySquares = setUp[1]
        self.difficulty = setUp[2]
        self.time = setUp[3]
        pygame.init()
        pygame.display.set_caption("A Shade Different")

        self.clock = pygame.time.Clock()

        #Load assets
        self.retry = pygame.image.load('Assets/retry.png')

        self.screen = pygame.display.set_mode((CLRX * (self.xSquares) + XSPACING * (self.xSquares + 1), CLRY * (self.ySquares) + YSPACING * (self.ySquares + 1) + TOPBAR))

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((200,200,200))

        if pygame.font:
            if self.xSquares > 2:
                self.font = pygame.font.Font(None, 38)
            else:
                self.font = pygame.font.Font(None, 30)

        self.score = 0
        self.timeOver = False
        self.clrShouldBeSet = True
        self.lost = False

        self.storedTime = 0

        self.squares = []

        self.SetUpSquares()

    def SetUpSquares(self):
        for i in range(0, self.xSquares):
            for j in range (0, self.ySquares):
                self.squares.append(ColourBlock((i * CLRX + (i + 1) * XSPACING, j * CLRY + (j + 1) * YSPACING + TOPBAR)))

    def Run(self):
        self.finished = False

        while not self.finished:
            #Handle input
            self.HandleInput()

            if self.clrShouldBeSet:
                self.clrShouldBeSet = False
                self.SetColourBlocks()

            #Draw screen
            self.Draw()

            self.clock.tick(60)
        
        pygame.quit()
        return True

    def HandleInput(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.lost == False and self.timeOver == False:
                    for s in self.squares:
                        if CheckTounching(pos, s.pos, (CLRX, CLRY)):
                            #You've clicked on a square
                            if s.isDifferent == True:
                                #Correct square, increase score
                                self.score += 1
                                self.clrShouldBeSet = True
                            else:
                                #Wrong square
                                self.lost = True
                if self.timeOver == True or self.lost == True:
                    if CheckTounching(pos, (self.screen.get_size()[0] - self.retry.get_size()[0] - XSPACING, 3 * YSPACING), self.retry.get_size()):
                        self.finished = True
    
    def SetColourBlocks(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colour = (r,g,b)
        for s in self.squares:
            s.SetColour((colour))
            s.isDifferent = False
        #Get the different colour
        valid = False
        while valid == False:
            i = random.randint(0,2)
            toChange = colour[i]
            if random.randint(0,1) == 0:
                toChange -= self.difficulty
            else:
                toChange += self.difficulty
            if toChange >= 0 and toChange <= 255:
                valid = True
                #Use a list to store the new colour values for the blocks
                newColour = []
                for j in range(0,3):
                    if j == i:
                        newColour.append(toChange)
                    else:
                        newColour.append(colour[j])
                difColour = (newColour[0], newColour[1], newColour[2])
        difBlock = random.randint(0, len(self.squares) - 1)
        self.squares[difBlock].SetColour(difColour)
        self.squares[difBlock].isDifferent = True

    
    def Draw(self):
        #clear screen
        self.screen.blit(self.background, (0,0))

        #Draw squares
        for s in self.squares:
            if (self.lost == True or self.timeOver == True) and s.isDifferent == True:
                backgroundRect = Rect(s.pos[0] - XSPACING/2, s.pos[1] - YSPACING/2, CLRX + XSPACING, CLRY + YSPACING)
                pygame.draw.rect(self.screen, (0,0,0), backgroundRect)
            clrRect = Rect(s.pos[0], s.pos[1], CLRX, CLRY)
            pygame.draw.rect(self.screen, s.colour, clrRect)

        #Draw score
        scoreStr = "Score: " + str(self.score)
        scoreTxt = self.font.render(scoreStr, True, (10,10,10))
        self.screen.blit(scoreTxt, (XSPACING,YSPACING))

        #Draw timer
        timeElapsed = pygame.time.get_ticks()/1000
        timeRemaining = math.floor(self.time - timeElapsed)
        if self.lost == True:
            timeRemaining = self.storedTime
        else:
            self.storedTime = timeRemaining
        if timeRemaining <= 0:
            self.timeOver = True
            timeRemaining = 0
        #Go onto two lines if the board is small
        if self.xSquares == 2:
            timeStr = "Time"
            timestr2 = "remaining: " + str(timeRemaining)
            timeTxt = self.font.render(timeStr, True, (10,10,10))
            timeTxt2 = self.font.render(timestr2, True, (10,10,10))
            self.screen.blit(timeTxt, (XSPACING, 3 * YSPACING))
            self.screen.blit(timeTxt2, (XSPACING, 4 * YSPACING))           
        else:
            timeStr = "Time remaining: " + str(timeRemaining)
            timeTxt = self.font.render(timeStr, True, (10,10,10))
            self.screen.blit(timeTxt, (XSPACING, 3 * YSPACING))

        if self.timeOver == True or self.lost == True:
            if self.timeOver == True:
                endStr = "Time over!"
            else:
                endStr = "You lose!"
            endText = self.font.render(endStr, True, (10,10,10))
            self.screen.blit(endText, (self.screen.get_size()[0] - endText.get_size()[0] - XSPACING, YSPACING))
            #Draw restart icon
            self.screen.blit(self.retry, (self.screen.get_size()[0] - self.retry.get_size()[0] - XSPACING, 3 * YSPACING))

        #Refresh the screen
        pygame.display.flip()