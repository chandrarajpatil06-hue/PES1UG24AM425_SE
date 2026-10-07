import math
import random
import pygame
from game.button import ChoiceButton


class GameEngine:
    HISTORY_WINDOW = 5
    MIN_HISTORY = 2

    def __init__(self, width, height, target_score=3):
        self.width = width
        self.height = height
        self.target_score = target_score

        self.choices = ["ROCK", "PAPER", "SCISSORS"]

        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(start_x, btn_y, btn_w, btn_h),
                (160, 50, 50),
                (200, 70, 70)
            ),
            ChoiceButton(
                "PAPER",
                pygame.Rect(
                    start_x + btn_w + gap,
                    btn_y,
                    btn_w,
                    btn_h
                ),
                (40, 100, 170),
                (60, 130, 210)
            ),
            ChoiceButton(
                "SCISSORS",
                pygame.Rect(
                    start_x + 2 * (btn_w + gap),
                    btn_y,
                    btn_w,
                    btn_h
                ),
                (180, 140, 30),
                (220, 180, 50)
            ),
        ]

        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0
        self.game_over = False
        self.match_winner = None
        self.player_history = []

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.reveal_started_time = 0
        self.reveal_duration = 650
        self.showing_result = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }

        return rules.get((player, cpu), "TIE")

    def predict_player_choice(self):
        if len(self.player_history) < self.MIN_HISTORY:
            return None

        recent_choices = self.player_history[-self.HISTORY_WINDOW:]
        frequencies = {
            choice: recent_choices.count(choice)
            for choice in self.choices
        }
        highest_frequency = max(frequencies.values())
        most_common_choices = [
            choice
            for choice, frequency in frequencies.items()
            if frequency == highest_frequency
        ]
        return random.choice(most_common_choices)

    def choose_cpu_choice(self):
        prediction = self.predict_player_choice()
        if prediction is None:
            return random.choice(self.choices)

        counters = {
            "ROCK": "PAPER",
            "PAPER": "SCISSORS",
            "SCISSORS": "ROCK",
        }
        return counters[prediction]

    def play_round(self, choice):
        self.player_choice = choice
        self.cpu_choice = self.choose_cpu_choice()
        self.player_history.append(choice)
        self.player_history = self.player_history[-self.HISTORY_WINDOW:]

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice
        )

        if outcome == "PLAYER":
            self.player_score += 1
            if self.player_score >= self.target_score:
                self.game_over = True
                self.match_winner = "PLAYER"
            self.result_text = (
                f"You Win! {self.player_choice} "
                f"beats {self.cpu_choice}."
            )
            self.result_color = (80, 230, 120)

        elif outcome == "CPU":
            self.cpu_score += 1
            if self.cpu_score >= self.target_score:
                self.game_over = True
                self.match_winner = "CPU"
            self.result_text = (
                f"You Lose! {self.cpu_choice} "
                f"beats {self.player_choice}."
            )
            self.result_color = (240, 80, 80)

        else:
            self.result_text = (
                f"It's a Draw! Both picked {self.player_choice}."
            )
            self.result_color = (240, 210, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()
        self.reveal_started_time = self.round_resolved_time

    def draw_gesture_icon(self, surface, choice, center):
        center_x, center_y = center
        skin = (239, 199, 155)
        outline = (65, 54, 49)
        highlight = (255, 229, 197)

        if choice == "ROCK":
            pygame.draw.rect(
                surface,
                skin,
                (center_x - 23, center_y - 13, 46, 31),
                border_radius=10
            )
            pygame.draw.rect(
                surface,
                outline,
                (center_x - 23, center_y - 13, 46, 31),
                width=3,
                border_radius=10
            )
            pygame.draw.line(
                surface,
                highlight,
                (center_x - 14, center_y - 5),
                (center_x + 14, center_y - 5),
                3
            )
            pygame.draw.line(
                surface,
                outline,
                (center_x - 8, center_y - 3),
                (center_x - 8, center_y + 7),
                2
            )
            pygame.draw.line(
                surface,
                outline,
                (center_x + 2, center_y - 3),
                (center_x + 2, center_y + 7),
                2
            )
            pygame.draw.rect(
                surface,
                skin,
                (center_x - 28, center_y - 3, 15, 16),
                border_radius=7
            )
            pygame.draw.rect(
                surface,
                outline,
                (center_x - 28, center_y - 3, 15, 16),
                width=2,
                border_radius=7
            )
        elif choice == "PAPER":
            for offset in (-17, -7, 3, 13):
                pygame.draw.rect(
                    surface,
                    skin,
                    (center_x + offset, center_y - 25, 10, 31),
                    border_radius=5
                )
                pygame.draw.rect(
                    surface,
                    outline,
                    (center_x + offset, center_y - 25, 10, 31),
                    width=2,
                    border_radius=5
                )
            pygame.draw.rect(
                surface,
                skin,
                (center_x - 21, center_y - 5, 42, 26),
                border_radius=8
            )
            pygame.draw.rect(
                surface,
                outline,
                (center_x - 21, center_y - 5, 42, 26),
                width=3,
                border_radius=8
            )
            pygame.draw.polygon(
                surface,
                skin,
                [(center_x - 19, center_y + 1),
                 (center_x - 31, center_y - 5),
                 (center_x - 35, center_y + 2),
                 (center_x - 21, center_y + 12)]
            )
            pygame.draw.lines(
                surface,
                outline,
                False,
                [(center_x - 19, center_y + 1),
                 (center_x - 31, center_y - 5),
                 (center_x - 35, center_y + 2),
                 (center_x - 21, center_y + 12)],
                2
            )
        elif choice == "SCISSORS":
            pygame.draw.polygon(
                surface,
                skin,
                [(center_x - 10, center_y + 2),
                 (center_x - 30, center_y - 24),
                 (center_x - 23, center_y - 29),
                 (center_x - 2, center_y - 7)]
            )
            pygame.draw.polygon(
                surface,
                outline,
                [(center_x - 10, center_y + 2),
                 (center_x - 30, center_y - 24),
                 (center_x - 23, center_y - 29),
                 (center_x - 2, center_y - 7)],
                width=2
            )
            pygame.draw.polygon(
                surface,
                skin,
                [(center_x + 8, center_y + 2),
                 (center_x + 24, center_y - 29),
                 (center_x + 32, center_y - 25),
                 (center_x + 17, center_y + 7)]
            )
            pygame.draw.polygon(
                surface,
                outline,
                [(center_x + 8, center_y + 2),
                 (center_x + 24, center_y - 29),
                 (center_x + 32, center_y - 25),
                 (center_x + 17, center_y + 7)],
                width=2
            )
            pygame.draw.rect(
                surface,
                skin,
                (center_x - 17, center_y - 5, 34, 27),
                border_radius=10
            )
            pygame.draw.rect(
                surface,
                outline,
                (center_x - 17, center_y - 5, 34, 27),
                width=3,
                border_radius=10
            )
            pygame.draw.circle(
                surface,
                highlight,
                (center_x - 7, center_y + 10),
                3
            )
            pygame.draw.circle(
                surface,
                highlight,
                (center_x + 7, center_y + 10),
                3
            )

    def handle_event(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_r
            and self.game_over
        ):
            self.player_score = 0
            self.cpu_score = 0
            self.player_choice = None
            self.cpu_choice = None
            self.result_text = "Make your move!"
            self.result_color = (220, 225, 235)
            self.round_resolved_time = 0
            self.showing_result = False
            self.game_over = False
            self.match_winner = None
            self.player_history.clear()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_over:
                return
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    break

    def update(self):
        now = pygame.time.get_ticks()

        if (
            self.showing_result
            and (now - self.round_resolved_time >= self.display_duration)
        ):
            self.player_choice = None
            self.cpu_choice = None
            if not self.game_over:
                self.result_text = "Make your move!"
                self.result_color = (190, 195, 205)
            self.showing_result = False

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245)
        )
        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                14
            )
        )

        p_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255)
        )

        c_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120)
        )

        screen.blit(p_surf, (35, 52))
        screen.blit(
            c_surf,
            (self.width - c_surf.get_width() - 35, 52)
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (25, 82),
            (self.width - 25, 82),
            2
        )

        if self.player_choice and self.cpu_choice:
            elapsed = pygame.time.get_ticks() - self.reveal_started_time
            progress = min(elapsed / self.reveal_duration, 1)
            shake = round(
                (1 - progress) * 9
                * math.sin(elapsed * 0.045 + math.pi / 2)
            )
            centers = (
                (self.width // 2 - 100 - shake, 145),
                (self.width // 2 + 100 + shake, 145)
            )
            labels = (
                ("Your Pick", self.player_choice, centers[0]),
                ("CPU Pick", self.cpu_choice, centers[1])
            )

            for title, choice, center in labels:
                title_surf = self.font_hud.render(
                    title,
                    True,
                    (225, 225, 230)
                )
                screen.blit(
                    title_surf,
                    (center[0] - title_surf.get_width() // 2, 88)
                )
                self.draw_gesture_icon(screen, choice, center)
                choice_surf = self.font_hud.render(
                    choice,
                    True,
                    (225, 225, 230)
                )
                screen.blit(
                    choice_surf,
                    (center[0] - choice_surf.get_width() // 2, 177)
                )
        else:
            p_str = self.player_choice if self.player_choice else "--"
            c_str = self.cpu_choice if self.cpu_choice else "--"
            arena_p = self.font_arena.render(
                f"Your Pick:  {p_str}",
                True,
                (225, 225, 230)
            )
            arena_c = self.font_arena.render(
                f"CPU Pick:  {c_str}",
                True,
                (225, 225, 230)
            )
            screen.blit(
                arena_p,
                (self.width // 2 - arena_p.get_width() // 2, 115)
            )
            screen.blit(
                arena_c,
                (self.width // 2 - arena_c.get_width() // 2, 155)
            )

        if self.game_over and not self.showing_result:
            winner_surf = self.font_title.render(
                f"{self.match_winner} WINS!",
                True,
                (100, 230, 140) if self.match_winner == "PLAYER"
                else (255, 120, 120)
            )
            restart_surf = self.font_hud.render(
                "Press R to restart",
                True,
                (225, 225, 230)
            )
            screen.blit(
                winner_surf,
                (self.width // 2 - winner_surf.get_width() // 2, 205)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, 239)
            )
        else:
            res_surf = self.font_arena.render(
                self.result_text,
                True,
                self.result_color
            )
            screen.blit(
                res_surf,
                (
                    self.width // 2 - res_surf.get_width() // 2,
                    211
                )
            )

        for btn in self.buttons:
            btn.render(screen)