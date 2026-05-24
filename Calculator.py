import pygame
import sys

pygame.init()

# Bigger screen
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Big Calculator")

# Colors
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)

# Bigger font
font = pygame.font.Font(None, 70)

text = ""

# Bigger buttons
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', 'C', '=', '+']
]

button_rects = []

button_width = 120
button_height = 120

for row in range(4):
    row_rects = []
    for col in range(4):
        rect = pygame.Rect(
            col * button_width + 10,
            180 + row * button_height,
            button_width - 10,
            button_height - 10
        )
        row_rects.append(rect)
    button_rects.append(row_rects)

running = True
while running:
    screen.fill(WHITE)

    # Bigger display
    pygame.draw.rect(screen, GRAY, (20, 20, 460, 120))
    display = font.render(text, True, BLACK)
    screen.blit(display, (30, 50))

    # Draw buttons
    for row in range(4):
        for col in range(4):
            rect = button_rects[row][col]
            pygame.draw.rect(screen, BLUE, rect, border_radius=20)

            label = font.render(buttons[row][col], True, WHITE)
            screen.blit(label, (rect.x + 40, rect.y + 35))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for row in range(4):
                for col in range(4):
                    if button_rects[row][col].collidepoint(pos):
                        value = buttons[row][col]

                        if value == "=":
                            try:
                                text = str(eval(text))
                            except:
                                text = "Error"

                        elif value == "C":
                            text = ""

                        else:
                            text += value

    pygame.display.update()

pygame.quit()
sys.exit()