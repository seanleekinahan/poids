import pygame_widgets
import ui
import grid
from poids import *
from config import *

# TODO: Refactor nearby_bird checks to search local grid rather than all birds - chokes approaching 1000 birds currently
# TODO - Stretch: Predators & Prey

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Poids")
clock = pygame.time.Clock()

# Create the screen
cfg["screen"] = pygame.display.set_mode((cfg["width"], cfg["height"]))
cells, grid_render = grid.create_grid()
sliders = ui.init_sliders()


# Create birds
birds = pygame.sprite.Group()

# Main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # smooth adjustment of visible birds
    diff = len(birds) - options["num_birds"][2]
    if diff > 1:
        birds.remove(birds.sprites()[0])

    if diff < -1:
        birds.add(Poid())

    # fix this bad code
    cells = grid.clear_grid()
    grid.update_cells(cells, birds)

    for bird in birds:
        bird.update(cells)

    # draw
    cfg["screen"].fill((0, 0, 0))
    birds.draw(cfg["screen"])
    grid_render.draw(cfg["screen"])

    for slider in sliders:
        slider.valueBox.setText(slider.getValue())
        tup = options[slider.name]
        options[slider.name] = (tup[0], tup[1], slider.getValue())

    pygame.display.flip()
    pygame_widgets.update(events)
    pygame.display.update()
    clock.tick(cfg["fps"])

pygame.quit()
