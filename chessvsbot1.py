import pygame
import chess
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (200, 200, 0)

# Unicode chess symbols
UNICODE_PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess vs Bot (Unicode)")
# Utiliser une police qui supporte les pièces Unicode
font = pygame.font.SysFont("DejaVu Sans Mono", 48)

board = chess.Board()
selected_square = None

def draw_board():
    for rank in range(8):
        for file in range(8):
            square_color = WHITE if (rank + file) % 2 == 0 else BROWN
            rect = pygame.Rect(file*SQUARE_SIZE, rank*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, square_color, rect)

            square = chess.square(file, 7 - rank)
            piece = board.piece_at(square)
            if piece:
                symbol = UNICODE_PIECES[piece.symbol()]
                color = (0, 0, 0) if piece.color else (255, 255, 255)
                text = font.render(symbol, True, color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    if selected_square is not None:
        file = chess.square_file(selected_square)
        rank = 7 - chess.square_rank(selected_square)
        highlight_rect = pygame.Rect(file*SQUARE_SIZE, rank*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, HIGHLIGHT, highlight_rect, 3)

def get_square_under_mouse(pos):
    file = pos[0] // SQUARE_SIZE
    rank = 7 - (pos[1] // SQUARE_SIZE)
    return chess.square(file, rank)

def bot_move():
    moves = list(board.legal_moves)
    if moves:
        board.push(random.choice(moves))

# --- MAIN LOOP ---
running = True
while running:
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if board.turn == chess.WHITE and not board.is_game_over():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_square = get_square_under_mouse(pygame.mouse.get_pos())
                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:
                        board.push(move)
                    selected_square = None

    if board.turn == chess.BLACK and not board.is_game_over():
        pygame.time.wait(300)
        bot_move()

    if board.is_game_over():
        print("Game over:", board.result())
        running = False

pygame.quit()
