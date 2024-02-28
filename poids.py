import pygame
from config import *
from random import uniform as ranf
import math


# Poid class
class Poid(pygame.sprite.Sprite):
    # birds

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))

        # initial position
        self.rect = self.image.get_rect()
        self.rect.center = (ranf(0, cfg["width"]), ranf(0, cfg["height"]))

        # initial velocity and magnitude
        self.velocity = pygame.Vector2(0.5, 0.5).rotate(ranf(0, 360)).normalize()
        self.velocity.scale_to_length(options["max_speed"][2])
        self.acceleration = pygame.Vector2(0, 0)

        # random per-bird attributes
        self.strength = ranf(0.8, 1.2)

    def get_distance(self, other_bird):
        dx = (self.rect.x - other_bird.rect.x) ** 2
        dy = (self.rect.y - other_bird.rect.y) ** 2
        return math.sqrt(dx + dy)

    def get_angle(self, other_bird):

        normal_velocity = self.velocity.normalize()
        dot = round((normal_velocity.x * other_bird.rect.x) + (normal_velocity.y * other_bird.rect.y), 3)
        bird_mag = round(self.velocity.normalize().magnitude(), 3)
        other_bird_mag = round(math.sqrt(other_bird.rect.x ** 2 + other_bird.rect.y ** 2), 3)

        if bird_mag == 0 or other_bird_mag == 0:
            return 0

        angle_radians = math.acos(dot / (bird_mag * other_bird_mag))
        angle_degrees = math.degrees(angle_radians)

        if angle_degrees > 180:
            angle_degrees = abs(360 - angle_degrees)
        return angle_degrees

    # finding all forces in one function to avoid looping more than once per bird
    def flocking(self, cells):
        self.acceleration.x, self.acceleration.y = 0, 0
        steering_force = pygame.Vector2(0, 0)

        alignment_force = pygame.Vector2(0, 0)
        cohesion_force = pygame.Vector2(0, 0)
        separation_force = pygame.Vector2(0, 0)
        nearby_birds = 0

        birds = []

        # big garbage code
        for col in cells:
            for row in col:
                try:
                    if row.index(self):
                        for bird in row:
                            birds.append(bird)
                finally:
                    continue



        # 1. get current bird's cell, add to list
        # 2. get cohesion distance and round to find cell distance
        # 3. get neighbouring cells within rounded distance, add to list
        # 4. iterate over list of cells with above garbage code

        for b in birds:
            d = self.get_distance(b)
            a = int(self.get_angle(b))

            if b is not self and options["cohesion_range"][2] > d and a < options["view_angle"][2]:
                alignment_force += b.velocity
                cohesion_force += b.rect.center

                if options["separation_distance"][2] > d:
                    pos = pygame.Vector2(self.rect.x, self.rect.y)
                    other_pos = pygame.Vector2(b.rect.x, b.rect.y)
                    separation_force += (pos - other_pos) / (d + 0.001)

                nearby_birds += 1

        birds.clear()

        if nearby_birds > 0:
            alignment_force /= nearby_birds
            cohesion_force /= nearby_birds
            separation_force /= nearby_birds

            alignment_force -= self.velocity
            cohesion_force -= self.rect.center

        steering_force += alignment_force * options["align_factor"][2] / 100
        steering_force += cohesion_force * options["cohesion_factor"][2] / 1000
        steering_force += separation_force * options["separation_factor"][2]

        if steering_force.magnitude() > 0:
            steering_force.scale_to_length(self.strength)

        self.acceleration += steering_force

    def update(self, cells):

        # perform checks for nearby birds and adjust vector
        self.flocking(cells)
        self.rect.center += self.velocity
        self.velocity += self.acceleration

        # clamp vector magnitude
        if self.velocity.magnitude() > options["max_speed"][2]:
            self.velocity.scale_to_length(options["max_speed"][2])

        if self.velocity.magnitude() < options["min_speed"][2]:
            self.velocity.scale_to_length(options["min_speed"][2])

        # wrap around the screen
        if self.rect.left > cfg["width"]:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = cfg["width"]
        if self.rect.top > cfg["height"]:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = cfg["height"]

