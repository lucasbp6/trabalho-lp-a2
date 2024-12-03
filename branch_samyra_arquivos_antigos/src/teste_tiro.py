import pygame
import math

# Inicializar o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jogo de Movimento e Tiro")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Classe do personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

# Classe do projetil
class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        # Calcular direção
        angle = math.atan2(target_y - y, target_x - x)
        self.speed_x = math.cos(angle) * 10
        self.speed_y = math.sin(angle) * 10

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Remover projetil se sair da tela
        if not (0 <= self.rect.x <= 800 and 0 <= self.rect.y <= 600):
            self.kill()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
projetils = pygame.sprite.Group()

# Criar o personagem
player = Personagem(400, 300)
all_sprites.add(player)

# Variável para controlar disparos
cooldown = 0

# Loop principal
running = True
while running:
    # Capturar eventos de saída
    if pygame.event.peek(pygame.QUIT):
        running = False

    # Controle de cooldown para tiros
    if cooldown > 0:
        cooldown -= 1

    # Capturar estado do teclado
    keys = pygame.key.get_pressed()

    # Capturar estado do mouse
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0] and cooldown == 0:  # Botão esquerdo do mouse pressionado
        mouse_x, mouse_y = pygame.mouse.get_pos()
        projetil = Projetil(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
        all_sprites.add(projetil)
        projetils.add(projetil)
        cooldown = 15  # Tempo entre tiros (ajuste conforme necessário)

    # Atualizar o personagem (passando as teclas)
    player.update(keys)

    # Atualizar os projetis e outros sprites
    projetils.update()

    # Desenhar na tela
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Controlar a taxa de quadros
    clock.tick(60)

pygame.quit()

