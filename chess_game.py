import pygame
from button import Button
import random


width = 800
eval_bar_width = 60
total_width = width + eval_bar_width
height = 800
rows = 8
cols = 8

def start_game_loop(screen, game_mode = "player"):
    #pygame.init()

    background_color = (118, 150, 86)
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    highlight_color = (255, 255, 0, 100)
    line_width = 3
    square_size = width // cols
    images_size = (square_size, square_size)
    font = pygame.font.SysFont('comicsans', 30, True)
    font_menu = pygame.font.SysFont('comicsans', 35, True)

    #screen = pygame.display.set_mode((width, height))
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
        "bP": black_pawn,
        "bR": black_rook,
        "bN": black_knight,
        "bB": black_bishop,
        "bQ": black_queen,
        "bK": black_king,
        "wP": white_pawn,
        "wR": white_rook,
        "wN": white_knight,
        "wB": white_bishop,
        "wQ": white_queen,
        "wK": white_king,
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
                    pygame.draw.rect(screen, white_color,
                                     pygame.Rect(col * square_size, row * square_size, square_size, square_size))
        load_pieces_on_table(screen)

    def is_valid_move(board, start_pos, end_pos, turn, castling_state, en_passant):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = board[start_row][start_col]
        piece_type = piece[1]
        destination_piece = board[end_row][end_col]
        if destination_piece != "" and destination_piece[0] == turn:
            return False
        move_shape = False
        if piece_type == "N":
            move_shape = knight_move_valid(start_pos, end_pos)
        elif piece_type == "P":
            move_shape = pawn_move_valid(board, start_pos, end_pos, turn, en_passant)
        elif piece_type == "R":
            move_shape = rook_move_valid(board, start_pos, end_pos)
        elif piece_type == "B":
            move_shape = bishop_move_valid(board, start_pos, end_pos)
        elif piece_type == "Q":
            move_shape = queen_move_valid(board, start_pos, end_pos)
        elif piece_type == "K":
            move_shape = king_move_valid(board, start_pos, end_pos, turn, castling_state)
        if not move_shape:
            return False
        temp_board = [row[:] for row in board]
        temp_board[end_row][end_col] = piece
        temp_board[start_row][start_col] = ""
        king_pos = None
        if turn == "w":
            king_piece = "wK"
        else:
            king_piece = "bK"
        for r in range(rows):
            for c in range(cols):
                if temp_board[r][c] == king_piece:
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        if king_pos is None:
            return False
        if turn == "w":
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        if is_square_attacked(temp_board, king_pos, enemy_color):
            return False
        return True

    def knight_move_valid(start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        abs_rows = abs(start_row - end_row)
        abs_cols = abs(start_col - end_col)
        if (abs_rows == 2 and abs_cols == 1) or (abs_rows == 1 and abs_cols == 2):
            return True
        return False

    def pawn_move_valid(board, start_pos, end_pos, turn, en_passant):
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
        # checking if en passant is possible
        if diff_row == direction and abs(diff_col) == 1 and destination_piece == "" and end_pos == en_passant:
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

    def king_move_valid(board, start_pos, end_pos, turn, castling_state):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        abs_rows = abs(start_row - end_row)
        abs_cols = abs(start_col - end_col)
        if abs_rows <= 1 and abs_cols <= 1:
            if abs_rows == 0 and abs_cols == 0:
                return False
            return True
        if abs_rows == 0 and abs_cols == 2:
            if turn == 'w':
                enemy_color = 'b'
            else:
                enemy_color = 'w'
            if is_square_attacked(board, start_pos, enemy_color):
                return False
            if (turn == 'w' and castling_state['wK_moved']) or (turn == 'b' and castling_state['bK_moved']):
                return False
            if end_col > start_col:  # short castle
                rook_col = 7
                if turn == 'w':
                    rook_key = "wR_moved_h1"
                else:
                    rook_key = "bR_moved_h8"
                path_squares = [(start_row, start_col + 1), (start_row, start_col + 2)]
            else:  # long castle
                rook_col = 0
                if turn == 'w':
                    rook_key = 'wR_moved_a1'
                else:
                    rook_key = 'bR_moved_a8'
                path_squares = [(start_row, start_col - 1), (start_row, start_col - 2)]
                if board[start_row][start_col - 3] != "":
                    return False
            if castling_state[rook_key]:  # check if rook moved
                return False
            for square in path_squares:
                if board[square[0]][square[1]] != "":  # blocked path
                    return False
                if is_square_attacked(board, square, enemy_color):  # if in check
                    return False
            return True
        return False

    def pawn_attacking_diagonal(start_pos, end_pos, turn):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if turn == "w":
            direction = 1
        else:
            direction = -1
        diff_row = start_row - end_row
        abs_cols = abs(start_col - end_col)
        if diff_row == direction and abs_cols == 1:
            return True
        return False

    def is_square_attacked(board, check_square, attack_color):
        end_pos = check_square
        for r in range(rows):
            for c in range(cols):
                piece = board[r][c]
                if piece != "" and piece[0] == attack_color:
                    start_pos = (r, c)
                    piece_type = piece[1]
                    if piece_type == "N":
                        if knight_move_valid(start_pos, end_pos): return True
                    elif piece_type == "R":
                        if rook_move_valid(board, start_pos, end_pos): return True
                    elif piece_type == "Q":
                        if queen_move_valid(board, start_pos, end_pos): return True
                    elif piece_type == "B":
                        if bishop_move_valid(board, start_pos, end_pos): return True
                    elif piece_type == "K":
                        abs_rows = abs(start_pos[0] - end_pos[0])
                        abs_cols = abs(start_pos[1] - end_pos[1])
                        if abs_rows <= 1 and abs_cols <= 1: return True
                    elif piece_type == "P":
                        if pawn_attacking_diagonal(start_pos, end_pos, attack_color): return True
        return False

    def get_legal_moves(board, turn, castling_state, en_passant):
        legal_moves = []
        for row in range(rows):
            for col in range(cols):
                piece = board[row][col]
                if piece != "" and piece[0] == turn:
                    start_pos = (row, col)
                    for end_row in range(rows):
                        for end_col in range(cols):
                            end_pos = (end_row, end_col)
                            if is_valid_move(board, start_pos, end_pos, turn, castling_state, en_passant):
                                legal_moves.append((start_pos, end_pos))
        return legal_moves

    running = True
    square_selected = None
    turn = 'w'
    castling_state = {
        'wK_moved': False,
        'bK_moved': False,
        'wR_moved_a1': False,
        'wR_moved_h1': False,
        'bR_moved_a8': False,
        'bR_moved_h8': False
    }
    en_passant = None
    game_over = False
    end_msg = ""
    back_button = Button(image = None, pos = (width // 2, height // 2 + 100),
                         text_input = "Back to main menu", font = font_menu,
                         base_color = "White", hovering_color = "Green")
    pieces_score = {
        'P' : 100,
        'N' : 320,
        'B' : 330,
        'R' : 500,
        'Q' : 900,
        'K' : 20000,
        'p' : -100,
        'n' : -320,
        'b' : -330,
        'r' : -500,
        'q' : -900,
        'k' : -20000
    }

    pawn_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    knight_table = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20,  0,  5,  5,  0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]
    bishop_table = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]
    rook_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ]
    queen_table = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]
    king_table = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]
    ]

    #calculates the score of the table (positive - white is winning, negative - black is winning)
    def eval_board(board_status):
        total_score = 0
        for row in range(rows):
            for col in range(cols):
                piece = board_status[row][col]
                if piece != "":
                    total_score += pieces_score.get(piece, 0)
                    if piece == "wP":
                        total_score += pawn_table[row][col]
                    elif piece == "bP":
                        total_score -= pawn_table[7 - row][col]
                    elif piece == "wN":
                        total_score += knight_table[row][col]
                    elif piece == "bN":
                        total_score -= knight_table[7 - row][col]
                    elif piece == "wB":
                        total_score += bishop_table[row][col]
                    elif piece == "bB":
                        total_score -= bishop_table[7 - row][col]
                    elif piece == "wR":
                        total_score += rook_table[row][col]
                    elif piece == "bR":
                        total_score -= rook_table[7 - row][col]
                    elif piece == "wQ":
                        total_score += queen_table[row][col]
                    elif piece == "bQ":
                        total_score -= queen_table[7 - row][col]
                    elif piece == "wK":
                        total_score += king_table[row][col]
                    elif piece == "bK":
                        total_score -= king_table[7 - row][col]
        return total_score

    def draw_eval_bar(screen, curr_score):
        bar_x = width
        bar_width = eval_bar_width
        block_score = max(min(curr_score, 1000), -1000)
        score_percentage = (block_score + 1000) / 2000
        white_height = height * score_percentage
        black_height = height - white_height
        pygame.draw.rect(screen, black_color, (bar_x, 0, bar_width, black_height))
        pygame.draw.rect(screen, white_color, (bar_x, black_height, bar_width, white_height))

    def minimax(board_state, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return eval_board(board_state)
        if maximizing_player:
            curr_turn = 'w'
        else:
            curr_turn = 'b'
        legal_moves = get_legal_moves(board_state, curr_turn, castling_state, en_passant)
        if len(legal_moves) == 0:
            king_pos = None
            if maximizing_player:
                king_piece = "wK"
                enemy_color = 'b'
            else:
                king_piece = "bK"
                enemy_color = 'w'
            for row in range(rows):
                for col in range(cols):
                    if board_state[row][col] == king_piece:
                        king_pos = (row, col)
                        break
                    if king_pos:
                        break
            if king_pos and is_square_attacked(board_state, king_pos, enemy_color):
                if maximizing_player:
                    return -float('inf')
                else:
                    return float('inf')
            else:
                return 0
        if maximizing_player:
            best_score = -float('inf')
            for move in legal_moves:
                temp_board = [row[:] for row in board_state]
                start_pos, end_pos = move
                piece = temp_board[start_pos[0]][start_pos[1]]
                temp_board[end_pos[0]][end_pos[1]] = piece
                temp_board[start_pos[0]][start_pos[1]] = ""
                score = minimax(temp_board, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in legal_moves:
                temp_board = [row[:] for row in board_state]
                start_pos, end_pos = move
                piece = temp_board[start_pos[0]][start_pos[1]]
                temp_board[end_pos[0]][end_pos[1]] = piece
                temp_board[start_pos[0]][start_pos[1]] = ""
                score = minimax(temp_board, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def find_best_move(board_state, turn, castling_state, en_passant):
        legal_moves = get_legal_moves(board_state, turn, castling_state, en_passant)
        random.shuffle(legal_moves)
        best_move = None
        depth = 4
        maximizing_player = (turn == 'b')
        if maximizing_player:
            best_score = -float('inf')
        else:
            best_score = float('inf')
        for move in legal_moves:
            temp_board = [row[:] for row in board_state]
            start_pos, end_pos = move
            piece = temp_board[start_pos[0]][start_pos[1]]
            temp_board[end_pos[0]][end_pos[1]] = piece
            temp_board[start_pos[0]][start_pos[1]] = ""
            score = minimax(temp_board, depth - 1, -float('inf'), float('inf'), not maximizing_player)
            if maximizing_player:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move

    while running:
        ai_turn = (game_mode == "ai" and turn == 'b')
        if not game_over:
            legal_moves = get_legal_moves(board, turn, castling_state, en_passant)
            if len(legal_moves) == 0:
                game_over = True
                king_pos = None
                if turn == 'w':
                    king_piece = 'wK'
                    enemy_color = 'b'
                else:
                    king_piece = 'bK'
                    enemy_color = 'w'
                for row in range(rows):
                    for col in range(cols):
                        if board[row][col] == king_piece:
                            king_pos = (row, col)
                            break
                        if king_pos:
                            break
                if king_pos and is_square_attacked(board, king_pos, enemy_color):
                    if turn == 'w':
                        winner = "Black"
                    else:
                        winner = "White"
                    end_msg = f"Checkmate: {winner} won!"
                else:
                    end_msg = "Stalemate!"
                print(end_msg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_over:
                    if back_button.check_for_input(mouse_pos):
                        return
                elif not ai_turn:
                    pos = mouse_pos
                    col = pos[0] // square_size
                    row = pos[1] // square_size
                    if square_selected is None:
                        piece = board[row][col]
                        if piece != "" and piece[0] == turn:
                            square_selected = (row, col)
                    else:
                        start_row, start_col = square_selected
                        end_row, end_col = row, col
                        if is_valid_move(board, square_selected, (end_row, end_col), turn,
                                         castling_state, en_passant):
                            piece_to_move = board[start_row][start_col]
                            if piece_to_move == 'wK': castling_state['wK_moved'] = True
                            if piece_to_move == 'bK': castling_state['bK_moved'] = True
                            if square_selected == (7, 0): castling_state['wR_moved_a1'] = True
                            if square_selected == (7, 7): castling_state['wR_moved_h1'] = True
                            if square_selected == (0, 0): castling_state['bR_moved_a8'] = True
                            if square_selected == (0, 7): castling_state['bR_moved_h8'] = True
                            board[end_row][end_col] = piece_to_move
                            board[start_row][start_col] = ""
                            if piece_to_move[1] == "P" and (end_row, end_col) == en_passant:
                                board[start_row][end_col] = ""
                            if piece_to_move[1] == 'K' and abs(start_col - end_col) == 2:  # checking if it's castling
                                if end_col > start_col:  # short castle
                                    rook = board[start_row][7]
                                    board[start_row][5] = rook
                                    board[start_row][7] = ""
                                else:  # long castle
                                    rook = board[start_row][0]
                                    board[start_row][3] = rook
                                    board[start_row][0] = ""
                            if piece_to_move[1] == "P":  # checking for promoting to a queen/knight/rook/bishop
                                if end_row == 0 and turn == 'w':
                                    board[end_row][end_col] = "wQ"
                                    pieces['wQ'] = white_queen
                                elif end_row == 7 and turn == 'b':
                                    board[end_row][end_col] = "bQ"
                                    pieces['bQ'] = black_queen
                            en_passant = None
                            if piece_to_move[1] == "P" and abs(start_row - end_row) == 2:
                                en_passant = ((start_row + end_row) // 2, start_col)
                            if turn == 'w':
                                turn = 'b'
                            else:
                                turn = 'w'
                            square_selected = None
                        else:
                            square_selected = None

        if not game_over and game_mode == "ai" and turn == 'b':
            best_move = find_best_move(board, turn, castling_state, en_passant)
            if best_move:
                start_row, start_col = best_move[0]
                end_row, end_col = best_move[1]
                square_selected = best_move[0]
                piece_to_move = board[start_row][start_col]
                if piece_to_move == 'wK': castling_state['wK_moved'] = True
                if piece_to_move == 'bK': castling_state['bK_moved'] = True
                if square_selected == (7, 0): castling_state['wR_moved_a1'] = True
                if square_selected == (7, 7): castling_state['wR_moved_h1'] = True
                if square_selected == (0, 0): castling_state['bR_moved_a8'] = True
                if square_selected == (0, 7): castling_state['bR_moved_h8'] = True
                board[end_row][end_col] = piece_to_move
                board[start_row][start_col] = ""
                if piece_to_move[1] == "P" and (end_row, end_col) == en_passant:
                    board[start_row][end_col] = ""
                if piece_to_move[1] == 'K' and abs(start_col - end_col) == 2:
                    if end_col > start_col:
                        rook = board[start_row][7]
                        board[start_row][5] = rook
                        board[start_row][7] = ""
                    else:
                        rook = board[start_row][0]
                        board[start_row][3] = rook
                        board[start_row][0] = ""
                if piece_to_move[1] == "P":
                    if end_row == 0 and turn == 'w':
                        board[end_row][end_col] = "wQ"
                    elif end_row == 7 and turn == 'b':
                        board[end_row][end_col] = "bQ"
                en_passant = None
                if piece_to_move[1] == "P" and abs(start_row - end_row) == 2:
                    en_passant = ((start_row + end_row) // 2, start_col)
                turn = 'w'
                square_selected = None

        draw_table(screen)
        curr_score = eval_board(board)
        draw_eval_bar(screen, curr_score)

        if square_selected is not None:
            row, col = square_selected
            transparent_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            transparent_surface.fill(highlight_color)
            screen.blit(transparent_surface, (col * square_size, row * square_size))

        if game_over:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 100))
            screen.blit(overlay, (0, 0))
            msg_surface = font.render(end_msg, True, white_color)
            msg_rect = msg_surface.get_rect(center = (width // 2, height // 2))
            screen.blit(msg_surface, msg_rect)
            mouse_pos = pygame.mouse.get_pos()
            back_button.change_color(mouse_pos)
            back_button.update(screen)

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((width, height))
    start_game_loop(test_screen)