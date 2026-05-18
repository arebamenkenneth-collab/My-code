import pygame
import sys
import math

WIDTH, HEIGHT = 720, 900
FPS = 60

BG          = (18,  18,  30)
CELL_BG     = (33,  33,  56)
BORDER      = (64,  64, 115)
X_COLOR     = (93, 184, 255)
O_COLOR     = (255, 115, 140)
WIN_BG      = (46,  71,  46)
WIN_BORDER  = (77, 230, 102)
STATUS_DEF  = (218, 218, 255)
BTN_BG      = (56,  56,  97)
BTN_HOVER   = (72,  72, 120)
DRAW_COLOR  = (230, 192,  77)
WHITE       = (255, 255, 255)
SCORE_DRAW  = (153, 153, 179)

BOARD_PAD   = 32
TITLE_H     = 70
STATUS_H    = 50
SCORE_H     = 50
BTN_H       = 56
SPACING     = 14

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic  Tac  Toe")
clock = pygame.time.Clock()

try:
    FONT_TITLE  = pygame.font.SysFont("DejaVu Sans", 36, bold=True)
    FONT_STATUS = pygame.font.SysFont("DejaVu Sans", 24, bold=True)
    FONT_CELL   = pygame.font.SysFont("DejaVu Sans", 96, bold=True)
    FONT_SCORE  = pygame.font.SysFont("DejaVu Sans", 22, bold=True)
    FONT_BTN    = pygame.font.SysFont("DejaVu Sans", 22, bold=True)
except:
    FONT_TITLE  = pygame.font.Font(None, 44)
    FONT_STATUS = pygame.font.Font(None, 30)
    FONT_CELL   = pygame.font.Font(None, 108)
    FONT_SCORE  = pygame.font.Font(None, 28)
    FONT_BTN    = pygame.font.Font(None, 28)


def draw_rounded_rect(surf, color, rect, radius=18, border_color=None, border_width=2):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border_color:
        pygame.draw.rect(surf, border_color, rect, border_width, border_radius=radius)


def center_text(surf, font, text, color, rect):
    s = font.render(text, True, color)
    x = rect[0] + (rect[2] - s.get_width())  // 2
    y = rect[1] + (rect[3] - s.get_height()) // 2
    surf.blit(s, (x, y))


def compute_layout():
    board_size = WIDTH - 2 * BOARD_PAD
    cell_size  = (board_size - 2 * SPACING) // 3

    y = BOARD_PAD
    title_rect  = (BOARD_PAD, y, board_size, TITLE_H);  y += TITLE_H + SPACING
    status_rect = (BOARD_PAD, y, board_size, STATUS_H); y += STATUS_H + SPACING
    board_rect  = (BOARD_PAD, y, board_size, board_size); y += board_size + SPACING
    score_rect  = (BOARD_PAD, y, board_size, SCORE_H);  y += SCORE_H + SPACING
    btn_rect    = (BOARD_PAD, y, board_size, BTN_H)

    cells = []
    for row in range(3):
        for col in range(3):
            cx = BOARD_PAD + col * (cell_size + SPACING)
            cy = board_rect[1] + row * (cell_size + SPACING)
            cells.append((cx, cy, cell_size, cell_size))

    return title_rect, status_rect, board_rect, score_rect, btn_rect, cells


class ScaleAnim:
    def __init__(self, duration=0.16):
        self.t = 0.0
        self.duration = duration
        self.active = False

    def start(self):
        self.t = 0.0
        self.active = True

    def update(self, dt):
        if self.active:
            self.t = min(self.t + dt / self.duration, 1.0)
            if self.t >= 1.0:
                self.active = False

    def scale(self):
        if not self.active and self.t == 0.0:
            return 1.0
        return 1.0 + 0.15 * math.sin(self.t * math.pi)


WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_winner(board):
    for a,b,c in WINS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a,b,c)
    return None, None


class Game:
    def __init__(self):
        self.score = {"X": 0, "O": 0, "Draw": 0}
        self.reset()

    def reset(self):
        self.board       = [""] * 9
        self.current     = "X"
        self.game_over   = False
        self.win_combo   = None
        self.status_text = "Player  X  .  Your Turn"
        self.status_col  = X_COLOR
        self.anims       = [ScaleAnim() for _ in range(9)]

    def play(self, idx):
        if self.game_over or self.board[idx]:
            return
        self.board[idx] = self.current
        self.anims[idx].start()

        winner, combo = check_winner(self.board)
        if winner:
            self.game_over  = True
            self.win_combo  = combo
            self.score[winner] += 1
            self.status_text = "Player  {}  Wins!".format(winner)
            self.status_col  = WIN_BORDER
        elif "" not in self.board:
            self.game_over  = True
            self.score["Draw"] += 1
            self.status_text = "It's a Draw!"
            self.status_col  = DRAW_COLOR
        else:
            self.current = "O" if self.current == "X" else "X"
            col = X_COLOR if self.current == "X" else O_COLOR
            self.status_text = "Player  {}  .  Your Turn".format(self.current)
            self.status_col  = col


def main():
    layout = compute_layout()
    title_rect, status_rect, board_rect, score_rect, btn_rect, cells = layout
    game = Game()

    while True:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, cr in enumerate(cells):
                    if pygame.Rect(cr).collidepoint(mx, my):
                        game.play(i)
                if pygame.Rect(btn_rect).collidepoint(mx, my):
                    game.reset()

        for anim in game.anims:
            anim.update(dt)

        screen.fill(BG)

        center_text(screen, FONT_TITLE, "TIC  TAC  TOE", STATUS_DEF, title_rect)
        center_text(screen, FONT_STATUS, game.status_text, game.status_col, status_rect)

        for i, cr in enumerate(cells):
            is_win = game.win_combo and i in game.win_combo
            bg  = WIN_BG     if is_win else CELL_BG
            brd = WIN_BORDER if is_win else BORDER
            draw_rounded_rect(screen, bg, cr, radius=22, border_color=brd, border_width=2)

            val = game.board[i]
            if val:
                scale = game.anims[i].scale()
                col   = X_COLOR if val == "X" else O_COLOR
                base_surf = FONT_CELL.render(val, True, col)
                if scale != 1.0:
                    w = int(base_surf.get_width()  * scale)
                    h = int(base_surf.get_height() * scale)
                    surf = pygame.transform.smoothscale(base_surf, (max(1,w), max(1,h)))
                else:
                    surf = base_surf
                cx = cr[0] + (cr[2] - surf.get_width())  // 2
                cy = cr[1] + (cr[3] - surf.get_height()) // 2
                screen.blit(surf, (cx, cy))

        sw = (score_rect[2] - 2 * SPACING) // 3
        for txt, col, idx in [
            ("X  {}".format(game.score["X"]),       X_COLOR,    0),
            ("O  {}".format(game.score["O"]),       O_COLOR,    1),
            ("Draw  {}".format(game.score["Draw"]), SCORE_DRAW, 2),
        ]:
            sr = (score_rect[0] + idx*(sw+SPACING), score_rect[1], sw, SCORE_H)
            center_text(screen, FONT_SCORE, txt, col, sr)

        hover = pygame.Rect(btn_rect).collidepoint(mx, my)
        draw_rounded_rect(screen, BTN_HOVER if hover else BTN_BG, btn_rect, radius=14)
        center_text(screen, FONT_BTN, "NEW GAME", WHITE, btn_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()