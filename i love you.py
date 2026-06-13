import pygame
import math
import random

pygame.init()

info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Programmed Love")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14, bold=True)

# Heart shape formula
def heart_point(t, scale=1):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
    return x * scale, y * scale

# Generate heart points
NUM_POINTS = 120
scale = min(W, H) // 28
heart_pts = [heart_point(2 * math.pi * i / NUM_POINTS, scale) for i in range(NUM_POINTS)]

# Spawn text particles along the heart
particles = []
for i, (hx, hy) in enumerate(heart_pts):
    particles.append({
        "x": W // 2 + hx,
        "y": H // 2 + hy,
        "alpha": 0,
        "delay": i * 3,  # stagger appearance
        "phase": random.uniform(0, 2 * math.pi),
    })

texts = ["I love you", "I love you", "I love you"]
colors = [(255, 80, 120), (255, 150, 170), (200, 50, 90), (255, 200, 210)]

tick = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.FINGERDOWN:
            running = False

    screen.fill((0, 0, 0))
    tick += 1

    for i, p in enumerate(particles):
        if tick < p["delay"]:
            continue

        # Fade in
        if p["alpha"] < 255:
            p["alpha"] = min(255, p["alpha"] + 4)

        # Pulse effect
        pulse = math.sin(tick * 0.05 + p["phase"]) * 0.3 + 0.7
        alpha = int(p["alpha"] * pulse)

        color = colors[i % len(colors)]
        label = texts[i % len(texts)]
        surf = font.render(label, True, color)
        surf.set_alpha(alpha)

        # Slight float animation
        offset_y = math.sin(tick * 0.03 + p["phase"]) * 3
        screen.blit(surf, (int(p["x"]) - surf.get_width() // 2,
                           int(p["y"] + offset_y) - surf.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()