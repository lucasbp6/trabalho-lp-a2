import pygame

class Coletavel:
    def __init__(self, x, y, altura, largura, path):
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (altura,largura))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Coletaveis:
    def __init__(self):
        self.coletaveis = []
    
    def add(self, coletavel):
        self.coletaveis.append(coletavel)

    def remove(self, coletavel):
        self.coletaveis.append(coletavel)

    def draw(self, tela):
        for coletavel in self.coletaveis:
            tela.blit(coletavel.image, coletavel.rect)


    