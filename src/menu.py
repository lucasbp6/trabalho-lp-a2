import pygame
import fase1 as f
import fase2 as f2
import sys
import os

LARGURA, ALTURA = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
#pygame.init()
FONTE = pygame.font.SysFont('arial', 30, False, False)
FONTE2 = pygame.font.SysFont('arial', 70, False, False)

#TELA = pygame.display.set_mode((LARGURA, ALTURA))
#pygame.display.set_caption('Menu')
# Parametrizar tudo, deixando em classes

class Text:
    
    def __init__(self,texto,  fonte, posicao_y, cor, cor_box, borda, posicao_x = None):
        self.render = fonte.render(texto, True, cor)
        self.cor = cor
        self.cor_box = cor_box
        self.tamanho = self.render.get_size()
        if posicao_x == None:
            self.posicao = ((LARGURA - self.tamanho[0])/2, posicao_y)
        else:
            self.posicao = (posicao_x, posicao_y)
        self.box = pygame.Rect(self.posicao[0] - borda, self.posicao[1] - borda, self.tamanho[0] + 2*borda, self.tamanho[1] + 2*borda)

    def desenhar(self, tela):
        tela.blit(self.render, self.posicao)  

    def on_contact(self, mouse_pos, tela):
        if self.box.collidepoint(mouse_pos):
            pygame.draw.rect(tela,self.cor_box, self.box)

    def on_click(self, click, func = None, tela = None):
        if click == None:
            return
        if self.box.collidepoint(click):
            if func != None:
                func(tela)
                return True
            else:
                return True
        return False
            
    def update(self, tela, mouse_pos, mouse_click, funcao = None):
        self.on_contact(mouse_pos, tela)
        self.on_click(mouse_click, funcao, tela)
        self.desenhar(tela)
    
class SelectPlayer:

    def __init__(self, folder, archive, num):
        self.address = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),folder, archive)
        self.image = pygame.transform.scale(pygame.image.load(self.address).convert_alpha(), (LARGURA/5, ALTURA/3))
        self.rect = pygame.Rect((num*2 + num - 2)*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
        self.num = num
        self.bordas = []

    def draw(self, tela):
        for borda in self.bordas:
            pygame.draw.rect(tela, (255,255,255), borda)
        tela.blit(self.image, ((self.num*3 - 2)*LARGURA/10, ALTURA/3))

    def on_contact(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.bordas.append(pygame.Rect(self.rect.x - 10, self.rect.y - 10, LARGURA/5 + 20, ALTURA/3 + 20))
            """self.bordas.append(pygame.Rect(self.rect.x - 10, self.rect.y - 10, LARGURA/5 + 20, 10))
            self.bordas.append(pygame.Rect(self.rect.x + LARGURA/5, self.rect.y - 10, 10, ALTURA/3 + 20))
            self.bordas.append(pygame.Rect(self.rect.x - 10, self.rect.y - 10, 10, ALTURA/3 +20))
            self.bordas.append(pygame.Rect(self.rect.x - 10, self.rect.y + ALTURA/3, LARGURA/5 +20, 10))"""
        else:
            self.bordas = []

    def on_click(self, click):
        if self.rect.collidepoint(click):
            f2.play(self.address)

    def update(self, tela, mouse_pos, mouse_click):
        self.on_contact(mouse_pos)
        if mouse_click != None:
            self.on_click(mouse_click)
        self.draw(tela)



def novo_jogo(tela):
    titulo = Text("Escolha seu persongem",FONTE2, 80, WHITE, GREEN,  10)
    back = Text("Voltar",FONTE, ALTURA-35, WHITE, GREEN, 5, LARGURA - 100)

    p1 = SelectPlayer("assets", "samyra.png", 2)
    p2 = SelectPlayer("assets", "lucas.png", 1)
    p3 = SelectPlayer("assets", "gabriel.png",3)

    selection = True
    while selection:
        click = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos


        pos = pygame.mouse.get_pos() 
        tela.fill(BLACK)
        p1.update(tela, pos, click)
        p2.update(tela, pos, click)
        p3.update(tela, pos, click)

        if back.on_click(click):
            selection = False
        back.on_contact(pos, tela)
        titulo.desenhar(tela)
        back.desenhar(tela)
        pygame.display.flip()
    return

def verifica_codigo(codigo):
    if codigo == "1111":
        print(codigo)
        return True
    else:
        codigo = ''
        return False

def carregar(tela):
    titulo = Text("Digite o codigo:", FONTE2, 120, WHITE, GREEN, 10)
    back = Text("Voltar", FONTE, ALTURA-35, WHITE, GREEN, 5, LARGURA - 100)
    enter = Text("Enviar", FONTE, ALTURA/2 + 50, WHITE, GREEN, 5)
    erro_t = Text("Erro, codigo invalido", FONTE, ALTURA/2 + 100, WHITE, GREEN, 5)
    input = pygame.Rect(LARGURA/2 - 85, ALTURA/2 - 35, 170, 70)
    codigo = ''
    ativo = False 
    carregando = True
    m_erro = False
    while carregando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input.collidepoint(event.pos):
                    ativo = not ativo
                else:
                    ativo = False
                if back.on_click(event.pos):
                    carregando = False
                if enter.on_click(event.pos):
                    if not verifica_codigo(codigo):
                        m_erro = True 
                    else:
                        pass
                        #fazer com que entre no jogo
                    codigo = ''
                
            if event.type == pygame.KEYDOWN:
                if ativo:
                    if event.key == pygame.K_RETURN:
                        if not verifica_codigo(codigo):
                            m_erro = True 
                        else:
                            pass
                            #fazer com que entre no jogo
                        codigo = ''
                    elif event.key == pygame.K_BACKSPACE:
                        codigo = codigo[:-1]  
                    elif len(codigo) > 3:
                        pass
                    else:
                        codigo += event.unicode  

        codigo_render = FONTE2.render(codigo, True, WHITE)

        tela.fill(BLACK)
        pos = pygame.mouse.get_pos() 

        tela.blit(codigo_render, (input.x + 5, input.y + 5))
        pygame.draw.rect(tela, GREEN, input, 2)
        if m_erro:
            erro_t.desenhar(tela)
        enter.on_contact(pos, tela)
        back.on_contact(pos, tela)
        titulo.desenhar(tela)
        back.desenhar(tela)
        enter.desenhar(tela)
        pygame.display.flip()

    return

def hub(tela):
    fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "hub.jpeg"))
    running_hub = True
    #titulo = Text("Jogo feito pelo grupo", FONTE2, 110, WHITE, GREEN,  10)
    txt = Text("Novo jogo", FONTE, 275, WHITE, GREEN, 5)
    txt2 = Text("Carregar", FONTE, 325, WHITE, GREEN, 5)
    txt3 = Text("Sair", FONTE, 375, WHITE, GREEN, 5)
    while running_hub:
        click_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_hub = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos

        pos = pygame.mouse.get_pos() 

        tela.blit(fundo,(0,0))
        txt.update(tela, pos, click_pos, novo_jogo)
        txt2.update(tela, pos, click_pos, carregar)
        txt3.update(tela, pos, click_pos, pygame.quit)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption('Menu')
    hub(TELA)

    pygame.quit()