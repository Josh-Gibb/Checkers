import pygame as pg
from game_control import GameControl


def main():
    FPS = 30
    DISPLAYSURF = pg.display.get_surface()
    if DISPLAYSURF is None:
        DISPLAYSURF = pg.display.set_mode((700, 500))
        pg.display.set_caption("Checkers in Python")

    clock = pg.time.Clock()

    # Set player color
    game_control = GameControl(player_color="W")

    # Font setup
    font = pg.font.SysFont("Arial", 25)
    turn_pos = (509, 26)
    winner_pos = (509, 152)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                game_control.hold_piece(event.pos)

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                game_control.release_piece()

        DISPLAYSURF.fill((0, 0, 0))
        game_control.draw_screen(DISPLAYSURF)

        turn_text = "White's turn" if game_control.get_turn() == "W" else "Black's turn"
        DISPLAYSURF.blit(font.render(turn_text, True, (255, 255, 255)), turn_pos)

        winner = game_control.get_winner()
        if winner is not None:
            winner_text = "White wins!" if winner == "W" else "Black wins!"
            DISPLAYSURF.blit(font.render(winner_text, True, (255, 255, 255)), winner_pos)
            pg.display.update()
            pg.time.wait(3000)
            running = False

        pg.display.update()
        clock.tick(FPS)



if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Checkers in Python")
    pg.display.set_mode((700, 500))
    main()
    pg.quit()