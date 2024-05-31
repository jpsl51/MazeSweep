import pygame
from stub.client_stub import ClientStub
# new
from stub import UP, DOWN, LEFT, RIGHT
# Constantes
#UP = 0
#RIGHT = 1
#DOWN = 2
#LEFT = 3

# Player 7 is part of the test example 7
# It defines a sprite with size rate
class Player(pygame.sprite.DirtySprite):
    # Já não precisamos da acelaração. As posições são as posições dos quadrados... size é a dimensão do quadrado
    def __init__(self,nr_player:int, pos_x:int, pos_y:int, size:int, *groups ):

    #def __init__(self,pos_x:int, pos_y:int, acc:int, size:int, *groups ):
        super().__init__(*groups)
        self.my_id = nr_player
        self.size = size
        self.image = pygame.image.load('images/player.png')
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * size ,pos_y * size), self.image.get_size())
        self.pos:list = [pos_x, pos_y]

    def get_size(self):
        return self.new_size

    def get_id(self):
        return self.my_id

    def set_pos(self, pos: list):
        self.rect.x = pos[0] * self.size
        self.rect.y = pos[1] * self.size

#    def update(self, dt:float, game:object):
    # Já não definimos a velocidade. Eles irão deslocar-se todos à mesma velocidade...
    def update(self, game:object, cs: ClientStub ):
        self.dirty = 1