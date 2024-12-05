import pygame
import math
import random
import armas


def load_sprites(path):
    frames = {
        'esquerda' : [pygame.image.load(f"../assets/personagens/{path}/esquerda/esquerda_{i}.png") for i in range(1, 4)],
        'direita' : [pygame.image.load(f"../assets/personagens/{path}/direita/direita_{i}.png") for i in range(1, 4)],
        'cima' : [pygame.image.load(f"../assets/personagens/{path}/cima/cima_{i}.png") for i in range(1, 4)],
        'baixo' : [pygame.image.load(f"../assets/personagens/{path}/baixo/baixo_{i}.png") for i in range(1, 4)]
    }
    return frames

class Personagem(pygame.sprite.Sprite):
    def __init__(self, path, x, y, largura, altura, vida):
        super().__init__()
        self.inicial = {"path":path,"x": x,"y": y,"largura": largura,"altura": altura, "vida":vida}
        if isinstance(self, Perso_controle):
            self.frames = load_sprites(path)
            self.frame = self.frames['direita']
            self.image = pygame.transform.scale(pygame.image.load(f"../assets/personagens/{path}.png").convert_alpha(), (largura,altura))
        else:
            self.image = pygame.transform.scale(pygame.image.load(f"../assets/{path}.png").convert_alpha(), (largura,altura))
        self.index = 0
        self.last_update = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vetor = (1,0)
        self.vida = vida
        self.tiros = armas.Balas()
    
    def draw(self, tela):
        tela.blit(self.image, self.rect)
    
    #verifica colisao com os inimigos
    def colisao_perso(self, personagens):
        if personagens == None:
            return
        for personagem in personagens.inimigos:
            if self.rect.colliderect(personagem.rect):
                return True
        return False

    #verifica colisao com paredes
    def colisao(self, paredes):
        for parede in paredes:
            if self.rect.colliderect(parede):
                return parede
        return None

    #define o movimento verificando possiveis colisoes com impecam o movimento
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

    #verifica a direcao em que o personagem se movimentou

    def direcao(self, delta_x, delta_y):
        d = ''
        if delta_x < 0:
            d = 'esquerda'
        elif delta_x > 0:
            d = 'direita'
        if delta_y < 0:
            d = 'cima'
        elif delta_y > 0:
            d = 'baixo'

        if d == '':
            return
        self.frame = self.frames[d]
        now = pygame.time.get_ticks()
        if now - self.last_update >200:  
            self.last_update = now
            self.index = (self.index + 1) % len(self.frame)  
            self.image = pygame.transform.scale(self.frame[self.index], (50,50)) 
    

    #Verifica a direção do mouse em relacao ao personagem
    def direcao_mouse(self, mouse_x, mouse_y):

        delta_x = mouse_x - self.rect.center[0]
        delta_y = mouse_y - self.rect.center[1]

        magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
        
        if magnitude != 0:
            vetor = [delta_x / magnitude, delta_y / magnitude]
        else:
            vetor = [0, 0]

        self.vetor = vetor
        return vetor

    def rotacionar_vetor(self, vetor, angulo):
        angulo_rad = math.radians(angulo)
        cos_ang = math.cos(angulo_rad)
        sin_ang = math.sin(angulo_rad)

        x_rot = vetor[0] * cos_ang - vetor[1] * sin_ang
        y_rot = vetor[0] * sin_ang + vetor[1] * cos_ang

        return x_rot, y_rot

    
    def update(self,tela, paredes):
        self.movimento(paredes)
        self.draw(tela)

class Perso_controle(Personagem):
    def __init__(self,path, x, y, largura, altura, vida):
        super().__init__(path, x, y, largura, altura, vida)
        self.stamina = 40
        self.imortal = 0
        self.coletou = 0
    
    #Coleta os controles do usuario
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
        if teclas[pygame.K_SPACE]  and self.stamina == 0:
            self.tiro()
        if pygame.mouse.get_pressed()[0] and self.stamina == 0:  # Botão esquerdo
            self.tiro()

        self.movimento(delta_x, delta_y, paredes)

    #caso o player tenha atirado, adiciona o tiro 
    def tiro(self):
        x, y = self.vetor
        #para testes
        x,y = pygame.mouse.get_pos()
        x,y = self.direcao_mouse(x,y)
        if self.inicial["path"] == "samyra":
            self.tiros.add(armas.Espada(self.rect, x, y, 60))
            self.stamina = 20
        elif self.inicial["path"] == "gabriel":
            self.tiros.add(armas.Pistola(self.rect, x, y, 6))
            self.stamina = 40
        else:
            x_d,y_d = self.rotacionar_vetor([x,y], 3)
            x_a,y_a = self.rotacionar_vetor([x,y], -3)
            self.tiros.add(armas.Espingarda(self.rect, x_a, y_a, 8))
            self.tiros.add(armas.Espingarda(self.rect, x_d, y_d, 8))
            self.stamina = 50
    
    def dano(self):
        if self.imortal == 50:
            self.vida -= 1
            self.imortal = 0
        if self.imortal < 50:
            self.imortal += 1
        
    def update(self,tela, paredes, inimigos):
        self.controle(paredes)
        if self.stamina > 0:
            self.stamina -= 1
        self.tiros.update(tela, paredes, inimigos)
        self.draw(tela)
        if self.colisao_perso(inimigos):
            self.dano()
        #print('vida:', self.vida, 'coletou:', self.coletou)
        
    
#armazena uma lista de inimigos
class Inimigos:
    def __init__(self):
        self.inimigos = []

    def add(self, inimigo):
        self.inimigos.append(inimigo)

    def clean(self):
        self.inimigos = []

    def update(self,tela, paredes, controlavel = None, v = False):
        to_remove = []
        for inimigo in self.inimigos:
            if inimigo.vida == 0:
                to_remove.append(inimigo)
            inimigo.update(tela, paredes, controlavel, v)
        for inimigo in to_remove:    
            self.inimigos.remove(inimigo)
        return to_remove

class Inimigo(Personagem):
    def __init__(self, path, x, y, largura, altura,vida,  sentido):
        super().__init__(path, x, y, largura, altura, vida)
        self.inicial = {"path":path,"x": x,"y": y,"largura": largura,"altura": altura, "vida":vida, "sentido":sentido}
        self.multiplicador = 1
        self.sentido = sentido
        self.velocidade = 3
        self.stamina = 40
        self.timer_aleatorio = 0

    
    #verifica a diferença entre o inimigo em relacao ao player
    """CHANCES DE SER REMOVIDA CASO NAO NECESSARIO"""
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

    #cria um linha entre o inimigo e o persongem
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

    #caso a linha criada acima passe por algum objeto, o inimigo nao viu o persongame, logo nao atira
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

    #cria um tiro para os inimigos
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
        self.tiros.add(armas.Bala(self.rect, direcao_x, direcao_y, 7))
        self.stamina = 80


    #dentre os varios tipos de movimentos, ele realiza de acordo com o parametro
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

        if self.sentido == 'atirador':
            if self.stamina <= 0 :  
                self.tiro(paredes, controlavel)
            if self.stamina > 0:
                self.stamina -= 1

        if self.sentido == 'caminhante' or self.sentido == 'atirador':
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
            if colisao_horizontal or self.rect.x < 0 or self.rect.x > 780:
                # Reverte o movimento horizontal em caso de colisão
                self.rect.x -= delta_x
                self.direcao_aleatoria[0] = random.choice([-1, 0, 1])  # Gera nova direção horizontal

            self.rect.y += delta_y
            colisao_vertical = self.colisao(paredes)
            if colisao_vertical or self.rect.y < 0 or self.rect.y > 580:
                # Reverte o movimento vertical em caso de colisão
                self.rect.y -= delta_y
                self.direcao_aleatoria[1] = random.choice([-1, 0, 1])  # Gera nova direção vertical

    

    def update(self,tela, paredes, controlavel = None, v = False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)