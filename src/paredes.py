import pygame


class Parede:
    def __init__(self, x, y, altura, largura, cor):
        self.rect = pygame.Rect(x,y,altura, largura)
        self.cor = cor
    

class Paredes:
    def __init__(self):
        self.paredes = []

    def add(self, parede):
        self.paredes.append(parede)

    def remove(self, parede):
        self.paredes.remove(parede)

    def draw(self, tela):
        for parede in self.paredes:
            pygame.draw.rect(tela, parede.cor, parede)


'''
class Parede:
    def __init__(self, x, y, largura, altura, textura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.textura = textura

    def draw(self, tela):
        pygame.draw.rect(tela, self.textura, self.rect)

class Paredes:
    def __init__(self):
        self.paredes = []
        self.fixas = []

    def add(self, parede):
        self.paredes.append(parede)

    def addfixa(self, parede):
        self.fixas.append(parede)

    def draw(self, tela):
        for parede in self.fixas:
            parede.draw(tela)
        for parede in self.paredes:
            parede.draw(tela)
    
    def colisao(self, personagem, botao):

        posicao_original = personagem.rect.topleft
        personagem.movimento(botao)
        
        for parede in self.paredes:
            if personagem.rect.colliderect(parede.rect):
                personagem.rect.topleft = posicao_original
                return
        for parede in self.fixas:
            if personagem.rect.colliderect(parede.rect):
                personagem.rect.topleft = posicao_original
                return
    
    def movimento(self, personagem, botao):
        if personagem.rect.x >= 4*LARGURA/5 and botao[pygame.K_d]:
            for parede in self.paredes:
                parede.rect.x -= 5
                #personagem.rect.x -= 5
        if personagem.rect.x <= LARGURA/5 and botao[pygame.K_a] and self.paredes[0].rect.x < 0:
            for parede in self.paredes:
                parede.rect.x += 5
                #personagem.rect.x += 5
                #if parede.rect.x + parede.rect.width <= 0:
                #    self.paredes.remove(parede)
                '''