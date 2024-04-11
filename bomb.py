import pygame


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, size, grid_width, grid_height, texture):
        super().__init__()

        self.image = pygame.Surface((size, size))
        #self.image.fill((255, 0, 0))
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.smoothscale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.grid_width = grid_width
        self.grid_height = grid_height


        if self.rect.x >= self.grid_width * size or self.rect.y >= self.grid_height * size:
            raise ValueError("Posição da bomba fora dos limites da grade!")
