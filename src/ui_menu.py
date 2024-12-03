import pygame
import sys
import os

pygame.init()
LARGURA, ALTURA = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
FONTE = pygame.font.SysFont('arial', 30, False, False)
FONTE2 = pygame.font.SysFont('arial', 70, False, False)


#blocos de texto para selecao no menu
class Text:
    """
    Caixas de texto não iterativa para usar em menu ou afins
    """
    def __init__(self, texto, fonte, x, y, cor, game, cor_caixa = None):
        """
        Parametros
        ----------
        texto: str
            texto que sera exibido
        fonte: pygame.font.Font
            fonte para o texto
        x: int
            posicao a esquerda do texo
        y: int
            posicao a cima do texto
        cor: tuple
            uma tupla indicando a cor em rgb
        game: Game
            espera receber a classe game para ter acesso a tela
        cor_caixa: tuple
            caso seja diferente de None quando passar o mouse o fundo ganha cor
        """
        self.tela = game.tela
        self.texto = texto
        self.render = fonte.render(texto, True, cor)
        self.cor = cor_caixa
        self.box = pygame.Rect(LARGURA/2 - self.render.get_size()[0]/2 , y , self.render.get_size()[0]+ 10, self.render.get_size()[1] + 10)

    def desenhar(self):
        """
        exibe as caixas de texto na tela

        Parametros
        ----------
        recebe apenas a propria classe

        Retorno
        -------
        nao retorna valor algum
        """
        self.tela.blit(self.render, (self.box.left + 5, self.box.top +5))  

    def on_contact(self, mouse_pos):
        """
        """
        if self.cor == None:
            return
        if self.box.collidepoint(mouse_pos):
            pygame.draw.rect(self.tela,self.cor, self.box)

    def on_click(self, click):
        if click == None:
            return None
        if self.box.collidepoint(click):
            return self.texto
        return None
            
    def update(self, mouse_pos, mouse_click):
        self.on_contact(mouse_pos)
        self.desenhar()
        return self.on_click(mouse_click)
    
#blocos de imagem para selecao de personagens
class SelectPlayer:

    def __init__(self, path, num, game):
        self.tela = game.tela
        self.path = path
        self.address = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets","personagens", f"{path}.png")
        self.image = pygame.transform.scale(pygame.image.load(self.address).convert_alpha(), (LARGURA/5, ALTURA/3))
        self.rect = pygame.Rect((num*2 + num - 2)*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
        self.num = num
        self.bordas = []

    def draw(self):
        for borda in self.bordas:
            pygame.draw.rect(self.tela, (255,255,255), borda)
        self.tela.blit(self.image, ((self.num*3 - 2)*LARGURA/10, ALTURA/3))

    def on_contact(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.bordas.append(pygame.Rect(self.rect.x - 10, self.rect.y - 10, LARGURA/5 + 20, ALTURA/3 + 20))
        else:
            self.bordas = []

    def on_click(self, click):
        if click != None:
            if self.rect.collidepoint(click):
                return self.path
        return None

    def update(self, mouse_pos, mouse_click):
        self.on_contact(mouse_pos)
        self.draw()
        return self.on_click(mouse_click)
        
