import pygame
import pygame_widgets
import ui
import grid
from poids import *
from config import *

# TODO: Refactor nearby_bird checks to search local grid rather than all birds - chokes approaching 1000 birds currently
# TODO - Stretch: Predators & Prey


cfg = Config({
    "width": 1200,
    "height": 800,
    "cell_size": 50,
    "target_fps": 24,
})

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Poids")
clock = pygame.time.Clock()

# Create the screen
cfg.screen = pygame.display.set_mode((cfg.width, cfg.height))
grid_list, grid_render = grid.create_grid(cfg)
sliders = ui.init_sliders(cfg, Poid.options)


# Create birds
birds_group = pygame.sprite.Group()

# Main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # smooth adjustment of visible birds
    diff = len(birds_group) - Poid.options["num_birds"][2]
    if diff > 1:
        birds_group.remove(birds_group.sprites()[0])

    if diff < -1:
        birds_group.add(Poid(cfg))

    for bird in birds_group:
        bird.update_all(birds_group)

    # draw
    cfg.screen.fill((0, 0, 0))
    birds_group.draw(cfg.screen)
    grid_render.draw(cfg.screen)

    for slider in sliders:
        slider.valueBox.setText(slider.getValue())
        tup = Poid.options[slider.name]
        Poid.options[slider.name] = (tup[0], tup[1], slider.getValue())

    pygame.display.flip()
    pygame_widgets.update(events)
    pygame.display.update()
    clock.tick(cfg.fps)

pygame.quit()
