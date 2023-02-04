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
    xr = random.randint(0,20)
    yr = random.randint(0,20)
    tp = (xr,yr)
    #removes duplicates
    if pygame.Rect(tp[0]*20, tp[1]*20, 20, 20) not in mObj:
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
    
    for w in range(0,50):
        cellGen()

    #Cria a matriz booleana com os valores das células
    #Update do display do pygame
    pygame.display.update()
    
    valCel = []
    #O jogo em si
    while True:
        window.fill((255,255,255))
        drawGrid()
        for i in mObj:
            pygame.draw.rect(window, (0,0,0), i)
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

        #VALCEL = TODOS OS QUADRADOS PINTADOS
        #ADJ_MATRIX = TODAS AS POSIÇÕES ADJACENTES AOS QUADRADOS PINTADOS
        #Quantas adjacências se interseccionam?
        adjacent = []
        nonAdjacent = []
        allAdj = []

        for i in range(0, len(adj_matrix)):
            for j in adj_matrix[i]:
                if j in valCel:
                    adjacent.append(j)       
        for e in valCel:
            if e not in adjacent:
                nonAdjacent.append(e)
        for x in range(0, len(adj_matrix)):
            for y in adj_matrix[x]:
                allAdj.append(y)

        adj_matrix = []
        c = Counter(adjacent)
        c2 = Counter(allAdj)

        #survival = dict()

        newCells = dict()

        deadCells = dict()
        #Todas as adjacencias
        for (key, value) in c.items():
            if value >= 4:
                deadCells[key] = value

        for (key, value) in c2.items():
            if value == 3:
                newCells[key] = value

        for values in newCells.keys():
            if (values[0],values[1]) not in valCel:
                celula = pygame.Rect(values[1]*20, values[0]*20, 20, 20)
                valCel.append((values[0],values[1]))
                mObj.append(celula)   

        #ESTA INVERTIDO EM mOBJ
        #CASO EM QUE AS CELULAS NAO TEM ADJACENCIAS
        for valores in nonAdjacent:

            while (valores[0],valores[1]) in valCel:
                valCel.remove((valores[0],valores[1]))

            object = pygame.Rect(valores[1]*20, valores[0]*20, 20, 20)

            if object in mObj:
                mObj.remove(object)

        #CASO EM QUE AS CELULAS TEM 4 OU MAIS ADJACENCIAS        
        for valores in deadCells.keys():

            if (valores[0],valores[1]) in valCel:
                valCel.remove((valores[0],valores[1]))

                object = pygame.Rect(valores[1]*20, valores[0]*20, 20, 20)

                if object in mObj:
                    mObj.remove(object)

        valCel = []
        pygame.display.update()
        
        #Framerate
        time.sleep(1/10)
        
        

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
