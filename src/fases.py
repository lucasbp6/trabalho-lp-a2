import pygame
import paredes
import personagem_novo as personagem
import os
import boss

# carregas os enderecos dos json das fases
class Fases:
    def __init__ (self, game):
        self.game  = game
        self.tela = game.tela
        self.fases = {
            "fase1": os.path.join("..", "data", "fase1_paredes.json"),
            "fase2": os.path.join("..", "config", "fase2.json"),
            "fase3": os.path.join("..", "data", "fase1_paredes.json"),
            "fase4": os.path.join("..", "data", "fase1_paredes.json"),
            "fase5": os.path.join("..","config", "fase5.json")
        }
        self.seletor = self.fases['fase2']
        self.quadro = 'hub'
        self.personagem = False
        self.inimigos = personagem.Inimigos()
        self.load = False
        self.troca = True
        self.mapa = paredes.Paredes()
        self.round = 1

    #carrega os parametros
    def load_mapa(self):
        #carrega todo json
        if self.troca:
            self.mapa.load(self.seletor)
            
            self.troca = False
        print('load')
        #self.inimigos.add(boss.Boss("../assets/samyra.png",350, 50, 100,100, 1, 'boss2', ))
        #self.inimigos.add(personagem.Inimigo("../assets/samyra.png", 350, 50, 50, 50, 3, "aleatorio"))
        self.mapa.ativar(self.quadro)
        self.inimigos.clean()
        for nimigo in self.mapa.npc:
            self.inimigos.add(personagem.Inimigo(nimigo[0], nimigo[1], nimigo[2], nimigo[3], nimigo[4], nimigo[5], nimigo[6]))
            
        self.load = True

    def limites(self):
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
            self.load = False
            self.quadro = self.mapa.limites[lim][0]
            x, y = self.mapa.limites[lim][1]
            if x == -1:
                pass
            else:
                self.personagem.rect.x = x
            if y == -1:
                pass
            else:
                self.personagem.rect.y = y
                

    def run(self):
        if self.personagem == False:
            self.personagem = personagem.Perso_controle(self.game.path, 375,275,50,50, 5)
        if not self.load:
            self.load_mapa()
        self.tela.fill((0,0,0))
        self.inimigos.update(self.tela, self.mapa.paredes, self.personagem, True)
        '''if self.inimigos.update(self.tela, self.mapa.paredes, self.personagem, True):
            if self.round == 2:
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 50,50, 1, 'boss3', ))
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 50,50, 1, 'boss3', ))
            if self.round == 1:
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 70,70, 1, 'boss2', ))
                self.inimigos.add(boss.Boss("../assets/samyra.png", 350, 50, 70,70, 1, 'boss2', ))
                self.round = 2'''


        self.personagem.update(self.tela, self.mapa.paredes, self.inimigos)
        #print(self.personagem.vida)
        self.mapa.draw(self.game.tela)
        self.limites()
        #print(pygame.mouse.get_pos())
