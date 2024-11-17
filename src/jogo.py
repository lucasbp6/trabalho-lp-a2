import pygame
from config import LARGURA_TELA, ALTURA_TELA, COR_FUNDO
from personagem import Personagem
from mapa import Parede

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("The Last Minute Coding")
        self.clock = pygame.time.Clock()
        self.personagem = Personagem(50, 50, "sprite.png")
        self.todas_sprites = pygame.sprite.Group()
        self.todas_sprites.add(self.personagem)
        
        self.paredes = pygame.sprite.Group()
        parede = Parede(300, 300, 50, 200)
        self.paredes.add(parede)
        self.todas_sprites.add(parede)

    def rodar(self):
        executando = True
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False

            teclas = pygame.key.get_pressed()
            self.personagem.atualizar(teclas, self.paredes)
            
            if not self.personagem.colisao_parede(self.paredes):
                print("colisão detectada")

            self.tela.fill(COR_FUNDO)
            self.todas_sprites.draw(self.tela)
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()