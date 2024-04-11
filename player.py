import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, grid_size, texture):
        super().__init__()
        self.grid_size = grid_size
        self.image = pygame.Surface((self.grid_size, self.grid_size))
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.smoothscale(self.image, (20, 20))

        # self.image.fill((255, 255, 255))
        #pygame.draw.circle(self.image, (0, 0, 0), (self.grid_size // 2, self.grid_size // 2), self.grid_size // 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.width = width
        self.height = height

    # todo Roda corretamente a textura do jogador
    def update(self, direction):
        if direction == "LEFT":
            self.rect.x = max(0, self.rect.x - self.grid_size)
            self.image = pygame.transform.rotate(self.image, -180)

        elif direction == "RIGHT":
            self.rect.x = min(self.width - self.grid_size, self.rect.x + self.grid_size)
            self.image = pygame.transform.rotate(self.image, 180)

        elif direction == "UP":
            self.rect.y = max(0, self.rect.y - self.grid_size)
            self.image = pygame.transform.rotate(self.image, -90)

        elif direction == "DOWN":
            self.rect.y = min(self.height - self.grid_size, self.rect.y + self.grid_size)
            self.image = pygame.transform.rotate(self.image, 90)

