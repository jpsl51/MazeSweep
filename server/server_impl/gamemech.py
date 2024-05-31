from typing import Union
# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
import random
from server_impl import NR_QUAD_Y, NR_QUAD_X, MAP
class GameMech:
    def __init__(self, nr_x: int, nr_y: int):
        self.nr_max_x = nr_x
        self.nr_max_y = nr_y
        self.players = dict()
        self.walls = dict()
        self.bombs = dict()  # Dicionário para armazenar as bombas
        self.world = dict()
        for x in range(self.nr_max_x):
            for y in range(self.nr_max_y):
                self.world[(x, y)] = []
        self.nr_players = 0

        self.pos_players = []

        self.nr_walls = 0
        self.nr_bombs = 0
        #self.add_wall_around()

        self.add_bomb_world()
        self.add_wall_world()

    def get_nr_x(self) -> int:
        return self.nr_max_x

    def get_nr_y(self) -> int:
        return self.nr_max_y

    def is_wall(self,objects)->bool:
        for obj in objects:
            if obj[0] == "wall" and obj[1] == "wall":
                return True
        return False

    def add_wall(self, x:int, y:int) -> bool:
        # If there is no all or ...

        if not self.is_wall(self.world[(x,y)]):
            self.walls[self.nr_walls]=["wall",(x,y)]
            self.world[(x,y)].append(["obst","wall",self.nr_walls])
            self.nr_walls += 1
            return True
        return False

    def get_players(self) -> dict:
        return self.players
    def get_walls(self) -> dict:
        return self.walls

    def add_wall_world(self) -> dict:
        for index, i in enumerate(MAP):
            if i == "#":
                row = index // 20
                col = index % 20
                self.add_wall(col, row)

    def add_wall_around(self) -> bool:
        """
        Adiciona obstáculos à volta do mundo
        :ret          self.world([2,2]).append(["obst","wall",self.nr_walls])
            self.nr_walls += 1
  urn: Retorna um booleano confirmando o sucesso da operação
        """
        for x in range(0,self.nr_max_x):
            for y in range(0,self.nr_max_y):
                if x in (0,self.nr_max_x - 1) or y in (0, self.nr_max_y - 1):
                    self.walls[self.nr_walls]=["wall",(x,y)]
                    self.world[(x,y)].append(["obst","wall",self.nr_walls])
                    self.nr_walls += 1

        #self.walls[self.nr_walls]=["wall",(10,12)]
        #self.world[(10,12)].append(["obst","wall",self.nr_walls])
        #self.nr_walls += 1

        return True

    def add_player(self, name: str) -> tuple:
        """
        Adiciona um jogador e retorna o seu número e a sua posição
        :param name: Nome do jogador
        :return: Retorna um túpulo com o número e posição do jogador com o formato (nr,(x,y))
        """

        # Lê a posição do jogador no mapa (?), e adiciona no jogo.
        for index, i in enumerate(MAP):
            if i == "?":
                row = index // 20
                col = index % 20
                self.pos_players.append((col, row))

        self.players[self.nr_players] = [name, self.pos_players[self.nr_players]]
        self.world[self.pos_players[self.nr_players]].append(["player", name, self.nr_players])
        self.nr_players += 1
        return (self.nr_players - 1, self.pos_players[self.nr_players - 1])

    def is_bomb(self, objects) -> bool:
        for obj in objects:
            if obj[0] == "bomb" and obj[1] == "bomb":
                return True
        return False

    def add_bomb(self, x: int, y: int) -> None:
        #if not self.is_bomb(self.world[(x, y)]) and self.is_wall(self.world[(x, y)]):
        if not self.is_bomb(self.world[(x, y)]):
            self.bombs[self.nr_bombs] = ["bomb", (x, y)]
            self.world[(x, y)].append(["objct", "bomb", self.nr_bombs])
            self.nr_bombs += 1
            return True
        return False

    def add_bomb_world(self) -> bool:
        for index, i in enumerate(MAP):
            if i == "*":
                row = index // 20
                col = index % 20
                self.add_bomb(col, row)

    def get_bombs(self) -> dict:
        # Retorna todas as bombas
        return self.bombs

    def move_to(self, pos: tuple, dir: int) -> tuple:
        if dir == UP:
            new_pos = (pos[0], pos[1]-1)
        elif dir == DOWN:
            new_pos = (pos[0], pos[1]+1)
        elif dir == LEFT:
            new_pos = (pos[0] - 1, pos[1])
        elif dir == RIGHT:
            new_pos = (pos[0] + 1, pos[1])

        if (0 <= new_pos[0] < self.nr_max_x) and (0 <= new_pos[1] < self.nr_max_y):
            return new_pos
        else:
            return pos  # Se estiver fora dos limites, retorna a posição atual


    #def is_obstacle(self,obj:list):
    #    return obj[0] == "obst"

    #TODO:
    def out_of_bounds(self, pos: tuple) -> bool:
        if pos[0] == NR_QUAD_X:
            return True
        else:
            return False

    def obstacle_in_pos(self, pos:tuple) -> bool:
        objects = self.world[pos]
        for obj in objects:
            if obj[0] == "obst":
                return True
        return False

        # TODO: using functional commands to do the search
        #res = list(map(self.is_obstacle,objects))
        #if res !=[]:
        #    return True
        #return False


    def execute(self,nr_player:int, dir:int) -> tuple:
        # ALTERAR A POSICAO DO PLAYER
        #  -- ir buscar a posicao anterior
        pos = self.players[nr_player][1]
        name = self.players[nr_player][0]
        #  -- nova posição
        new_pos = self.move_to(pos, dir)
        #  -- verificar se se pode mover na direção desejada.
        # TODO: adicionar verificação para movimento fora de campo.
        if self.obstacle_in_pos(new_pos) or self.out_of_bounds(new_pos):
            new_pos = pos
        #  -- acrescentar ao dicionário players
        self.players[nr_player] = [name,new_pos]
        #  -- mudar o mundo
        self.world[pos].remove(["player",name,nr_player])
        self.world[new_pos].append(["player",name,nr_player])
        return new_pos

def main():
    gm = GameMech(10, 10)
    print(gm.world[(0, 2)])
    j1 = gm.add_player("jose")
    j2 = gm.add_player("miguel")

    gm.execute(j1[0],DOWN)
    print("Jogador 0:", gm.players[0])
    print("Posição (5,5):", gm.world[5, 5])
    print("Posição (5,6):", gm.world[5, 6])
    print("BOMBA (6,7):", gm.world[6, 7])
    print("BOMBA (6,8):", gm.world[6, 8])

if __name__ == '__main__':
    main()