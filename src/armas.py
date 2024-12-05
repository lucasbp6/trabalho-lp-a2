import pygame
import math

class Balas:
    def __init__(self):
        self.balas = []

    # Verifica a colisao entre cada um dos objetos com o tiro
    def colisao(self, paredes, bala, inimigos, v = False):
        rect = pygame.Rect(bala.pos[0]-bala.raio, bala.pos[1]-bala.raio, 2*bala.raio, 2*bala.raio)
        for parede in paredes:
            if parede.colliderect(rect) :
                return True
        if v == True:        
            for inimigo in inimigos.inimigos:
                if inimigo.rect.colliderect(rect):
                    inimigo.vida -= 1
                    return True
        else:
            if inimigos.rect.colliderect(rect):
                    inimigos.vida -= 1
                    return True
        return False

    #adiciona balas a lista
    def add(self, bala):
        self.balas.append(bala)
    
    #desenha as balas
    def draw(self, tela):
        for bala in self.balas:
            pygame.draw.circle(tela, (255, 255, 255), bala.pos, bala.raio)

    #atualiza as balas, o parametro v indica se é tiro do inimigo ou do personagem
    def update(self, tela, paredes, inimigos, v = False):
        balas_remove = []
        for bala in self.balas:
            if v == False:
                bala_colisao = self.colisao(paredes, bala, inimigos, True)
                if (bala_colisao and bala.raio < 50) or bala.update() == 0:
                    balas_remove.append(bala)
            else: 
                bala_colisao = self.colisao(paredes, bala, inimigos)
                if (bala_colisao and bala.raio < 50) or bala.update() == 0:
                    balas_remove.append(bala)
        if len(balas_remove) != 0:
            for bala in balas_remove:
                self.balas.remove(bala)
        self.draw(tela)

class Bala:
    def __init__(self, rect_per, d_x, d_y, raio):
        self.contador = 70
        self.raio = raio
        self.per = rect_per
        self.pos = [rect_per.center[0], rect_per.center[1]]
        self.sentido = (d_x, d_y)
        self.p_inicial()
    
    #define um sentido da bala 
    def p_inicial(self):
        if self.sentido[0] == 1:
            self.pos[0] = self.per.right
        elif self.sentido[0] == -1:
            self.pos[0] = self.per.left
        
        if self.sentido[1] == 1:
            self.pos[1] == self.per.bottom
        elif self.sentido[1] == -1:
            self.pos[1] == self.per.top
        

    #aumenta a posição da bala no sentido definido    
    def update(self):
        self.contador -= 1
        self.pos = (self.pos[0] + self.sentido[0]*8, self.pos[1]+ self.sentido[1]*8)
        return self.contador
    
class Pistola:
    def __init__(self, rect_per, d_x, d_y, raio):
        self.contador = 70
        self.raio = raio
        self.per = rect_per
        self.pos = [rect_per.center[0], rect_per.center[1]]
        self.sentido = (d_x, d_y)
        self.p_inicial()
    
    #define um sentido da bala 
    def p_inicial(self):
        if self.sentido[0] == 1:
            self.pos[0] = self.per.right
        elif self.sentido[0] == -1:
            self.pos[0] = self.per.left
        
        if self.sentido[1] == 1:
            self.pos[1] == self.per.bottom
        elif self.sentido[1] == -1:
            self.pos[1] == self.per.top
        

    #aumenta a posição da bala no sentido definido    
    def update(self):
        self.contador -= 1
        self.pos = (self.pos[0] + self.sentido[0]*8, self.pos[1]+ self.sentido[1]*8)
        return self.contador
    
class Espada:
    def __init__(self, rect_per, d_x, d_y, raio):
        self.contador = 10
        self.raio = raio
        self.per = rect_per
        self.pos = [rect_per.center[0], rect_per.center[1]]
        self.sentido = (d_x, d_y)
    
    #aumenta a posição da bala no sentido definido    
    def update(self):
        self.contador -= 1
        #self.pos = (self.pos[0] + self.sentido[0]*8, self.pos[1]+ self.sentido[1]*8)
        return self.contador
    
class Espingarda:
    def __init__(self, rect_per, d_x, d_y, raio):
        self.contador = 50
        self.raio = raio
        self.per = rect_per
        self.pos = [rect_per.center[0], rect_per.center[1]]
        self.sentido = (d_x, d_y)
        self.p_inicial()
    
    #define um sentido da bala 
    def p_inicial(self):
        if self.sentido[0] == 1:
            self.pos[0] = self.per.right
        elif self.sentido[0] == -1:
            self.pos[0] = self.per.left
        
        if self.sentido[1] == 1:
            self.pos[1] == self.per.bottom
        elif self.sentido[1] == -1:
            self.pos[1] == self.per.top
    

    #aumenta a posição da bala no sentido definido    
    def update(self):
        self.contador -= 1
        self.pos = (self.pos[0] + self.sentido[0]*8, self.pos[1]+ self.sentido[1]*8)
        return self.contador