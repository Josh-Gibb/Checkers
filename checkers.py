import pygame as pg
from sys import exit, argv
from pygame.locals import *
from board_gui import BoardGUI
from game_control import GameControl

def main(gamemode):
    # Main setup
    pg.init()
    FPS = 30
    PLAYER_COLOR = "W"

    DISPLAYSURF = pg.display.set_mode((700, 500))
    pg.display.set_caption('Checkers in Python')
    fps_clock = pg.time.Clock()
    game_control = None

    # Creates a GameControl with an AI instance if gamemode is "cpu"
    if gamemode == "cpu":
        game_control = GameControl(PLAYER_COLOR, True)
    else:
        game_control = GameControl(PLAYER_COLOR, False)

    # Font setup
    main_font = pg.font.SysFont("Arial", 25)
    turn_rect = (509, 26)
    winner_rect = (509, 152)

    while True:
        # GUI
        DISPLAYSURF.fill((0, 0, 0))
        game_control.draw_screen(DISPLAYSURF)

        turn_display_text = "White's turn" if game_control.get_turn() == "W" else "Black's turn"
        DISPLAYSURF.blit(main_font.render(turn_display_text, True, (255, 255, 255)), turn_rect)

        if game_control.get_winner() is not None:
            winner_display_text = "White wins!" if game_control.get_winner() == "W" else "Black wins!"
            DISPLAYSURF.blit(main_font.render(winner_display_text, True, (255, 255, 255)), winner_rect)

        # Event handling
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return
            
            if event.type == MOUSEBUTTONDOWN:
                game_control.hold_piece(event.pos)
            
            if event.type == MOUSEBUTTONUP:
                game_control.release_piece()

                if game_control.get_turn() != PLAYER_COLOR and gamemode == "cpu":
                    pg.time.set_timer(USEREVENT, 400)
            
            if event.type == USEREVENT:
                # AI movement
                if game_control.get_winner() is not None:
                    continue

                game_control.move_ai()

                if game_control.get_turn() == PLAYER_COLOR:
                    pg.time.set_timer(USEREVENT, 0)
        
        pg.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    if len(argv) != 2:
        print("Please specify the game mode. Example: python checkers.py cpu")
    else:
        if argv[1] in ["cpu", "pvp"]:
            main(argv[1])
        else:
            print("Game mode not found.")
    
    exit()