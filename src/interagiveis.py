import pygame

#a mexer
class Coletavel:
    def __init__(self):
        self.lista = []

    def add(self, path, x, y, largura, altura):
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (largura,altura))
        rect = image.get_rect()
        rect.topleft = [x,y]
        self.lista.append([image, rect])

    def draw(self, tela):
        for coletavel in self.lista:
            tela.blit(coletavel[0],coletavel[1])

    def colisao(self, personagem):
        for coletavel in self.lista:
            if coletavel[1].colliderect(personagem.rect):
                personagem.coletou += 1
                self.lista.remove(coletavel)
    def update(self, tela, personagem):
        self.draw(tela)
        self.colisao(personagem)

