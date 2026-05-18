import pygame
import math
import sys

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
clock = pygame.time.Clock()

NUM_SEGMENTS = 80
SEGMENT_LEN = 25
RIB_LEN = 45

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

def rainbow_color(index, total):
    hue = (index / total) * 360
    h = hue / 60
    x = 1 - abs(h % 2 - 1)
    if h < 1: r, g, b = 1, x, 0
    elif h < 2: r, g, b = x, 1, 0
    elif h < 3: r, g, b = 0, 1, x
    elif h < 4: r, g, b = 0, x, 1
    elif h < 5: r, g, b = x, 0, 1
    else: r, g, b = 1, 0, x
    return (int(r * 255), int(g * 255), int(b * 255))

mouse_x, mouse_y = w // 2, h // 2
color_offset = 0

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
    color_offset = (color_offset + 1) % NUM_SEGMENTS

    # Update segments
    follow(segments[0], mouse_x, mouse_y)
    for i in range(1, NUM_SEGMENTS):
        follow(segments[i], segments[i - 1].x, segments[i - 1].y)

    # Draw skeleton
    for i in range(len(segments) - 1):
        s1 = segments[i]
        s2 = segments[i + 1]

        color = rainbow_color((i + color_offset) % NUM_SEGMENTS, NUM_SEGMENTS)
        dim_color = tuple(c // 2 for c in color)

        # Spine
        pygame.draw.line(screen, color,
                         (int(s1.x), int(s1.y)),
                         (int(s2.x), int(s2.y)), 4)

        # Ribs every other segment
        if i % 2 == 0:
            rib_scale = RIB_LEN * (1 - i / NUM_SEGMENTS * 0.5)
            perp = s1.angle + math.pi / 2

            # Left rib
            rx1 = s1.x + math.cos(perp) * rib_scale
            ry1 = s1.y + math.sin(perp) * rib_scale
            rx1 += math.cos(s1.angle - math.pi / 4) * rib_scale * 0.5
            ry1 += math.sin(s1.angle - math.pi / 4) * rib_scale * 0.5
            pygame.draw.line(screen, dim_color,
                             (int(s1.x), int(s1.y)),
                             (int(rx1), int(ry1)), 2)

            # Right rib
            rx2 = s1.x - math.cos(perp) * rib_scale
            ry2 = s1.y - math.sin(perp) * rib_scale
            rx2 += math.cos(s1.angle - math.pi / 4) * rib_scale * 0.5
            ry2 += math.sin(s1.angle - math.pi / 4) * rib_scale * 0.5
            pygame.draw.line(screen, dim_color,
                             (int(s1.x), int(s1.y)),
                             (int(rx2), int(ry2)), 2)

        # Joints
        pygame.draw.circle(screen, color,
                           (int(s1.x), int(s1.y)), 5)

    # Head
    head_color = rainbow_color(color_offset % NUM_SEGMENTS, NUM_SEGMENTS)
    pygame.draw.circle(screen, head_color,
                       (int(segments[0].x), int(segments[0].y)), 12)
    # Eyes
    eye_offset = segments[0].angle
    ex1 = int(segments[0].x + math.cos(eye_offset + 0.5) * 8)
    ey1 = int(segments[0].y + math.sin(eye_offset + 0.5) * 8)
    ex2 = int(segments[0].x + math.cos(eye_offset - 0.5) * 8)
    ey2 = int(segments[0].y + math.sin(eye_offset - 0.5) * 8)
    pygame.draw.circle(screen, (255, 255, 255), (ex1, ey1), 3)
    pygame.draw.circle(screen, (255, 255, 255), (ex2, ey2), 3)

    pygame.display.flip()
    clock.tick(60)