import pygame 

class PersonagemTeste:
    def __init__(self, x, y, path):
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        #self.rect = pygame.Rect(x, y, 64, 64)

    def update(self, tela):
        # Desenha a imagem do personagem na tela
        tela.blit(self.image, self.rect)

    def movimento(self, botao):

        if botao[pygame.K_d] and self.rect.x < 770:
            self.rect.x += 5
        if botao[pygame.K_a]:
            self.rect.x -= 5
        if botao[pygame.K_w]:
            self.rect.y -= 5
        if botao[pygame.K_s]:
            self.rect.y += 5
        

    def colisao(self, parede, botao):
        # Guardar a posição original antes de mover
        posicao_original = self.rect.topleft
        print(posicao_original)

        # Mover o objeto
        self.movimento(botao)
        
        # Atualizar a posição do retângulo depois de mover
        novo_pos = self.rect.topleft
        
        if self.rect.colliderect(parede):
            print('contato')
            # Reverter para a posição original em caso de colisão
            self.rect.topleft = posicao_original
        else:
            print(f"Nova posição: {novo_pos}")

    

class Inimigo:
    def __init__(self):
        self.rect = pygame.Rect(300, 300, 64, 64)

    def update(self,tela):
        pygame.draw.rect(tela, (255,255,255), self.rect)

    def colisao(self, tiros):
        for tiro in tiros:
            # Encontra o ponto mais próximo do círculo no retângulo
            closest_x = max(rect.left, min(circle_x, rect.right))
            closest_y = max(rect.top, min(circle_y, rect.bottom))
            
            # Calcula a distância entre o ponto mais próximo e o centro do círculo
            distance_x = circle_x - closest_x
            distance_y = circle_y - closest_y
            distance = math.sqrt(distance_x**2 + distance_y**2)
            
            # Verifica se a distância é menor ou igual ao raio do círculo
            return distance <= radius