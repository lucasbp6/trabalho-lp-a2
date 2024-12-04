import pygame
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import personagem as per
import armas as a
import boss as b
import interagiveis as intr




def create_key_mock(pressed_keys):

    def mocked_get_pressed():
        tmp = [0] * 300
        for key in pressed_keys:
            tmp[key] = 1
        return tmp

    return mocked_get_pressed


class TestPlayer(unittest.TestCase):

    personagem = per.Perso_Controle("../assets/personagens/gabriel.png",0,0,10,10,5)
    #Personagem Padrão para Teste
    
    
    def test_moves(self):
        self.assertEqual(personagem.rect.topleftx,0)
        self.assertEqual(personagem.rect.toplefty,0)
        
        mock_function = create_key_mock([pygame.K_w])
        pygame.key.get_pressed = mock_function
        
        personagem.controle([])
        
        self.assertEqual(personagem.rect.topleftx,0)
        self.assertEqual(personagem.rect.toplefty,-5)
 
        mock_function = create_key_mock([pygame.K_s])
        pygame.key.get_pressed = mock_function

        personagem.controle([])
        
        self.assertEqual(personagem.rect.topleftx,0)
        self.assertEqual(personagem.rect.toplefty,0)

        mock_function = create_key_mock([pygame.K_a])
        pygame.key.get_pressed = mock_function

        personagem.controle([])
        
        self.assertEqual(personagem.rect.topleftx,-5)
        self.assertEqual(personagem.rect.toplefty,0)

        mock_function = create_key_mock([pygame.K_d])
        pygame.key.get_pressed = mock_function

        personagem.controle([])
        
        self.assertEqual(personagem.rect.topleftx,0)
        self.assertEqual(personagem.rect.toplefty,0)
        
        
    def test_direction(self):
        self.assertEqual(personagem.direcao(1,1),[1,1])
        self.assertEqual(personagem.direcao(1,0),[1,0])
        self.assertEqual(personagem.direcao(0,1),[0,1])
        self.assertEqual(personagem.direcao(1,0),[1,0])
        self.assertEqual(personagem.direcao(-1,0),[-1,0])
        self.assertEqual(personagem.direcao(0,-1),[0,-1])
        self.assertEqual(personagem.direcao(-1,-1),[-1,-1])
        
        self.assertEqual(personagem.direcao_mouse(1,1),[1,-1])
        
    def test_colision(self):
        parede = pygame.rect(5,0,10,10)
        inimigo = per.Inimigo("../assets/personagens/samyra.png",0,5,10,10,5,"seguir")
        
        enemies = per.Inimigos()
        enemies.add(inimigo)
        
        self.assertEqual(personagem.colisao(parede),parede)
        self.assertTrue(colisao_perso(enemies))
    
    @patch('pygame.mouse.get_pos', return_value=(1, 1)):    
    def test_tiro(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        
        mock_function = create_key_mock([pygame.K_SPACE])
        pygame.key.get_pressed = mock_function
        
        personagem.controle([])
        
        self.assertEqual(len(personagem.tiros),1)



class TestEnemy(unittest.TestCase):

    inimigo = per.Inimigo("../assets/personagens/samyra.png", 50, 50, 40, 40, 10, sentido="seguir")
    
    paredes = [pygame.Rect(200, 200, 50, 50), pygame.Rect(300, 300, 50, 50)]

    jogador = pygame.Rect(100, 100, 50, 50)

    def test_delta(self):
    delta_x, delta_y = self.inimigo.delta(jogador)
    self.assertEqual(delta_x, 1)
    self.assertEqual(delta_y, 1)

    def test_movimento_seguir(self):
        self.inimigo.movimento(paredes,jogador)
        self.assertGreater(inimigo.rect.x, 50)
        self.assertGreater(inimigo.rect.y, 50)

    def test_movimento_aleatorio(self):
        inimigo.sentido = "aleatorio"
        with patch("random.choice", side_effect=[1, 0]):
            inimigo.movimento(paredes)
            self.assertEqual(inimigo.rect.x, 50 + inimigo.velocidade)
            self.assertEqual(inimigo.rect.y, 50)

    def test_tiro(self):
        inimigo.stamina = 0
        inimigo.tiro(paredes, jogador)
        self.assertEqual(len(inimigo.tiros.balas), 1) 

    def test_colision_line(self):
        resultado = inimigo.linha_colide_com_paredes(paredes, jogador)
        self.assertTrue(resultado)


if __name__ == '__main__':
    pygame.init() 
    pygame.display.set_mode((1000, 1000))
    
    
    unittest.main