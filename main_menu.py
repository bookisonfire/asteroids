import pygame
from highscores import load_high_scores
import pygame.display

def main_menu(screen, show_fps=False, sound_volume=1.0, fullscreen=True):
    big_font = pygame.font.SysFont("Arial", 100)
    medium_font = pygame.font.SysFont("Arial", 60)
    small_font = pygame.font.SysFont("Arial", 30)
    button_font = pygame.font.SysFont("Arial", 40)

    # Title lines (centered at the top)
    title_text = medium_font.render("Welcome", True, "white")
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 60))
    intro_text = small_font.render("to David's", True, "white")
    intro_rect = intro_text.get_rect(center=(screen.get_width() // 2, 120))
    game_title_text = big_font.render("Asteroids", True, "white")
    game_title_rect = game_title_text.get_rect(center=(screen.get_width() // 2, 200))

    # Buttons/settings on the left
    button_y_start = 300
    button_spacing = 80
    left_x = 180
    right_x = screen.get_width() - 280
    button_width = 200
    button_height = 60
    play_button = pygame.Rect(
        (screen.get_width() - button_width) // 2,
        button_y_start,
        button_width,
        button_height
    )
    quit_button = pygame.Rect(
        (screen.get_width() - button_width) // 2,
        button_y_start + button_spacing,
        button_width,
        button_height
    )

    # Settings area on the left, formatted as a vertical list
    settings_left = 80
    settings_top = button_y_start
    settings_gap = 70
    square_size = 32
    toggle_gap = 18  # a bit more gap for clarity
    label_width = max(
        button_font.size("Show FPS:")[0],
        button_font.size("Sound: 100%") [0],
        button_font.size("Toggle Fullscreen:")[0]
    )
    control_x = settings_left + label_width + toggle_gap

    # FPS toggle rect and position
    fps_label = button_font.render("Show FPS:", True, "white")
    fps_label_x = settings_left + label_width - fps_label.get_width()
    fps_label_y = settings_top
    fps_square_x = control_x
    fps_square_y = fps_label_y + (fps_label.get_height() - square_size) // 2
    fps_toggle = pygame.Rect(fps_square_x, fps_square_y, square_size, square_size)

    # Sound slider rect and position
    sound_label = button_font.render(f"Sound: {int(sound_volume * 100)}%", True, "white")
    sound_label_x = settings_left + label_width - sound_label.get_width()
    sound_label_y = fps_label_y + settings_gap
    sound_bar_x = control_x
    sound_bar_y = sound_label_y + (sound_label.get_height() - 32) // 2
    sound_bar_width = 180
    sound_bar_height = 32
    sound_toggle = pygame.Rect(sound_bar_x, sound_bar_y, sound_bar_width, sound_bar_height)

    # Fullscreen toggle rect and position
    fullscreen_label = button_font.render("Toggle Fullscreen:", True, "white")
    fullscreen_label_x = settings_left + label_width - fullscreen_label.get_width()
    fullscreen_label_y = sound_label_y + settings_gap
    fullscreen_square_x = control_x
    fullscreen_square_y = fullscreen_label_y + (fullscreen_label.get_height() - square_size) // 2
    fullscreen_toggle = pygame.Rect(fullscreen_square_x, fullscreen_square_y, square_size, square_size)

    # High scores on the right
    high_scores = load_high_scores()
    score_title = medium_font.render("High Scores:", True, "white")
    score_title_rect = score_title.get_rect(midtop=(right_x, button_y_start))
    high_score_texts = []
    for i, (score, date) in enumerate(high_scores):
        hs_text = small_font.render(f"{i+1}: {score} ({date})", True, "white")
        hs_rect = hs_text.get_rect(midtop=(right_x, button_y_start + 100 + i * 40))
        high_score_texts.append((hs_text, hs_rect))

    # Use the passed-in values as initial state
    show_fps = bool(show_fps)
    sound_volume = float(sound_volume)
    fullscreen = bool(fullscreen)

    while True:
        screen.fill("black")
        # Centered titles
        screen.blit(title_text, title_rect)
        screen.blit(intro_text, intro_rect)
        screen.blit(game_title_text, game_title_rect)

        # Left buttons/settings
        pygame.draw.rect(screen, (100, 200, 100), play_button)
        pygame.draw.rect(screen, (200, 100, 100), quit_button)
        play_text = button_font.render("Play", True, "white")
        quit_text = button_font.render("Quit", True, "white")
        screen.blit(play_text, play_text.get_rect(center=play_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        # FPS toggle
        pygame.draw.rect(screen, (50, 50, 50), fps_toggle)
        color = (120, 220, 120) if show_fps else (220, 120, 120)
        pygame.draw.rect(screen, color, fps_toggle, border_radius=8)
        screen.blit(fps_label, (fps_label_x, fps_label_y))
        state_label = small_font.render("On" if show_fps else "Off", True, "white")
        state_x = fps_square_x + (square_size - state_label.get_width()) // 2
        state_y = fps_square_y + square_size + 6
        screen.blit(state_label, (state_x, state_y))

        # Sound slider
        pygame.draw.rect(screen, (50, 50, 50), sound_toggle)
        fill_width = int(sound_toggle.width * sound_volume)
        fill_rect = pygame.Rect(sound_toggle.left, sound_toggle.top, fill_width, sound_toggle.height)
        pygame.draw.rect(screen, (100, 200, 100), fill_rect)
        pygame.draw.rect(screen, "white", sound_toggle, 2)
        screen.blit(sound_label, (sound_label_x, sound_label_y))

        # Fullscreen toggle
        pygame.draw.rect(screen, (50, 50, 50), fullscreen_toggle)
        color = (120, 220, 120) if fullscreen else (220, 120, 120)
        pygame.draw.rect(screen, color, fullscreen_toggle, border_radius=8)
        screen.blit(fullscreen_label, (fullscreen_label_x, fullscreen_label_y))
        state_label = small_font.render("On" if fullscreen else "Off", True, "white")
        state_x = fullscreen_square_x + (square_size - state_label.get_width()) // 2
        state_y = fullscreen_square_y + square_size + 6
        screen.blit(state_label, (state_x, state_y))

        # Right high scores
        screen.blit(score_title, score_title_rect)
        for hs_text, hs_rect in high_score_texts:
            screen.blit(hs_text, hs_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", show_fps, sound_volume, fullscreen
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    return "play", show_fps, sound_volume, fullscreen
                if quit_button.collidepoint(event.pos):
                    return "quit", show_fps, sound_volume, fullscreen
                if fps_toggle.collidepoint(event.pos):
                    show_fps = not show_fps
                if sound_toggle.collidepoint(event.pos):
                    # Set volume based on click position
                    rel_x = event.pos[0] - sound_toggle.left
                    sound_volume = min(max(rel_x / sound_toggle.width, 0.0), 1.0)
                if fullscreen_toggle.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    # Instantly change window mode
                    
                    if fullscreen:
                        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280, 720))
                    # Recompute rects for new screen size
                    left_x = 180
                    right_x = screen.get_width() - 280
                    play_button = pygame.Rect(
                        (screen.get_width() - button_width) // 2,
                        button_y_start,
                        button_width,
                        button_height
                    )
                    quit_button = pygame.Rect(
                        (screen.get_width() - button_width) // 2,
                        button_y_start + button_spacing,
                        button_width,
                        button_height
                    )
                    fps_toggle = pygame.Rect(fps_square_x, fps_square_y, square_size, square_size)
                    sound_toggle = pygame.Rect(sound_bar_x, sound_bar_y, sound_bar_width, sound_bar_height)
                    fullscreen_toggle = pygame.Rect(fullscreen_square_x, fullscreen_square_y, square_size, square_size)
                    score_title_rect = score_title.get_rect(midtop=(right_x, button_y_start))
                    high_score_texts = []
                    for i, (score, date) in enumerate(high_scores):
                        hs_text = small_font.render(f"{i+1}: {score} ({date})", True, "white")
                        hs_rect = hs_text.get_rect(midtop=(right_x, button_y_start + 100 + i * 40))
                        high_score_texts.append((hs_text, hs_rect))
            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if sound_toggle.collidepoint(event.pos):
                    rel_x = event.pos[0] - sound_toggle.left
                    sound_volume = min(max(rel_x / sound_toggle.width, 0.0), 1.0)
