import pygame
import random
import math

# TODO: Implement forward vision cone to avoid cohesion & alignment with birds to rear.
# TODO: Implement distance based force modifiers for cohesion & separation
# TODO: Implement sliders for bird variables
# TODO - Stretch: Predators & Prey

# Initialize Pygame
pygame.init()

# rendering
WIDTH, HEIGHT = 1200, 800
FPS = 24

# birds
NUM_BIRDS = 32
COHESION_RANGE = 30
SEPARATION_DISTANCE = 10
MIN_SPEED = 1
MAX_SPEED = 10
ALIGN_FACTOR = 0.1
COHESION_FACTOR = 0.001
SEPARATION_FACTOR = 2


# Poid class
class Poid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))

        # initial position
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(0, WIDTH), random.uniform(0, HEIGHT))

        # initial velocity and magnitude
        random_angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(0.5, 0.5).rotate(random_angle).normalize()
        self.velocity.scale_to_length(MAX_SPEED)
        self.acceleration = pygame.Vector2(0, 0)

        # random per-bird attributes
        self.strength = random.uniform(0.8, 1.2)

    def get_distance(self, other_bird):
        dX = (self.rect.x - other_bird.rect.x) ** 2
        dY = (self.rect.y - other_bird.rect.y) ** 2
        return math.sqrt(dX + dY)

    # finding all forces in one function to avoid looping more than once per bird
    def flocking(self, birds):

        self.acceleration.x, self.acceleration.y = 0, 0

        steering_force = pygame.Vector2(0, 0)
        alignment_force = pygame.Vector2(0, 0)
        cohesion_force = pygame.Vector2(0, 0)
        separation_force = pygame.Vector2(0, 0)
        nearby_birds = 0

        for bird in birds:
            d = self.get_distance(bird)
            if bird is not self and COHESION_RANGE > d:
                alignment_force += bird.velocity
                cohesion_force += bird.rect.center

                if SEPARATION_DISTANCE > d:
                    pos = pygame.Vector2(self.rect.x, self.rect.y)
                    other_pos = pygame.Vector2(bird.rect.x, bird.rect.y)
                    separation_force += (pos - other_pos) / (d + 0.001)

                nearby_birds += 1

        if nearby_birds > 0:
            alignment_force /= nearby_birds
            cohesion_force /= nearby_birds
            separation_force /= nearby_birds

            alignment_force -= self.velocity
            cohesion_force -= self.rect.center

        steering_force += alignment_force * ALIGN_FACTOR
        steering_force += cohesion_force * COHESION_FACTOR
        steering_force += separation_force * SEPARATION_FACTOR

        if steering_force.length() > 0:
            steering_force.scale_to_length(self.strength)

        self.acceleration += steering_force

    def update(self, birds):

        # perform checks for nearby birds and adjust vector
        self.flocking(birds)
        self.rect.center += self.velocity
        self.velocity += self.acceleration

        # clamp vector magnitude
        if self.velocity.magnitude() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)

        if self.velocity.magnitude() < MIN_SPEED:
            self.velocity.scale_to_length(MIN_SPEED)

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
clock = pygame.time.Clock()

# Create birds
birds_group = pygame.sprite.Group()
for _ in range(NUM_BIRDS):
    new_bird = Poid()
    birds_group.add(new_bird)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update birds
    for bird in birds_group:
        bird.update(birds_group)

    # draw
    screen.fill((0, 0, 0))
    birds_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

pygame.quit()
