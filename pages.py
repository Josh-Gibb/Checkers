from __future__ import annotations
from checkers import main

import pygame

pygame.init()

from ui_elements import *
from user_manager import User_manager

WIDTH, HEIGHT = 720, 480

MODE_LOGIN = "login"
MODE_SIGNUP = "signup"
MODE_HOME = "home"

user_man = User_manager()

# Class for a base screen
class ScreenBase:
    def __init__(self, screen):
        self.screen = screen
        self.message = ""
        self.message_color = Theme.MUTED

    def on_enter(self):
        self.message_color = Theme.MUTED
        self.message = ""

    def set_message(self, text, color: pygame.Color):
        self.message = text
        self.message_color = color

    def handle_event(self, event) -> None: ...
    def update(self, dt_ms: int) -> None: ...
    def draw(self, surf) -> None: ...

# Class for a base
class CardMixin:
    def card_rect(self) -> pygame.Rect:
        # Center the card in the window
        w, h = 520, 360
        x = (WIDTH - w) // 2
        y = (HEIGHT - h) // 2
        return pygame.Rect(x, y, w, h)

    def draw_card(self, surf, title_text: str) -> pygame.Rect:
        rect = self.card_rect()
        shadow = rect.copy()
        shadow.move_ip(0, 2)
        pygame.draw.rect(surf, Theme.SHADOW, shadow, border_radius=16)

        pygame.draw.rect(surf, Theme.CARD, rect, border_radius=16)
        pygame.draw.rect(surf, Theme.BORDER, rect, width=2, border_radius=16)

        title = Theme.FONT_LG.render(title_text, True, Theme.TEXT)
        surf.blit(title, (rect.x + 32, rect.y + 24))

        if getattr(self, "message", ""):
            msg = Theme.FONT_SM.render(self.message, True, self.message_color)
            surf.blit(msg, (rect.x + 32, rect.y + 60))
        return rect


# Screen for the Login Page
class LoginPage(ScreenBase, CardMixin):
    # Drawing all Elements on Login Page
    def __init__(self, screen):
        super().__init__(screen)
        rect = self.card_rect()
        pad_x = rect.x + 32
        pad_y = rect.y + 96
        pad_w = rect.w - 64
        height = 44

        self.username = InputBox(pad_x, pad_y, pad_w, height, "Username")
        self.password = InputBox(pad_x, pad_y + 56, pad_w, height, "Password", is_password=True)
        self.btn_login = Button(pad_x, pad_y + 120, 180, height, "Login")
        self.btn_goto_signup = Button(pad_x + 275, pad_y + 120, 180, height, "Sign Up")
        self.username.active = True

    # A class thst handles any interaction from user
    def handle_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return
            if event.key == pygame.K_RETURN:
                self.try_login()

        self.username.handle_event(event)
        self.password.handle_event(event)

        if self.btn_login.handle_event(event):
            self.try_login()
        if self.btn_goto_signup.handle_event(event):
            self.screen.goto(MODE_SIGNUP)

    # Action for when the user attempts to login
    def try_login(self):
        uname = self.username.get_value()
        pwd = self.password.get_value()

        ok, msg = user_man.verify_login(uname, pwd)
        if ok:
            self.screen.current_user = uname
            self.username.clear()
            self.password.clear()
            self.screen.goto(MODE_HOME, toast=("Logged in successfully.", Theme.SUCCESS))
        else:
            self.set_message(msg, Theme.DANGER)

    def update(self, dt_ms):
        self.username.update(dt_ms)
        self.password.update(dt_ms)
        self.btn_goto_signup.update(dt_ms)
        self.btn_login.update(dt_ms)

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill(Theme.BG)
        self.draw_card(surf, "Login")
        self.username.draw(surf)
        self.password.draw(surf)
        self.btn_goto_signup.draw(surf)
        self.btn_login.draw(surf)

# Class for the Sign Up Page
class SignupPage(ScreenBase, CardMixin):
    def __init__(self, screen):
        super().__init__(screen)
        rect = self.card_rect()
        pad_x = rect.x + 32
        y = rect.y + 88
        w = rect.w - 64

        self.username = InputBox(pad_x, y, w, 44, "New username")
        self.password = InputBox(pad_x, y + 56, w, 44, "New password", is_password=True)
        self.confirm = InputBox(pad_x, y + 112, w, 44, "Confirm password", is_password=True)
        self.btn_create = Button(pad_x, y + 176, 160, 44, "Create", primary=True)
        self.btn_back = Button(pad_x + 275, y + 176, 180, 44, "Back to Login", primary=True)
        self.username.active = True

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.screen.goto(MODE_LOGIN); return
            if event.key == pygame.K_RETURN:
                self.try_create()

        self.username.handle_event(event)
        self.password.handle_event(event)
        self.confirm.handle_event(event)

        if self.btn_create.handle_event(event):
            self.try_create()
        if self.btn_back.handle_event(event):
            self.screen.goto(MODE_LOGIN)


    def try_create(self) -> None:
        uname = self.username.get_value().strip()
        pwd1 = self.password.get_value()
        pwd2 = self.confirm.get_value()
        ok, msg = user_man.create_user(uname, pwd1, pwd2)
        if ok:
            self.username.clear(); self.password.clear(); self.confirm.clear()
            self.screen.goto(MODE_LOGIN, toast=(msg, Theme.SUCCESS))
        else:
            self.set_message(msg, Theme.DANGER)

    def update(self, dt_ms: int) -> None:
        self.username.update(dt_ms)
        self.password.update(dt_ms)
        self.confirm.update(dt_ms)
        self.btn_create.update(dt_ms)
        self.btn_back.update(dt_ms)

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill(Theme.BG)
        self.draw_card(surf, "Create account")
        self.username.draw(surf)
        self.password.draw(surf)
        self.confirm.draw(surf)
        self.btn_create.draw(surf)
        self.btn_back.draw(surf)


class HomePage(ScreenBase, CardMixin):
    # Initialize all GUI elements for the home page
    def __init__(self, screen):
        super().__init__(screen)
        rect = self.card_rect()
        self.btn_ai = Button(rect.x, rect.y, 320, 48, "Play vs AI", primary=True)
        self.btn_player = Button(rect.x, rect.y, 320, 48, "Play vs Player", primary=False)
        self.btn_record = Button(rect.x, rect.y, 320, 48, "Record", primary=False)
        self.btn_logout = Button(rect.x, rect.y, 320, 48, "Log Out", primary=False)
        self._buttons = [self.btn_ai, self.btn_player, self.btn_record, self.btn_logout]

    def _apply_vertical_layout(self) -> None:
        rect = self.card_rect()
        column_w = 320
        column_x = rect.centerx - column_w // 2
        start_y = rect.y + 96
        gap = 14
        h = 48
        for i, b in enumerate(self._buttons):
            b.rect.update(column_x, start_y + i * (h + gap), column_w, h)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.btn_ai.handle_event(event):
            main()
        if self.btn_player.handle_event(event):
            main()
        if self.btn_record.handle_event(event):
            self.set_message("Recording… (placeholder)", Theme.SUCCESS)
        if self.btn_logout.handle_event(event):
            self.screen.current_user = None
            self.screen.goto(MODE_LOGIN, toast=("You have been logged out.", Theme.MUTED))

    def update(self, dt_ms: int) -> None:
        for b in self._buttons:
            b.update(dt_ms)

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill(Theme.BG)
        title = f"Welcome, {self.screen.current_user or ''}"
        self.draw_card(surf, title)
        self._apply_vertical_layout()
        for b in self._buttons:
            b.draw(surf)

# Class for the screen
class Screen:
    def __init__(self, size: tuple[int, int] = (WIDTH, HEIGHT)):
        self.title = "CHECKERS"
        self.size = size
        self.current_user: str | None = None
        Theme.init_fonts()

        # Screens
        self._screens: dict[str, ScreenBase] = {
            MODE_LOGIN:  LoginPage(self),
            MODE_SIGNUP: SignupPage(self),
            MODE_HOME:   HomePage(self),
        }
        self._mode = MODE_LOGIN
        self._toast: tuple[str, pygame.Color] | None = None

        self._screens[self._mode].on_enter()

    # Switch screen mode between login. signup, main page
    def goto(self, mode: str, toast: tuple[str, pygame.Color] | None = None) -> None:
        self._mode = mode
        self._toast = toast
        self._screens[self._mode].on_enter()
        if self._toast:
            text, color = self._toast
            self._screens[self._mode].set_message(text, color)
            self._toast = None

    @property
    def screen(self) -> ScreenBase:
        return self._screens[self._mode]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            self.goto(MODE_SIGNUP if self._mode == MODE_LOGIN else MODE_LOGIN)
            return
        self.screen.handle_event(event)

    def update(self, dt_ms: int) -> None:
        self.screen.update(dt_ms)

    def draw(self, surf: pygame.Surface) -> None:
        self.screen.draw(surf)
