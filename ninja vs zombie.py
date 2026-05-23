import pygame
from sys import exit
import random
import math

pygame.init()

info = pygame.display.Info()
SW = info.current_w
SH = info.current_h

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Ninja vs Zombies")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

GROUND_Y = SH - 100

# --- Draw Ninja ---
def make_ninja():
    surf = pygame.Surface((80, 120), pygame.SRCALPHA)
    # Legs
    pygame.draw.rect(surf, (20, 20, 80), (18, 75, 18, 40))
    pygame.draw.rect(surf, (20, 20, 80), (44, 75, 18, 40))
    # Boots
    pygame.draw.rect(surf, (10, 10, 10), (14, 105, 22, 15))
    pygame.draw.rect(surf, (10, 10, 10), (44, 105, 22, 15))
    # Body
    pygame.draw.rect(surf, (20, 20, 80), (15, 40, 50, 40))
    # Belt
    pygame.draw.rect(surf, (200, 150, 0), (15, 62, 50, 8))
    # Arms
    pygame.draw.rect(surf, (20, 20, 80), (0, 42, 18, 12))
    pygame.draw.rect(surf, (20, 20, 80), (62, 42, 18, 12))
    # Hands
    pygame.draw.circle(surf, (255, 200, 150), (8, 54), 7)
    pygame.draw.circle(surf, (255, 200, 150), (72, 54), 7)
    # Sword
    pygame.draw.rect(surf, (180, 180, 200), (68, 30, 6, 50))
    pygame.draw.rect(surf, (150, 100, 50), (64, 50, 14, 8))
    # Head
    pygame.draw.circle(surf, (255, 200, 150), (40, 25), 20)
    # Mask
    pygame.draw.rect(surf, (10, 10, 10), (20, 15, 40, 10))
    pygame.draw.rect(surf, (10, 10, 10), (20, 25, 40, 8))
    # Eyes
    pygame.draw.circle(surf, (255, 50, 50), (30, 22), 4)
    pygame.draw.circle(surf, (255, 50, 50), (50, 22), 4)
    # Headband
    pygame.draw.rect(surf, (200, 0, 0), (20, 10, 40, 7))
    return surf

# --- Draw Zombie ---
def make_zombie():
    surf = pygame.Surface((80, 130), pygame.SRCALPHA)
    # Legs
    pygame.draw.rect(surf, (60, 100, 60), (15, 80, 20, 45))
    pygame.draw.rect(surf, (60, 100, 60), (45, 80, 20, 45))
    # Shoes
    pygame.draw.rect(surf, (40, 20, 10), (10, 115, 28, 15))
    pygame.draw.rect(surf, (40, 20, 10), (42, 115, 28, 15))
    # Torn shirt body
    pygame.draw.rect(surf, (80, 120, 80), (12, 38, 56, 46))
    # Tear marks
    pygame.draw.line(surf, (50, 80, 50), (20, 50), (28, 70), 2)
    pygame.draw.line(surf, (50, 80, 50), (50, 45), (44, 68), 2)
    # Arms stretched forward
    pygame.draw.rect(surf, (150, 200, 150), (58, 38, 22, 12))
    pygame.draw.rect(surf, (150, 200, 150), (0, 42, 16, 10))
    # Hands with claws
    pygame.draw.circle(surf, (150, 200, 150), (72, 42), 8)
    pygame.draw.line(surf, (50, 150, 50), (76, 36), (80, 30), 2)
    pygame.draw.line(surf, (50, 150, 50), (72, 34), (74, 27), 2)
    pygame.draw.line(surf, (50, 150, 50), (68, 36), (66, 29), 2)
    # Head
    pygame.draw.circle(surf, (150, 200, 150), (40, 22), 22)
    # Dead eyes
    pygame.draw.circle(surf, (255, 50, 0), (30, 18), 6)
    pygame.draw.circle(surf, (255, 50, 0), (50, 18), 6)
    pygame.draw.circle(surf, (0, 0, 0), (30, 18), 3)
    pygame.draw.circle(surf, (0, 0, 0), (50, 18), 3)
    # X marks on eyes
    pygame.draw.line(surf, (200, 0, 0), (26, 14), (34, 22), 2)
    pygame.draw.line(surf, (200, 0, 0), (34, 14), (26, 22), 2)
    # Mouth
    pygame.draw.arc(surf, (150, 0, 0), (28, 28, 24, 14), math.pi, 2 * math.pi, 3)
    pygame.draw.line(surf, (200, 50, 50), (32, 35), (35, 40), 2)
    pygame.draw.line(surf, (200, 50, 50), (40, 36), (40, 42), 2)
    # Hair messy
    pygame.draw.lines(surf, (30, 20, 10), False,
                      [(22, 5), (20, 0), (28, 6), (30, 0), (38, 4),
                       (40, 0), (50, 5), (55, 0), (58, 6)], 3)
    return surf

# --- Draw Rock obstacle ---
def make_rock():
    surf = pygame.Surface((60, 55), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (120, 100, 80), (0, 15, 60, 40))
    pygame.draw.ellipse(surf, (140, 115, 90), (10, 0, 40, 35))
    pygame.draw.ellipse(surf, (80, 65, 50), (0, 15, 60, 40), 3)
    pygame.draw.ellipse(surf, (80, 65, 50), (10, 0, 40, 35), 3)
    return surf

# --- Draw Background ---
def draw_background():
    # Dark night sky
    screen.fill((10, 10, 30))
    # Moon
    pygame.draw.circle(screen, (240, 240, 200), (SW - 100, 100), 50)
    pygame.draw.circle(screen, (10, 10, 30), (SW - 80, 85), 40)
    # Stars
    for i in range(40):
        x = (i * 173) % SW
        y = (i * 97) % (SH // 2)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)
    # Ground
    pygame.draw.rect(screen, (20, 60, 20), (0, GROUND_Y, SW, SH - GROUND_Y))
    pygame.draw.rect(screen, (30, 80, 30), (0, GROUND_Y, SW, 12))

ninja_surf = make_ninja()
zombie_surf = make_zombie()
rock_surf = make_rock()

def reset_game():
    player_rect = ninja_surf.get_rect(midbottom=(SW // 5, GROUND_Y))
    return player_rect

player_rect = reset_game()
player_gravity = 0
score = 0
high_score = 0
game_active = False
start_time = 0

zombies = []
rocks = []
zombie_timer = 0
rock_timer = 0
flash_timer = 0

play_button_rect = pygame.Rect(SW // 2 - 110, SH // 2 + 60, 220, 70)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.bottom >= GROUND_Y:
                    player_gravity = -30
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_active = True
                    player_rect = reset_game()
                    player_gravity = 0
                    zombies = []
                    rocks = []
                    zombie_timer = 0
                    rock_timer = 0
                    flash_timer = 0
                    start_time = pygame.time.get_ticks()

    if game_active:
        draw_background()

        score = (pygame.time.get_ticks() - start_time) // 1000
        speed = min(4 + score * 0.3, 18)

        # Score display
        score_surf = test_font.render(f'Score: {score}', False, (255, 255, 100))
        score_rect_pos = score_surf.get_rect(center=(SW // 2, 50))
        pygame.draw.rect(screen, (0, 0, 0, 150), score_rect_pos.inflate(20, 10), border_radius=8)
        pygame.draw.rect(screen, (255, 255, 100), score_rect_pos.inflate(20, 10), 2, border_radius=8)
        screen.blit(score_surf, score_rect_pos)

        # Spawn zombies
        zombie_timer += 1
        zombie_spawn = max(80, 200 - score * 4)
        if zombie_timer >= zombie_spawn:
            zrect = zombie_surf.get_rect(bottomleft=(SW + random.randint(0, 200), GROUND_Y))
            zombies.append(zrect)
            zombie_timer = 0

        # Spawn rocks
        rock_timer += 1
        rock_spawn = max(120, 300 - score * 3)
        if rock_timer >= rock_spawn:
            rrect = rock_surf.get_rect(bottomleft=(SW + random.randint(50, 300), GROUND_Y))
            rocks.append(rrect)
            rock_timer = 0

        # Move and draw zombies
        for zrect in zombies:
            zrect.x -= int(speed)
            zrect.bottom = GROUND_Y
            screen.blit(zombie_surf, zrect)
        zombies = [z for z in zombies if z.right > 0]

        # Move and draw rocks
        for rrect in rocks:
            rrect.x -= int(speed) + 2
            rrect.bottom = GROUND_Y
            screen.blit(rock_surf, rrect)
        rocks = [r for r in rocks if r.right > 0]

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= GROUND_Y:
            player_rect.bottom = GROUND_Y
            player_gravity = 0
        screen.blit(ninja_surf, player_rect)

        # Collision
        player_hitbox = player_rect.inflate(-30, -20)
        hit = False
        for zrect in zombies:
            if player_hitbox.colliderect(zrect.inflate(-20, -20)):
                hit = True
        for rrect in rocks:
            if player_hitbox.colliderect(rrect.inflate(-10, -10)):
                hit = True
        if hit:
            if score > high_score:
                high_score = score
            game_active = False

        # Flash red near zombie
        for zrect in zombies:
            if abs(player_rect.centerx - zrect.centerx) < 150:
                pygame.draw.rect(screen, (255, 0, 0, 30),
                                 (0, 0, SW, SH), 12)

    else:
        # Game over / start screen
        screen.fill((10, 10, 30))
        for i in range(40):
            x = (i * 173) % SW
            y = (i * 97) % (SH // 2)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

        title_surf = test_font.render('NINJA VS ZOMBIES', False, (255, 50, 50))
        title_rect = title_surf.get_rect(center=(SW // 2, SH // 4))
        screen.blit(title_surf, title_rect)

        # Show ninja and zombie on menu
        screen.blit(ninja_surf, ninja_surf.get_rect(center=(SW // 2 - 80, SH // 2 - 20)))
        screen.blit(zombie_surf, zombie_surf.get_rect(center=(SW // 2 + 80, SH // 2 - 20)))

        if score > 0:
            final_surf = test_font.render(f'Score: {score}', False, (255, 255, 100))
            final_rect = final_surf.get_rect(center=(SW // 2, SH // 2 + 20))
            screen.blit(final_surf, final_rect)

        if high_score > 0:
            hs_surf = small_font.render(f'Best: {high_score}', False, (100, 255, 100))
            hs_rect = hs_surf.get_rect(center=(SW // 2, SH // 2 + 60))
            screen.blit(hs_surf, hs_rect)

        pygame.draw.rect(screen, (200, 0, 0), play_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 100, 100), play_button_rect, 3, border_radius=12)
        btn_text = test_font.render('PLAY', False, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=play_button_rect.center)
        screen.blit(btn_text, btn_rect)

    pygame.display.update()
    clock.tick(60)