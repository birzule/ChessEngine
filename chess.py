import pygame

pygame.init()

background_color = (118, 150, 86)
white_color = (255, 255, 255)
black_color = (0, 0, 0)
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
    pygame.display.update()


def main(screen):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        draw_table(screen)


if __name__ == "__main__":
    main(screen)