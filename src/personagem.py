import pygame
import mapa
from config import VELOCIDADE_PERSONAGEM

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, caminho_imagem):
        super().__init__()
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = VELOCIDADE_PERSONAGEM

    def atualizar(self, teclas, parede):
        p = self.rect.topleft
        if teclas[pygame.K_LEFT] :
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] :
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] :
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] :
            self.rect.y += self.velocidade
        if not self.colisao_parede(parede):
            print(self.rect.topleft)
            self.rect.topleft=p
        
    def colisao_parede(self, parede: mapa.Parede):
        if pygame.sprite.spritecollide(self, parede, False):
            return False
        else:
            return True
        
