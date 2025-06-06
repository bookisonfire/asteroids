import pygame 
import random
from player import Player, Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from main_menu import main_menu
from highscores import save_high_score, load_high_scores

def game_over(screen, game_over_text, final_score_text, final_score_rect, text_rect):
    screen.blit(game_over_text, text_rect)
    screen.blit(final_score_text, final_score_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()


def main(score=0, lives=3, show_fps=False, sound_on=True, fullscreen=True):
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    font = pygame.font.SysFont("Arial", 35)
    game_over_font = pygame.font.SysFont("Arial", 75)
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    if fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1200, 900))
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
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, sound_volume=sound_on)
    pygame.mixer.music.set_volume(sound_on)
    asteroid_field = AsteroidField(SCREEN_WIDTH, SCREEN_HEIGHT)
    background_image = pygame.image.load("assets/background.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    heart_image = pygame.image.load("assets/heart.png")
    heart_image = pygame.transform.scale(heart_image, (55, 55))
    score_text = font.render(f"Score: {score}", True, "white")
    game_over_text = game_over_font.render("Game Over!", True, "white")
    final_score_text = font.render(f"Final Score: {score}", True, "white")
    final_score_rect = final_score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    while True:
        dt = clock.tick(60) / 1000.0
        updateable.update(dt)
        for asteroid in asteroids:    
            if not player.invulnerable and player.collision(asteroid):
                lives -= 1
                if lives >= 1:
                    player.respawn()
                else:
                    save_high_score(score)
                    final_score_text = font.render(f"Final Score: {score}", True, "white")
                    final_score_rect = final_score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
                    result = game_over_menu(screen, game_over_text, final_score_text, final_score_rect, text_rect)
                    if result == "restart":
                        return "restart"
                    elif result == "quit":
                        return "main_menu"
        for asteroid in asteroids:
            for shot in player.shots:
                if shot.collision(asteroid):
                    asteroid.split(drawable, updateable)
                    shot.kill()
                    score += 1
        window_width, window_height = screen.get_size()
        scaled_bg = pygame.transform.scale(background_image, (window_width, window_height))
        screen.blit(scaled_bg, (0, 0))
        for sprite in drawable:
            sprite.draw(screen)
        # Draw explosions last (if any)
        for sprite in drawable:
            if hasattr(sprite, 'alpha'):
                sprite.draw(screen)
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        for i in range(lives):
            x = screen.get_width() - (i + 1) * heart_image.get_width() - 10
            screen.blit(heart_image, (x, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                result = pause_menu(screen, score, font)
                if result == "resume":
                    continue  # Resume game
                elif result == "restart":
                    return "restart"
                elif result == "quit":
                    pygame.quit()
                    return
        if show_fps:
            fps = int(clock.get_fps())
            fps_font = pygame.font.SysFont("Arial", 30)
            fps_text = fps_font.render(f"FPS: {fps}", True, "yellow")
            screen.blit(fps_text, (10, 50))
        pygame.display.flip()

def pause_menu(screen, score, font):
    pause_font = pygame.font.SysFont("Arial", 75)
    menu_font = pygame.font.SysFont("Arial", 40)
    pause_text = pause_font.render("Paused", True, "white")
    score_text = font.render(f"Score: {score}", True, "white")
    pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    button_y = screen.get_height() // 2 + 60
    resume_button = pygame.Rect(screen.get_width() // 2 - 200, button_y, 120, 50)
    restart_button = pygame.Rect(screen.get_width() // 2 - 60, button_y, 120, 50)
    quit_button = pygame.Rect(screen.get_width() // 2 + 80, button_y, 120, 50)
    while True:
        screen.fill("black")
        screen.blit(pause_text, pause_rect)
        screen.blit(score_text, score_rect)
        pygame.draw.rect(screen, (100, 200, 100), resume_button)
        pygame.draw.rect(screen, (100, 100, 200), restart_button)
        pygame.draw.rect(screen, (200, 100, 100), quit_button)
        resume_text = menu_font.render("Resume", True, "white")
        restart_text = menu_font.render("Restart", True, "white")
        quit_text = menu_font.render("Quit", True, "white")
        screen.blit(resume_text, resume_text.get_rect(center=resume_button.center))
        screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.collidepoint(event.pos):
                    return "resume"
                elif restart_button.collidepoint(event.pos):
                    return "restart"
                elif quit_button.collidepoint(event.pos):
                    return "quit"

def game_over_menu(screen, game_over_text, final_score_text, final_score_rect, text_rect):
    from highscores import load_high_scores
    font = pygame.font.SysFont("Arial", 40)
    score_font = pygame.font.SysFont("Arial", 30)

    # Centered at the top
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, 80))
    final_score_rect = final_score_text.get_rect(center=(screen.get_width() // 2, 150))

    # Buttons on the left
    button_y_start = 250
    button_spacing = 80
    restart_button = pygame.Rect(100, button_y_start, 200, 60)
    quit_button = pygame.Rect(100, button_y_start + button_spacing, 200, 60)

    # High scores on the right
    high_scores = load_high_scores(limit=3)
    score_title = score_font.render("High Scores:", True, "white")
    score_title_rect = score_title.get_rect(midtop=(screen.get_width() - 200, button_y_start))
    high_score_texts = []
    for i, (score, date) in enumerate(high_scores):
        hs_text = score_font.render(f"{i+1}: {score} ({date})", True, "white")
        hs_rect = hs_text.get_rect(midtop=(screen.get_width() - 200, button_y_start + 50 + i * 40))
        high_score_texts.append((hs_text, hs_rect))

    while True:
        screen.fill("black")
        # Centered top
        screen.blit(game_over_text, game_over_rect)
        screen.blit(final_score_text, final_score_rect)

        # Left buttons
        pygame.draw.rect(screen, (100, 200, 100), restart_button)
        pygame.draw.rect(screen, (200, 100, 100), quit_button)
        restart_text = font.render("Restart", True, "white")
        quit_text = font.render("Quit", True, "white")
        screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        # Right high scores
        screen.blit(score_title, score_title_rect)
        for hs_text, hs_rect in high_score_texts:
            screen.blit(hs_text, hs_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    return "restart"
                if quit_button.collidepoint(event.pos):
                    return "quit"


if __name__ == "__main__": 
    pygame.init()
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    fullscreen = True
    show_fps = False
    sound_volume = 1.0
    while True:
        # Loop to allow immediate fullscreen/windowed changes in the menu
        prev_fullscreen = None
        while prev_fullscreen != fullscreen:
            prev_fullscreen = fullscreen
            if fullscreen:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((1200, 900))
            menu_result = main_menu(screen, show_fps=show_fps, sound_volume=sound_volume, fullscreen=fullscreen)
            # Update settings from menu
            _, show_fps, sound_volume, fullscreen = menu_result
        if menu_result[0] == "play":
            result = main(show_fps=show_fps, sound_on=sound_volume, fullscreen=fullscreen)
            if result == "main_menu":
                continue  # Go back to main menu
            if result != "restart":
                break
        else:
            break