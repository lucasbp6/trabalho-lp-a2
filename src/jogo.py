import pygame
from sys import exit


filepath = "..\data\labirintodiminuido.png"

class Labirinto:
    def __init__(self,filepath:str):
        self.image = pygame.image.load(filepath)
    
    def localizar_paredes(self):
        limites = []
        wall_color = (0,0,0)
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                if self.image.get_at((x, y))[:3] == wall_color:
                    parede = Objeto(wall_color,x,y, 1, 1)
                    limites.append(parede)
        return limites

"""
Define as paredes analisando a cor onde estão as cores pretas
na imagem. Literalmente muito simples e símio da minha parte,
não deve funcionar

"""





class Objeto:
    def __init__(self,color,posx: int,posy: int,larg: int,alt: int):
        self.rect = pygame.Rect(posx ,posy ,larg ,alt)
        self.color = color
"""
Essa classe seria usada para representar objetos (IMÓVEIS)
do jogo. A ser revisitada na formulação, mas por enquanto é
suficiente.
"""



class Tela:
    def __init__(self, height, width, image, legenda):
        self.screen = pygame.display.set_mode((height,width))
        self.legenda = pygame.display.set_caption(legenda)
        
    def desenhar_personagem(self,personagem):
        pygame.draw.rect(self.screen,personagem.color,personagem.rect)
        
    def draw_object(self,objeto):
        pygame.draw.rect(self.screen,objeto.color,objeto.rect)
"""
Essa classe é usada para representar a tela do jogo, ou seja,
onde irá se passar o jogo. Provavelmente quando aplicarmos mudanças
de tela, ou criaremos uma nova ou criaremos algo parecido com uma
tela de loading.
"""



class Personagem:
    def __init__(self,color,x, y, width = 40, height = 40):
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        
    def actions(self):
        pass
    def movements(self,keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2
        if keys[pygame.K_UP]:
            self.rect.y -= 2
        if keys[pygame.K_DOWN]:
            self.rect.y += 2
"""
Essa classe representa o personagem jogável.
 Já introduzi a movimentação.
"""



class Jogo():
        
    def __init__(self):
        self.Background = Tela(800,600,None,"Teste")
        self.personagem = Personagem((100,100,193),10,20,32,32)
        self.Labirinto = Labirinto(filepath)

        
    def run(self):
        pygame.init()
        self.Background.screen
        wall_list = self.Labirinto.localizar_paredes() 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            self.Background.screen.fill((255,255,255))
            self.Background.desenhar_personagem(self.personagem)
            self.personagem.movements(keys)
            
            for wall in wall_list:
                self.Background.draw_object(wall)
            
            clock = pygame.time.Clock()
            clock.tick(30)
            pygame.display.flip()
            
        pygame.quit()

"""
Essa classe representa o jogo rodando, obviamente.
"""
if __name__ == '__main__': 
    jojo = Jogo()
    jojo.run()
