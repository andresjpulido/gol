import pygame
import numpy as np
import time
import sys
from configparser import ConfigParser
from palette import Color


def run(screen=None):
    print('[main] run')

    width, height = 800, 450
    cfg = ConfigParser()
    cfg.read('app_config.ini')
    apptittle = cfg.get('settings', 'app-tittle')

    if not screen:
        pygame.init()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(apptittle)

        pygame.display.set_icon(screen)
        programIcon = pygame.image.load('dna.png')
        pygame.display.set_icon(programIcon)
        mainloop(screen, cfg)


def mainloop(screen, cfg):
    print('[main] mainloop')

    white = (255, 255, 255)
    green = (42, 168, 78)
    liveColor = (249, 130, 41)
    rgbvalue = cfg.get('settings', 'bg-color').split(',')
    bg = list(map(int, rgbvalue))
    bg = Color.BACKGROUND.value

    txt_height = 100

    nxC, nyC = 100, 50

    iteration = 0

    width, height = 800, 400

    dimCW = width / nxC
    dimCH = height / nyC

    # estado de las celdas
    gameState = np.zeros((nxC, nyC))

    # gameState[5,3] = 1
    # gameState[5,4] = 1
    # gameState[5,5] = 1

    gameState[11, 11] = 1
    gameState[12, 12] = 1
    gameState[12, 13] = 1
    gameState[11, 13] = 1
    gameState[10, 13] = 1

    pauseExect = False

    font = pygame.font.Font('BebasNeue-Regular.ttf', 16)
    font32 = pygame.font.Font('BebasNeue-Regular.ttf', 32)

    display_surface = pygame.display.set_mode((width, height + txt_height))

    running = True
    while running:

        newGameState = np.copy(gameState)
        screen.fill(bg)
        time.sleep(0.1)


        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.KEYDOWN:
                pauseExect = not pauseExect

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouseClick = pygame.mouse.get_pressed()
            if sum(mouseClick) > 0:
                # print('mouseClick: ' + str(mouseClick))
                posX, posY = pygame.mouse.get_pos()
                # print(posX, posY)
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                # print(celX, celY)
                newGameState[celX, celY] = not mouseClick[2]

        for x in range(0, nxC):
            for y in range(0, nyC):

                if pauseExect:

                    # calculamos los vecinos cercanos
                    n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                              gameState[(x) % nxC, (y - 1) % nyC] + \
                              gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                              gameState[(x - 1) % nxC, (y) % nyC] + \
                              gameState[(x + 1) % nxC, (y) % nyC] + \
                              gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                              gameState[(x) % nxC, (y + 1) % nyC] + \
                              gameState[(x + 1) % nxC, (y + 1) % nyC]

                    # Rule 1: una celula muerta con exactamente 3 vecinas vivas revive
                    if gameState[x, y] == 0 and n_neigh == 3:
                        newGameState[x, y] = 1

                    elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[x, y] = 0

                # Rule 2: una celula viva con menos de 2 o mas de 3 vecinas vivas muere

                poly = [
                    (x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)
                ]

                # print(x, y)
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, Color.GRID.value, poly, 1)
                else:
                    pygame.draw.polygon(screen, Color.INDIVIDUAL.value, poly, 0)

        gameState = np.copy(newGameState)

        if pauseExect:
            iteration = iteration + 1

        #create toolbar
        txt_X = 40
        txt_Y = 405

        spacewidth = 8

        #borders
        borderleftwidht = 60
        txt_X = 0
        pygame.draw.rect(display_surface, Color.BUTTON_FOUR.value, pygame.Rect(txt_X, txt_Y, borderleftwidht, 80),0,border_bottom_left_radius=30)

        #cuadrado
        #pygame.draw.rect(display_surface, Color.BUTTON_FOUR.value, pygame.Rect(30, txt_Y, borderleftwidht, 80) )
        txt_X = txt_X + borderleftwidht
        pygame.draw.rect(display_surface, Color.BUTTON_FOUR.value, pygame.Rect(txt_X, txt_Y +15 , borderleftwidht*2, 65))

        #generation
        txt_X = txt_X + borderleftwidht*2 + spacewidth
        txt_Y = txt_Y + 15
        text = font32.render(generationformat(iteration), True, Color.BUTTON_FOUR.value, Color.BACKGROUND.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y)
        display_surface.blit(text, textRect)

        #play
        playwidth = 80
        txt_X = txt_X + 75
        pygame.draw.rect(display_surface, Color.BUTTON_THREE.value, pygame.Rect(txt_X, txt_Y , playwidth, 28))
        text = font.render("Play", True, Color.BACKGROUND.value, Color.BUTTON_THREE.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y )
        display_surface.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                mousePosition = pygame.mouse.get_pos()
                if pygame.Rect(txt_X, txt_Y , playwidth, 28).collidepoint(mousePosition):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    pauseExect = not pauseExect



        #stop
        pygame.draw.rect(display_surface, Color.BUTTON_ONE.value, pygame.Rect(txt_X, txt_Y + 35, playwidth, 28))
        text = font.render("Stop", True, Color.BACKGROUND.value, Color.BUTTON_ONE.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y + 35)
        display_surface.blit(text, textRect)

        #next
        txt_X = txt_X + playwidth + spacewidth
        pygame.draw.rect(display_surface, Color.BUTTON_ONE.value, pygame.Rect(txt_X, txt_Y , playwidth, 28))
        text = font.render("Next", True, Color.BACKGROUND.value, Color.BUTTON_ONE.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y )
        display_surface.blit(text, textRect)

        #reset
        pygame.draw.rect(display_surface, Color.BUTTON_FOUR.value, pygame.Rect(txt_X, txt_Y+35, playwidth, 28))
        text = font.render("Reset", True, Color.BACKGROUND.value, Color.BUTTON_FOUR.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y + 35)
        display_surface.blit(text, textRect)

        #patterns
        txt_X = txt_X + playwidth + spacewidth
        pygame.draw.rect(display_surface, Color.BUTTON_ONE.value, pygame.Rect(txt_X, txt_Y , playwidth, 28))
        text = font.render("Patterns", True, Color.BACKGROUND.value, Color.BUTTON_ONE.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y )
        display_surface.blit(text, textRect)

        #info
        pygame.draw.rect(display_surface, Color.BUTTON_FOUR.value, pygame.Rect(txt_X, txt_Y+35, playwidth, 28))
        text = font.render("Info", True, Color.BACKGROUND.value, Color.BUTTON_FOUR.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y + 35)
        display_surface.blit(text, textRect)

        #speed
        txt_X = txt_X + 150
        speedwidth = 135
        pygame.draw.rect(display_surface, Color.BUTTON_TWO.value, pygame.Rect(txt_X, txt_Y , speedwidth, 28))
        text = font.render("Speed", True, Color.BACKGROUND.value, Color.BUTTON_TWO.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y )
        display_surface.blit(text, textRect)

        #size
        sizewith = 135
        pygame.draw.rect(display_surface, Color.BUTTON_ONE.value, pygame.Rect(txt_X, txt_Y+35, 135, 28))
        text = font.render("Size", True, Color.BACKGROUND.value, Color.BUTTON_ONE.value)
        textRect = text.get_rect()
        textRect.topleft = (txt_X, txt_Y+35)
        display_surface.blit(text, textRect)

        #borders
        txt_X = txt_X + sizewith + spacewidth
        pygame.draw.rect(display_surface, Color.BUTTON_TWO.value, pygame.Rect(txt_X, txt_Y , 28, 28), 0, border_top_right_radius=25, border_bottom_right_radius=25)
        pygame.draw.rect(display_surface, Color.BUTTON_ONE.value, pygame.Rect(txt_X, txt_Y+35, 28, 28), 0, border_top_right_radius=25, border_bottom_right_radius=25)

        #render
        pygame.display.flip()


def generationformat(generation):
    result  = str(generation).zfill(5)
    return result


if __name__ == '__main__':
    run()
