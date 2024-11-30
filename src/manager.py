import pygame
import mapa
import personagem
import os
import boss
import interagiveis


coracao = pygame.transform.scale(pygame.image.load("../assets/principal/vida_personagem.png"), (20,20))


# Gerencia as fases e concatena todos os modulos do jogo
class Manager:
    def __init__ (self, game):
        self.game = game
        self.tela = game.tela
        # Organizar os enderecos corretos
        self.fases = {
            "fase1": os.path.join("..", "data", "fase1_paredes.json"),
            "fase2": os.path.join("..", "config", "fase2.json"),
            "fase3": os.path.join("..", "config", "fase3.json"),
            "fase4": os.path.join("..", "data", "fase1_paredes.json"),
            "fase5": os.path.join("..","config", "fase5.json")
        }
        # Seletor padrao = fase1
        self.seletor = self.fases['fase3']
        self.troca = True
        self.quadro = 'hub'
        self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "fase3", "mapa", f"{self.quadro}.png"))
        self.load = False
        self.personagem = personagem.Perso_controle(game.path, 375,275,50,50,5) # posicoes rever
        self.inimigos = personagem.Inimigos()
        self.mapa = mapa.Mapa()
        self.coletaveis = interagiveis.Coletavel()
        
        

        #ignorar --- testes
        self.round = 1

    #carrega os parametros
    def load_mapa(self):

        #carrega todo json
        if  self.troca:
            print("testando o mapa")
            self.mapa.load(self.seletor)
            self.troca = False
            self.quadro = 'hub'
            self.personagem.rect.topleft = self.mapa.posicao

        #self.inimigos.add(boss.Boss("../assets/samyra.png",350, 50, 100,100, 1, 'boss1', ))
        #self.inimigos.add(personagem.Inimigo("../assets/samyra.png", 350, 50, 50, 50, 3, "aleatorio"))
        
        # ativa o quadro atual
        self.mapa.ativar(self.quadro)

        #carrega os inimigos
        self.inimigos.clean()
        for nimigo in self.mapa.npc:
            self.inimigos.add(personagem.Inimigo(nimigo[0], nimigo[1], nimigo[2], nimigo[3], nimigo[4], nimigo[5], nimigo[6]))   
        self.load = True

        self.coletaveis = interagiveis.Coletavel()
        for coletaveis in self.mapa.coletaveis:
            self.coletaveis.add(coletaveis[0], coletaveis[1], coletaveis[2], 50, 50)
        self.coletaveis.exibir("objetivos", (8,80), self.mapa.objetivo)
            
    #verifica qual o proximo quadro
    def portas(self):
        x, y = self.personagem.rect.center
        lim = '0'

        if y < -20:
            lim = '1'
        if x > 820:
            lim = '2'
        if y > 620:
            lim = '3'
        if x < -20:
            lim = '4'

        if lim != '0':
            #define o validador para poder carregar o novo quadro
            self.load = False
            self.quadro = self.mapa.portas[lim][0]
            
            if self.quadro in self.fases:
                self.troca = True
                self.seletor = self.fases[self.quadro]
                return

            self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "fase3", "mapa", f"{self.quadro}.png"))
            #altera as posicoes de acordo com o json
            # uma posicao = -1 indica mante-la
            x, y = self.mapa.portas[lim][1]
            if x == -1:
                pass
            else:
                self.personagem.rect.x = x
            if y == -1:
                pass
            else:
                self.personagem.rect.y = y
                
    #roda o jogo chamando os updates
    def run(self):
        if not self.load:
            self.load_mapa()
        self.tela.blit(self.fundo, (0,0))

        mortes = self.inimigos.update(self.tela, self.mapa.paredes, self.personagem, True)
        for inimigo in mortes:
            self.mapa.dados[self.quadro]["inimigos"].remove(inimigo.inicial)

        '''if self.inimigos.update(self.tela, self.mapa.paredes, self.personagem, True):
            if self.round == 2:
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 50,50, 1, 'boss3', ))
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 50,50, 1, 'boss3', ))
            if self.round == 1:
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 70,70, 1, 'boss2', ))
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 70,70, 1, 'boss2', ))
                self.round = 2'''
        
        """TESTES DE EXIBICAO DE VIDA E PROGRESSO"""
        for i in range(self.personagem.vida):
            self.tela.blit(coracao, (770 - 22*i, 10))
 
        
        self.personagem.update(self.tela, self.mapa.paredes, self.inimigos)
        #print(self.personagem.vida)
        #self.mapa.draw(self.tela)

        coletavel = self.coletaveis.update(self.tela, self.personagem)
        if coletavel != None:
            self.mapa.dados[self.quadro]["coletaveis"].remove({"path" :coletavel[2], "x":coletavel[1].x, "y": coletavel[1].y})

        self.portas()
        #print(pygame.mouse.get_pos())