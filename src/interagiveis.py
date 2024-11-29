import pygame

fonte = pygame.font.SysFont('arial', 17, False, False)

#a mexer
class Coletavel:
    def __init__(self):
        self.lista = []
        self.targets = False
        self.name = ''
        self.position = []
        self.barra = pygame.Rect(10, 30, 0, 6)
        self.total = 0

    def exibir(self, nome, posicao):
        self.nome = fonte.render(nome, True, (255,255,255))
        self.position = posicao
        self.targets = True

    def add(self, path, x, y, largura, altura):
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (largura,altura))
        rect = image.get_rect()
        rect.topleft = [x,y]
        self.lista.append([image, rect])

    def draw(self, tela, personagem):
        if self.targets:
            tela.blit(self.nome, (8,8)) 
            pygame.draw.rect(tela,(255,255,255), pygame.Rect(8, 28, 50, 10))
            self.barra.width = personagem.coletou*46/self.total
            pygame.draw.rect(tela,(0,0,255), self.barra)

        for coletavel in self.lista:
            tela.blit(coletavel[0],coletavel[1])

    def colisao(self, personagem):
        for coletavel in self.lista:
            if coletavel[1].colliderect(personagem.rect):
                personagem.coletou += 1
                self.lista.remove(coletavel)
                
    def update(self, tela, personagem):
        self.total = max(self.total, len(self.lista))
        self.draw(tela, personagem)
        self.colisao(personagem)

