# made by muhsin
import pygame
import sys
import random
from pygame.locals import *

pygame.display.set_icon(pygame.image.load("C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\flappy.png"))
pygame.font.init()
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'pngs/bird.png'
BACKGROUND = 'pngs/background.png'
PIPE = 'pngs/pipe.png'
font = pygame.font.SysFont('bold', 30)
red = (255, 0, 0)

def text_screen(text, colour, x,y):
    screen_text = font.render(text, True, colour)
    SCREEN.blit(screen_text, [x,y])

def welcomescreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def maingame():
    global SCORE
    SCORE = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
            {'x' : SCREENWIDTH+250, 'y' :newPipe1[0]['y'] },
            {'x' : SCREENWIDTH+250+(SCREENWIDTH/2),'y' : newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x' : SCREENWIDTH+250, 'y' : newPipe1[1]['y']},
        {'x' : SCREENWIDTH+250+(SCREENWIDTH/2),'y' : newPipe2[1]['y']}   
    ]

    pipeVelX = -4

    playerVely = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashText = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashText:

            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidpos <= playerMidPos < pipeMidpos +4:
                SCORE += 1
                GAME_SOUNDS['point'].play()


        if playerVely < playerMaxVelY and not playerFlapped:
            playerVely += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)


        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(SCORE))]
        width = 0
        height = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)

        for digit in myDigits:
            text_screen("Score : " + str(SCORE), (red), 5, 5)
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):

    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['die'].play()
        welcomescreen()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            welcomescreen()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            welcomescreen()
            return True

        return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x' : pipeX, 'y' : -y1},
        {'x' : pipeX, 'y' : y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Ahamed Muhsin")
    # GAME_SPRITES['numbers'] = (
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\0.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\1.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\2.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\3.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\4.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\5.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\6.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\7.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\8.png.png').convert_alpha(),
    #     pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\numbers\\9.png.png').convert_alpha(),
    # )

    GAME_SPRITES['message'] = pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\message.png.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\base.png.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load("C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\pipe.png.png").convert_alpha(), 180),
    pygame.image.load("C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\pipe.png.png").convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\voice\\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\voice\\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\voice\\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\voice\\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\voice\\wing.wav')

    GAME_SPRITES['background'] = pygame.image.load("C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\bacground.png.png").convert()
    GAME_SPRITES['player'] = pygame.image.load('C:\\Users\\MUHSIN\\My Projects\\flappy bird game\\pngs\\bird.png.png').convert_alpha()

    while True:
        welcomescreen()
        maingame()
