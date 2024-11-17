import pygame
import modulos as menu
import fase2 as f2
import sys
import os

LARGURA, ALTURA = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
FONTE = pygame.font.SysFont('arial', 30, False, False)
FONTE2 = pygame.font.SysFont('arial', 70, False, False)

class Menu:
    def __init__(self, game):
        self.game = game
        self.objetos = []
        self.personagens = [menu.SelectPlayer("assets", "samyra.png", 2, self.game), menu.SelectPlayer("assets", "lucas.png", 1, self.game), menu.SelectPlayer("assets", "gabriel.png",3, self.game)]
        self.estados = {
            "hub": self.hub,
            "Novo jogo": self.novo_jogo,
            "Carregar": self.carregar,
            "Sair": pygame.quit,
            "Voltar": self.hub,
        }
        self.atual = self.estados['hub']
        self.troca = True
        self.codigo = ''

    def eventos(self):
        click_pos = None
        for evento in self.game.eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos
        pos = pygame.mouse.get_pos()

        if self.atual == self.novo_jogo :
            for personagem in self.personagens:
                r = personagem.update(pos, click_pos)
                if r != None:
                    print(r)
        
        for objeto in self.objetos:
            a = objeto.update(pos, click_pos)
            if a in self.estados:
                self.troca = True
                self.atual = self.estados[a]
            if a == "Enviar":
                self.verifica_codigo()

        
    def hub(self):
        if self.troca == True:
            self.objetos = [menu.Text("Novo jogo", FONTE,0,  275, WHITE, self.game, GREEN),menu.Text("Carregar", FONTE,0, 325, WHITE,  self.game, GREEN), menu.Text("Sair", FONTE, 0,375, WHITE, self.game, GREEN)]
            self.contador = False
        fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "hub.jpeg"))
        self.game.tela.blit(fundo,(0,0))
        #verificar se é melhor colocar assim ou carregar os objetos apenas aqui

        self.eventos()

    def novo_jogo(self):
        if self.troca == True:
            self.objetos = [menu.Text("Escolha seu persongem",FONTE2, 80,10,  WHITE,self.game),menu.Text("Voltar",FONTE, LARGURA - 100,ALTURA-35, WHITE,  self.game, GREEN)]
            self.contador = False
        self.game.tela.fill(BLACK)
        self.eventos()


    def verifica_codigo(self):
        print("entrei")
        if self.codigo == "1111":
            print(self.codigo)
            self.objetos.remove(menu.Text("Erro, codigo invalido", FONTE,10, ALTURA/2 + 100, WHITE, self.game))
        else:
            self.codigo = ''
            self.objetos.append(menu.Text("Erro, codigo invalido", FONTE,10, ALTURA/2 + 100, WHITE, self.game))
        return


######### arrumar a função carregar
    def carregar(self):
        if self.troca == True:
            self.objetos = [menu.Text("Digite o codigo:", FONTE2, 0, 120, WHITE, self.game), menu.Text("Voltar", FONTE,0,  ALTURA-35, WHITE, self.game, GREEN),
                            menu.Text("Enviar", FONTE,0, ALTURA/2 + 50, WHITE, self.game, GREEN)]
            self.troca = False
        input = pygame.Rect(LARGURA/2 - 85, ALTURA/2 - 35, 170, 70)

        
        for event in self.game.eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.verifica_codigo()   
                elif event.key == pygame.K_BACKSPACE:
                    self.codigo = self.codigo[:-1]  
                elif len(self.codigo) < 4:
                    self.codigo += event.unicode  

        self.game.tela.fill(BLACK)
        codigo_render = FONTE2.render(self.codigo, True, WHITE)
        self.game.tela.blit(codigo_render, (input.x + 5, input.y + 5))
        pygame.draw.rect(self.game.tela, GREEN, input, 2)
        self.eventos()

    def run(self):
        self.atual()

class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.estados = {
            "menu": Menu(self)
        }
        self.atual = self.estados["menu"]
        self.eventos = []
        self.personagem = []

    def seletor(self, fase):
        self.atual = self.estados[fase]

    def iniciar(self):
        while self.rodando:
            self.clock.tick(60)
            self.eventos = pygame.event.get()
            for evento in self.eventos:
                if evento.type == pygame.QUIT:
                    self.rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.rodando = False
            #teste de criacao
            self.seletor("menu")
            self.atual.run()

            pygame.display.flip()

        pygame.quit()

g = Game()
g.iniciar()