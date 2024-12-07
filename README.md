A2 - Linguagens de Programação
------------------------------

O presente trabalho foi realizado para a segunda avaliação da disciplina de Linguagens de Programação ministrada pelo Prof. Dr. Matheus Werner.
A temática era usar os conteúdos aprendidos em sala de programação orientada à objetos de forma a fazer um jogo usando `Pygame`. O grupo é composto por:

* Lucas Batista Pereira
* Samyra Mara
* Gabriel Carneiro

Como executar o jogo
--------------------

Após clonar o repositório, precisamos instalar as bibliotecas:

```pip install requirements.txt```

Após isso, estando no repositório, precisamos dar os seguintes comandos em sequências

```
cd src
python3 game.py
```

Como executar os testes
-----------------------

Estando na branch "gabriel" do repositório:

```
git switch gabriel
```

Basta mandar os seguintes comandos em sequência:

```
cd tests
python3 testes_in_game.py
```

Breve Tutorial
--------------
O jogo é inspirados em típicos jogos de plataforma top-down, inspirado principalmente pelo jogo "The Binding of Isaac"

O objetivo do jogo é passar de cada uma das fases (de preferência o mais rápido possível), considerando que sua vida é mantida no passar das fases, considerando como objetivo coletar todos os coletáveis.Seu personagem é decidido no menu de seleção, e os comandos é simples: WASD para movimentações e o botão direito do mouse para ataque.

Inicialmente, apenas a fase 1 está disponível, e conforme o progresso no jogo elas serão desbloqueadas.

