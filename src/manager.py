import pygame
import mapa
import personagem
import os
import boss
import interagiveis
import ui_menu

fonte = pygame.font.SysFont('arial', 25, False, False)
coracao = pygame.transform.scale(pygame.image.load("../assets/principal/vida_personagem.png"), (20,20))



# Gerencia as fases e concatena todos os modulos do jogo
class Manager:
    def __init__ (self, game):
        self.game = game
        self.tela = game.tela
        # Organizar os enderecos corretos
        self.fases = {
            "fase1": os.path.join("..", "config", "fase1.json"),
            "fase2": os.path.join("..", "config", "fase2.json"),
            "fase3": os.path.join("..", "config", "fase3.json"),
            "fase4": os.path.join("..", "config", "fase4.json"),
            "fase5": os.path.join("..","config", "fase5.json")
        }

        # Seletor padrao = fase1
        self.fase = self.game.fase
        self.seletor = self.fases[f"fase{self.fase}"]
        self.troca = True
        self.quadro = 'hub'
        self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", f"fase{self.fase}", "mapa", f"{self.quadro}.png"))
        self.load = False
        self.personagem = personagem.Perso_controle(game.path, 25,25,50,50,5) # posicoes rever
        self.inimigos = personagem.Inimigos()
        self.mapa = mapa.Mapa()
        self.coletaveis = interagiveis.Coletavel()
        self.time_inicial = pygame.time.get_ticks()
        self.objetivos = False
        


    #carrega os parametros
    def load_mapa(self):

        #carrega todo json
        if  self.troca:
            self.seletor = self.fases[f"fase{self.fase}"]
            self.mapa.load(self.seletor)
            self.troca = False
            self.quadro = 'hub'
            self.personagem.rect.topleft = self.mapa.posicao
            self.objetivos = False
            self.personagem.coletou = 0
            self.time_inicial = pygame.time.get_ticks()

        #self.inimigos.add(boss.Boss("../assets/samyra.png",350, 50, 100,100, 1, 'boss1', ))
        #self.inimigos.add(personagem.Inimigo("../assets/samyra.png", 350, 50, 50, 50, 3, "aleatorio"))
        
        # ativa o quadro atual
        self.mapa.ativar(self.quadro)
  
        

        #carrega os inimigos
        self.inimigos.clean()
        for inimigo in self.mapa.npc:
            self.inimigos.add(inimigo)  

        self.load = True
        if self.fase == 3  and self.quadro == 'fim':
            self.inimigos.add(boss.Snake("samyra", 350, 50, 100,100, 1, 1))
        if self.fase == 4:
            self.inimigos.add(boss.Esfinge("samyra", 350, 50, 100,100, 1))
        if self.fase == 5:
            self.inimigos.add(boss.Gato("samyra", 350, 50, 100,100, 1))

        self.coletaveis = interagiveis.Coletavel()
        for coletaveis in self.mapa.coletaveis:
            self.coletaveis.add(coletaveis[0], coletaveis[1], coletaveis[2], 50, 50)
        self.coletaveis.exibir("objetivos", (8,80), self.mapa.objetivo)
        
            
    def fim_fase(self):
        clock = pygame.time.Clock()
        fonte2 = pygame.font.SysFont('arial', 50, False, False)
        tempo = self.tempo(True)
        objetos = [ui_menu.Text("Proxima fase", fonte2,400,  450, (255,255,255), self.game, (0,0,150)),
                   ui_menu.Text("Voltar ao menu", fonte2,400,  500, (255,255,255), self.game, (0,0,150)),
                   ui_menu.Text("Parabens", fonte2,400,  100, (255,255,255), self.game),
                   ui_menu.Text(f"Tempo : {tempo}", fonte2,400,  200, (255,255,255), self.game),
                   ui_menu.Text(f"Fase {self.fase} concluida", fonte2,400,  300, (255,255,255), self.game)]
        rodando = True
        if self.game.stats[f"fase{self.fase}"] == 0:
            self.game.stats[f"fase{self.fase}"] = tempo
        while rodando:
            clock.tick(60)
            click_pos = None
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos

            pos = pygame.mouse.get_pos()
            self.tela.fill((0,0,0))
            

            for objeto in objetos:
                a = objeto.update(pos, click_pos)
                if a == "Proxima fase":
                    self.troca = True
                    self.fase += 1
                    self.quadro = 'hub'
                    return True
                if a == "Voltar ao menu":
                    self.game.seletor("menu")
                    return False
            pygame.display.flip()

    def morte(self):
        clock = pygame.time.Clock()
        fonte2 = pygame.font.SysFont('arial', 50, False, False)
        tempo = self.tempo(True)
        objetos = [ui_menu.Text("Reiniciar fase", fonte2,400,  450, (255,255,255), self.game, (0,0,150)),
                   ui_menu.Text("Voltar ao menu", fonte2,400,  500, (255,255,255), self.game, (0,0,150)),
                   ui_menu.Text("ihishaihihi", fonte2,400,  100, (255,255,255), self.game),
                   ui_menu.Text(f"Voce não foi pareo", fonte2,400,  200, (255,255,255), self.game),
                   ui_menu.Text(f"Fase {self.fase} falha", fonte2,400,  300, (255,255,255), self.game)]
        rodando = True
        if self.game.stats[f"fase{self.fase}"] == 0:
            self.game.stats[f"fase{self.fase}"] = tempo
        while rodando:
            clock.tick(60)
            click_pos = None
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos

            pos = pygame.mouse.get_pos()
            self.tela.fill((0,0,0))
            

            for objeto in objetos:
                a = objeto.update(pos, click_pos)
                if a == "Reiniciar fase":
                    self.troca = True
                    self.personagem.vida = 5
                    self.personagem.stamina = 40
                    self.quadro = 'hub'
                    return True
                if a == "Voltar ao menu":
                    self.game.seletor("menu")
                    return False
            pygame.display.flip()


    def vitoria(self):
        clock = pygame.time.Clock()
        fonte2 = pygame.font.SysFont('arial', 50, False, False)
        tempo = self.tempo(True)
        objetos = [ui_menu.Text("Voltar ao menu", fonte2,400,  500, (255,255,255), self.game, (0,0,150)),
                   ui_menu.Text("Parabéns, voce finalizou o jogo", fonte2,400,  50, (255,255,255), self.game),
                   ui_menu.Text(f"bora de speedrun??", fonte2,400,  125, (255,255,255), self.game)]
        rodando = True
        if self.game.stats[f"fase{self.fase}"] == 0:
            self.game.stats[f"fase{self.fase}"] = tempo
        i = 0
        for key, value in self.game.stats.items():
            objetos.append(ui_menu.Text(f"{key}    {value}", fonte2,400,  200 + 50*i, (255,255,255), self.game))
            i += 1
        while rodando:
            clock.tick(60)
            click_pos = None
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos

            pos = pygame.mouse.get_pos()
            self.tela.fill((0,0,0))
            

            for objeto in objetos:
                a = objeto.update(pos, click_pos)
                if a == "Voltar ao menu":
                    self.game.seletor("menu")
                    return False
            pygame.display.flip()
    #verifica qual o proximo quadro
    def portas(self):
        x, y = self.personagem.rect.center
        lim = '0'

        if y < -20:
            lim = '1'
        if x > 810:
            lim = '2'
        if y > 620:
            lim = '3'
        if x < -20:
            lim = '4'

        if lim != '0':
            #define o validador para poder carregar o novo quadro
            self.load = False
            self.quadro = self.mapa.portas[lim][0]
            
            if self.quadro == "end":
                if self.fim_fase():
                    self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", f"fase{self.fase}", "mapa", f"{self.quadro}.png"))
                return

            self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", f"fase{self.fase}", "mapa", f"{self.quadro}.png"))
            #altera as posicoes de acordo com o json
            # uma posicao = -1 indica mante-la
            x, y = self.mapa.portas[lim][1]
            if x == -1:
                pass
            else:
                self.personagem.rect.x = x
            if y == -1:
                pass
            else:
                self.personagem.rect.y = y

    def tempo(self, retorno = False):
        self.tempo_decorrido = (pygame.time.get_ticks() - self.time_inicial)
        minutos = self.tempo_decorrido // 60000  
        segundos = (self.tempo_decorrido % 60000) // 1000  
        milissegundos = self.tempo_decorrido % 1000  //100

        if retorno:
            return f"{minutos:02}:{segundos:02}.{milissegundos}"

        render = fonte.render(f"Tempo: {minutos:02}:{segundos:02}.{milissegundos}", True, (0,0,0))
        fundin = render.get_rect()
        fundin.topleft = (330,10)
        pygame.draw.rect(self.tela, (255,255,255), fundin)
        self.tela.blit(render, (330, 10))

        
                
    #roda o jogo chamando os updates
    def run(self):
        if not self.load:
            self.load_mapa()
        self.tela.blit(self.fundo, (0,0))
        mortes = self.inimigos.update(self.tela, self.mapa.paredes, self.personagem, True)
        for inimigo in mortes:
            if isinstance(inimigo, personagem.Inimigo):
                self.mapa.dados[self.quadro]["inimigos"].remove(inimigo.inicial)
            if isinstance(inimigo, boss.Boss):
                inimigo.morte(self.inimigos, self.coletaveis)

        
        """TESTES DE EXIBICAO DE VIDA E PROGRESSO"""
        for i in range(self.personagem.vida):
            self.tela.blit(coracao, (770 - 22*i, 10))

        """Muito especifico para a fase 2"""
        if self.fase == 2 and self.quadro == 'hub' and self.objetivos:
            portal = pygame.Rect(360, 260, 80, 80)
            pygame.draw.rect(self.tela, (0,0,255), portal)
            if portal.colliderect(self.personagem.rect):
                if self.fim_fase():
                    self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", f"fase{self.fase}", "mapa", f"{self.quadro}.png"))
                    self.load = False
                return
            
        """Muito especifico para a fase 4"""
        if self.fase == 4 and self.quadro == 'hub' and self.objetivos:
            portal = pygame.Rect(360, 260, 80, 80)
            pygame.draw.rect(self.tela, (0,0,255), portal)
            if portal.colliderect(self.personagem.rect):
                if self.fim_fase():
                    self.fundo = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets", f"fase{self.fase}", "mapa", f"{self.quadro}.png"))
                    self.load = False
                return
            
        """Muito especifico para a fase 5"""
        if self.fase == 5 and self.quadro == 'hub' and self.objetivos:
            portal = pygame.Rect(360, 260, 80, 80)
            pygame.draw.rect(self.tela, (0,0,255), portal)
            if portal.colliderect(self.personagem.rect):
                self.vitoria()
                return
            

        """ Muito especifico para a fase 3"""
        if self.fase == 3 and self.quadro == "parte5" and not self.objetivos:
            bloqueio = pygame.Rect(550, 0,  20,  200)
            pygame.draw.rect(self.tela, (255,0,0), bloqueio)
            self.mapa.paredes.append(bloqueio)
            self.personagem.update(self.tela, self.mapa.paredes, self.inimigos)
            self.mapa.paredes.remove(bloqueio)

        elif self.quadro == "fim":
            bloqueio = pygame.Rect(0, 0,  20,  600)
            pygame.draw.rect(self.tela, (255,0,0), bloqueio)
            self.mapa.paredes.append(bloqueio)
            self.personagem.update(self.tela, self.mapa.paredes, self.inimigos)
            self.mapa.paredes.remove(bloqueio)
        else:
            self.personagem.update(self.tela, self.mapa.paredes , self.inimigos)


       
      
        self.objetivos, coletavel = self.coletaveis.update(self.tela, self.personagem)
        #print(self.objetivos)
        if coletavel != None:
            try:
                self.mapa.dados[self.quadro]["coletaveis"].remove({"path" :coletavel[2], "x":coletavel[1].x, "y": coletavel[1].y})
            except:
                pass
        self.portas()
        self.tempo()
        if self.personagem.vida <= 0:
            self.morte()
        #print(pygame.mouse.get_pos())