import pygame
import json
import personagem_novo as personagem
class Paredes:
    def __init__(self):
        self.paredes = []
        self.limites = []
        self.npc = []
        self.dados = None

    def load(self, path):
        with open(path, 'r') as arquivo:
            print(path)
            dados = json.load(arquivo)
        self.dados = dados

    def ativar(self, chave):
        self.paredes = []
        print(chave)
        print(type(self.dados))
        print(self.dados)
        if self.dados == None:
            raise TypeError("Nao ha dados carregados")
        paredes = self.dados[chave]["paredes"]
        print(paredes)
        for i in range(len(paredes)):
            print(paredes[i])
            rect = pygame.Rect(paredes[i]['x'], paredes[i]['y'], paredes[i]['largura'], paredes[i]['altura'])
            print('sim')
            self.paredes.append(rect)
        self.limites = self.dados[chave]["limites"]
        print(self.limites)
        print(self.dados[chave]["inimigos"])
        self.npc = []
        for inimigos in self.dados[chave]["inimigos"]:
            if len(inimigos) != 0:
                if inimigos[7] == "t":
                    self.npc.append([inimigos[0], inimigos[1], inimigos[2], inimigos[3], inimigos[4], inimigos[5], inimigos[6]])


    def draw(self, tela):
        for parede in self.paredes:
            pygame.draw.rect(tela, (255,155,243), parede)  
        