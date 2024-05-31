import pygame

import client.ui.bomb
from bomb import Bomb
import player7
import player8
import wall
from stub.client_stub import ClientStub


# ----------------------------------------------------------------------------
# A grid is added to the world. Now, sprites move step by step
# on the grid. This will allow us to discretise the world
# It is used the DirtySprite concept. It allows to update only the part of
# the screen that changes.
# We need to align objects position to the grid. How?
# ----------------------------------------------------------------------------

# PROTOCOLO "nr quad"
# pedir nr quad x e receber o valor
# pedir nr qud y e recebe o valor

# PROTOCOLO "player "
# O jogador (client) envia o seu nome
# Servidor devolve o ID

# PROTOCOLO "update "
# O jogador envia movimento
# Servidor envia ok (?)

# PROTOCOLO "game update"
# O jogador pede uma atualização do estado do mundo
# Servidor envia msg com essa atualização

class Game(object):
    def __init__(self,cs: ClientStub, size:int):
        self.cs = cs
        # new
        self.id = ""
        # Size of the game
        nr_x = self.cs.get_nr_quad_x()
        nr_y = self.cs.get_nr_quad_y()

        self.width, self.height = nr_x * size, nr_y * size
        self.max_x, self.max_y = nr_x, nr_y

        # define a altura do UI do jogo
        self.ui_height = 100
        self.game_heigth = self.height
        self.total_height = self.game_heigth + self.ui_height

        self.ui_surface = pygame.Surface((self.width, self.ui_height))
        self.ui_surface.fill((200, 200, 200))

        self.screen = pygame.display.set_mode((self.width, self.total_height))
        pygame.display.set_caption("MazeSweep")

        self.clock = pygame.time.Clock()
        # Grid
        self.grid_size = size

        # Create The Backgound
        self.background = pygame.Surface((self.width, self.game_heigth))
        # Convert the image to a better format to blit
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background,(0,0))
        self.draw_grid(self.width,self.height,self.grid_size,(0,0,0))

        self.bomb_hits = 0

        pygame.display.update()

    def draw_ui(self, name: str, bombs: int):
        # Clear the UI surface
        self.ui_surface.fill((200, 200, 200))

        # Example: Draw a simple text element
        font = pygame.font.Font(None, 36)
        player1_text = font.render('Player: ' + name, True, (0, 0, 0))
        bombs_text = font.render('Bombs: ' + str(bombs), True, (0, 0, 0))

        self.ui_surface.blit(player1_text, (10, 10))
        self.ui_surface.blit(bombs_text, (10, 30))

        # Blit the UI surface onto the main screen
        self.screen.blit(self.ui_surface, (0, self.game_heigth))

    def draw_grid(self,width:int, height:int, size: int, colour:tuple):
        '''
        Desenha uma grelha, assumindo que o mundo é quadrado. Como fazer se o mundo não é quadrado?
        :param width: dimensão no eixo dos xx da janela
        :param height: dimensão no eixo dos yy da janela
        :param size: the size of the grid
        :param colour:
        :return:
        '''
        # Desenhar as linhas horizontais
        for pos in range(0, height, size):
            pygame.draw.line(self.screen, colour, (0, pos), (width,pos))
        # Desenhar as linhas verticais
        for pos in range(0, width, size):
            pygame.draw.line(self.screen, colour, (pos, 0), (pos,height))
    # new:
    # modify name for create_player instead create_players
    # ask for the player's name
    # get the id
    def create_player(self,size:int) -> str:
        '''
        :param self:
        :param size:
        :return:
        '''
        self.players = pygame.sprite.LayeredDirty()
        name = input("What is your name?")
        (self.id, pos) = self.cs.set_player(name)
        print("Player ",name," created with id: ",self.id)
        self.playerA = player7.Player(self.id, pos[0], pos[1], size, self.players)
        self.players.add(self.playerA)
        return name

    #new
    def create_walls(self, size:int):
        '''
        :param self:
        :param wall_size:
        :return:
        '''
        self.walls = pygame.sprite.Group()
        walls: dict = self.cs.get_walls()

        for wl in walls.values():
            (x,y) = wl[1]
            w = wall.Wall(0, x, y, size, self.walls)
            self.walls.add(w)

    #def create_bomb(self, size):
    #    self.bombs = pygame.sprite.Group()
    #    bombs: dict = self.cs.get_bombs()
    #
    #    for bl in bombs.values():
    #        (x, y) = bl[1]
    #        b = Bomb(0, x, y, size, self.bombs)
    #        self.bombs.add(b)

    def create_bomb(self, size):
        self.bombs = pygame.sprite.Group()
        self.bomb_positions = []  # Store bomb positions here
        bombs: dict = self.cs.get_bombs()

        for bl in bombs.values():
            (x, y) = bl[1]
            b = Bomb(0, x, y, size, self.bombs)
            self.bombs.add(b)
            self.bomb_positions.append((x, y))  # Store each bomb's position

    def get_objects(self, size):
        objects = self.cs.get_objects()
        print("Objects: ", objects)
        # OS objects é um dicionario
        # {'1':["nome", [x,y];'2':[...]}
        # Para cada objecto, verificar que o ID não é igual ao meu ID
        # Se não for criar um objeto DirtySprite provavelmente de acordo com o nome
        # Adicionar esse DirtuSprite á lista de objetos
        for id in objects.keys():
            if int(id) != self.id:
                self.player = player8.Player(id, objects[id][1][0], objects[id][1][1], size, self.players)
                self.players.add(self.player)

    def update_objects(self):
        objects: dict = self.cs.get_objects()
        for player in self.players:
            if player.get_id() != self.id:
                pos = objects[str(player.get_id())][1]
                player.set_pos(pos)

    def start_game(self)-> bool:
        return bool(self.cs.execute_start_game())

    #TODO:
    #def check_bomb_collision(self, player):
    #    player_pos = (player.rect.x, player.rect.y)
    #    for bomb_pos in self.bomb_positions:
    #        if player_pos == bomb_pos:
    #            self.bomb_hits += 1

    def run(self):
        self.create_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.walls.update()

        self.create_bomb(self.grid_size)
        self.bombs.draw(self.screen)
        self.bombs.update()

        player_name = self.create_player(self.grid_size)

        self.start_game()
        self.get_objects(self.grid_size)

        end = False
        while not end:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
            self.players.update(self,self.cs)
            rects = self.players.draw(self.screen)
            self.draw_grid(self.width,self.height,self.grid_size,(0, 0, 0))
            self.update_objects()

            #TODO: Adicionar contador de bombas
            #TODO: Para cada bomba será necessário remove-la
            #for player in self.players:
            #    self.check_bomb_collision(player)

            self.draw_ui(player_name, self.bomb_hits)

            pygame.display.update(rects)
            self.players.clear(self.screen,self.background)

        return

