import pygame
import math
import personagem
import random
import armas

''' CONTEM MUITAS COPIAS DA CLASSE INIMIGOS, PORÉM A IDEIA PRINCIPAL É SER UMA CLASSE FILHO DE INIMIGOS
    NESSA CLASSE DEVEM TER OS DIVERSOS ATAQUES QUE OS BOSSES TERÃO E SUAS LOGICAS DE MOVIMENTO
    '''
class Boss(personagem.Personagem):
    def __init__(self, path, x, y, largura, altura,vida):
        super().__init__(path, x, y, largura, altura, vida)
        self.multiplicador = 1
        self.velocidade = 3
        self.stamina = 300
        self.movimentar = 500
        self.raios = False
        self.aumentar = [-200,0]
        self.ataque = {
    
        }
        self.ataque_atual = False

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


    def movimento(self, paredes, controlavel=None):
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


        if self.stamina <= 0 :  
            self.tiro(paredes, controlavel)
        if self.stamina > 0:
            self.stamina -= 1


    def update(self,tela, paredes, controlavel = None, v = False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)
    
        

class Snake(Boss):
    def __init__(self, path, x, y, largura, altura,vida, estagio):
        super().__init__(path, x, y, largura, altura, vida)
        self.multiplicador = 1
        self.estagio = estagio
        self.velocidade = 3
        self.stamina = 80
        self.movimentar = 500
        self.raios = False
        self.aumentar = [-200,0]
        self.ataque = {
        
        }
        self.ataque_atual = False
    
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
        self.tiros.add(armas.Bala(self.rect, direcao_x, direcao_y, 7*(4-self.estagio)))
        self.stamina = 80
    
    def update(self,tela, paredes, controlavel = None, v = False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)

    def morte(self, lista, coletavel):
        if self.estagio == 1:
            print('morreu estagio 1')
            lista.add(Snake("fase3/inimigos/python_g", 350, 50, 80,80, 2, 2))
            lista.add(Snake("fase3/inimigos/python_g", 350, 50, 80,80, 2, 2))
        if self.estagio == 2:
            print('morreu estagio 2')
            lista.add(Snake("fase3/inimigos/python_m", 350, 50, 50,50, 1, 3))
            lista.add(Snake("fase3/inimigos/python_m", 350, 50, 50,50, 1, 3))
        if self.estagio == 3:
            print('morreu estagio 3')
        

class Esfinge(Boss):
    def __init__(self, path, x, y, largura, altura,vida):
        super().__init__(path, x, y, largura, altura, vida)
        self.multiplicador = 1
        self.velocidade = 3
        self.stamina = 300
        self.movimentar = 500
        self.raios = False
        self.aumentar = [-200,0]
        self.ataque = {
            1 : self.raioss,
            2 : self.raioss_rodar,
            3 : self.raioss_pulsantes
        }
        self.ataque_atual = False
    
    def movimento(self, paredes, controlavel=None):
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


    def raioss(self,tela):
        if self.raios == False:
            self.raios = []
            for i in range(7):
                self.raios.append([(255,0,0), (114 + 114*i, 8), (114+114*i, 695), 1])
        
        for raio in self.raios:
            pygame.draw.line(tela, raio[0], raio[1], raio[2], raio[3])
            
        if self.aumentar[0] == 100 and self.aumentar[1] < 10:
            for raio in self.raios:
                raio[3] += 2
            self.aumentar[0] = 0
            self.aumentar[1] += 1
        elif self.aumentar[0] == 300 and self.aumentar[1] ==10:
            self.raios = []
            self.aumentar = [-120,0]
        else:
            self.aumentar[0] += 1

    def raioss_rodar(self, tela):
        centro = (400, 300)  # Supondo que o centro da tela esteja em (400, 400)
        r = 700     
        
        # Inicializa os raios em formato circular
        if self.raios == False:
            self.raios = []
            centro = (400, 300)  # Supondo que o centro da tela esteja em (400, 400)
            raio = 700           # Tamanho do raio para os pontos finais

            # Distribui os raios em 7 ângulos uniformemente ao redor do círculo
            for i in range(7):
                angulo = math.radians(i * (360 / 7))  # Ângulos igualmente espaçados
                ponto_final = (
                    centro[0] + raio * math.cos(angulo),  # Calcula a posição X
                    centro[1] + raio * math.sin(angulo)   # Calcula a posição Y
                )
                self.raios.append([(255, 0, 0), centro, ponto_final, 8])

        # Desenha os raios
        for raio in self.raios:
            pygame.draw.line(tela, raio[0], raio[1], raio[2], raio[3])

        # Aumenta a espessura dos raios de forma progressiva
        if self.aumentar[0] == 1 and self.aumentar[1] <720:
            
            c = 0   
            for raio in self.raios:
                angulo = math.radians(c * ((360 / 7)) +2*self.aumentar[1])  # Ângulos igualmente espaçados
                raio[2] = (
                    centro[0] + r * math.cos(angulo),  # Calcula a posição X
                    centro[1] + r * math.sin(angulo)   # Calcula a posição Y
                )
                c +=1
            self.aumentar[0] = 0
            self.aumentar[1] += 1
        elif self.aumentar[0] == 300 and self.aumentar[1] == 720:
            self.raios = []
            self.aumentar = [-120, 0]
        else:
            self.aumentar[0] += 1

    def raioss_pulsantes(self, tela):
        centro = (400, 300)  # Centro da tela (ajuste conforme necessário)
        raio_max = 700  # Distância máxima dos raios
        raio_min = 100  # Distância mínima dos raios

    # Inicializa os raios se ainda não existirem
        if self.raios == False:
            self.raios = []
            self.expansao = True  # Define se os raios estão expandindo
            self.angulo_base = 0  # Ângulo inicial para rotação
            for i in range(7):  # 7 raios, como nos ataques anteriores
                self.raios.append([(255, 0, 0), centro, centro, 8])  # Raios começam no centro

        # Determina o raio atual com base na expansão ou retração
        if not hasattr(self, 'raio_atual'):
            self.raio_atual = raio_min
        if self.expansao:
            self.raio_atual += 5  # Expande
            if self.raio_atual >= raio_max:
                self.expansao = False
        else:
            self.raio_atual -= 5  # Retrai
            if self.raio_atual <= raio_min:
                self.expansao = True

        # Atualiza os raios para o estado atual
        for i, raio in enumerate(self.raios):
            angulo = math.radians(i * (360 / 7) + self.angulo_base)  # Calcula o ângulo com rotação
            ponto_final = (
                centro[0] + self.raio_atual * math.cos(angulo),  # Posição X
                centro[1] + self.raio_atual * math.sin(angulo)   # Posição Y
            )
            raio[2] = ponto_final  # Atualiza a posição final do raio

        # Desenha os raios
        for raio in self.raios:
            pygame.draw.line(tela, raio[0], raio[1], raio[2], raio[3])

        # Incrementa a rotação
        self.angulo_base += 1  # Ajuste a velocidade de rotação se necessário

        # Reinicia após uma sequência completa
        if self.angulo_base >= 360:
            self.angulo_base = 0
    
    def linhas_intersectam(self, p1, p2, p3, p4):
        """
        Verifica se a linha de p1 a p2 intersecta a linha de p3 a p4.
        """
        def orientacao(a, b, c):
            # Calcula a orientação de três pontos (a, b, c)
            return (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])

        o1 = orientacao(p1, p2, p3)
        o2 = orientacao(p1, p2, p4)
        o3 = orientacao(p3, p4, p1)
        o4 = orientacao(p3, p4, p2)

        # Caso geral: os segmentos se cruzam
        if o1 * o2 < 0 and o3 * o4 < 0:
            return True

        return False


    def linha_colide_com_retangulo(self, linha, ret):
        """
        Verifica se uma linha (definida por dois pontos) colide com um retângulo.
        linha: ((x1, y1), (x2, y2)) -> início e fim da linha
        ret: pygame.Rect -> retângulo
        """
        # Definir as bordas do retângulo como segmentos de linha
        bordas = [
            ((ret.left, ret.top), (ret.right, ret.top)),    # Borda superior
            ((ret.right, ret.top), (ret.right, ret.bottom)),  # Borda direita
            ((ret.right, ret.bottom), (ret.left, ret.bottom)),  # Borda inferior
            ((ret.left, ret.bottom), (ret.left, ret.top))   # Borda esquerda
        ]

        # Verifica se a linha intersecta alguma borda
        for borda in bordas:
            if self.linhas_intersectam(linha[0], linha[1], borda[0], borda[1]):
                return True

        return False

    

    def verificar_dano(self, controlavel):
        if not self.raios:
            return

        # Verifica colisão da linha (raio) com o retângulo do personagem
        for raio in self.raios:
            linha = (raio[1], raio[2])  # Ponto inicial e final do raio
            if self.linha_colide_com_retangulo(linha, controlavel.rect):
                controlavel.dano()  # Aplica o dano

    def morte(self, lista, coletavel):
        coletavel.add("../assets/personagens/samyra.png", 375, 275, 50, 50)

    def update(self, tela, paredes, controlavel=None, v=False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)

        # Define o ataque atual aleatoriamente, se não houver nenhum
        if not self.ataque_atual:
            self.ataque_atual = self.ataque[random.randint(1, 3)]

        # Executa o ataque
        self.ataque_atual(tela)


        # Verifica dano causado pelos raios
        self.verificar_dano(controlavel)


class Gato(Boss):
    def __init__(self, path, x, y, largura, altura,vida):
        super().__init__(path, x, y, largura, altura, vida)
        self.multiplicador = 1
        self.velocidade = 3
        self.stamina = 80
        self.movimentar = 500
        self.raios = False
        self.aumentar = [-200,0]
        self.ataque_atual = False
    
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
        self.tiros.add(armas.Git(self.rect, direcao_x, direcao_y, 7))
        self.stamina = 60
    
    def update(self,tela, paredes, controlavel = None, v = False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)

    def morte(self, lista, coletavel):
        coletavel.add("../assets/personagens/samyra.png", 375, 275, 50, 50)
        print('miaaaaaau')
        