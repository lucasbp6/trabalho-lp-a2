import pygame
import fase1 as f
import sys
import os

LARGURA, ALTURA = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

pygame.init()
FONTE = pygame.font.SysFont('arial', 30, False, False)
FONTE2 = pygame.font.SysFont('arial', 70, False, False)
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Menu')
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

    def size(self):
        return self.tamanho
    
    def box_draw(self, tela):
        pygame.draw.rect(tela,self.cor_box, self.box)

    def on_contact(self, mouse_pos, tela):
        if self.box.collidepoint(mouse_pos):
            self.box_draw(tela)

    def on_click(self, click):
        if self.box.collidepoint(click):
            return True
        return False
    
def selecao_personagem(tela):
    p1_i = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"samyra.png")).convert_alpha()
    p1 = pygame.transform.scale(p1_i, (LARGURA/5, ALTURA/3))

    p2_i = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"lucas.png")).convert_alpha()
    p2 = pygame.transform.scale(p2_i, (LARGURA/5, ALTURA/3))

    p3_i = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"gabriel.png")).convert_alpha()
    p3 = pygame.transform.scale(p3_i, (LARGURA/5, ALTURA/3))

    #p1 = pygame.Rect(LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
    #p2 = pygame.Rect(4*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
    #p3 = pygame.Rect(7*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
    
    #pygame.draw.rect(tela, GREEN, p1)
    #pygame.draw.rect(tela, GREEN, p2)
    #pygame.draw.rect(tela, GREEN, p3)
    tela.blit(p1, (LARGURA/10, ALTURA/3))
    tela.blit(p2, (4*LARGURA/10, ALTURA/3))
    tela.blit(p3, (7*LARGURA/10, ALTURA/3))


def novo_jogo(tela):
    titulo = Text("Escolha seu persongem",FONTE2, 80, WHITE, GREEN,  10)
    back = Text("Voltar",FONTE, ALTURA-35, WHITE, GREEN, 5, LARGURA - 100)

    p1_i = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "samyra.png")).convert_alpha()
    p1_r = pygame.transform.scale(p1_i, (LARGURA/5, ALTURA/3))
    p2_i = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "lucas.png")).convert_alpha()
    p2_r = pygame.transform.scale(p2_i, (LARGURA/5, ALTURA/3))
    p3_i = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "gabriel.png")).convert_alpha()
    p3_r = pygame.transform.scale(p3_i, (LARGURA/5, ALTURA/3))
    p1 = pygame.Rect(LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
    p2 = pygame.Rect(4*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)
    p3 = pygame.Rect(7*LARGURA/10, ALTURA/3, LARGURA/5, ALTURA/3)

    selection = True
    while selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos
                if p1.collidepoint(click):
                    f.play(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "lucas.png"))
                    return 'p1'
                if p2.collidepoint(click):
                    f.play(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "samyra.png"))
                    return 'p2'
                if p3.collidepoint(click):
                    f.play(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", "gabriel.png"))
                    return 'p3'
                if back.on_click(click):
                    selection = False
        pos = pygame.mouse.get_pos() 
        tela.fill(BLACK)
    
        tela.blit(p1_r, (4*LARGURA/10, ALTURA/3))
        tela.blit(p2_r, (LARGURA/10, ALTURA/3))
        tela.blit(p3_r, (7*LARGURA/10, ALTURA/3))

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_hub = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                if txt.on_click(click_pos):
                    personagem = novo_jogo(tela)
                    print(personagem)
                    #iniciar game
                if txt2.on_click(click_pos):
                    carregar(tela)
                if txt3.on_click(click_pos):
                    running_hub = False

        pos = pygame.mouse.get_pos() 

        tela.blit(fundo,(0,0))

        txt.on_contact(pos, tela)
        txt2.on_contact(pos,tela)
        txt3.on_contact(pos,tela)

        #titulo.desenhar(tela)
        txt.desenhar(tela)
        txt2.desenhar(tela)
        txt3.desenhar(tela)

        pygame.display.flip()

hub(TELA)

pygame.quit()