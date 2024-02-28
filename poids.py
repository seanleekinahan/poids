import pygame

from random import uniform as ranf
import math


# Poid class
class Poid(pygame.sprite.Sprite):
    # birds
    options = {
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

    def __init__(self, cfg):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.cfg = cfg

        # initial position
        self.rect = self.image.get_rect()
        self.rect.center = (ranf(0, cfg.width), ranf(0, cfg.height))

        # initial velocity and magnitude
        self.velocity = pygame.Vector2(0.5, 0.5).rotate(ranf(0, 360)).normalize()
        self.velocity.scale_to_length(self.options["max_speed"][2])
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
            if b is not self and self.options["cohesion_range"][2] > d:
                alignment_force += b.velocity
                cohesion_force += b.rect.center

                if self.options["separation_distance"][2] > d:
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

        steering_force += alignment_force * self.options["align_factor"][2]
        steering_force += cohesion_force * self.options["cohesion_factor"][2]
        steering_force += separation_force * self.options["separation_factor"][2]

        if steering_force.length() > 0:
            steering_force.scale_to_length(self.strength)

        self.acceleration += steering_force

    def update_all(self, birds):

        # perform checks for nearby birds and adjust vector
        self.flocking(birds)
        self.rect.center += self.velocity
        self.velocity += self.acceleration

        # clamp vector magnitude
        if self.velocity.magnitude() > self.options["max_speed"][2]:
            self.velocity.scale_to_length(self.options["max_speed"][2])

        if self.velocity.magnitude() < self.options["min_speed"][2]:
            self.velocity.scale_to_length(self.options["min_speed"][2])

        # wrap around the screen
        if self.rect.left > self.cfg.width:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = self.cfg.width
        if self.rect.top > self.cfg.height:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = self.cfg.height

