import pygame
import unittest
import sys
import os
from unittest.mock import patch

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
    pygame.init()
    pygame.display.set_mode((1000, 1000))
    
    personagem = per.Perso_controle("../assets/personagens/gabriel.png",0,0,10,10,5)
    #personagem Padrão para Teste
    parede = pygame.Rect(5,0,10,10)
    
    inimigo = per.Inimigo("../assets/personagens/samyra.png",0,5,10,10,5,"seguir")
    
    def test_moves(self):
        self.assertEqual(self.personagem.rect.topleft[0],0)
        self.assertEqual(self.personagem.rect.topleft[1],0)
        
        mock_function = create_key_mock([pygame.K_w])
        pygame.key.get_pressed = mock_function
        
        self.personagem.controle([])
        
        self.assertEqual(self.personagem.rect.topleft[0],0)
        self.assertEqual(self.personagem.rect.topleft[1],-5)
 
        mock_function = create_key_mock([pygame.K_s])
        pygame.key.get_pressed = mock_function

        self.personagem.controle([])
        
        self.assertEqual(self.personagem.rect.topleft[0],0)
        self.assertEqual(self.personagem.rect.topleft[1],0)

        mock_function = create_key_mock([pygame.K_a])
        pygame.key.get_pressed = mock_function

        self.personagem.controle([])
        
        self.assertEqual(self.personagem.rect.topleft[0],-5)
        self.assertEqual(self.personagem.rect.topleft[1],0)

        mock_function = create_key_mock([pygame.K_d])
        pygame.key.get_pressed = mock_function

        self.personagem.controle([])
        
        self.assertEqual(self.personagem.rect.topleft[0],0)
        self.assertEqual(self.personagem.rect.topleft[1],0)
        
        
    def test_direction(self):
        self.assertEqual(self.personagem.direcao(1,1),[1,1])
        self.assertEqual(self.personagem.direcao(1,0),[1,0])
        self.assertEqual(self.personagem.direcao(0,1),[0,1])
        self.assertEqual(self.personagem.direcao(1,0),[1,0])
        self.assertEqual(self.personagem.direcao(-1,0),[-1,0])
        self.assertEqual(self.personagem.direcao(0,-1),[0,-1])
        self.assertEqual(self.personagem.direcao(-1,-1),[-1,-1])
        
        self.assertEqual(self.personagem.direcao_mouse(1,1),[-1,-1])
        
    def test_colision(self):
        parede = [self.parede]
        # inimigo = per.Inimigo("../assets/personagens/samyra.png",0,5,10,10,5,"seguir")
        
        enemies = per.Inimigos()
        enemies.add(self.inimigo)
        
        self.assertEqual(self.personagem.colisao(parede),self.parede)
        self.assertTrue(self.personagem.colisao_perso(enemies))
    
    @patch('pygame.mouse.get_pos', return_value=(1, 1))   
    def test_tiro(self,mock_mouse_get_pos):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        
        mock_function = create_key_mock([pygame.K_SPACE])
        pygame.key.get_pressed = mock_function
        
        self.personagem.stamina = 0
        #Como estamos apenas testando, os ticks que descontariam a stamina não funcionam
        self.personagem.controle([])
        
        self.assertEqual(len(self.personagem.tiros.balas),1)



class TestEnemy(unittest.TestCase):
    pygame.init()
    inimigo = per.Inimigo("../assets/personagens/samyra.png", 100, 100, 40, 40, 10, sentido="seguir")
    
    paredes = [pygame.Rect(0, 200, 100, 20), pygame.Rect(300, 300, 50, 50)]

    jogador = per.Perso_controle("../assets/personagens/gabriel.png",0,0,10,10,5)

    def test_delta(self):
        delta_x, delta_y = self.inimigo.delta(self.jogador)
        self.assertEqual(delta_x, -1)
        self.assertEqual(delta_y, -1)

    def test_movimento_seguir(self):
        self.inimigo.movimento(self.paredes,self.jogador)
        self.assertGreater(self.inimigo.rect.x, 100)
        # self.assertLess(self.inimigo.rect.y, 50)

    def test_movimento_aleatorio(self):
        self.inimigo.sentido = "aleatorio"
        with patch("random.choice", side_effect=[1, 0]):
            self.inimigo.movimento(self.paredes)
            self.assertEqual(self.inimigo.rect.x, 100 + self.inimigo.velocidade)
            self.assertEqual(self.inimigo.rect.y, 100)

    def test_tiro(self):
        self.inimigo.stamina = 0
        self.inimigo.tiro(self.paredes, self.jogador)
        self.assertEqual(len(self.inimigo.tiros.balas), 1) 

    def test_colision_line(self):
        self.paredes = [pygame.Rect(0, 21,300,2)]
        resultado = self.inimigo.linha_colide_com_paredes(self.paredes, self.jogador)
        self.assertTrue(resultado)


if __name__ == '__main__':
    unittest.main()