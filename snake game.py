import pygame
import random
import sys

pygame.init()

info = pygame.display.Info()
SW, SH = info.current_w, info.current_h
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake")

BLACK   = (0, 0, 0)
GREEN   = (0, 200, 0)
DKGREEN = (0, 140, 0)
RED     = (220, 30, 30)
WHITE   = (255, 255, 255)
GRAY    = (100, 100, 100)
DGRAY   = (60, 60, 60)

CELL = max(16, SW // 22)
COLS = SW // CELL
ROWS = SH // CELL

FPS   = 10
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont(None, int(SH * 0.07))
font_small = pygame.font.SysFont(None, int(SH * 0.04))

class Button:
    def __init__(self, cx, cy, r, label):
        self.cx    = cx
        self.cy    = cy
        self.r     = r
        self.label = label

    def draw(self, surf):
        pygame.draw.circle(surf, GRAY, (self.cx, self.cy), self.r)
        pygame.draw.circle(surf, DGRAY, (self.cx, self.cy), self.r, 3)
        txt = font_big.render(self.label, True, WHITE)
        surf.blit(txt, txt.get_rect(center=(self.cx, self.cy)))

    def is_pressed(self, x, y):
        return (x - self.cx)**2 + (y - self.cy)**2 <= self.r**2


def random_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def game_loop():
    snake     = [(COLS // 2, ROWS // 2),
                 (COLS // 2 - 1, ROWS // 2),
                 (COLS // 2 - 2, ROWS // 2)]
    direction = (1, 0)
    next_dir  = (1, 0)
    food      = random_food(snake)
    score     = 0
    alive     = True

    btn_r     = int(SW * 0.09)
    btn_x     = int(SW * 0.13)
    btn_plus  = Button(btn_x, SH // 2 - btn_r - 10, btn_r, "+")
    btn_minus = Button(btn_x, SH // 2 + btn_r + 10, btn_r, "-")

    dir_order = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def turn(cw):
        nonlocal next_dir
        idx      = dir_order.index(direction)
        next_dir = dir_order[(idx + (1 if cw else -1)) % 4]

    move_timer = 0
    move_delay = 1000 // FPS
    last_time  = pygame.time.get_ticks()

    while True:
        now       = pygame.time.get_ticks()
        dt        = now - last_time
        last_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.FINGERDOWN:
                tx = int(event.x * SW)
                ty = int(event.y * SH)
                if btn_plus.is_pressed(tx, ty):
                    turn(False)
                elif btn_minus.is_pressed(tx, ty):
                    turn(True)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_dir = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_dir = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_dir = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        move_timer += dt
        if alive and move_timer >= move_delay:
            move_timer = 0
            direction  = next_dir
            head       = (snake[0][0] + direction[0],
                          snake[0][1] + direction[1])

            if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
                alive = False
            elif head in snake:
                alive = False
            else:
                snake.insert(0, head)
                if head == food:
                    score += 10
                    food   = random_food(snake)
                else:
                    snake.pop()

        screen.fill(BLACK)

        for c in range(COLS + 1):
            pygame.draw.line(screen, (15, 15, 15), (c * CELL, 0), (c * CELL, SH))
        for r in range(ROWS + 1):
            pygame.draw.line(screen, (15, 15, 15), (0, r * CELL), (SW, r * CELL))

        fx = food[0] * CELL + 3
        fy = food[1] * CELL + 3
        pygame.draw.rect(screen, RED, (fx, fy, CELL - 6, CELL - 6))

        for i, seg in enumerate(snake):
            color = GREEN if i == 0 else DKGREEN
            rx    = seg[0] * CELL + 1
            ry    = seg[1] * CELL + 1
            pygame.draw.rect(screen, color,
                             (rx, ry, CELL - 2, CELL - 2),
                             border_radius=3 if i == 0 else 1)

        score_surf = font_small.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_surf,
                    (SW // 2 - score_surf.get_width() // 2, 10))

        if alive:
            btn_plus.draw(screen)
            btn_minus.draw(screen)

        if not alive:
            overlay = pygame.Surface((SW, SH), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            go_txt = font_big.render("GAME OVER", True, RED)
            sc_txt = font_small.render(f"Score: {score}", True, WHITE)
            re_txt = font_small.render("Tap screen to restart", True, GRAY)

            screen.blit(go_txt, go_txt.get_rect(center=(SW // 2, SH // 2 - 50)))
            screen.blit(sc_txt, sc_txt.get_rect(center=(SW // 2, SH // 2 + 10)))
            screen.blit(re_txt, re_txt.get_rect(center=(SW // 2, SH // 2 + 55)))

            for event in pygame.event.get():
                if event.type in (pygame.FINGERDOWN,
                                  pygame.MOUSEBUTTONDOWN,
                                  pygame.KEYDOWN):
                    return

        pygame.display.flip()
        clock.tick(60)


while True:
    game_loop()