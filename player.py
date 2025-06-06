from circleshape import CircleShape
from constants import *
import pygame

class Player(CircleShape):
    def __init__(self, x, y, screen_width, screen_height, sound_volume=1.0):
        super().__init__(x, y, PLAYER_RADIUS)
        self.invulnerable = False
        self.respawn_timer = 0.0
        self.rotation = 0
        self.timer = 0
        self.shots = pygame.sprite.Group()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sound_volume = sound_volume
        try:
            self.shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
            self.shoot_sound.set_volume(self.sound_volume)
        except Exception:
            self.shoot_sound = None
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def shoot(self):
        new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        new_shot.velocity = velocity * PLAYER_SHOOT_SPEED
        self.shots.add(new_shot)
        if self.sound_volume > 0 and self.shoot_sound:
            self.shoot_sound.set_volume(self.sound_volume)
            self.shoot_sound.play()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        if self.invulnerable:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.invulnerable = False
                self.respawn_timer = 0.0
        if self.timer > 0: 
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)         
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
            self.timer = 0.3
        # Update and remove off-screen shots
        for shot in list(self.shots):
            shot.update(dt)
            if (shot.position.x < 0 or shot.position.x > self.screen_width or
                shot.position.y < 0 or shot.position.y > self.screen_height):
                self.shots.remove(shot)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        # Screen wrapping
        self.position.x %= self.screen_width
        self.position.y %= self.screen_height

    def respawn(self):
        self.position = pygame.Vector2(self.screen_width / 2, self.screen_height / 2)
        self.invulnerable = True
        self.respawn_timer = 2.0

    def draw(self, screen):
        points = self.triangle()
        if self.invulnerable:
            # Blink: only draw if respawn_timer*5 is even (blinks 5 times per second)
            if int(self.respawn_timer * 5) % 2 == 0:
                pygame.draw.polygon(screen, "black", points)
                pygame.draw.polygon(screen, "white", points, 2)
        else:
            pygame.draw.polygon(screen, "black", points)
            pygame.draw.polygon(screen, "white", points, 2)
        # Draw all shots
        for shot in self.shots:
            shot.draw(screen)

    def collision(self, other):
        # Assume other is an asteroid with .position and .radius
        triangle_points = self.triangle()
        circle_center = (other.position.x, other.position.y)
        circle_radius = other.radius
        return triangle_circle_collision(triangle_points, circle_center, circle_radius)

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

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

def triangle_circle_collision(triangle_points, circle_center, circle_radius):
    # 1. Check if circle center is inside the triangle
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(circle_center, triangle_points[0], triangle_points[1]) < 0.0
    b2 = sign(circle_center, triangle_points[1], triangle_points[2]) < 0.0
    b3 = sign(circle_center, triangle_points[2], triangle_points[0]) < 0.0

    if ((b1 == b2) and (b2 == b3)):
        return True  # Center is inside triangle

    # 2. Check if circle intersects any triangle edge
    for i in range(3):
        p1 = triangle_points[i]
        p2 = triangle_points[(i + 1) % 3]
        # Closest point on edge to circle center
        edge = pygame.Vector2(p2) - pygame.Vector2(p1)
        t = max(0, min(1, (pygame.Vector2(circle_center) - pygame.Vector2(p1)).dot(edge) / edge.length_squared()))
        closest = pygame.Vector2(p1) + t * edge
        if (pygame.Vector2(closest) - pygame.Vector2(circle_center)).length() <= circle_radius:
            return True

    return False
