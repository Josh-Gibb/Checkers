from __future__ import annotations
import pygame



# Basic Theme of the project
class Theme:
    FONT_SM = None
    FONT_MD = None
    FONT_LG = None

    @classmethod
    def init_fonts(cls) -> None:
        cls.FONT_SM = pygame.font.SysFont(None, 18)
        cls.FONT_MD = pygame.font.SysFont(None, 24)
        cls.FONT_LG = pygame.font.SysFont(None, 32)
        cls._fonts_ready = True

    # Colors
    BG = pygame.Color(244, 246, 250)
    CARD = pygame.Color(255, 255, 255)
    TEXT = pygame.Color(17, 24, 39)
    MUTED = pygame.Color(100, 116, 139)
    BORDER = pygame.Color(226, 232, 240)
    SHADOW = pygame.Color(0, 0, 0, 32)

    PRIMARY = pygame.Color(37, 99, 235)
    PRIMARY_HOVER = pygame.Color(29, 78, 216)
    SUCCESS = pygame.Color(22, 163, 74)
    DANGER = pygame.Color(220, 38, 38)

    INPUT_BG = pygame.Color(250, 250, 250)
    INPUT_FG = TEXT
    ACTIVE = pygame.Color(99, 102, 241)


def _blend(c1: pygame.Color, c2: pygame.Color, t: float) -> pygame.Color:
    t = max(0.0, min(1.0, t))
    return pygame.Color(
        int(c1.r + (c2.r - c1.r) * t),
        int(c1.g + (c2.g - c1.g) * t),
        int(c1.b + (c2.b - c1.b) * t),
    )


# Class for the input boxes
class InputBox:
    def __init__(self, x: int, y: int, w: int, h: int, placeholder: str = "", is_password: bool = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.placeholder = placeholder
        self.is_password = is_password

        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_pos = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                relx = event.pos[0] - (self.rect.x + 12)
                approx_char_w = max(1, Theme.FONT_MD.size("a")[0])
                self.cursor_pos = max(0, min(len(self.text), relx // approx_char_w))
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                    self.cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[: self.cursor_pos] + self.text[self.cursor_pos + 1 :]
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            elif event.unicode and event.key not in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE):
                if 32 <= ord(event.unicode) <= 126:
                    self.text = self.text[: self.cursor_pos] + event.unicode + self.text[self.cursor_pos :]
                    self.cursor_pos += 1

    def update(self, dt_ms: int) -> None:
        self.cursor_timer += dt_ms
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surf: pygame.Surface) -> None:
        # soft shadow
        shadow = self.rect.copy()
        shadow.move_ip(0, 1)
        pygame.draw.rect(surf, Theme.SHADOW, shadow, border_radius=10)

        pygame.draw.rect(surf, Theme.INPUT_BG, self.rect, border_radius=10)
        border_col = Theme.ACTIVE if self.active else Theme.BORDER
        pygame.draw.rect(surf, border_col, self.rect, width=2, border_radius=10)

        display = self.text if not self.is_password else ("•" * len(self.text))
        if not self.text and not self.active:
            txt = Theme.FONT_MD.render(self.placeholder, True, Theme.MUTED)
        else:
            txt = Theme.FONT_MD.render(display, True, Theme.INPUT_FG)
        surf.blit(txt, (self.rect.x + 12, self.rect.y + (self.rect.h - txt.get_height()) // 2))

        if self.active and self.cursor_visible:
            prefix = display[: self.cursor_pos] if not self.is_password else ("•" * self.cursor_pos)
            cursor_x = self.rect.x + 12 + Theme.FONT_MD.size(prefix)[0]
            pygame.draw.line(
                surf, Theme.INPUT_FG,
                (cursor_x, self.rect.y + 8),
                (cursor_x, self.rect.y + self.rect.h - 8),
                2
            )

    def get_value(self) -> str:
        return self.text

    def clear(self) -> None:
        self.text = ""
        self.cursor_pos = 0

# Class for buttons
class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, primary: bool = True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.primary = primary
        self.hovered = False
        self._hover_t = 0.0  # 0..1 for animation state

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update(self, dt_ms: int) -> None:
        # ease toward target (hovered -> 1, else -> 0)
        target = 1.0 if self.hovered else 0.0
        speed = 0.012  # tuned for ~60 FPS
        self._hover_t += (target - self._hover_t) * min(1.0, dt_ms * speed)

    def draw(self, surf: pygame.Surface) -> None:
        # slight "lift" on hover
        lift = int(2 * self._hover_t)
        draw_rect = self.rect.move(0, -lift)

        if self.primary:
            base = Theme.PRIMARY
            hov = Theme.PRIMARY_HOVER
            bg = _blend(base, hov, self._hover_t)
            fg = pygame.Color(255, 255, 255)
            # shadow grows a touch on hover
            shadow = draw_rect.move(0, 2)
            pygame.draw.rect(surf, Theme.SHADOW, shadow, border_radius=12)
            pygame.draw.rect(surf, bg, draw_rect, border_radius=12)
        else:
            # outline button with subtle fill blend toward primary on hover
            fg = _blend(Theme.PRIMARY, Theme.PRIMARY_HOVER, self._hover_t)
            fill = _blend(Theme.CARD, Theme.PRIMARY, 0.06 * self._hover_t)  # faint fill
            pygame.draw.rect(surf, fill, draw_rect, border_radius=12)
            pygame.draw.rect(surf, fg, draw_rect, 2, border_radius=12)

        txt = Theme.FONT_MD.render(self.text, True, fg)
        surf.blit(
            txt,
            (draw_rect.centerx - txt.get_width() // 2,
             draw_rect.centery - txt.get_height() // 2),
        )
