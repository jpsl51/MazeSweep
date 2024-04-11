import pygame
import player
import bomb
import walls
import random


class GameMech:
    def __init__(self, width, height, grid_size, bomb_count):
        pygame.init()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size
        self.bomb_count = bomb_count
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.player = player.Player(self.width, self.height, self.grid_size, "player.png")
        self.bombs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.place_bombs()
        self.create_maze()

    def create_maze(self):
        wall_positions = [
            (self.grid_size * 0, self.grid_size * 1),
            (self.grid_size * 1, self.grid_size * 1),
            (self.grid_size * 1, self.grid_size * 2),
            (self.grid_size * 2, self.grid_size * 2),
            (self.grid_size * 3, self.grid_size * 2),
            (self.grid_size * 3, self.grid_size * 0),
            (self.grid_size * 4, self.grid_size * 0),
            (self.grid_size * 4, self.grid_size * 2),
            (self.grid_size * 4, self.grid_size * 3),
            (self.grid_size * 4, self.grid_size * 4),
            (self.grid_size * 4, self.grid_size * 5),
            (self.grid_size * 5, self.grid_size * 6)
        ]

        for pos in wall_positions:
            wall = walls.Wall(pos[0], pos[1], self.grid_size, self.grid_size)
            self.walls.add(wall)

    def place_bombs(self):
        valid_positions = [
            (x, y) for x in range(self.grid_width) for y in range(self.grid_height)
            if not any(wall.rect.collidepoint(x * self.grid_size, y * self.grid_size) for wall in self.walls)
        ]

        if len(valid_positions) < self.bomb_count:
            raise ValueError("Não há posições suficientes para colocar as bombas!")

        bomb_positions = random.sample(valid_positions, self.bomb_count)

        for pos in bomb_positions:
            new_bomb = bomb.Bomb(pos[0] * self.grid_size, pos[1] * self.grid_size, self.grid_size, self.grid_width ,self.grid_height, "bomb.png")
            self.bombs.add(new_bomb)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.try_move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.try_move_player(1, 0)
                    elif event.key == pygame.K_UP:
                        self.try_move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.try_move_player(0, 1)

            if pygame.sprite.spritecollideany(self.player, self.bombs):
                print("Você perdeu!")
                running = False

            self.screen.fill((255, 255, 255))

            self.walls.draw(self.screen)

            for x in range(0, self.width, self.grid_size):
                pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height))
            for y in range(0, self.height, self.grid_size):
                pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.width, y))

            self.bombs.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def try_move_player(self, dx, dy):
        new_rect = self.player.rect.move(dx * self.grid_size, dy * self.grid_size)

        for wall in self.walls:
            if new_rect.colliderect(wall.rect):
                return

        self.player.rect = new_rect.clamp(pygame.Rect(0, 0, self.width, self.height))


if __name__ == "__main__":
    game = GameMech(800, 600, 20, 10)
    game.run()
