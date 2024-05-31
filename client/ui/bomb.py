import pygame


class Bomb(pygame.sprite.Sprite):
    def __init__(self, nr_bomb: int, pos_x: int, pos_y: int, size: int, *groups ):
        super().__init__(*groups)
        self.my_id = nr_bomb
        self.size = size
        self.image = pygame.image.load('images/bomb.png')
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = pygame.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        self.pos: list = [pos_x,pos_y]
