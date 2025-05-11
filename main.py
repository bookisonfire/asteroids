import pygame 
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player, Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    game_over_font = pygame.font.SysFont("Arial", 75)
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
    score = pygame.sprite.Group()
    score.containers = (updateable, drawable)
    Shot.containers = (updateable, drawable)
    AsteroidField.containers = updateable
    Asteroid.containers = (updateable, drawable, asteroids)
    Player.containers = (updateable, drawable)
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    score = 0

    while True:
        dt = clock.tick(60) / 1000.0
        updateable.update(dt)
        for asteroid in asteroids:
            if player.collision(asteroid):
                screen.fill("black")
                screen.blit(game_over_text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.quit()
                return
        for asteroid in asteroids:
            for shot in player.shots:
                if shot.collision(asteroid):
                    asteroid.split()
                    shot.kill()
                    score += 1
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        score_text = font.render(f"Score: {score}", True, "white")
        game_over_text = game_over_font.render("Game Over!", True, "white")
        text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(score_text, (10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.flip()


if __name__ == "__main__": 
    main()