import pygame
from sys import exit
from load_json import data_loader
import os

filepath = os.path.join("..", "data", "fase1_paredes.json")


def data_loader(caminho:str):
    with open(caminho,"r") as file:
        data = json.load(file)
    return data
"""
Carrega dados de um arquivo json
"""



class Paredes:
    def __init__(self,color:tuple,dados:str):
        self.walls = dados
        self.cor = color
        
    def get_walls(self):
        wall_list = []
        for wall in self.walls:
            parede = Objeto(self.cor, wall["x"], wall["y"], wall["width"], wall["height"])
            wall_list.append(parede)
        return wall_list
        
        
        


class Objeto:
    def __init__(self,color,posx: int,posy: int,larg: int,alt: int):
        self.rect = pygame.Rect(posx ,posy ,larg ,alt)
        self.color = color
        
    def on_collision(self,personagem):
        if self.rect.colliderect(personagem.rect):
            if self.rect.topleft[0] = personagem.rect.x:
                personagem.rect.right = self.rect.left
            elif self.rect.topleft[1] = personagem.rect.y:
                personagem.rect.bottom = self.rect.top


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
    def __init__(self,color,x, y,speed_x,speed_y, width = 40, height = 40):
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.vel_x = speed_x
        self.vel_y = speed_y
        
    def actions(self):
        pass
        
    def movements(self,keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vel_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vel_x
        if keys[pygame.K_UP]:
            self.rect.y -= self.vel_y
        if keys[pygame.K_DOWN]:
            self.rect.y += self.vel_y
"""
Essa classe representa o personagem jogável.
 Já introduzi a movimentação.
"""


# class Fase_1:
    # __init__(self,paredes,ads)
















class Jogo():
        
    def __init__(self):
        self.Background = Tela(800,600,None,"Teste")
        self.personagem = Personagem((100,100,193),10,20,3,3,50,50)
        self.Paredes = Paredes((0,0,0),data_loader(filepath))

        
    def run(self):
        pygame.init()
        self.Background.screen
        walls = self.Paredes.get_walls()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            self.Background.screen.fill((255,255,255))
            self.Background.desenhar_personagem(self.personagem)
            self.personagem.movements(keys)
            
            
            for wall in walls:
                self.Background.draw_object(wall)
                wall.on_collision(self.personagem)
            
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
