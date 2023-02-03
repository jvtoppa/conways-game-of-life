import pygame
import numpy
import sys
import time
import random
from collections import Counter

mObj = []
map = [(x, y) for x in range(0,20) for y in range(0,20)] 

pontos_mapa = [(x, y) for x in range(1, 400, 20) for y in range(1, 400, 20)] 

def drawGrid():
    blockSize = 20 
    for x in range(0, 400, blockSize):
        for y in range(0, 400, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(window, (0,0,0), rect, 1)

def cellGen():
    global mObj
    xr = random.randint(1,21)
    yr = random.randint(1,21)
    tp = (xr,yr)
    if tp in map:
        cell = pygame.Rect(tp[0]*20, tp[1]*20, 20, 20)
        pygame.draw.rect(window, (0,0,0), cell)
        mObj.append(cell)

def matrixGen(cells):
    map_coords_bool = []
    for coordinates in pontos_mapa:
        for i in cells:
            val = int(i.collidepoint(coordinates))
            if val == 1:
                break
        
        map_coords_bool.append(val)
        
    
    return map_coords_bool

def main():
    mGen = []
    global window
    pygame.init()
    window = pygame.display.set_mode((400, 400))

    window.fill((255, 255, 255))
    drawGrid()
    for w in range(0,50):
        cellGen()

    #Cria a matriz booleana com os valores das células
    #Update do display do pygame
    pygame.display.update()
    #O jogo em si
    while True:
        events = pygame.event.get()
        listM = matrixGen(mObj)

        m = []

        while listM != []:
            m.append(listM[:20])
            listM = listM[20:]
        array = numpy.array(m)
        array_transposto = array.transpose()
        print(array_transposto)

        #Localiza os pontos com 1
        array_tp_lista = array_transposto.tolist()
        positive_cell = numpy.where((array_transposto > 0))
        posl = positive_cell[0].tolist()
        valCel = []

        for i in range(0, len(posl)):
            val = (positive_cell[0][i], positive_cell[1][i])
            valCel.append(val)

        #valCel[célula][x ou y]
        adj_matrix = []
        #indices adjacentes
        for valo in range(0, len(valCel)):
            adj = []
            if valCel[valo][0] > 0:
                adj.append((valCel[valo][0] - 1, valCel[valo][1]))

            if valCel[valo][0] > 0 and valCel[valo][1] > 0:
                adj.append((valCel[valo][0] - 1, valCel[valo][1] - 1))

            if valCel[valo][0] + 1 < len(array_tp_lista[0]):
                adj.append((valCel[valo][0] + 1, valCel[valo][1]))
            
            if valCel[valo][0] + 1 < len(array_tp_lista[0]) and valCel[valo][1] > 0:
                adj.append((valCel[valo][0] + 1, valCel[valo][1] - 1))
            
            if valCel[valo][1] > 0:
                adj.append((valCel[valo][0], valCel[valo][1] - 1))

            if valCel[valo][0] + 1 < len(array_tp_lista[0]) and valCel[valo][1] + 1 < len(array_tp_lista[0]):
                adj.append((valCel[valo][0] + 1, valCel[valo][1] + 1))

            if valCel[valo][1] + 1 < len(array_tp_lista):
                adj.append((valCel[valo][0], valCel[valo][1] + 1))

            if valCel[valo][0] > 0 and valCel[valo][1] + 1 < len(array_tp_lista):
                adj.append((valCel[valo][0] - 1, valCel[valo][1] + 1))

            adj_matrix.append(adj)
          #  print("Para", valCel[valo], ":")
        #    print(adj)

        #VALCEL = TODOS OS QUADRADOS PINTADOS
        #ADJ_MATRIX = TODAS AS POSIÇÕES ADJACENTES AOS QUADRADOS PINTADOS
        #Quantas adjacências se interseccionam?
        lst = []
        for i in range(0, len(adj_matrix)):
            for j in adj_matrix[i]:
                lst.append(j)
        c = Counter(lst)
        #print(c)       

        newDict = dict()
        
        #Todas as adjacencias
        for (key, value) in c.items():
            if value >= 2:
                newDict[key] = value
        print(newDict)

                    
                    
        #Framerate
        time.sleep(3/1)

        pygame.display.update()

        #Esc p/ fechar o programa
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        
        

if __name__ == "__main__":
    main()
