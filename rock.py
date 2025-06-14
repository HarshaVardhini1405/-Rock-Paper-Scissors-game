import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 640, 480
FPS = 60
BG_COLOR = (30, 30, 30)

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
WIN_COLOR = (72, 255, 0)
LOSE_COLOR = (255, 50, 50)
DRAW_COLOR = (200, 200, 200)
BUTTON_BG = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)

CHOICES = ['Rock', 'Paper', 'Scissors']

FONT_NAME = pygame.font.match_font('arial')
FONT_LG = pygame.font.Font(FONT_NAME, 48)
FONT_MD = pygame.font.Font(FONT_NAME, 32)
FONT_SM = pygame.font.Font(FONT_NAME, 24)

def draw_text(surface, text, size, color, pos, center=False):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos
    surface.blit(text_surface, text_rect)

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.hover = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hover else BUTTON_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        draw_text(surface, self.text, 24, WHITE, self.rect.center, center=True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover and event.button == 1:
                self.callback(self.text)

class RockPaperScissorsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Rock Paper Scissors 2D")

        self.clock = pygame.time.Clock()

        self.player_choice = None
        self.computer_choice = None
        self.result = ""
        self.score_player = 0
        self.score_computer = 0
        self.score_draw = 0

        button_width = 140
        button_height = 60
        spacing = 40
        total_width = button_width * 3 + spacing * 2
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT - 100

        self.buttons = []
        for i, choice in enumerate(CHOICES):
            rect = (start_x + i * (button_width + spacing), y, button_width, button_height)
            self.buttons.append(Button(rect, choice, self.on_player_choice))

    def on_player_choice(self, choice):
        self.player_choice = choice
        self.computer_choice = random.choice(CHOICES)
        self.result = self.determine_winner(self.player_choice, self.computer_choice)
        if self.result == "You Win!":
            self.score_player += 1
        elif self.result == "You Lose!":
            self.score_computer += 1
        else:
            self.score_draw += 1

    def determine_winner(self, player, computer):
        if player == computer:
            return "Draw!"
        wins = {
            'Rock': 'Scissors',
            'Paper': 'Rock',
            'Scissors': 'Paper',
        }
        if wins[player] == computer:
            return "You Win!"
        else:
            return "You Lose!"

    def draw_choice_card(self, surface, choice, pos, title):
        card_w, card_h = 140, 180
        card_rect = pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = pos

        shadow_offset = 5
        shadow_rect = card_rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(surface, (10,10,10), shadow_rect, border_radius=16)
        pygame.draw.rect(surface, (70, 70, 70), card_rect, border_radius=16)

        icon_radius = 48
        icon_center = (card_rect.centerx, card_rect.top + 70)
        colors = {
            'Rock': (120, 120, 120),
            'Paper': (200, 200, 240),
            'Scissors': (200, 140, 140)
        }
        pygame.draw.circle(surface, colors.get(choice, (150, 150, 150)), icon_center, icon_radius)

        draw_text(surface, choice[0], 48, (255, 255, 255), icon_center, center=True)
        draw_text(surface, title, 20, WHITE, (card_rect.centerx, card_rect.top + 15), center=True)

    def draw(self):
        self.screen.fill(BG_COLOR)

        draw_text(self.screen, "Rock Paper Scissors", 48, WHITE, (WIDTH // 2, 40), center=True)
        draw_text(self.screen, "Choose your move:", 24, LIGHT_GRAY, (WIDTH // 2, 120), center=True)

        if self.player_choice:
            self.draw_choice_card(self.screen, self.player_choice, (WIDTH // 4, HEIGHT // 2), "You")

        if self.computer_choice:
            self.draw_choice_card(self.screen, self.computer_choice, (WIDTH * 3 // 4, HEIGHT // 2), "Computer")

        for button in self.buttons:
            button.draw(self.screen)

        if self.result:
            color = WIN_COLOR if self.result == "You Win!" else LOSE_COLOR if self.result == "You Lose!" else DRAW_COLOR
            draw_text(self.screen, self.result, 36, color, (WIDTH // 2, HEIGHT // 2 + 120), center=True)

        score_text = f"You: {self.score_player}    Computer: {self.score_computer}    Draws: {self.score_draw}"
        draw_text(self.screen, score_text, 20, LIGHT_GRAY, (20, 10))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                button_width = 140
                button_height = 60
                spacing = 40
                total_width = button_width * 3 + spacing * 2
                start_x = (WIDTH - total_width) // 2
                y = HEIGHT - 100
                for i, button in enumerate(self.buttons):
                    button.rect.topleft = (start_x + i * (button_width + spacing), y)
            else:
                for button in self.buttons:
                    button.handle_event(event)

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()
