import pygame
import random

pygame.init()

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = WIN.get_size()
pygame.display.set_caption("Space Dodge")

BG = pygame.image.load("/storage/emulated/0/Pictures/bg.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

try:
    PLAYER_IMG = pygame.image.load("/storage/emulated/0/Pictures/player.png")
    PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (60, 80))
    USE_IMG = True
except:
    USE_IMG = False

try:
    pygame.mixer.init()
    pygame.mixer.music.load("/storage/emulated/0/Xender/audio/7yearsold.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except:
    pass

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
PLAYER_VEL = 8

STAR_WIDTH = 30
STAR_HEIGHT = 30
BASE_STAR_VEL = 6

SHIELD_WIDTH = 40
SHIELD_HEIGHT = 40
SHIELD_DURATION = 300
SHIELD_SPAWN_THRESHOLD = 35

LEFT_BTN = pygame.Rect(30, HEIGHT - 120, 150, 100)
RIGHT_BTN = pygame.Rect(WIDTH - 180, HEIGHT - 120, 150, 100)
PAUSE_BTN = pygame.Rect(WIDTH // 2 - 60, 20, 120, 80)

HIGH_SCORE_FILE = "/storage/emulated/0/spacedodge_highscore.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except:
        pass

def draw_shield_icon(surface, cx, cy, radius, alpha):
    shield_surf = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
    pygame.draw.circle(shield_surf, (0, 200, 255, 60), (radius + 10, radius + 10), radius + 8)
    pygame.draw.circle(shield_surf, (0, 180, 255, alpha), (radius + 10, radius + 10), radius)
    pygame.draw.circle(shield_surf, (255, 255, 255, 80), (radius + 4, radius + 4), radius // 3)
    surface.blit(shield_surf, (cx - radius - 10, cy - radius - 10))

def draw(player, stars, score, lives, high_score, explosions, shield_item, shield_timer, paused):
    WIN.blit(BG, (0, 0))

    for star in stars:
        pygame.draw.rect(WIN, (255, 255, 255), star)

    if shield_item:
        draw_shield_icon(WIN, shield_item.centerx, shield_item.centery, SHIELD_WIDTH // 2, 200)

    for exp in explosions:
        pygame.draw.circle(WIN, exp["color"], exp["pos"], exp["radius"])

    if USE_IMG:
        WIN.blit(PLAYER_IMG, (player.x, player.y))
    else:
        pygame.draw.rect(WIN, "red", player)

    if shield_timer > 0:
        shield_surf = pygame.Surface((PLAYER_WIDTH + 40, PLAYER_HEIGHT + 40), pygame.SRCALPHA)
        pulse = abs(pygame.time.get_ticks() % 600 - 300) / 300
        alpha = int(80 + 80 * pulse)
        pygame.draw.ellipse(shield_surf, (0, 200, 255, alpha), (0, 0, PLAYER_WIDTH + 40, PLAYER_HEIGHT + 40), 4)
        pygame.draw.ellipse(shield_surf, (0, 200, 255, 30), (4, 4, PLAYER_WIDTH + 32, PLAYER_HEIGHT + 32))
        WIN.blit(shield_surf, (player.x - 20, player.y - 20))

    font = pygame.font.SysFont("arial", 50, bold=True)

    pygame.draw.rect(WIN, (100, 100, 255), LEFT_BTN, border_radius=20)
    pygame.draw.rect(WIN, (100, 100, 255), RIGHT_BTN, border_radius=20)
    pygame.draw.rect(WIN, (80, 180, 80) if not paused else (200, 120, 0), PAUSE_BTN, border_radius=20)

    WIN.blit(font.render("<", True, "white"), (LEFT_BTN.x + 50, LEFT_BTN.y + 20))
    WIN.blit(font.render(">", True, "white"), (RIGHT_BTN.x + 50, RIGHT_BTN.y + 20))

    pause_label = "II" if not paused else "▶"
    WIN.blit(font.render(pause_label, True, "white"), (PAUSE_BTN.x + 35, PAUSE_BTN.y + 15))

    WIN.blit(font.render(f"Score: {score}", True, "white"), (10, 120))
    WIN.blit(font.render(f"Lives: {lives}", True, "red"), (10, 175))
    WIN.blit(font.render(f"Best: {high_score}", True, "yellow"), (10, 230))

    if shield_timer > 0:
        bar_width = 200
        bar_height = 18
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 115
        ratio = shield_timer / SHIELD_DURATION
        pygame.draw.rect(WIN, (30, 30, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=9)
        pygame.draw.rect(WIN, (0, 200, 255), (bar_x, bar_y, int(bar_width * ratio), bar_height), border_radius=9)
        label = pygame.font.SysFont("arial", 28, bold=True).render("SHIELD", True, (0, 220, 255))
        WIN.blit(label, (WIDTH // 2 - label.get_width() // 2, bar_y + 22))

    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        WIN.blit(overlay, (0, 0))
        big_font = pygame.font.SysFont("arial", 100, bold=True)
        msg = big_font.render("PAUSED", True, "white")
        WIN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60))

    pygame.display.update()

def show_game_over(score, high_score, new_best):
    """Shows game over screen with replay and quit buttons. Returns True to replay, False to quit."""
    font_big = pygame.font.SysFont("arial", 90, bold=True)
    font_med = pygame.font.SysFont("arial", 55, bold=True)

    replay_btn = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 60, 300, 100)
    quit_btn = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 180, 300, 100)

    while True:
        WIN.blit(BG, (0, 0))

        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        WIN.blit(overlay, (0, 0))

        # Game Over text
        go_text = font_big.render("GAME OVER", True, (255, 60, 60))
        WIN.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 220))

        # Score lines
        if new_best:
            s1 = font_med.render(f"New Best: {high_score}!", True, "yellow")
            WIN.blit(s1, (WIDTH // 2 - s1.get_width() // 2, HEIGHT // 2 - 120))
        else:
            s1 = font_med.render(f"Score: {score}", True, "white")
            s2 = font_med.render(f"Best: {high_score}", True, "yellow")
            WIN.blit(s1, (WIDTH // 2 - s1.get_width() // 2, HEIGHT // 2 - 130))
            WIN.blit(s2, (WIDTH // 2 - s2.get_width() // 2, HEIGHT // 2 - 70))

        # Replay button
        pygame.draw.rect(WIN, (50, 180, 50), replay_btn, border_radius=22)
        r_label = font_med.render("▶  REPLAY", True, "white")
        WIN.blit(r_label, (replay_btn.x + replay_btn.width // 2 - r_label.get_width() // 2,
                            replay_btn.y + replay_btn.height // 2 - r_label.get_height() // 2))

        # Quit button
        pygame.draw.rect(WIN, (180, 50, 50), quit_btn, border_radius=22)
        q_label = font_med.render("✕  QUIT", True, "white")
        WIN.blit(q_label, (quit_btn.x + quit_btn.width // 2 - q_label.get_width() // 2,
                            quit_btn.y + quit_btn.height // 2 - q_label.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.FINGERDOWN:
                fx = int(event.x * WIDTH)
                fy = int(event.y * HEIGHT)
                if replay_btn.collidepoint(fx, fy):
                    return True
                if quit_btn.collidepoint(fx, fy):
                    return False

def main():
    while True:  # outer loop allows replay
        run = True
        clock = pygame.time.Clock()
        move_left = False
        move_right = False
        paused = False

        player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 130, PLAYER_WIDTH, PLAYER_HEIGHT)

        stars = []
        explosions = []
        frame_count = 0
        score = 0
        lives = 3
        high_score = load_high_score()

        shield_item = None
        shield_timer = 0
        shield_spawn_counter = 0

        try:
            pygame.mixer.music.play(-1)
        except:
            pass

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.FINGERDOWN:
                    fx = int(event.x * WIDTH)
                    fy = int(event.y * HEIGHT)
                    if PAUSE_BTN.collidepoint(fx, fy):
                        paused = not paused
                        if paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif not paused:
                        if LEFT_BTN.collidepoint(fx, fy):
                            move_left = True
                        if RIGHT_BTN.collidepoint(fx, fy):
                            move_right = True
                if event.type == pygame.FINGERUP:
                    move_left = False
                    move_right = False

            if paused:
                draw(player, stars, score, lives, high_score, explosions, shield_item, shield_timer, paused)
                continue

            frame_count += 1
            star_vel = BASE_STAR_VEL + score // 8
            spawn_rate = max(8, 25 - score // 4)

            if move_left and player.x > 0:
                player.x -= PLAYER_VEL
            if move_right and player.x < WIDTH - PLAYER_WIDTH:
                player.x += PLAYER_VEL

            if frame_count % spawn_rate == 0:
                count = 1
                if score >= 25:
                    count = random.randint(1, 2)
                if score >= 50:
                    count = random.randint(2, 3)
                for _ in range(count):
                    x = random.randint(0, WIDTH - STAR_WIDTH)
                    stars.append(pygame.Rect(x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT))

            if shield_item is None and shield_timer == 0 and shield_spawn_counter >= SHIELD_SPAWN_THRESHOLD:
                x = random.randint(0, WIDTH - SHIELD_WIDTH)
                shield_item = pygame.Rect(x, -SHIELD_HEIGHT, SHIELD_WIDTH, SHIELD_HEIGHT)
                shield_spawn_counter = 0

            if shield_item:
                shield_item.y += max(3, star_vel - 4)
                if shield_item.y > HEIGHT:
                    shield_item = None
                elif shield_item.colliderect(player):
                    shield_item = None
                    shield_timer = SHIELD_DURATION

            if shield_timer > 0:
                shield_timer -= 1

            for star in stars[:]:
                star.y += star_vel
                if star.y > HEIGHT:
                    stars.remove(star)
                    score += 1
                    shield_spawn_counter += 1
                elif star.colliderect(player):
                    stars.remove(star)
                    if shield_timer > 0:
                        explosions.append({
                            "pos": (star.centerx, star.centery),
                            "radius": 8,
                            "color": (0, 200, 255),
                            "life": 15
                        })
                    else:
                        lives -= 1
                        explosions.append({
                            "pos": (player.centerx, player.centery),
                            "radius": 10,
                            "color": (255, 100, 0),
                            "life": 20
                        })
                        if lives <= 0:
                            pygame.mixer.music.stop()
                            new_best = score > high_score
                            if new_best:
                                high_score = score
                                save_high_score(high_score)
                            run = False

            for exp in explosions[:]:
                exp["radius"] += 5
                exp["life"] -= 1
                if exp["life"] <= 0:
                    explosions.remove(exp)

            draw(player, stars, score, lives, high_score, explosions, shield_item, shield_timer, paused)

        # Show game over screen and check if replay
        replay = show_game_over(score, high_score, new_best)
        if not replay:
            break

    pygame.quit()

if __name__ == "__main__":
    main()