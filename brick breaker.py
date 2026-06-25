import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
ORANGE = (255, 140, 0)
RED = (255, 60, 60)
GREEN = (60, 255, 100)
YELLOW = (255, 230, 0)
GRAY = (180, 180, 180)

# Paddle
paddle_w, paddle_h = 90, 14
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - 50, paddle_w, paddle_h)
paddle_speed = 0

# Ball
ball = pygame.Rect(WIDTH // 2 - 8, HEIGHT // 2, 16, 16)
ball_dx, ball_dy = 4, -4

# Bricks
ROWS, COLS = 5, 7
brick_w = WIDTH // COLS - 4
brick_h = 22
bricks = []
brick_colors = [RED, ORANGE, YELLOW, GREEN, CYAN]
for r in range(ROWS):
    for c in range(COLS):
        bx = c * (brick_w + 4) + 2
        by = r * (brick_h + 6) + 60
        bricks.append(pygame.Rect(bx, by, brick_w, brick_h))

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

score = 0
lives = 3
game_over = False
won = False
clock = pygame.time.Clock()

def reset_ball():
    ball.x = WIDTH // 2 - 8
    ball.y = HEIGHT // 2
    return 4, -4

while True:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
            tx = int(event.x * WIDTH)
            paddle.x = tx - paddle_w // 2
            paddle.x = max(0, min(WIDTH - paddle_w, paddle.x))

    if not game_over and not won:
        # Move ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall bounce
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx *= -1
        if ball.top <= 0:
            ball_dy *= -1

        # Paddle bounce
        if ball.colliderect(paddle) and ball_dy > 0:
            ball_dy *= -1
            offset = (ball.centerx - paddle.centerx) / (paddle_w / 2)
            ball_dx = int(offset * 5)
            if ball_dx == 0:
                ball_dx = 1

        # Ball falls
        if ball.top > HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                ball_dx, ball_dy = reset_ball()

        # Brick collision
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy *= -1
                score += 10
                break

        if not bricks:
            won = True

    # Draw bricks
    for i, brick in enumerate(bricks):
        row = (brick.y - 60) // (brick_h + 6)
        color = brick_colors[row % len(brick_colors)]
        pygame.draw.rect(screen, color, brick, border_radius=4)
        pygame.draw.rect(screen, BLACK, brick, 1, border_radius=4)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, paddle, border_radius=7)

    # Draw ball
    pygame.draw.ellipse(screen, CYAN, ball)

    # HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 110, 10))

    # Game Over / Win screen
    if game_over:
        msg = font.render("GAME OVER!", True, RED)
        sub = small_font.render(f"Score: {score}", True, GRAY)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 30))

    if won:
        msg = font.render("YOU WIN! 🎉", True, GREEN)
        sub = small_font.render(f"Score: {score}", True, GRAY)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 30))

    pygame.display.flip()