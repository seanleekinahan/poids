import pygame


def create_grid(cfg):
    num_cols = int(cfg.width // cfg.cell_size)
    num_rows = int(cfg.height // cfg.cell_size)
    grid = [[None for _ in range(num_cols)] for _ in range(num_rows)]
    cells = pygame.sprite.Group()

    for i in range(num_cols):
        line = pygame.sprite.Sprite()
        line.image = pygame.Surface((1, cfg.height))
        line.image.fill((255, 0, 0))
        line.rect = line.image.get_rect()
        line.rect.left = cfg.cell_size * i
        line.image.set_alpha(0.1*255)
        cells.add(line)

    for i in range(num_rows):
        line = pygame.sprite.Sprite()
        line.image = pygame.Surface((cfg.width, 1))
        line.image.fill((255, 0, 0))
        line.rect = line.image.get_rect()
        line.rect.bottom = cfg.cell_size * i
        line.image.set_alpha(0.1*255)
        cells.add(line)

    return grid, cells
