import pygame

pygame.init()

background_color = (118, 150, 86)
white_color = (255, 255, 255)
black_color = (0, 0, 0)
highlight_color = (255, 255, 0, 100)
width = 800
height = 800
rows = 8
cols = 8
line_width = 3
square_size = width // cols
images_size = (square_size, square_size)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Game / Engine')
white_pawn = pygame.image.load('images/white_pawn_chess.png')
white_king = pygame.image.load('images/white_king_chess.png')
white_queen = pygame.image.load('images/white_queen_chess.png')
white_rook = pygame.image.load('images/white_rook_chess.png')
white_knight = pygame.image.load('images/white_knight_chess.png')
white_bishop = pygame.image.load('images/white_bishop_chess.png')

black_pawn = pygame.image.load('images/black_pawn_chess.png')
black_king = pygame.image.load('images/black_king_chess.png')
black_queen = pygame.image.load('images/black_queen_chess.png')
black_rook = pygame.image.load('images/black_rook_chess.png')
black_knight = pygame.image.load('images/black_knight_chess.png')
black_bishop = pygame.image.load('images/black_bishop_chess.png')

white_pawn = pygame.transform.scale(white_pawn, images_size)
white_king = pygame.transform.scale(white_king, images_size)
white_queen = pygame.transform.scale(white_queen, images_size)
white_rook = pygame.transform.scale(white_rook, images_size)
white_knight = pygame.transform.scale(white_knight, images_size)
white_bishop = pygame.transform.scale(white_bishop, images_size)

black_pawn = pygame.transform.scale(black_pawn, images_size)
black_king = pygame.transform.scale(black_king, images_size)
black_queen = pygame.transform.scale(black_queen, images_size)
black_rook = pygame.transform.scale(black_rook, images_size)
black_knight = pygame.transform.scale(black_knight, images_size)
black_bishop = pygame.transform.scale(black_bishop, images_size)

board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

pieces = {
    "bP" : black_pawn,
    "bR" : black_rook,
    "bN" : black_knight,
    "bB" : black_bishop,
    "bQ" : black_queen,
    "bK" : black_king,
    "wP" : white_pawn,
    "wR" : white_rook,
    "wN" : white_knight,
    "wB" : white_bishop,
    "wQ" : white_queen,
    "wK" : white_king,
}

def load_pieces_on_table(screen):
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != "":
                screen.blit(pieces[piece], (col * square_size, row * square_size))


def draw_table(screen):
    screen.fill(background_color)
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                continue
            else:
                pygame.draw.rect(screen, white_color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
    load_pieces_on_table(screen)

def is_valid_move(board, start_pos, end_pos, turn):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]
    piece_type = piece[1]
    destination_piece = board[end_row][end_col]
    if destination_piece != "" and destination_piece[0] == turn:
        return False
    if piece_type == "N":
        return knight_move_valid(start_pos, end_pos)
    if piece_type == "P":
        return pawn_move_valid(board, start_pos, end_pos, turn)
    if piece_type == "R":
        return rook_move_valid(board, start_pos, end_pos)
    if piece_type == "B":
        return bishop_move_valid(board, start_pos, end_pos)
    if piece_type == "Q":
        return queen_move_valid(board, start_pos, end_pos)
    if piece_type == "K":
        return king_move_valid(board, start_pos, end_pos)
    return False

def knight_move_valid(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    abs_rows = abs(start_row - end_row)
    abs_cols = abs(start_col - end_col)
    if (abs_rows == 2 and abs_cols == 1) or (abs_rows == 1 and abs_cols == 2):
        return True
    return False

def pawn_move_valid(board, start_pos, end_pos, turn):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    destination_piece = board[end_row][end_col]
    if turn == "w":
        direction = 1
        start_row_pawn = 6
    else:
        direction = -1
        start_row_pawn = 1
    diff_row = start_row - end_row
    diff_col = start_col - end_col
    if diff_row == direction and diff_col == 0 and destination_piece == "":
        return True
    if (start_row == start_row_pawn and diff_row == 2 * direction and diff_col == 0 and
        destination_piece == "" and board[start_row - direction][start_col] == ""):
        return True
    if diff_row == direction and abs(diff_col) == 1 and destination_piece != "" and destination_piece[0] != turn:
        return True
    return False

def rook_move_valid(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    destination_piece = board[end_row][end_col]
    if start_row != end_row and start_col != end_col:
        return False
    if start_row == end_row:
        min_col = min(start_col, end_col)
        max_col = max(start_col, end_col)
        for col in range(min_col + 1, max_col):
            if board[start_row][col] != "":
                return False
    if start_col == end_col:
        min_row = min(start_row, end_row)
        max_row = max(start_row, end_row)
        for row in range(min_row + 1, max_row):
            if board[row][start_col] != "":
                return False
    return True

def bishop_move_valid(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    abs_rows = abs(start_row - end_row)
    abs_cols = abs(start_col - end_col)
    if abs_rows != abs_cols or abs_rows == 0:
        return False
    if end_row > start_row:
        step_row = 1
    else:
        step_row = -1
    if end_col > start_col:
        step_col = 1
    else:
        step_col = -1
    current_row, current_col = start_row, start_col
    for i in range(abs(abs_rows - 1)):
        current_row += step_row
        current_col += step_col
        if board[current_row][current_col] != "":
            return False
    return True

def queen_move_valid(board, start_pos, end_pos):
    return bishop_move_valid(board, start_pos, end_pos) or rook_move_valid(board, start_pos, end_pos)

def king_move_valid(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    abs_rows = abs(start_row - end_row)
    abs_cols = abs(start_col - end_col)
    if abs_rows <= 1 and abs_cols <= 1:
        if  abs_rows == 0 and abs_cols == 0:
            return False
        return True
    # sa adaug castling mai tarziu
    return False

def main(screen):
    running = True
    square_selected = None
    turn = 'w'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                col = pos[0] // square_size
                row = pos[1] // square_size

                if square_selected is None:
                    piece = board[row][col]
                    if piece != "" and piece[0] == turn:
                        square_selected = (row, col)
                else:
                    start_row, start_col = square_selected
                    end_row, end_col = row, col

                    if is_valid_move(board, square_selected, (end_row, end_col), turn):
                        piece_to_move = board[start_row][start_col]
                        board[end_row][end_col] = piece_to_move
                        board[start_row][start_col] = ""
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                        square_selected = None
                    else:
                        square_selected = None

        draw_table(screen)

        if square_selected is not None:
            row, col = square_selected
            transparent_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            transparent_surface.fill(highlight_color)
            screen.blit(transparent_surface, (col * square_size, row * square_size))

        pygame.display.update()

if __name__ == "__main__":
    main(screen)