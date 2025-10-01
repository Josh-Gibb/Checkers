import sys
import pygame

pygame.init()

from pages import Screen

FPS = 60
WIDTH, HEIGHT = 720, 480


def main() -> int:
    app = Screen(size=(WIDTH, HEIGHT))
    pygame.display.set_caption(app.title)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        dt_ms = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                app.handle_event(event)

        app.update(dt_ms)
        app.draw(screen)
        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
