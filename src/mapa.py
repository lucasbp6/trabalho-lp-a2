import pygame
import json


class Mapa:
    # Inicia todas as listas relacionadas ao mapa presentes no json
    def __init__(self):
        self.paredes = []
        self.portas = []
        self.npc = []
        self.coletaveis = []
        self.dados = None

    #Carrega todo o arquivo json da fase para a memoria
    def load(self, path):
        with open(path, 'r') as arquivo:
            print(path)
            dados = json.load(arquivo)
        self.dados = dados

    #Ativa um quadro especifico do mapa, de acordo com o personagem
    def ativar(self, chave):
        if self.dados == None:
            raise TypeError("Nao ha dados carregados")
        
        #carrega as paredes do mapa
        self.paredes = []
        paredes = self.dados[chave]["paredes"]
        for i in range(len(paredes)):
            rect = pygame.Rect(paredes[i]['x'], paredes[i]['y'], paredes[i]['largura'], paredes[i]['altura'])
            self.paredes.append(rect)
        
        #carrega as portas do mapa
        self.portas = self.dados[chave]["portas"]
        
        #carrega os inimigos do mapa
        self.npc = []
        for inimigos in self.dados[chave]["inimigos"]:
            if len(inimigos) != 0:
                #verifica se o inimigo ja foi morto 'f'
                if inimigos[7] == "t":
                    self.npc.append([inimigos[0], inimigos[1], inimigos[2], inimigos[3], inimigos[4], inimigos[5], inimigos[6]])
        
        self.coletaveis = []
        for coletaveis in self.dados[chave]["coletaveis"]:
            self.coletaveis.append([coletaveis["path"],coletaveis["x"], coletaveis["y"]] )


    '''REMOVER QUANDO TERMINAR DE USAR'''
    #apenas para visualizacao do mapa
    def draw(self, tela):
        for parede in self.paredes:
            pygame.draw.rect(tela, (255,155,243), parede)  
        