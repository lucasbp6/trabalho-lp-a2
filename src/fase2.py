import pygame
import perso_test as p
import paredes as pa
import sys
import os
pygame.init()

LARGURA, ALTURA = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

        
def play(path, x=375, y=275):
    rodar = True
    tela = pygame.display.set_mode((800, 600))
    teste = p.PersonagemTeste(x, y, path)
    #inimigo = p.Inimigo()
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    #Paredes com portas
    lista.add(pa.Parede(0, 0, LARGURA/2 - 40, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 40, 0, LARGURA/2 - 40, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 - 45, 5, 5, 7, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 40, 5, 5, 7, WHITE))

    lista.add(pa.Parede(0, ALTURA-5, LARGURA/2 - 40, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-5, LARGURA/2 - 40, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 - 45, ALTURA-10, 5, 7, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-10, 5, 7, WHITE))
    
    lista.add(pa.Parede(0,0,5, ALTURA/2 - 40, WHITE)) 
    lista.add(pa.Parede(0, ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE))
    lista.add(pa.Parede(5, ALTURA/2 + 40, 7, 5, WHITE))
    lista.add(pa.Parede(5, ALTURA/2 - 45, 7, 5, WHITE))
    
    lista.add(pa.Parede(795,0,5, ALTURA/2 - 40, WHITE)) 
    lista.add(pa.Parede(795,ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE)) 
    lista.add(pa.Parede(788, ALTURA/2 - 45, 7, 5, WHITE))
    lista.add(pa.Parede(788, ALTURA/2 + 40, 7, 5, WHITE))
    #Fim das paredes com portas

    #Postos para colocar cada um dos itens coletados em cada porta
    lista.add(pa.Parede(LARGURA/2 + 100, ALTURA/2 -150, 50, 50, GREEN))
    lista.add(pa.Parede(LARGURA/2 - 150, ALTURA/2 -150, 50, 50, GREEN))
    lista.add(pa.Parede(LARGURA/2 + 100, ALTURA/2 +100, 50, 50, GREEN))
    lista.add(pa.Parede(LARGURA/2 - 150, ALTURA/2 +100, 50, 50, GREEN))

    #coletaveis = c.Coletaveis()
    #coletaveis.add(c.Coletavel(500,40,40, 40, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "bet.png")))
    #coletaveis.add(c.Coletavel(500,500,40, 40, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "bet.png")))
    #coletaveis.add(c.Coletavel(500,300,40, 40, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "bet.png")))

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
        perso_pos = teste.movimento(botao)
        if perso_pos[0] < -20:
            porta4(path, tela)
            teste = p.PersonagemTeste(0, 275, path)
        elif perso_pos[0] > 820:
            porta2(path, tela)
            teste = p.PersonagemTeste(750, 275, path)
        elif perso_pos[1] > 620:
            porta3(path, tela)
            teste = p.PersonagemTeste(375, 550, path)
        elif perso_pos[1] < -20:
            porta1(path, tela)
            teste = p.PersonagemTeste(375, 0, path)
        #lista.colisao(teste, botao)
        #lista.movimento(teste, botao)
        # Personagem -- modulo
        teste.update(tela)
        #inimigo.update(tela)
        # -----------

        lista.draw(tela)
        #coletaveis.draw(tela)

        pygame.display.flip()

    pygame.quit()

def porta1_p2(path, tela, x):
    rodar = True
    personagem = p.PersonagemTeste(x, ALTURA - 50, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    lista.add(pa.Parede(0,0, LARGURA, 5, WHITE))
    lista.add(pa.Parede(0, 0, 5, ALTURA, WHITE))
    lista.add(pa.Parede(LARGURA-5, 0, 5, ALTURA, WHITE))

    #lado direito
    lista.add(pa.Parede(550, 540, 10, 60, WHITE))
    lista.add(pa.Parede(350, 360, 300, 10, WHITE))
    lista.add(pa.Parede(590, 0, 10, 230, WHITE))
    lista.add(pa.Parede(170, 160, 310, 10, WHITE))
    #lado esquerdo
    lista.add(pa.Parede(0,490, 360, 10, WHITE ))
    lista.add(pa.Parede(350, 160, 10, 340, WHITE))
    lista.add(pa.Parede(350, 0, 10, 70, WHITE))
    lista.add(pa.Parede(0, 270, 220, 10, WHITE))
    lista.add(pa.Parede(90, 380, 260, 10, WHITE))

    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        print(pygame.mouse.get_pos())
        if botao[pygame.K_q]:
            rodar = False
        perso_pos = personagem.movimento(botao)
        if perso_pos[1] > 620:
            rodar = False
        
        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()

def porta1(path, tela):
    rodar = True
    personagem = p.PersonagemTeste(LARGURA/2 - 25, ALTURA -50, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    #Paredes com portas
    #lista.add(pa.Parede(0, 0, LARGURA, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, 0, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, 5, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, 5, 5, 7, WHITE))

    #baixo
    lista.add(pa.Parede(0, ALTURA-5, LARGURA/2 - 60, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 60, ALTURA-5, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, ALTURA-10, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-10, 5, 7, WHITE))
    
    #esquerda
    lista.add(pa.Parede(0,0,5, ALTURA, WHITE)) 
    #lista.add(pa.Parede(0, ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE))
    #lista.add(pa.Parede(5, ALTURA/2 + 40, 7, 5, WHITE))
    #lista.add(pa.Parede(5, ALTURA/2 - 45, 7, 5, WHITE))
    
    #direita
    lista.add(pa.Parede(795,0,5, ALTURA, WHITE)) 
    #lista.add(pa.Parede(795,ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE)) 
    #lista.add(pa.Parede(788, ALTURA/2 - 45, 7, 5, WHITE))
    #lista.add(pa.Parede(788, ALTURA/2 + 40, 7, 5, WHITE))
    #Fim das paredes com portas

    #desenhando retangulos internos
    lista.add(pa.Parede(LARGURA/2 - 70, ALTURA-150, 10, 150, WHITE))
    lista.add(pa.Parede(0, ALTURA-150, 180, 10, WHITE))
    lista.add(pa.Parede(260, ALTURA-150, 70, 10, WHITE))
    lista.add(pa.Parede(200, 350, 80, 10,WHITE))
    lista.add(pa.Parede(200, 290, 10, 60, WHITE))
    lista.add(pa.Parede(100, 290, 100, 10, WHITE))
    lista.add(pa.Parede(100, 190, 10, 100, WHITE))
    lista.add(pa.Parede(200, 170, 200, 10, WHITE))
    lista.add(pa.Parede(100, 70, 300, 10, WHITE))

    #lado direito
    lista.add(pa.Parede(LARGURA/2 + 60, ALTURA-150, 10, 150, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 60, ALTURA -150, 200, 10, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 250, ALTURA - 250, 10, 100, WHITE))
    lista.add(pa.Parede(7*LARGURA/10 - 40, ALTURA/2 - 40, 3*LARGURA/10 + 40,10 , WHITE))
    lista.add(pa.Parede(7*LARGURA/10  - 40, 120, 10, 140,WHITE))
    lista.add(pa.Parede(7*LARGURA/10 + 70, 120, 170, 10, WHITE ))
    lista.add(pa.Parede(550, 0, 10, 40, WHITE))

    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        print(pygame.mouse.get_pos())
        if botao[pygame.K_q]:
            rodar = False
        perso_pos = personagem.movimento(botao)
        if perso_pos[1] > 620:
            rodar = False
        if perso_pos[1] < -20:
            porta1_p2(path, tela, perso_pos[0])
        
        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()
    return

def porta2_p2(path, tela, x):
    rodar = True
    personagem = p.PersonagemTeste(800 - x, ALTURA - 50, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    lista.add(pa.Parede(0,0, LARGURA, 5, WHITE))
    lista.add(pa.Parede(0, 0, 5, ALTURA, WHITE))
    lista.add(pa.Parede(LARGURA-5, 0, 5, ALTURA, WHITE))
    lista.add(pa.Parede(200, 595, 600, 5, WHITE))

    #lado direito
    lista.add(pa.Parede(0, 450, 600, 10, WHITE))
    lista.add(pa.Parede(200, 300, 600, 10, WHITE))
    lista.add(pa.Parede(0, 150,600, 10, WHITE))


    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        print(pygame.mouse.get_pos())
        if botao[pygame.K_q]:
            rodar = False
        perso_pos = personagem.movimento(botao)
        if perso_pos[1] > 620:
            rodar = False
        
        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()

def porta2(path, tela):
    rodar = True
    personagem = p.PersonagemTeste(0, 275, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    #Paredes com portas
    lista.add(pa.Parede(0, 0, LARGURA-200, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, 0, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, 5, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, 5, 5, 7, WHITE))

    #baixo
    lista.add(pa.Parede(0, ALTURA-5, LARGURA, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-5, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, ALTURA-10, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-10, 5, 7, WHITE))
    
    #esquerda
    lista.add(pa.Parede(0,0,5, ALTURA/2 - 40, WHITE)) 
    lista.add(pa.Parede(0, ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE))
    lista.add(pa.Parede(5, ALTURA/2 + 40, 7, 5, WHITE))
    lista.add(pa.Parede(5, ALTURA/2 - 45, 7, 5, WHITE))
    
    #direita
    lista.add(pa.Parede(795,0,5, ALTURA, WHITE)) 
    #lista.add(pa.Parede(795,ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE)) 
    #lista.add(pa.Parede(788, ALTURA/2 - 45, 7, 5, WHITE))
    #lista.add(pa.Parede(788, ALTURA/2 + 40, 7, 5, WHITE))
    #Fim das paredes com portas

    #mapa direita

    #mapa esquerda
    lista.add(pa.Parede(0, 250, 180, 10, WHITE))
    lista.add(pa.Parede(180,250,10, 250, WHITE ))
    lista.add(pa.Parede(390, 120, 10, 480, WHITE))
    lista.add(pa.Parede(590, 0, 10, 480, WHITE))

    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        
        if botao[pygame.K_q]:
            return
        perso_pos = personagem.movimento(botao)
        if perso_pos[0] < -20:
            rodar = False
        if perso_pos[1] < -20:
            porta2_p2(path, tela, perso_pos[0])
        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()
    return

def porta3_p2(path, tela, x):
    rodar = True
    personagem = p.PersonagemTeste(0, ALTURA - 50, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    lista.add(pa.Parede(0,0, LARGURA, 5, WHITE))
    lista.add(pa.Parede(0, 0, 5, 500, WHITE))
    lista.add(pa.Parede(LARGURA-5, 0, 5, 600, WHITE))
    lista.add(pa.Parede(0, 595, 800, 5, WHITE))

    #paredes moveis
    lista.add(pa.Parede(300, 410, 10, 185, (200, 0, 200)))
    lista.add(pa.Parede(450, 410, 10, 185, (200, 0, 200)))
    lista.add(pa.Parede(600, 410, 10, 185, (200, 0, 200)))

    #lado direito
    lista.add(pa.Parede(0, 400, 650, 10, WHITE))
    lista.add(pa.Parede(650, 200, 10, 210, WHITE))
    lista.add(pa.Parede(150, 200, 500, 10, WHITE))



    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        print(pygame.mouse.get_pos())
        if botao[pygame.K_q]:
            rodar = False
        perso_pos = personagem.movimento(botao)
        if perso_pos[0] < -20:
            rodar = False
        
        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()

def porta3(path, tela):
    rodar = True
    personagem = p.PersonagemTeste(375, 0, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    #Paredes com portas
    lista.add(pa.Parede(0, 0, LARGURA/2 - 40, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 40, 0, LARGURA/2 - 40, 5, WHITE))
    lista.add(pa.Parede(LARGURA/2 - 45, 5, 5, 7, WHITE))
    lista.add(pa.Parede(LARGURA/2 + 40, 5, 5, 7, WHITE))

    #baixo
    lista.add(pa.Parede(0, ALTURA-5, LARGURA, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-5, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, ALTURA-10, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-10, 5, 7, WHITE))
    
    #esquerda
    lista.add(pa.Parede(0,0,5, ALTURA, WHITE)) 
    #lista.add(pa.Parede(0, ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE))
    #lista.add(pa.Parede(5, ALTURA/2 + 40, 7, 5, WHITE))
    #lista.add(pa.Parede(5, ALTURA/2 - 45, 7, 5, WHITE))
    
    #direita
    lista.add(pa.Parede(795,0,5, ALTURA-100, WHITE)) 
    #lista.add(pa.Parede(795,ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE)) 
    #lista.add(pa.Parede(788, ALTURA/2 - 45, 7, 5, WHITE))
    #lista.add(pa.Parede(788, ALTURA/2 + 40, 7, 5, WHITE))
    #Fim das paredes com portas

    #porta vermelha
    lista.add(pa.Parede(350, 190, 100,10, (255,0,0)))

    #desenho mapa
    lista.add(pa.Parede(200, 0, 10, 200, WHITE))
    lista.add(pa.Parede(590, 0, 10, 200, WHITE))
    lista.add(pa.Parede(200, 190, 150, 10, WHITE))
    lista.add(pa.Parede(450, 190, 150, 10, WHITE))

    lista.add(pa.Parede(100, 300, 10, 300, WHITE))
    lista.add(pa.Parede(100, 400, 350, 10, WHITE))
    lista.add(pa.Parede(250, 300, 450, 10, WHITE))
    lista.add(pa.Parede(700, 300, 10, 210, WHITE))
    lista.add(pa.Parede(300, 500, 400, 10, WHITE))

    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        
        if botao[pygame.K_q]:
            return
        perso_pos = personagem.movimento(botao)
        if perso_pos[1] < -20:
            rodar = False
        if perso_pos[0] > 820:
            porta3_p2(path, tela, perso_pos[0])

        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()
    return

def porta4_p2(path, tela):
    rodar = True
    personagem = p.PersonagemTeste(750, 25, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    lista.add(pa.Parede(0,0, LARGURA, 5, WHITE))
    lista.add(pa.Parede(0, 0, 5, 600, WHITE))
    lista.add(pa.Parede(LARGURA-5, 100, 5, 500, WHITE))
    lista.add(pa.Parede(0, 595, 800, 5, WHITE))

    #paredes
    lista.add(pa.Parede(150, 120, 650, 10, WHITE))
    lista.add(pa.Parede(150, 120, 10, 360, WHITE))
    lista.add(pa.Parede(150,470, 500, 10, WHITE ))
    lista.add(pa.Parede(640, 240, 10, 240,WHITE))
    lista.add(pa.Parede(300, 240, 350, 10, WHITE))
    lista.add(pa.Parede(300, 240, 10, 120, WHITE))
    lista.add(pa.Parede(300, 360, 150, 10, WHITE))



    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        print(pygame.mouse.get_pos())
        if botao[pygame.K_q]:
            rodar = False
        perso_pos = personagem.movimento(botao)
        if perso_pos[0] > 820:
            rodar = False
        
        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()

def porta4(path, tela):
    rodar = True
    personagem = p.PersonagemTeste(750, 275, path)
    clock = pygame.time.Clock()

    lista = pa.Paredes()
    #Paredes com portas
    lista.add(pa.Parede(0, 0, LARGURA, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, 0, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, 5, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, 5, 5, 7, WHITE))

    #baixo
    lista.add(pa.Parede(0, ALTURA-5, LARGURA, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-5, LARGURA/2 - 40, 5, WHITE))
    #lista.add(pa.Parede(LARGURA/2 - 45, ALTURA-10, 5, 7, WHITE))
    #lista.add(pa.Parede(LARGURA/2 + 40, ALTURA-10, 5, 7, WHITE))
    
    #esquerda
    lista.add(pa.Parede(0,100,5, ALTURA-100, WHITE)) 
    #lista.add(pa.Parede(0, ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE))
    #lista.add(pa.Parede(5, ALTURA/2 + 40, 7, 5, WHITE))
    #lista.add(pa.Parede(5, ALTURA/2 - 45, 7, 5, WHITE))
    
    #direita
    lista.add(pa.Parede(795,0,5, ALTURA/2 - 40, WHITE)) 
    lista.add(pa.Parede(795,ALTURA/2 + 40,5, ALTURA/2 - 40, WHITE)) 
    lista.add(pa.Parede(788, ALTURA/2 - 45, 7, 5, WHITE))
    lista.add(pa.Parede(788, ALTURA/2 + 40, 7, 5, WHITE))
    #Fim das paredes com portas


    #desenhando paredes
    lista.add(pa.Parede(100, 100,70, 10, WHITE))
    lista.add(pa.Parede(100, 100, 10, 400, WHITE))
    lista.add(pa.Parede(100, 500, 70, 10, WHITE))
    lista.add(pa.Parede(620, 100, 80, 10,WHITE))
    lista.add(pa.Parede(690, 100, 10, 400,WHITE))
    lista.add(pa.Parede(620, 500, 80, 10, WHITE))
    lista.add(pa.Parede(215, 285, 50, 50,WHITE))
    lista.add(pa.Parede(375, 285, 50, 50,WHITE))
    lista.add(pa.Parede(535, 285, 50, 50,WHITE))
    lista.add(pa.Parede(235, 120, 10, 380,WHITE))
    lista.add(pa.Parede(395, 120, 10, 380, WHITE))
    lista.add(pa.Parede(555, 120, 10, 380, WHITE))


    while rodar:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False

        tela.fill((0, 0, 0))
        
        botao = pygame.key.get_pressed()
        
        if botao[pygame.K_q]:
            return
        perso_pos = personagem.movimento(botao)
        if perso_pos[0] > 820:
            rodar = False
        if perso_pos[0] < -20:
            porta4_p2(path, tela)
            personagem.rect.x = 0

        personagem.update(tela)
        lista.draw(tela)
        pygame.display.flip()
    return

if __name__ == "__main__":
    play(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "lucas.png")) 