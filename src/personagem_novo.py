import pygame
import math
import random


class Balas:
    def __init__(self):
        self.balas = []

    # Verifica a colisao entre cada um dos objetos com o tiro
    def colisao(self, paredes, bala, inimigos, v = False):
        rect = pygame.Rect(bala.pos[0]-bala.raio, bala.pos[1]-bala.raio, 2*bala.raio, 2*bala.raio)
        for parede in paredes:
            if parede.colliderect(rect):
                return True
        if v == True:        
            for inimigo in inimigos.inimigos:
                if inimigo.rect.colliderect(rect):
                    inimigo.vida -= 1
                    return True
        else:
            if inimigos.rect.colliderect(rect):
                    inimigos.vida -= 1
                    return True
        return False

    def add(self, bala):
        self.balas.append(bala)
    
    def draw(self, tela):
        for bala in self.balas:
            pygame.draw.circle(tela, (255, 255, 255), bala.pos, bala.raio)


    def update(self, tela, paredes, inimigos, v = False):
        balas_remove = []
        for bala in self.balas:
            if v == False:
                bala_colisao = self.colisao(paredes, bala, inimigos, True)
                if bala_colisao != None or bala.update() == 0:
                    balas_remove.append(bala)
            else: 
                bala_colisao = self.colisao(paredes, bala, inimigos)
                if bala_colisao or bala.update() == 0:
                    balas_remove.append(bala)
        if len(balas_remove) != 0:
            for bala in balas_remove:
                self.balas.remove(bala)
        self.draw(tela)

class Bala:
    def __init__(self, rect_per, d_x, d_y, raio):
        self.contador = 120
        self.raio = raio
        self.per = rect_per
        self.pos = [rect_per.center[0], rect_per.center[1]]
        self.sentido = (d_x, d_y)
        self.p_inicial()
        
    def p_inicial(self):
        if self.sentido[0] == 1:
            self.pos[0] = self.per.right
        elif self.sentido[0] == -1:
            self.pos[0] = self.per.left
        
        if self.sentido[1] == 1:
            self.pos[1] == self.per.bottom
        elif self.sentido[1] == -1:
            self.pos[1] == self.per.top
        

    
    def update(self):
        self.contador -= 1
        self.pos = (self.pos[0] + self.sentido[0]*10, self.pos[1]+ self.sentido[1]*10)

        return self.contador
    

class Coletavel:
    def __init__(self):
        self.lista = []

    def add(self, path, x, y, largura, altura):
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (largura,altura))
        rect = image.get_rect()
        rect.topleft = [x,y]
        self.lista.append([image, rect])

    def draw(self, tela):
        for coletavel in self.lista:
            tela.blit(coletavel[0],coletavel[1])

    def colisao(self, personagem):
        for coletavel in self.lista:
            if coletavel[1].colliderect(personagem.rect):
                personagem.coletou += 1
                self.lista.remove(coletavel)
    def update(self, tela, personagem):
        self.draw(tela)
        self.colisao(personagem)



class Personagem(pygame.sprite.Sprite):
    def __init__(self, path, x, y, largura, altura, vida):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (largura,altura))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vetor = (1,0)
        self.vida = vida
        self.tiros = Balas()

    def draw(self, tela):
        tela.blit(self.image, self.rect)
    
    def colisao_perso(self, personagens):
        if personagens == None:
            return
        for personagem in personagens.inimigos:
            if self.rect.colliderect(personagem.rect):
                return True
        return False

    def colisao(self, paredes):
        for parede in paredes:
            if self.rect.colliderect(parede):
                return parede
        return None

    def movimento(self, delta_x, delta_y, paredes):
        
        self.rect.x += delta_x
        colisao_horizontal = self.colisao(paredes)
        if colisao_horizontal:
            if delta_x > 0:  
                self.rect.right = colisao_horizontal.left
            elif delta_x < 0: 
                self.rect.left = colisao_horizontal.right

        self.rect.y += delta_y
        colisao_vertical = self.colisao(paredes)
        if colisao_vertical:
            if delta_y > 0:  
                self.rect.bottom = colisao_vertical.top
            elif delta_y < 0:  
                self.rect.top = colisao_vertical.bottom
        self.direcao(delta_x, delta_y)

    def direcao(self, delta_x, delta_y):
        vetor = [0, 0]
        if delta_x < 0:
            vetor[0] = -1
        elif delta_x > 0:
            vetor[0] = 1
        if delta_y < 0:
            vetor[1] = -1
        elif delta_y > 0:
            vetor[1] = 1
        
        if not (vetor[0] == 0 and vetor[1] == 0):
            self.vetor = vetor

        return vetor
    #teste
    import math

    def direcao_mouse(self, mouse_x, mouse_y):
    # Calcula o vetor do centro até o clique do mouse
        delta_x = mouse_x - self.rect.center[0]
        delta_y = mouse_y - self.rect.center[1]
        
        # Calcula o ângulo em relação ao eixo X (convertido para graus)
        angulo = math.degrees(math.atan2(-delta_y, delta_x))  # Invertendo delta_y porque o eixo Y cresce para baixo no Pygame
        if angulo < 0:
            angulo += 360  # Ajusta ângulo para ser sempre positivo (0 a 360)

        # Define os setores (cada 45° é um setor)
        if 0 <= angulo < 22.5 or 315 <= angulo < 376.5:
            vetor = [1, 0]  # Direita
        elif 22.5 <= angulo < 67.5:
            vetor = [1, -1]  # Cima-direita
        elif 67.5 <= angulo < 112.5:
            vetor = [0, -1]  # Cima
        elif 112.5 <= angulo < 157.5:
            vetor = [-1, -1]  # Cima-esquerda
        elif 157.5 <= angulo < 202.5:
            vetor = [-1, 0]  # Esquerda
        elif 202.5 <= angulo < 247.5:
            vetor = [-1, 1]  # Baixo-esquerda
        elif 247.5 <= angulo < 292.5:
            vetor = [0, 1]  # Baixo
        else:
            vetor = [1, 1]  # Baixo-direita
        
        # Atualiza o vetor da classe
        self.vetor = vetor
        return vetor

    
    def update(self,tela, paredes):
        self.movimento(paredes)
        self.draw(tela)

class Perso_controle(Personagem):
    def __init__(self,path, x, y, largura, altura, vida):
        super().__init__(path, x, y, largura, altura, vida)
        self.stamina = 40
        self.imortal = 0
        self.coletou = 0
        
    def controle(self, paredes):
        teclas = pygame.key.get_pressed()
        delta_x, delta_y = 0, 0

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            delta_x += 5
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            delta_x -= 5
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            delta_y -= 5
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            delta_y += 5
        if teclas[pygame.K_SPACE]  and self.stamina <= 0:
            self.tiro()
        self.movimento(delta_x, delta_y, paredes)

    def tiro(self):
        x, y = self.vetor
        #para testes
        x,y = pygame.mouse.get_pos()
        x,y = self.direcao_mouse(x,y)
        self.tiros.add(Bala(self.rect, x, y, 7))
        self.stamina = 40
  
        
    def update(self,tela, paredes, inimigos):
        self.controle(paredes)
        self.draw(tela)
        if self.stamina > 0:
            self.stamina -= 1
        self.tiros.update(tela, paredes, inimigos)
        if self.colisao_perso(inimigos) and self.imortal == 60:
            self.vida -= 1
            self.imortal = 0
        if self.imortal < 60:
            self.imortal += 1
        if self.vida == 0:
            return 'a'
        #print('vida:', self.vida, 'coletou:', self.coletou)
        
    
class Inimigos:
    def __init__(self):
        self.inimigos = []

    def add(self, inimigo):
        self.inimigos.append(inimigo)
    def clean(self):
        print(len(self.inimigos))
        print("apagou")
        self.inimigos = []
        print(len(self.inimigos))

    def update(self,tela, paredes, controlavel = None, v = False):
        to_remove = []
        
        b = False
        for inimigo in self.inimigos:
            if inimigo.vida == 0:
                to_remove.append(inimigo)
            inimigo.update(tela, paredes, controlavel, v)
        for inimigo in to_remove:    
            self.inimigos.remove(inimigo)
            if inimigo.sentido == 'boss2':
                b = True
        return b

class Inimigo(Personagem):
    def __init__(self, path, x, y, largura, altura,vida,  sentido):
        super().__init__(path, x, y, largura, altura, vida)
        self.multiplicador = 1
        self.sentido = sentido
        self.velocidade = 3
        self.stamina = 40
        self.timer_aleatorio = 0

    def delta(self, controlavel):
        deltax = self.rect.x - controlavel.rect.x
        deltay = self.rect.y - controlavel.rect.y
        if deltax > 0:
            x = -1
        else:
            x = 1

        if deltay > 0:
            y = -1
        else:
            y = 1
        if deltax < self.velocidade and deltax > -self.velocidade:
            x = 0
        if deltay < self.velocidade and deltay > -self.velocidade:
            y = 0
        return x,y 


    def linha_colide_com_paredes(self, paredes, controlavel):

        linha_inicio = self.rect.center
        linha_fim = controlavel.rect.center

        for parede in paredes:
            arestas = [
                (parede.topleft, parede.topright),  # cima
                (parede.topright, parede.bottomright),  # direita
                (parede.bottomright, parede.bottomleft),  # baixo
                (parede.bottomleft, parede.topleft),  # esquerda
            ]

            for aresta in arestas:
                if self.linha_intersecta(linha_inicio, linha_fim, aresta[0], aresta[1]):
                    return True

        return False  

    def linha_intersecta(self, p1, p2, q1, q2):

        def orientacao(a, b, c):
            val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
            return 0 if val == 0 else (1 if val > 0 else -1)

        def no_segmento(a, b, c):
            return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])

        o1 = orientacao(p1, p2, q1)
        o2 = orientacao(p1, p2, q2)
        o3 = orientacao(q1, q2, p1)
        o4 = orientacao(q1, q2, p2)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and no_segmento(p1, p2, q1): return True
        if o2 == 0 and no_segmento(p1, p2, q2): return True
        if o3 == 0 and no_segmento(q1, q2, p1): return True
        if o4 == 0 and no_segmento(q1, q2, p2): return True

        return False


    def tiro(self, paredes, controlavel):
  
        if self.linha_colide_com_paredes(paredes, controlavel):
            return
        # Calcula a direção do tiro
        x1 = controlavel.rect.center[0] - self.rect.center[0]
        y1 = controlavel.rect.center[1] - self.rect.center[1]

        distancia = math.sqrt(x1**2 + y1**2)
        if distancia != 0: 
            direcao_x = x1 / distancia
            direcao_y = y1 / distancia
        else:
            direcao_x, direcao_y = 0, 0  

        # Adiciona a bala
        self.tiros.add(Bala(self.rect, direcao_x, direcao_y, 7))
        self.stamina = 40



    def movimento(self, paredes, controlavel = None):

        delta_x, delta_y = 0,0
        if self.sentido == 'x':
            delta_x = self.velocidade*self.multiplicador
            delta_y = 0
            self.rect.x += delta_x
            colisao_horizontal = self.colisao(paredes)
            if colisao_horizontal:
                if delta_x > 0:  
                    self.rect.right = colisao_horizontal.left
                    self.multiplicador = -1
                elif delta_x < 0: 
                    self.rect.left = colisao_horizontal.right
                    self.multiplicador = 1
        if self.sentido == 'y':
            delta_y = self.velocidade*self.multiplicador
            delta_x = 0
            self.rect.y += delta_y
            colisao_horizontal = self.colisao(paredes)
            if colisao_horizontal:
                if delta_y > 0:  
                    self.rect.bottom = colisao_horizontal.top
                    self.multiplicador = -1
                elif delta_y < 0: 
                    self.rect.top = colisao_horizontal.bottom
                    self.multiplicador = 1

    
        if self.sentido == 'seguir':
            multi_x, multi_y = self.delta(controlavel)
            delta_x = self.velocidade*multi_x
            delta_y = self.velocidade*multi_y
            self.rect.x += delta_x
            colisao_horizontal = self.colisao(paredes)
            if colisao_horizontal:
                if delta_x > 0:  
                    self.rect.right = colisao_horizontal.left
                elif delta_x < 0: 
                    self.rect.left = colisao_horizontal.right
            self.rect.y += delta_y
            colisao_vertical = self.colisao(paredes)
            if colisao_vertical:
                if delta_y > 0:  
                    self.rect.bottom = colisao_vertical.top
                elif delta_y < 0:  
                    self.rect.top = colisao_vertical.bottom  

        if self.sentido == 'aleatorio':
            if not hasattr(self, 'direcao_aleatoria') or self.direcao_aleatoria is None:
                # Inicializa uma direção aleatória
                self.direcao_aleatoria = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
                self.timer_aleatorio = 0

            # Atualiza a cada 30 ticks (ajustável)
            self.timer_aleatorio += 1
            if self.timer_aleatorio >= 30:
                self.direcao_aleatoria = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
                self.timer_aleatorio = 0

            delta_x = self.velocidade * self.direcao_aleatoria[0]
            delta_y = self.velocidade * self.direcao_aleatoria[1]

            # Movimenta na direção aleatória
            self.rect.x += delta_x
            colisao_horizontal = self.colisao(paredes)
            if colisao_horizontal:
                # Reverte o movimento horizontal em caso de colisão
                self.rect.x -= delta_x
                self.direcao_aleatoria[0] = random.choice([-1, 0, 1])  # Gera nova direção horizontal

            self.rect.y += delta_y
            colisao_vertical = self.colisao(paredes)
            if colisao_vertical:
                # Reverte o movimento vertical em caso de colisão
                self.rect.y -= delta_y
                self.direcao_aleatoria[1] = random.choice([-1, 0, 1])  # Gera nova direção vertical

            if self.stamina <= 0 :  
                self.tiro(paredes, controlavel)
            if self.stamina > 0:
                self.stamina -= 1
      

        if self.sentido == 'atirador' and self.stamina <= 0:
            self.tiro(paredes, controlavel)
        if self.stamina > 0:
            self.stamina -= 1



        self.direcao(delta_x, delta_y)

    def update(self,tela, paredes, controlavel = None, v = False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)