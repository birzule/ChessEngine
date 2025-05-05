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

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Game / Engine')

def draw_table(screen):
    screen.fill(background_color)
    for row in range(rows):
        x = 0
        for col in range(cols):
            y = row * square_size
            if (row + col) % 2 == 0:
                x += square_size
            else:
                pygame.draw.rect(screen, white_color, pygame.Rect(x, y, square_size, square_size))
                x += square_size
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