import pygame

'''Uma ideia pra organização das classes do projeto. Por enquanto está bem incompleto(não implementei basicamente nada), mas conforme formos adicionando
coisas vamos incrementando. Talvez valha a pena colocar o "personagem" (que planejo dividir entre os inimigos e o personagem principal) herdando a classes
objeto, mas conforme for evoluindo no código decidimos isso melhor''' 

'''
class Objeto():
    def __init__(self,posx,posy,larg,alt,color):
        self.rect = pygame.Rect(posx ,posy ,larg ,alt)
        self.color = color
        
    def draw_object(object,Tela):
        pygame.draw.rect(Tela.screen,self.color,self.rect)
'''
        
        
    

class Tela:
    def __init__(self, height, width, image, legenda, objetos):
        self.screen = pygame.display.set_mode((height,width))
        self.legenda = pygame.display.set_caption(legenda)
        
    def desenhar_personagem(self,personagem):
        pygame.draw.rect(self.screen,personagem.color,personagem.rect)
            


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

class Jogo():
        
    def __init__(self):
        self.Background = Tela(480,600,None,"Teste",None)
        self.personagem = Personagem((100,100,193),240,300,40,40)   

        
    def run(self):
        pygame.init()
        self.Background.screen
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            keys = pygame.key.get_pressed()
            self.Background.screen.fill((0,0,0))
            self.Background.desenhar_personagem(self.personagem)
            self.personagem.movements(keys)
            
            pygame.display.flip()
            
        pygame.quit()
        

if __name__ == '__main__': 
    jojo = Jogo()
    jojo.run()
