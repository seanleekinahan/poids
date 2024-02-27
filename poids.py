import pygame
import pygame_widgets
from random import uniform as ranf
import math
import ui

# TODO: Implement forward vision cone to avoid cohesion & alignment with birds to rear.
# TODO: Implement distance based force modifiers for cohesion & separation
# TODO: Break screen into grid and refactor nearbybird checks to search local grid rather than all birds - chokes approaching 1000 birds currently
# TODO - Stretch: Predators & Prey

# Initialize Pygame
pygame.init()

# rendering
WIDTH, HEIGHT = 1200, 800
FPS = 24

# birds
bvars = {
    # (min, max, default)
    "num_birds": (1, 250, 32),
    "cohesion_range": (1, 100, 30),
    "separation_distance": (1, 100, 10),
    "min_speed": (0.1, 1, 1),
    "max_speed": (0.1, 50, 10),
    "align_factor": (0.01, 1, 0.1),
    "cohesion_factor": (0.0001, 0.01, 0.001),
    "separation_factor": (0.2, 20, 2)
}


# Poid class
class Poid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))

        # initial position
        self.rect = self.image.get_rect()
        self.rect.center = (ranf(0, WIDTH), ranf(0, HEIGHT))

        # initial velocity and magnitude
        self.velocity = pygame.Vector2(0.5, 0.5).rotate(ranf(0, 360)).normalize()
        self.velocity.scale_to_length(bvars["max_speed"][2])
        self.acceleration = pygame.Vector2(0, 0)

        # random per-bird attributes
        self.strength = ranf(0.8, 1.2)

    def get_distance(self, other_bird):
        dx = (self.rect.x - other_bird.rect.x) ** 2
        dy = (self.rect.y - other_bird.rect.y) ** 2
        return math.sqrt(dx + dy)

    # finding all forces in one function to avoid looping more than once per bird
    def flocking(self, birds):

        self.acceleration.x, self.acceleration.y = 0, 0

        steering_force = pygame.Vector2(0, 0)
        alignment_force = pygame.Vector2(0, 0)
        cohesion_force = pygame.Vector2(0, 0)
        separation_force = pygame.Vector2(0, 0)
        nearby_birds = 0

        for b in birds:
            d = self.get_distance(b)
            if b is not self and len(bvars["cohesion_range"]) >= 3 and bvars["cohesion_range"][2] > d:
                alignment_force += b.velocity
                cohesion_force += b.rect.center

                if bvars["separation_distance"][2] > d:
                    pos = pygame.Vector2(self.rect.x, self.rect.y)
                    other_pos = pygame.Vector2(b.rect.x, b.rect.y)
                    separation_force += (pos - other_pos) / (d + 0.001)

                nearby_birds += 1

        if nearby_birds > 0:
            alignment_force /= nearby_birds
            cohesion_force /= nearby_birds
            separation_force /= nearby_birds

            alignment_force -= self.velocity
            cohesion_force -= self.rect.center

        steering_force += alignment_force * bvars["align_factor"][2]
        steering_force += cohesion_force * bvars["cohesion_factor"][2]
        steering_force += separation_force * bvars["separation_factor"][2]

        if steering_force.length() > 0:
            steering_force.scale_to_length(self.strength)

        self.acceleration += steering_force

    def update(self, birds):

        # perform checks for nearby birds and adjust vector
        self.flocking(birds)
        self.rect.center += self.velocity
        self.velocity += self.acceleration

        # clamp vector magnitude
        if self.velocity.magnitude() > bvars["max_speed"][2]:
            self.velocity.scale_to_length(bvars["max_speed"][2])

        if self.velocity.magnitude() < bvars["min_speed"][2]:
            self.velocity.scale_to_length(bvars["min_speed"][2])

        # wrap around the screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poids")

sliders = ui.init_sliders(screen, bvars)

clock = pygame.time.Clock()

# Create birds
birds_group = pygame.sprite.Group()
for _ in range(bvars["num_birds"][2]):
    new_bird = Poid()
    birds_group.add(new_bird)

# Main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    current_birds = len(birds_group)
    goal_birds = bvars["num_birds"][2]
    diff = current_birds - goal_birds

    if diff > 0:
            birds_group.remove(birds_group.sprites()[0])

    if diff < 0:
            new_bird = Poid()
            birds_group.add(new_bird)

    for bird in birds_group:
        bird.update(birds_group)

    # draw
    screen.fill((0, 0, 0))
    birds_group.draw(screen)

    for slider in sliders:
        slider.valueBox.setText(slider.getValue())
        tup = bvars[slider.name]
        bvars[slider.name] = (tup[0], tup[1], slider.getValue())

    pygame.display.flip()
    pygame_widgets.update(events)
    pygame.display.update()
    clock.tick(FPS)

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

pygame.quit()
