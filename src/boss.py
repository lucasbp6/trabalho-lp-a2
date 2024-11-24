import pygame
import math
import personagem_novo as personagem
import random

class Boss(personagem.Personagem):
    def __init__(self, path, x, y, largura, altura,vida,  sentido):
        super().__init__(path, x, y, largura, altura, vida)
        self.multiplicador = 1
        self.sentido = sentido
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

    def tiro(self, controlavel):
        x1 = controlavel.rect.center[0] - self.rect.center[0]
        y1 = controlavel.rect.center[1] - self.rect.center[1]

       
        distancia = math.sqrt(x1**2 + y1**2)
        if distancia != 0: 
            direcao_x = x1 / distancia
            direcao_y = y1 / distancia
        else:
            direcao_x, direcao_y = 0, 0  

        self.tiros.add(personagem.Bala(self.rect, direcao_x, direcao_y, 15))
        self.stamina = 100


            


    def movimento(self, paredes, controlavel=None):

        if self.movimentar < 100 and self.movimentar > 0:    
            multi_x, multi_y = self.delta(controlavel)
            delta_x = self.velocidade*multi_x
            delta_y = self.velocidade*multi_y 

        elif self.movimentar > 50:
            # Inicializa as variáveis de direção e timer se ainda não existirem
            if not hasattr(self, 'direcao_atual'):
                self.direcao_atual = [0, 0]  # Direção inicial do boss
            if not hasattr(self, 'timer_troca'):
                self.timer_troca = 0  # Tempo restante para troca de direção
            if not hasattr(self, 'direcao_alvo'):
                self.direcao_alvo = [0, 0]  # Próxima direção do boss

            # Reduz o timer a cada chamada
            self.timer_troca -= 1
            if self.timer_troca <= 0:
                # Gera uma nova direção alvo aleatória
                self.direcao_alvo = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                self.timer_troca = random.randint(30, 60)  # Troca de direção a cada 0.5 a 1 segundo (30-60 frames)

            # Suaviza a transição entre a direção atual e a direção alvo
                self.direcao_atual[0] += (self.direcao_alvo[0] - self.direcao_atual[0]) * 0.1
            self.direcao_atual[1] += (self.direcao_alvo[1] - self.direcao_atual[1]) * 0.1

            # Calcula o movimento baseado na direção atual
            delta_x = self.direcao_atual[0] * 5
            delta_y = self.direcao_atual[1] * 5
        else:
            self.movimentar = 500
            delta_x, delta_y = 0,0
        # Aplica movimento horizontal
        self.rect.x += delta_x
        colisao_horizontal = self.colisao(paredes)
        if colisao_horizontal:
            if delta_x > 0:  
                self.rect.right = colisao_horizontal.left
            elif delta_x < 0: 
                self.rect.left = colisao_horizontal.right

        # Aplica movimento vertical
        self.rect.y += delta_y
        colisao_vertical = self.colisao(paredes)
        if colisao_vertical:
            if delta_y > 0:  
                self.rect.bottom = colisao_vertical.top
            elif delta_y < 0:  
                self.rect.top = colisao_vertical.bottom    

        # Realiza ação de tiro quando a stamina acaba
        if (self.sentido == 'boss2' or self.sentido == 'boss3') and self.stamina <= 0:
            self.tiro(controlavel)
        if self.stamina > 0:
            self.stamina -= 1

        self.movimentar -= 1
        print(self.movimentar)
        # Atualiza a direção visual do boss
        self.direcao(delta_x, delta_y)


    def raioss(self,tela):
        if self.raios == False:
            self.raios = []
            print('daks')
            for i in range(7):
                self.raios.append([(255,0,0), (114 + 114*i, 5), (114+114*i, 695), 1])
        
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

        print(self.aumentar)


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
                self.raios.append([(255, 0, 0), centro, ponto_final, 5])

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

        print(self.aumentar)

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
                self.raios.append([(255, 0, 255), centro, centro, 5])  # Raios começam no centro

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

        print(f"Raio Atual: {self.raio_atual}, Expansão: {self.expansao}, Ângulo Base: {self.angulo_base}")


    def update(self,tela, paredes, controlavel = None, v = False):
        self.tiros.update(tela, paredes, controlavel, v)
        self.movimento(paredes, controlavel)
        self.draw(tela)
        '''if self.ataque_atual == False:
            self.ataque_atual = self.ataque[random.randint(1,3)]
        self.ataque_atual(tela)'''
        