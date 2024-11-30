import pygame

fonte = pygame.font.SysFont('arial', 25, False, False)

#a mexer
class Coletavel:
    def __init__(self):
        self.lista = []
        self.targets = False
        self.name = ''
        self.position = []
        self.barra = pygame.Rect(10, 30, 0, 6)
        self.total = 0

    def exibir(self, nome, posicao, total):
        self.nome = fonte.render(nome, True, (255,255,255))
        self.position = posicao
        self.targets = True
        self.total = total

    def add(self, path, x, y, largura, altura):
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (largura,altura))
        rect = image.get_rect()
        rect.topleft = [x,y]
        self.lista.append([image, rect, path])

    def draw(self, tela, personagem):
        if self.targets:
            tela.blit(self.nome, (8,2)) 
            pygame.draw.rect(tela,(255,255,255), pygame.Rect(8, 28, 100, 10))
            self.barra.width = personagem.coletou*96/self.total
            pygame.draw.rect(tela,(0,0,255), self.barra)

        for coletavel in self.lista:
            tela.blit(coletavel[0],coletavel[1])

    def colisao(self, personagem):
        for coletavel in self.lista:
            if coletavel[1].colliderect(personagem.rect):
                personagem.coletou += 1
                self.lista.remove(coletavel)
                return coletavel
        return None
                
    def update(self, tela, personagem):
        self.draw(tela, personagem)
        return self.colisao(personagem)

