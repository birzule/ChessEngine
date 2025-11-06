import sys
import pygame
from Tools.scripts.parse_html5_entities import write_items

import chess_game
from button import Button

width = 800
height = 800

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MENU")
bg = pygame.image.load("assets/Background.png")
bg = pygame.transform.scale(bg, (width, height))

def get_font_size(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill("black")
        text_menu = get_font_size(28).render("Please select the game mode", True, "White")
        rect_menu = text_menu.get_rect(center=(width // 2, 150))
        screen.blit(text_menu, rect_menu)
        pvp_button = Button(image = None, pos = (width // 2, 300), text_input = "Player vs Player",
                            font = get_font_size(30), base_color = "White", hovering_color = "Green")
        pvai_button = Button(image = None, pos = (width // 2, 450), text_input = "Player vs AI",
                             font = get_font_size(30), base_color = "White", hovering_color = "Green")
        back_button = Button(image = None, pos = (width // 2, 600), text_input = "Back",
                             font = get_font_size(30), base_color = "White", hovering_color = "Green")
        for button in (pvp_button, pvai_button, back_button):
            button.change_color(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(mouse_pos):
                    return
                if pvp_button.check_for_input(mouse_pos):
                    chess_game.start_game_loop(screen, game_mode = "player")
                if pvai_button.check_for_input(mouse_pos):
                    chess_game.start_game_loop(screen, game_mode = "ai")
        pygame.display.update()

def options():
    pass

def main_menu():
    while True:
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        text_menu = get_font_size(65).render("Main Menu", True, "#b68f40")
        rect_menu = text_menu.get_rect(center = (width // 2, 100))
        play_button = Button(image = pygame.image.load("assets/Play Rect.png"), pos = (width // 2, 250),
                             text_input = "Play", font = get_font_size(50), base_color = "#d7fcd4",
                             hovering_color = "White")
        optios_button = Button(image = pygame.image.load("assets/Options Rect.png"), pos = (width // 2, 400),
                             text_input = "Options", font = get_font_size(50), base_color = "#d7fcd4",
                             hovering_color = "White")
        quit_button = Button(image = pygame.image.load("assets/Quit Rect.png"), pos = (width // 2, 550),
                             text_input = "Quit", font = get_font_size(50), base_color = "#d7fcd4",
                             hovering_color = "White")
        screen.blit(text_menu, rect_menu)
        for button in [play_button, optios_button, quit_button]:
            button.change_color(mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(mouse_pos):
                    play()
                if optios_button.check_for_input(mouse_pos):
                    options()
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()