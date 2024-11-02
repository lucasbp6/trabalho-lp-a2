import pygame

LARGURA, ALTURA = 800, 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
# Parametrizar tudo, deixando em classes
class Text:

    def __init__(self,texto,  fonte, posicao_y, cor, cor_box, borda):
        self.render = fonte.render(texto, True, cor)
        self.cor = cor
        self.cor_box = cor_box
        self.tamanho = self.render.get_size()
        self.posicao = ((LARGURA - self.tamanho[0])/2, posicao_y)
        self.box = pygame.Rect(self.posicao[0] - borda, self.posicao[1] - borda, self.tamanho[0] + 2*borda, self.tamanho[1] + 2*borda)
    
    #def box(self, borda):
    #    pygame.Rect(self.posicao[0] - borda, self.posicao[1] - borda, self.tamanho[0] + 2*borda, self.tamanho[1] + 2*borda)

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
            print("apertou")


pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Menu')
#pygame.clock.tick(30)
running = True
cora = (0,0,0)
corb = (0,255,0)
fonte = pygame.font.SysFont('arial', 30, False, False)
fonte2 = pygame.font.SysFont('arial', 70, False, False)
cor4 = cora

titulo = Text("Jogo feito pelo grupo",fonte2, 110, WHITE, GREEN,  10)


txt = fonte.render("Novo jogo", True, (255,255,255))
r_l, r_a = txt.get_size()
rect = pygame.Rect((LARGURA - r_l)/2 -5, 275,r_l+10, r_a+10 )

txt2 = fonte.render("Carregar", True, (255,255,255))
r_l2, r_a2 = txt2.get_size()
rect2 = pygame.Rect((LARGURA - r_l2)/2 -5, 325,r_l2+10, r_a2+10 )

txt3 = fonte.render("Sair", True, (255,255,255))
r_l3, r_a3 = txt3.get_size()
rect3 = pygame.Rect((LARGURA - r_l3)/2 -5, 375,r_l3+10, r_a3+10 )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos
            if rect.collidepoint(click_pos):
                print("novo jogo")
            if rect2.collidepoint(click_pos):
                print('carregar')
            if rect3.collidepoint(click_pos):
                running = False
    pos = pygame.mouse.get_pos() 
    
    if rect.collidepoint(pos):
        cor = corb
    else:
        cor = cora

    if rect2.collidepoint(pos):
        cor2 = corb
    else:
        cor2 = cora
    if rect3.collidepoint(pos):
        cor3 = corb
    else:
        cor3 = cora
    tela.fill((0,0,0))

    titulo.on_contact(pos, tela)
    pygame.draw.rect(tela, cor2, rect2)
    pygame.draw.rect(tela, cor3, rect3)
    pygame.draw.rect(tela, cor, rect)

    titulo.desenhar(tela)
    #tela.blit(titulo, ((LARGURA - t_l)/2 , 100 + 10))
    tela.blit(txt, ((LARGURA - r_l)/2, 280))
    tela.blit(txt2, ((LARGURA - r_l2)/2, 330))
    tela.blit(txt3, ((LARGURA - r_l3)/2, 380))
    pygame.display.flip()

pygame.quit()