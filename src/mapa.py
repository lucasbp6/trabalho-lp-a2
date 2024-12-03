import pygame
import json
import personagem as per


class Mapa:
    # Inicia todas as listas relacionadas ao mapa presentes no json
    def __init__(self):
        self.paredes = []
        self.portas = []
        self.npc = []
        self.coletaveis = []
        self.objetivo = 0
        self.posicao = []
        self.dados = None

    #Carrega todo o arquivo json da fase para a memoria
    def load(self, path):
        with open(path, 'r') as arquivo:
            dados = json.load(arquivo)
        self.dados = dados
        self.objetivo = dados["objetivo"]
        self.posicao = (dados["posicao"][0], dados["posicao"][1]) 

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

        for inimigo in self.dados[chave]["inimigos"]:
            if len(inimigo) != 0:
                self.npc.append(per.Inimigo(inimigo['path'],inimigo['x'],inimigo['y'],inimigo['largura'],inimigo['altura'],inimigo['vida'],inimigo['sentido']))
    
    
        self.coletaveis = []
        for coletaveis in self.dados[chave]["coletaveis"]:
            self.coletaveis.append([coletaveis["path"],coletaveis["x"], coletaveis["y"]] )