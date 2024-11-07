import pygame
import perso_test as p
import paredes as pa
import coletavel as c
import sys
import os
pygame.init()

LARGURA, ALTURA = 800, 600
WHITE = (255, 255, 255)

        
def play(path):
    rodar = True
    teste = p.PersonagemTeste(5, 5, path)
    inimigo = p.Inimigo()
    tela = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    lista.add(pa.Parede(0, 0, LARGURA, 5, WHITE))
    lista.add(pa.Parede(0, ALTURA-5, LARGURA, 5, WHITE))

    lista.add(pa.Parede(0,0,5, ALTURA, WHITE)) 
    lista.add(pa.Parede(795,0,5, ALTURA, WHITE)) 
    lista.add(pa.Parede(45, 0, 10, ALTURA - 100, WHITE))
    lista.add(pa.Parede(500, ALTURA/2 + 40, 10, ALTURA/2 - 40, WHITE))
    lista.add(pa.Parede(500, 0, 10, ALTURA/2 - 40, WHITE))
    lista.add(pa.Parede(500,ALTURA/2 + 40, 200, 10, WHITE))
    lista.add(pa.Parede(700, 80, 10, ALTURA - 160, WHITE))

    coletaveis = c.Coletaveis()
    coletaveis.add(c.Coletavel(500,40,40, 40, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "bet.png")))
    coletaveis.add(c.Coletavel(500,500,40, 40, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "bet.png")))
    coletaveis.add(c.Coletavel(500,300,40, 40, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "bet.png")))

    while rodar:
        clock.tick(60)
        #print(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False

        tela.fill((0, 0, 0))
        botao = pygame.key.get_pressed()
        if botao[pygame.K_q]:
            return
        teste.movimento(botao)
        #lista.colisao(teste, botao)
        #lista.movimento(teste, botao)
        # Personagem -- modulo
        teste.update(tela)
        inimigo.update(tela)
        # -----------

        lista.draw(tela)
        coletaveis.draw(tela)

        pygame.display.flip()

    pygame.quit()
