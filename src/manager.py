import pygame
import menu 

LARGURA, ALTURA = 800, 600

class GameManager:
    def __init__(self):
        pass

    def colisao(self, personagem, objetos):
        for objeto in objetos:
            if personagem.rect.colliderect(objeto):
                return True
        return False
    


pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Menu')
menu.hub(TELA)

pygame.quit()