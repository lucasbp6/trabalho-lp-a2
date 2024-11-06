import pygame

'''Uma ideia pra organização das classes do projeto. Por enquanto está bem incompleto(não implementei basicamente nada), mas conforme formos adicionando
coisas vamos incrementando. Talvez valha a pena colocar o "personagem" (que planejo dividir entre os inimigos e o personagem principal) herdando a classes
objeto, mas conforme for evoluindo no código decidimos isso melhor''' 


class Objeto():
    self __init__(self,posx,posy,larg,alt,color):
        self.rect = pygame.Rect(posx ,posy ,larg ,alt)
        self.color = color
        
    def draw_object(object,Tela):
        pygame.draw.rect(Tela.screen,self.color,self.rect)
        
        
        
    

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

    
class Jogo():
        
    def __init__(self):
        pygame.init()
        self.Background = Tela(480,600,None,"Teste",None)
        self.personagem = Personagem((100,100,193),240,300,40,40)   

        
    def run(self):
        self.Background.screen.fill((0,0,0))
        running = True
        while running:
            pygame.display.flip
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            self.Background.desenhar_personagem(self.personagem)
            pygame.display.flip()
        

if __name__ == '__main__': 
    jojo = Jogo()
    jojo.run()
