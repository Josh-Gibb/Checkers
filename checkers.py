import pygame as pg
from game_control import GameControl


# Main class
def main():
    pg.init()
    FPS = 30
    PLAYER_COLOR = "W"

    DISPLAYSURF = pg.display.set_mode((700, 500))
    pg.display.set_caption('Checkers in Python')
    fps_clock = pg.time.Clock()
    game_control = None

    game_control = GameControl(PLAYER_COLOR)

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

        pg.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()