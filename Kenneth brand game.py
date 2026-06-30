"""
CodeWithKenneth presents: SKY DODGER (Mobile Edition)
Touch-controlled endless dodging game for Pydroid 3 on Android.
No image files needed - everything is drawn with code.

Controls (TOUCH):
  Drag finger anywhere   -> move player left/right
  Tap screen             -> restart after game over

Brand: CodeWithKenneth (orange & white theme)
"""

import pygame
import random
import sys
import math

pygame.init()

# ---------- CONFIG ----------
# Auto-fit to phone screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

ORANGE = (255, 122, 0)
DARK_ORANGE = (204, 87, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BG_TOP = (25, 25, 35)
BG_BOTTOM = (45, 25, 10)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CodeWithKenneth - Sky Dodger")
clock = pygame.time.Clock()

# Scale fonts/sizes relative to screen width so it looks right on any phone
SCALE = WIDTH / 480

font_big = pygame.font.SysFont("arial", int(48 * SCALE), bold=True)
font_med = pygame.font.SysFont("arial", int(28 * SCALE), bold=True)
font_small = pygame.font.SysFont("arial", int(18 * SCALE))


# ---------- HELPERS ----------
def draw_vertical_gradient(surface, top_color, bottom_color):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = top_color[0] + (bottom_color[0] - top_color[0]) * t
        g = top_color[1] + (bottom_color[1] - top_color[1]) * t
        b = top_color[2] + (bottom_color[2] - top_color[2]) * t
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, 1.5) * SCALE
        self.vy = random.uniform(-1.5, 0.5) * SCALE
        self.life = random.randint(15, 30)
        self.max_life = self.life
        self.color = color
        self.size = random.randint(2, 5) * SCALE

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = max(1, int(self.size * alpha))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)


class Player:
    def __init__(self):
        self.w, self.h = int(40 * SCALE), int(40 * SCALE)
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - int(150 * SCALE)
        self.target_x = self.x
        self.speed = 0.25  # smoothing factor for touch follow
        self.particles = []

    def update(self, touch_x):
        if touch_x is not None:
            self.target_x = touch_x - self.w / 2

        self.target_x = max(0, min(WIDTH - self.w, self.target_x))
        # smooth glide toward finger position
        self.x += (self.target_x - self.x) * self.speed

        cx = self.x + self.w / 2
        cy = self.y + self.h
        self.particles.append(Particle(cx, cy, ORANGE))
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
        r = self.rect()
        pygame.draw.rect(surface, ORANGE, r, border_radius=int(10 * SCALE))
        pygame.draw.rect(surface, WHITE, r, width=max(2, int(3 * SCALE)), border_radius=int(10 * SCALE))
        logo = font_small.render("K", True, WHITE)
        surface.blit(logo, (r.centerx - logo.get_width() // 2, r.centery - logo.get_height() // 2))


class Obstacle:
    def __init__(self, speed):
        self.size = random.randint(int(28 * SCALE), int(55 * SCALE))
        self.x = random.randint(0, max(1, WIDTH - self.size))
        self.y = -self.size
        self.speed = speed
        self.rot = 0
        self.rot_speed = random.uniform(-4, 4)
        self.shape = random.choice(["circle", "square"])

    def update(self):
        self.y += self.speed

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        cx, cy = self.x + self.size / 2, self.y + self.size / 2
        if self.shape == "circle":
            pygame.draw.circle(surface, DARK_ORANGE, (int(cx), int(cy)), self.size // 2)
            pygame.draw.circle(surface, BLACK, (int(cx), int(cy)), self.size // 2, 2)
        else:
            pts = []
            half = self.size / 2
            for ang in (45, 135, 225, 315):
                rad = math.radians(ang + self.rot)
                pts.append((cx + half * math.cos(rad), cy + half * math.sin(rad)))
            pygame.draw.polygon(surface, BLACK, pts)
            pygame.draw.polygon(surface, DARK_ORANGE, pts, 0)
            pygame.draw.polygon(surface, WHITE, pts, 2)


def draw_text_center(surface, text, font, color, y, shake=(0, 0)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2 + shake[0], y + shake[1]))
    surface.blit(img, rect)


def main():
    player = Player()
    obstacles = []
    spawn_timer = 0
    spawn_delay = 45
    obstacle_speed = 4.0 * SCALE
    score = 0
    game_over = False
    shake_amount = 0
    touch_x = None
    finger_down = False

    bg = pygame.Surface((WIDTH, HEIGHT))
    draw_vertical_gradient(bg, BG_TOP, BG_BOTTOM)

    running = True
    while running:
        clock.tick(60)
        shake = (0, 0)
        if shake_amount > 0:
            shake = (random.randint(-int(shake_amount), int(shake_amount)),
                      random.randint(-int(shake_amount), int(shake_amount)))
            shake_amount *= 0.85
            if shake_amount < 0.5:
                shake_amount = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- Touch events (Pydroid 3 / Android) ---
            elif event.type == pygame.FINGERDOWN:
                finger_down = True
                touch_x = event.x * WIDTH
                if game_over:
                    return main()  # tap to restart
            elif event.type == pygame.FINGERMOTION:
                touch_x = event.x * WIDTH
            elif event.type == pygame.FINGERUP:
                finger_down = False

            # --- Mouse fallback (so it also works testing on PC) ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                finger_down = True
                touch_x = event.pos[0]
                if game_over:
                    return main()
            elif event.type == pygame.MOUSEMOTION and finger_down:
                touch_x = event.pos[0]
            elif event.type == pygame.MOUSEBUTTONUP:
                finger_down = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and game_over:
                    return main()

        if not game_over:
            player.update(touch_x if finger_down else None)

            spawn_timer += 1
            if spawn_timer >= spawn_delay:
                spawn_timer = 0
                obstacles.append(Obstacle(obstacle_speed))

            for obs in obstacles:
                obs.update()
            obstacles = [o for o in obstacles if o.y < HEIGHT + 60]

            for obs in obstacles[:]:
                if obs.rect().colliderect(player.rect()):
                    game_over = True
                    shake_amount = 18 * SCALE

            score += 1
            if score % 300 == 0:
                obstacle_speed += 0.6 * SCALE
                spawn_delay = max(18, spawn_delay - 3)

        # ---------- DRAW ----------
        screen.blit(bg, (0, 0))
        pygame.draw.line(screen, WHITE, (0, HEIGHT - int(60 * SCALE)), (WIDTH, HEIGHT - int(60 * SCALE)), 2)

        for obs in obstacles:
            obs.draw(screen)
        player.draw(screen)

        hud = font_med.render(f"Score: {score // 5}", True, WHITE)
        screen.blit(hud, (int(15 * SCALE), int(15 * SCALE)))
        brand = font_small.render("CodeWithKenneth", True, ORANGE)
        screen.blit(brand, (WIDTH - brand.get_width() - int(15 * SCALE), int(20 * SCALE)))

        if not game_over and score < 30:
            # quick onboarding hint for first half-second
            draw_text_center(screen, "Drag finger to move", font_small, WHITE, int(HEIGHT * 0.6))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            draw_text_center(screen, "GAME OVER", font_big, ORANGE, HEIGHT // 2 - int(60 * SCALE), shake)
            draw_text_center(screen, f"Score: {score // 5}", font_med, WHITE, HEIGHT // 2, shake)
            draw_text_center(screen, "Tap screen to retry", font_small, WHITE, HEIGHT // 2 + int(50 * SCALE), shake)
            draw_text_center(screen, "@CodeWithKenneth - Learn Python on your phone!",
                              font_small, ORANGE, HEIGHT // 2 + int(90 * SCALE), shake)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()