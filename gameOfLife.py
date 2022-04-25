#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:46:23 2020

@author: apulido
"""

import pygame
import numpy as np
import time
import sys

pygame.init()

width, height = 800, 400
white = (255, 255, 255)
green = (42, 168, 78)
liveColor = (249, 130, 41)
bg = (25, 25, 25)

txt_X = 200
txt_Y = 425
txt_height = 50

nxC, nyC = 100, 50

iteration = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game of Life')
screen.fill(bg)

pygame.display.set_icon(screen)
programIcon = pygame.image.load('dna.png')
pygame.display.set_icon(programIcon)

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

font = pygame.font.Font('freesansbold.ttf', 32)

display_surface = pygame.display.set_mode((width, height + txt_height))

while True:

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
            #print('mouseClick: ' + str(mouseClick))
            posX, posY = pygame.mouse.get_pos()
            #print(posX, posY)
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            #print(celX, celY)
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

            #print(x, y)
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, green, poly, 1)
            else:
                pygame.draw.polygon(screen, liveColor, poly, 0)

    gameState = np.copy(newGameState)

    if pauseExect:
        iteration = iteration + 1

    text = font.render(str(iteration), True, green, bg)
    textRect = text.get_rect()
    textRect.center = (txt_X, txt_Y)
    display_surface.blit(text, textRect)

    pygame.display.flip()
