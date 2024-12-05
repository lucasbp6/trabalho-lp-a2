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
    Caixas iterativas de texto fixo para usar em menu ou afins
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

    def _desenhar(self):
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

    def _on_contact(self, mouse_pos):
        """
        verifica se o ponteiro do mouse esta sob o texto
        em caso positivo cria um contorno de fundo com a cor definida
        se na criacao exite uma cor definida

        Parametros
        ----------
        mouse_pos: tuple
            posicao do mouse na tela

        Retorno
        -------
        Nao retorna valor algum
        """
        if self.cor == None:
            return
        if self.box.collidepoint(mouse_pos):
            pygame.draw.rect(self.tela,self.cor, self.box)

    def _on_click(self, click):
        """
        Verifica se houve um click do usuario no texto
        
        Parametros
        ----------
        click: 
            local onde o usuario clickou

        Retorno
        -------
        None
            caso o click nao foi no texto
        self.texto
            caso o click foi no texto
        """
        if click == None:
            return None
        if self.box.collidepoint(click):
            return self.texto
        return None
            
    def update(self, mouse_pos, mouse_click):
        """
        realiza o update de todo o texto,
        faz a conexao com as funcoes privadas

        Parametros
        ----------
        mouse_pos: tuple
            tupla indicando a posicao atual do mouse na tela
        mouse_click:
            None caso nao tenha click ou a posicao do click

        Retorno
        -------
        self._on_click(mouse_click): str
            caso exista um click, retorna uma string com o nome do texto
        """
        self._on_contact(mouse_pos)
        self._desenhar()
        return self._on_click(mouse_click)
    
#blocos de imagem para selecao de personagens
class SelectPlayer:
    """
    Caixas de exibicao de personagens para selecao no menu
    """
    def __init__(self, path, num, game):
        """
        Parametros
        ----------
        path: str
            indica o nome do personagem
        num: int 
            variavel para demarcar a ordem de exibicao
        game: Game
            recebe a classe game para acessar a tela principal
        """
        self.tela = game.tela
        self.path = path
        self.address = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets","personagens", f"{path}.png")
        self.image = pygame.transform.scale(pygame.image.load(self.address).convert_alpha(), (LARGURA/5, ALTURA/3))
        self.rect = pygame.Rect((num*2 + num - 2)*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
        self.num = num
        self.bordas = []

    def _draw(self):
        """
        desenha na tela o personagem e possiveis bordas

        Parametros
        ----------
        nao recebe parametros

        Retorno
        -------
        nao retorna valor algum
        """
        for borda in self.bordas:
            pygame.draw.rect(self.tela, (255,255,255), borda)
        self.tela.blit(self.image, ((self.num*3 - 2)*LARGURA/10, ALTURA/3))

    def _on_contact(self, mouse_pos):
        """
        Verifica se o mouse esta sobre o personagem
        para poder criar uma borda ao redor dele
        
        Parametros
        ----------
        mouse_pos: tuple
            indica a posicao atual do mouse na tela
        
        Retorno
        -------
        nao ha reotno algum
        """
        if self.rect.collidepoint(mouse_pos):
            self.bordas.append(pygame.Rect(self.rect.x - 10, self.rect.y - 10, LARGURA/5 + 20, ALTURA/3 + 20))
        else:
            self.bordas = []

    def _on_click(self, click):
        """
        verifica se houve um click e relatar click

        Parametros
        ----------
        click: tuple
            None caso na haja click e tupla caso exista

        Retorno
        -------
        None
            caso nao exista click ou o click nao esteja sobre
        self.path: str
            retorna o nome do personagem
        """
        if click != None:
            if self.rect.collidepoint(click):
                return self.path
        return None

    def update(self, mouse_pos, mouse_click):
        """
        realiza o update de todo o texto,
        faz a conexao com as funcoes privadas

        Parametros
        ----------
        mouse_pos: tuple
            tupla indicando a posicao atual do mouse na tela
        mouse_click:
            None caso nao tenha click ou a posicao do click

        Retorno
        -------
        self._on_click(mouse_click): str
            caso exista um click, retorna uma string com o nome do texto
        """
        self._on_contact(mouse_pos)
        self._draw()
        return self._on_click(mouse_click)
        
