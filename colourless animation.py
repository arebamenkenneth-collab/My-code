import pygame
import math
import sys

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
clock = pygame.time.Clock()

NUM_SEGMENTS = 60
SEGMENT_LEN = 18
RIB_LEN = 22

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

segments = [Segment(w // 2, h // 2) for _ in range(NUM_SEGMENTS)]

def follow(seg, target_x, target_y):
    dx = target_x - seg.x
    dy = target_y - seg.y
    seg.angle = math.atan2(dy, dx)
    dist = math.hypot(dx, dy)
    if dist > SEGMENT_LEN:
        seg.x = target_x - math.cos(seg.angle) * SEGMENT_LEN
        seg.y = target_y - math.sin(seg.angle) * SEGMENT_LEN

mouse_x, mouse_y = w // 2, h // 2

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = e.pos
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((0, 0, 0))

    # Update segments
    follow(segments[0], mouse_x, mouse_y)
    for i in range(1, NUM_SEGMENTS):
        follow(segments[i], segments[i - 1].x, segments[i - 1].y)

    # Draw skeleton
    for i in range(len(segments) - 1):
        s1 = segments[i]
        s2 = segments[i + 1]

        # Spine
        pygame.draw.line(screen, (200, 200, 200),
                         (int(s1.x), int(s1.y)),
                         (int(s2.x), int(s2.y)), 2)

        # Ribs (every other segment)
        if i % 2 == 0:
            rib_scale = RIB_LEN * (1 - i / NUM_SEGMENTS * 0.5)
            perp = s1.angle + math.pi / 2

            # Left rib
            rx1 = s1.x + math.cos(perp) * rib_scale
            ry1 = s1.y + math.sin(perp) * rib_scale
            # Curve tip outward
            rx1 += math.cos(s1.angle - math.pi / 4) * rib_scale * 0.4
            ry1 += math.sin(s1.angle - math.pi / 4) * rib_scale * 0.4
            pygame.draw.line(screen, (180, 180, 180),
                             (int(s1.x), int(s1.y)),
                             (int(rx1), int(ry1)), 1)

            # Right rib
            rx2 = s1.x - math.cos(perp) * rib_scale
            ry2 = s1.y - math.sin(perp) * rib_scale
            rx2 += math.cos(s1.angle - math.pi / 4) * rib_scale * 0.4
            ry2 += math.sin(s1.angle - math.pi / 4) * rib_scale * 0.4
            pygame.draw.line(screen, (180, 180, 180),
                             (int(s1.x), int(s1.y)),
                             (int(rx2), int(ry2)), 1)

        # Joints
        pygame.draw.circle(screen, (220, 220, 220),
                           (int(s1.x), int(s1.y)), 3)

    # Head
    pygame.draw.circle(screen, (255, 255, 255),
                       (int(segments[0].x), int(segments[0].y)), 6)

    pygame.display.flip()
    clock.tick(60)