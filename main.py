import pygame 
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player, Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0 # Placeholder for delta time
    clock = pygame.time.Clock()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shot = pygame.sprite.Group()
    Shot.containers = (updateable, drawable)
    AsteroidField.containers = updateable
    Asteroid.containers = (updateable, drawable, asteroids)
    Player.containers = (updateable, drawable)
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        dt = clock.tick(60) / 1000.0
        updateable.update(dt)
        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game Over!")
                pygame.quit()
                return
        for asteroid in asteroids:
            for shot in player.shots:
                if shot.collision(asteroid):
                    asteroid.split()
                    shot.kill()
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.flip()


if __name__ == "__main__": 
    main()