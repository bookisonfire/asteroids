from circleshape import CircleShape
import pygame
import random
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        r_a2 = self.velocity.rotate(random_angle)
        r_a3 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        a_1 = Asteroid(self.position.x, self.position.y, new_radius)
        a_2 = Asteroid(self.position.x, self.position.y, new_radius)
        for group in self.containers:
            group.add(a_1)
            group.add(a_2)
        a_1.velocity = r_a2 * 1.2
        a_2.velocity = r_a3 * 1.2
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            self.radius,
             2
        )

    def update(self, dt):
        self.position += self.velocity * dt