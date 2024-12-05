import pygame
import ui_menu as menu
import manager
import sys
import os

LARGURA, ALTURA = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
FONTE = pygame.font.SysFont('arial', 30, False, False)
FONTE2 = pygame.font.SysFont('arial', 70, False, False)

class Menu:
    #ja tem na memoria os botoes dos personagens e tem os objetos vazios para trocar de tela no menu
    def __init__(self, game):
        self.game = game
        self.objetos = []
        self.personagens = [menu.SelectPlayer("samyra", 2, self.game), menu.SelectPlayer("lucas", 1, self.game), menu.SelectPlayer("gabriel",3, self.game)]
        self.estados = {
            "hub": self.hub,
            "Novo jogo": self.novo_jogo,
            "Carregar": self.carregar,
            "Sair": pygame.quit,
            "Voltar": self.hub,
            "fases": self.fase_seletor
        }
        self.atual = self.estados['hub']
        self.troca = True
        self.codigo = ''

    # verifica todos eventos que acontecem no menu
    def eventos(self):
        click_pos = None
        for evento in self.game.eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos
        pos = pygame.mouse.get_pos()
        #na tela de novo jogo, as funções que representam as imagens do personagem retornam o endereço deles quando clicadas
        if self.atual == self.novo_jogo :
            for personagem in self.personagens:
                r = personagem.update(pos, click_pos)
                if r != None:
                    #define o path do personagem e troca o seletor do game para a classe responsavel pelas fases
                    self.game.path = r
                    self.atual = self.estados['fases']
                    
        #caso click troca entre as telas do menu
        for objeto in self.objetos:
            a = objeto.update(pos, click_pos)
            if a in self.estados:
                self.troca = True
                self.atual = self.estados[a]
            if a == "Enviar":
                self.verifica_codigo()
            if a in self.game.stats:
                if a == 'fase1':
                    self.game.fase = 1
                if a == 'fase2':
                    self.game.fase = 2
                if a == 'fase3':
                    self.game.fase = 3
                if a == 'fase4':
                    self.game.fase = 4
                if a == 'fase5':
                    self.game.fase = 5    
                self.game.seletor('fase')

    #primeiro contato do usuario com o menu   
    def hub(self):
        # se acabou de abrir essa funcao, carrega os objetos dela mesma
        if self.troca == True:
            self.objetos = [menu.Text("Novo jogo", FONTE,0,  275, WHITE, self.game, BLUE),menu.Text("Carregar", FONTE,0, 325, WHITE,  self.game, BLUE), menu.Text("Sair", FONTE, 0,375, WHITE, self.game, BLUE)]
            self.troca = False
        fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "principal", "hub.png"))
        self.game.tela.blit(fundo,(0,0))

    def fase_seletor(self):
        if self.troca == True:
            self.objetos = [menu.Text("Escolha a fase dentre as disponiveis",FONTE, 80,10,  WHITE,self.game),menu.Text("Voltar",FONTE, LARGURA - 100,ALTURA-35, WHITE,  self.game, GREEN)]
            self.contador = False
            i = 1
            liberado = True
            for key, value in self.game.stats.items():
                if liberado:
                    self.objetos.append(menu.Text(f"{key}", FONTE2,0,  50+80*i, WHITE, self.game, BLUE))
                    i += 1
                liberado = False
                if value != 0:
                    liberado = True
        self.game.tela.fill(BLACK)

    #renderiza as imagens do jogadores para escolher    
    def novo_jogo(self):
        if self.troca == True:
            self.objetos = [menu.Text("Escolha seu persongem",FONTE2, 80,10,  WHITE,self.game),menu.Text("Voltar",FONTE, LARGURA - 100,ALTURA-35, WHITE,  self.game, GREEN)]
            self.contador = False
        self.game.tela.fill(BLACK)
        
    #funcao em desenvolvimento para um futuro, caso de tempo
    def verifica_codigo(self):
        if self.codigo == "1111":
            print(self.codigo)
            self.objetos.remove(menu.Text("Erro, codigo invalido", FONTE,10, ALTURA/2 + 100, WHITE, self.game))
        else:
            self.codigo = ''
            self.objetos.append(menu.Text("Erro, codigo invalido", FONTE,10, ALTURA/2 + 100, WHITE, self.game))
        return


######### em desenvolvimento para salvar o jogo
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

    #roda o loop atual
    def run(self):
        self.atual()
        #verifica todos eventos, inclusive o de troca de cores
        self.eventos()

class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.estados = {
            "menu": Menu,
            "fase": manager.Manager
        }
        self.atual = self.estados["menu"](self)
        self.eventos = []
        self.personagem = []
        self.path = ''
        self.fase = 1
        self.stats = {
            "fase1": 0,
            "fase2": 0,
            "fase3": 0,
            "fase4": 0,
            "fase5": 0
        }

    #troca entre o menu e as fases do jogo
    def seletor(self, fase):

        self.atual = self.estados[fase](self)

    #loop principal do jogo, coleta os principais eventos
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
            #chama a fncao atual para modificar a tela
            self.atual.run()

            pygame.display.flip()

        pygame.quit()

g = Game()
g.iniciar()