from circleshape import CircleShape
import pygame
import random
from constants import *
import math
import pygame.sprite

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, screen_width, screen_height):
        super().__init__(x, y, radius)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lumpy_points = []
        num_points = 16
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            lump_radius = radius * random.uniform(0.7, 1.2)
            x_offset = math.cos(angle) * lump_radius
            y_offset = math.sin(angle) * lump_radius
            self.lumpy_points.append((x_offset, y_offset))

    def split(self, drawable_group, updateable_group):
        # Spawn explosion before killing (only in drawable group)
        Explosion(self.position.x, self.position.y, [drawable_group, updateable_group])
        self.kill()
        new_radius = self.radius / 2
        if new_radius < ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        r_a2 = self.velocity.rotate(random_angle)
        r_a3 = self.velocity.rotate(-random_angle)
        a_1 = Asteroid(self.position.x, self.position.y, new_radius, self.screen_width, self.screen_height)
        a_2 = Asteroid(self.position.x, self.position.y, new_radius, self.screen_width, self.screen_height)
        for group in self.containers:
            group.add(a_1)
            group.add(a_2)
        a_1.velocity = r_a2 * 1.2
        a_2.velocity = r_a3 * 1.2

    def draw(self, screen):
        points = [
            (self.position.x + x, self.position.y + y)
            for (x, y) in self.lumpy_points
        ]
        pygame.draw.polygon(screen, "black", points)   # Fill
        pygame.draw.polygon(screen, "white", points, 2)  # Outline

    def update(self, dt):
        self.position += self.velocity * dt
        # Screen wrapping
        self.position.x %= self.screen_width
        self.position.y %= self.screen_height

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, num_particles=24):
        super().__init__(*groups)
        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(0.25, 0.5)
            size = random.randint(3, 7)
            color = random.choice([(255, 200, 50), (255, 255, 100), (255, 160, 60), (255, 255, 255)])
            self.particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'lifetime': lifetime,
                'timer': 0,
                'size': size,
                'color': color,
            })
        self.done = False

    def update(self, dt):
        alive = False
        for p in self.particles:
            p['timer'] += dt
            if p['timer'] < p['lifetime']:
                alive = True
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
        if not alive:
            self.kill()

    def draw(self, screen):
        for p in self.particles:
            if p['timer'] < p['lifetime']:
                alpha = int(255 * (1 - p['timer'] / p['lifetime']))
                surf = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
                pygame.draw.rect(surf, p['color'] + (alpha,), (0, 0, p['size'], p['size']))
                screen.blit(surf, (p['x'] - p['size']//2, p['y'] - p['size']//2))