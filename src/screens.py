import pygame

try:
    from PIL import Image, ImageSequence
except ImportError:
    Image = None
    ImageSequence = None
from gmat_inputs import get_gmat_inputs
from rocket import CheapRocket, MediumRocket, ExpensiveRocket
from roles import load_roles


class Screen:
    def __init__(self, surface, background, font_file):
        self.surface = surface
        self.background = background
        self.font_file = font_file

    def handle_event(self, event):
        return None

    def draw_background(self):
        self.surface.blit(self.background, (0, 0))

    def draw_button(self, rect, label, selected=False):
        color = (55, 55, 55) if rect.collidepoint(pygame.mouse.get_pos()) else "black"
        pygame.draw.rect(self.surface, color, rect)
        if selected:
            pygame.draw.rect(self.surface, "white", rect, 3)
        self.surface.blit(label, label.get_rect(center=rect.center))


class MainScreen(Screen):
    def __init__(self, surface, background, font_file):
        super().__init__(surface, background, font_file)
        self.title = pygame.font.Font(font_file, 58).render("Moonbreakers", True, "white")
        self.title_rect = self.title.get_rect(center=surface.get_rect().center)
        self.button = pygame.Rect(0, 0, 150, 60)
        self.button.centerx = surface.get_width() // 2 - 90
        self.button.bottom = surface.get_rect().bottom - 40
        self.label = pygame.font.Font(font_file, 36).render("Start", True, "white")
        self.load_button = pygame.Rect(0, 0, 150, 60)
        self.load_button.centerx = surface.get_width() // 2 + 90
        self.load_button.bottom = surface.get_rect().bottom - 40
        self.load_label = pygame.font.Font(font_file, 32).render("Load", True, "white")
        self.notice_font = pygame.font.Font(font_file, 16)
        self.notice = ""

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button.collidepoint(event.pos):
                return "difficulty"
            if self.load_button.collidepoint(event.pos):
                return "load_game"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        self.draw_button(self.button, self.label)
        self.draw_button(self.load_button, self.load_label)
        if self.notice:
            notice = self.notice_font.render(self.notice, True, "white")
            self.surface.blit(notice, notice.get_rect(center=(self.surface.get_width() // 2, 520)))


class DifficultyScreen(Screen):
    LEVELS = ("Clear skies", "First Ascent", "No mercy")

    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.title = pygame.font.Font(font_file, 42).render("Select difficulty", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 65))
        button_font = pygame.font.Font(font_file, 32)
        self.level_buttons = []
        for index, level in enumerate(self.LEVELS):
            rect = pygame.Rect(0, 0, 340, 60)
            rect.center = (surface.get_width() // 2, 155 + index * 85)
            label = button_font.render(level, True, "white")
            self.level_buttons.append((level, rect, label))
        self.back_button = pygame.Rect(0, 0, 150, 55)
        self.back_button.centerx = surface.get_rect().centerx
        self.back_button.bottom = surface.get_rect().bottom - 15
        self.back_label = button_font.render("Back", True, "white")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for level, rect, _ in self.level_buttons:
                if rect.collidepoint(event.pos):
                    self.game_state.difficulty = level
                    return "menu"
            if self.back_button.collidepoint(event.pos):
                return "main"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        for level, rect, label in self.level_buttons:
            self.draw_button(rect, label, level == self.game_state.difficulty)
        self.draw_button(self.back_button, self.back_label)


class MenuScreen(Screen):
    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.title = pygame.font.Font(font_file, 48).render("Player selection", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 55))
        self.prompt = pygame.font.Font(font_file, 30).render(
            "Select number of players:", True, "white"
        )
        self.prompt_rect = self.prompt.get_rect(center=(surface.get_width() // 2, 135))
        self.player_buttons = []
        button_font = pygame.font.Font(font_file, 30)
        for count in range(1, 5):
            column = (count - 1) % 2
            row = (count - 1) // 2
            rect = pygame.Rect(0, 0, 210, 60)
            rect.center = (surface.get_width() // 2 - 115 + column * 230, 235 + row * 85)
            label = button_font.render(f"{count} player" + ("s" if count > 1 else ""), True, "white")
            self.player_buttons.append((count, rect, label))
        self.button = pygame.Rect(0, 0, 150, 60)
        self.button.centerx = surface.get_rect().centerx
        self.button.bottom = surface.get_rect().bottom - 20
        self.label = pygame.font.Font(font_file, 36).render("Back", True, "white")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for count, rect, _ in self.player_buttons:
                if rect.collidepoint(event.pos):
                    self.game_state.set_player_count(count)
                    return "rover_intro"
            if self.button.collidepoint(event.pos):
                return "difficulty"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        self.surface.blit(self.prompt, self.prompt_rect)
        for count, rect, label in self.player_buttons:
            self.draw_button(rect, label, count == self.game_state.player_count)
        self.draw_button(self.button, self.label)


class RoleSelectionScreen(Screen):
    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.roles = load_roles()
        self.open_player = None
        self.scroll_offset = 0
        self.visible_count = 5
        self.title = pygame.font.Font(font_file, 38).render("Select player roles", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 35))
        self.font = pygame.font.Font(font_file, 24)
        self.option_font = pygame.font.Font(font_file, 22)
        self.info_font = pygame.font.Font(font_file, 18)
        x_offset = (surface.get_width() - 650) // 2
        y_offset = (surface.get_height() - 480) // 2
        self.rows = []
        for index in range(4):
            y = 75 + y_offset + index * 55
            name = self.font.render(f"Player {index + 1}", True, "white")
            name_rect = name.get_rect(midleft=(40 + x_offset, y + 21))
            dropdown = pygame.Rect(285 + x_offset, y, 345, 42)
            self.rows.append((name, name_rect, dropdown))
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.centerx = surface.get_width() // 2 - 90
        self.back_button.bottom = 350 + y_offset
        self.back_label = pygame.font.Font(font_file, 28).render("Back", True, "white")
        self.start_button = pygame.Rect(0, 0, 150, 45)
        self.start_button.centerx = surface.get_width() // 2 + 90
        self.start_button.bottom = 350 + y_offset
        self.start_label = pygame.font.Font(font_file, 28).render("Start", True, "white")
        self.info_rect = pygame.Rect(15, 365 + y_offset, surface.get_width() - 30, 100)

    def ready_to_start(self):
        return bool(self.game_state.players) and all(player.role for player in self.game_state.players)

    def available_roles(self, player_number):
        assigned_elsewhere = {
            player.role for player in self.game_state.players
            if player.number != player_number and player.role is not None
        }
        return [role for role in self.roles if role.name not in assigned_elsewhere]

    def option_rects(self, player_index):
        options = self.available_roles(player_index + 1)
        dropdown = self.rows[player_index][2]
        visible = options[self.scroll_offset:self.scroll_offset + self.visible_count]
        option_height = 35
        above = dropdown.bottom + option_height * len(visible) > self.info_rect.top
        top = dropdown.top - option_height * len(visible) if above else dropdown.bottom
        return [
            (role, pygame.Rect(dropdown.left, top + i * option_height, dropdown.width, option_height))
            for i, role in enumerate(visible)
        ]

    def fit_text(self, text, font, width):
        if font.size(text)[0] <= width:
            return text
        while text and font.size(text + "...")[0] > width:
            text = text[:-1]
        return text + "..."

    def draw_description(self, role):
        pygame.draw.rect(self.surface, "black", self.info_rect)
        pygame.draw.rect(self.surface, "white", self.info_rect, 2)
        words = (role.name + ": " + role.description).split()
        lines = []
        line = ""
        for word in words:
            candidate = (line + " " + word).strip()
            if line and self.info_font.size(candidate)[0] > self.info_rect.width - 24:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        for index, value in enumerate(lines[:4]):
            image = self.info_font.render(value, True, "white")
            self.surface.blit(image, (self.info_rect.left + 12, self.info_rect.top + 9 + index * 22))

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.open_player is not None:
            max_offset = max(0, len(self.available_roles(self.open_player + 1)) - self.visible_count)
            self.scroll_offset = max(0, min(max_offset, self.scroll_offset - event.y))
            return None
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None
        if self.open_player is not None:
            for role, rect in self.option_rects(self.open_player):
                if rect.collidepoint(event.pos):
                    self.game_state.assign_role(self.open_player + 1, role.name)
                    self.open_player = None
                    return None
        for index, (_, _, dropdown) in enumerate(self.rows[:len(self.game_state.players)]):
            if dropdown.collidepoint(event.pos):
                self.open_player = None if self.open_player == index else index
                self.scroll_offset = 0
                return None
        self.open_player = None
        if self.back_button.collidepoint(event.pos):
            return "menu"
        if self.start_button.collidepoint(event.pos) and self.ready_to_start():
            return "roster"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        hovered_role = None
        for index, (name, name_rect, dropdown) in enumerate(self.rows[:len(self.game_state.players)]):
            player = self.game_state.players[index]
            self.surface.blit(name, name_rect)
            pygame.draw.rect(self.surface, "black", dropdown)
            pygame.draw.rect(self.surface, "white", dropdown, 2)
            pygame.draw.polygon(self.surface, "white", [
                (dropdown.right - 25, dropdown.centery - 4),
                (dropdown.right - 13, dropdown.centery - 4),
                (dropdown.right - 19, dropdown.centery + 4),
            ])
            value_text = self.fit_text(player.role or "Select role", self.font, dropdown.width - 52)
            value = self.font.render(value_text, True, "white")
            self.surface.blit(value, value.get_rect(midleft=(dropdown.left + 12, dropdown.centery)))
            if player.role and dropdown.collidepoint(pygame.mouse.get_pos()):
                hovered_role = next(role for role in self.roles if role.name == player.role)
        self.draw_button(self.back_button, self.back_label)
        if self.ready_to_start():
            self.draw_button(self.start_button, self.start_label)
        else:
            pygame.draw.rect(self.surface, (35, 35, 35), self.start_button)
            self.surface.blit(
                self.start_label,
                self.start_label.get_rect(center=self.start_button.center),
            )

        if self.open_player is not None and self.open_player < len(self.game_state.players):
            for role, rect in self.option_rects(self.open_player):
                color = (55, 55, 55) if rect.collidepoint(pygame.mouse.get_pos()) else "black"
                pygame.draw.rect(self.surface, color, rect)
                pygame.draw.rect(self.surface, "white", rect, 1)
                label = self.option_font.render(
                    self.fit_text(role.name, self.option_font, rect.width - 24), True, "white"
                )
                self.surface.blit(label, label.get_rect(midleft=(rect.left + 12, rect.centery)))
                if rect.collidepoint(pygame.mouse.get_pos()):
                    hovered_role = role

        if hovered_role is not None:
            self.draw_description(hovered_role)
        elif not self.ready_to_start():
            hint = self.info_font.render("Assign a role to each player to continue.", True, "white")
            self.surface.blit(hint, hint.get_rect(center=self.info_rect.center))


class RoverIntroScreen(Screen):
    """Full-window animated scene between player count and role selection."""

    def __init__(self, surface, gif_path, font_file):
        super().__init__(surface, None, font_file)
        self.frames = []
        self.frame_durations = []
        self.total_duration_ms = 0
        if Image is not None:
            with Image.open(gif_path) as gif:
                for frame in ImageSequence.Iterator(gif):
                    rgba = frame.convert("RGBA")
                    image = pygame.image.fromstring(rgba.tobytes(), rgba.size, "RGBA").convert_alpha()
                    self.frames.append(pygame.transform.smoothscale(image, surface.get_size()))
                    duration = max(20, int(frame.info.get("duration", 100)))
                    self.frame_durations.append(duration)
                    self.total_duration_ms += duration
        else:
            first_frame = pygame.image.load(str(gif_path)).convert()
            self.frames.append(pygame.transform.scale(first_frame, surface.get_size()))
            self.frame_durations.append(100)
            self.total_duration_ms = 100

        self.back_button = pygame.Rect(20, surface.get_height() - 62, 150, 45)
        self.next_button = pygame.Rect(surface.get_width() - 170, surface.get_height() - 62, 150, 45)
        self.button_font = pygame.font.Font(font_file, 26)
        self.back_label = self.button_font.render("Back", True, "white")
        self.next_label = self.button_font.render("Next", True, "white")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "menu"
            if self.next_button.collidepoint(event.pos):
                return "roles"
        return None

    def draw(self):
        elapsed = pygame.time.get_ticks() % self.total_duration_ms
        frame_index = 0
        for index, duration in enumerate(self.frame_durations):
            if elapsed < duration:
                frame_index = index
                break
            elapsed -= duration
        self.surface.blit(self.frames[frame_index], (0, 0))
        for rect in (self.back_button, self.next_button):
            pygame.draw.rect(self.surface, (0, 0, 0, 180), rect)
            pygame.draw.rect(self.surface, "white", rect, 2)
        self.surface.blit(self.back_label, self.back_label.get_rect(center=self.back_button.center))
        self.surface.blit(self.next_label, self.next_label.get_rect(center=self.next_button.center))


class RosterSelectionScreen(Screen):
    POSITIONS = (
        "Geologist",
        "Physicists",
        "Astrobiologist",
        "Signal Engineer",
        "Astronaut",
        "Doctor",
        "Psychologist",
        "Geneticist",
        "Epidemiologist",
        "Computer Scientist/Engineer",
        "Linguist",
        "Flight Director",
        "Propulsion Engineer",
    )

    def __init__(self, surface, background, font_file, game_state, crew_icons):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.crew_icons = crew_icons
        self.title = pygame.font.Font(font_file, 38).render("Roster selection", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 40))
        self.count_font = pygame.font.Font(font_file, 17)
        self.card_font = pygame.font.Font(font_file, 12)
        self.card_width = 140
        self.card_height = 130
        self.card_gap = 10
        card_left = (surface.get_width() - 6 * self.card_width - 5 * self.card_gap) // 2
        self.position_buttons = []
        for index, position in enumerate(self.POSITIONS):
            column = index % 6
            row = index // 6
            rect = pygame.Rect(
                card_left + column * (self.card_width + self.card_gap),
                125 + row * 150,
                self.card_width,
                self.card_height,
            )
            self.position_buttons.append((position, rect, self.make_label(position)))
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.centerx = surface.get_width() // 2 - 90
        self.back_button.bottom = surface.get_rect().bottom - 15
        self.back_label = pygame.font.Font(font_file, 28).render("Back", True, "white")
        self.next_button = pygame.Rect(0, 0, 150, 45)
        self.next_button.centerx = surface.get_width() // 2 + 90
        self.next_button.bottom = surface.get_rect().bottom - 15
        self.next_label = pygame.font.Font(font_file, 28).render("Next", True, "white")

    def make_label(self, position):
        lines = []
        current = ""
        for word in position.replace("/", "/ ").split():
            while self.card_font.size(word)[0] > self.card_width - 16:
                prefix = word
                while self.card_font.size(prefix)[0] > self.card_width - 16:
                    prefix = prefix[:-1]
                if current:
                    lines.append(current)
                    current = ""
                lines.append(prefix)
                word = word[len(prefix):]
            candidate = (current + " " + word).strip()
            if current and self.card_font.size(candidate)[0] > self.card_width - 16:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        label = pygame.Surface((self.card_width - 16, len(lines) * 15), pygame.SRCALPHA)
        for index, line in enumerate(lines):
            image = self.card_font.render(line, True, "white")
            label.blit(image, image.get_rect(center=(label.get_width() // 2, 8 + index * 15)))
        return label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for position, rect, _ in self.position_buttons:
                if rect.collidepoint(event.pos):
                    self.game_state.toggle_roster_position(position)
                    return None
            if self.back_button.collidepoint(event.pos):
                return "roles"
            if self.next_button.collidepoint(event.pos) and len(self.game_state.roster) == 4:
                return "rocket_builder"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        count = self.count_font.render(f"Select 4 people: {len(self.game_state.roster)}/4", True, "white")
        self.surface.blit(count, count.get_rect(center=(self.surface.get_width() // 2, 69)))
        for position, rect, label in self.position_buttons:
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(self.surface, (55, 55, 55) if hovered else "black", rect)
            pygame.draw.rect(self.surface, "white" if position in self.game_state.roster else (160, 160, 160),
                             rect, 3 if position in self.game_state.roster else 2)
            icon = self.crew_icons[position]
            self.surface.blit(icon, icon.get_rect(center=(rect.centerx, rect.top + 43)))
            self.surface.blit(label, label.get_rect(center=(rect.centerx, rect.bottom - 27)))
        self.draw_button(self.back_button, self.back_label)
        if len(self.game_state.roster) == 4:
            self.draw_button(self.next_button, self.next_label)
        else:
            pygame.draw.rect(self.surface, (35, 35, 35), self.next_button)
            self.surface.blit(self.next_label, self.next_label.get_rect(center=self.next_button.center))


MISSION_BUDGET = 8_000_000_000
DIFFICULTY_BUDGETS = {
    "Clear skies": 8_000_000_000,
    "First Ascent": 3_500_000_000,
    "No mercy": 1_200_000_000,
}


def mission_budget(game_state):
    return DIFFICULTY_BUDGETS.get(game_state.difficulty, MISSION_BUDGET)
INSTRUMENT_ITEMS = (
    ("Hyperspectral Imager", 0, "Mass: 11.3 kg."),
    ("Lunar Magnetometer", 4_000_000, "Detects and measures the intensity of magnetic fields on the Moon."),
    ("X-Ray Spectrometer", 35_000, "Identifies elemental composition. Mass: 6.8 kg."),
    ("Food", 35_000, "Food is priced per kg per day for each astronaut. Total: $35,000 × days × 4 astronauts."),
    ("Infrared (Thermal) Camera", 80_000, "Detects infrared radiation. Mass: 5.4 kg."),
    ("Star Trackers", 0, "Two star trackers. Combined mass: 6.8 kg."),
    ("Flash LIDAR System", 4_500_000, "3D terrain scanner. Mass: 20.4 kg."),
    ("Ka-Band Radar Altimeter", 3_000_000, "Measures lunar altitude and descent speed. Mass: 13.6 kg."),
    ("Deep-Space Transponder", 2_500_000, "Two-way high-frequency radio. Mass: 11.3 kg."),
    ("Radiation Dosimeter", 400_000, "Four dosimeters. Combined mass: 3.6 kg."),
    ("Cabin Atmosphere Monitor", 0, "Monitors cabin air. Mass: 15.9 kg."),
)
ROCKET_PART_ITEMS = (
    ("Main Cryogenic Engines", 75_000_000, "Five engines. Combined mass: 8.16 t."),
    ("Lunar Lander Descent Engine", 25_000_000, "Throttleable landing engine. Mass: 0.54 t."),
    ("RCS Thruster Pod", 8_000_000, "Sixteen steering thrusters. Combined mass: 0.43 t."),
    ("Cryogenic Propellant Tanks", 40_000_000, "Mass: 20.41 t."),
    ("Thermal Protection Heat Shield", 35_000_000, "Mass: 2.95 t."),
    ("Multi-Layer Insulation (MLI)", 0, "Thermal insulation. Mass: 0.36 t."),
    ("Landing Legs", 12_000_000, "Sixteen landing legs. Combined mass: 1.91 t."),
)
INSTRUMENT_WEIGHTS_KG = {
    "Hyperspectral Imager": 11.3, "Lunar Magnetometer": 8.2, "X-Ray Spectrometer": 6.8,
    "Food": 0.0, "Infrared (Thermal) Camera": 5.4, "Star Trackers": 6.8,
    "Flash LIDAR System": 20.4, "Ka-Band Radar Altimeter": 13.6,
    "Deep-Space Transponder": 11.3, "Radiation Dosimeter": 3.6,
    "Cabin Atmosphere Monitor": 15.9,
}
ROCKET_PART_WEIGHTS_KG = {
    "Main Cryogenic Engines": 8160, "Lunar Lander Descent Engine": 540,
    "RCS Thruster Pod": 430, "Cryogenic Propellant Tanks": 20410,
    "Thermal Protection Heat Shield": 2950, "Multi-Layer Insulation (MLI)": 360,
    "Landing Legs": 1910,
}
MISSION_DAYS = 9
MISSION_FUEL_KG = 958 * MISSION_DAYS
PROPELLANT_OPTIONS = (
    ("RP-1", 3.07, 3.0),
    ("Liquid Methane", 1.6, 3.5),
    ("Liquid Hydrogen", 0.27, 3.0),
)


class ItemBudgetScreen(Screen):
    ITEM_LIST = ()
    STATE_KEY = ""
    TITLE = ""
    BACK_SCREEN = ""
    NEXT_SCREEN = ""
    ROW_START_Y = 95

    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.title = pygame.font.Font(font_file, 34).render(self.TITLE, True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 45))
        self.font = pygame.font.Font(font_file, 15)
        self.price_item_font = pygame.font.Font(font_file, 13)
        self.small_font = pygame.font.Font(font_file, 15)
        self.budget_font = pygame.font.Font(font_file, 18)
        self.rows = []
        for index, item in enumerate(self.ITEM_LIST):
            col, row = divmod(index, 5)
            x, y = 30 + col * 465, self.ROW_START_Y + row * 58
            row_rect = pygame.Rect(x, y, 440, 50)
            minus_rect = pygame.Rect(x + 330, y + 8, 30, 32)
            plus_rect = pygame.Rect(x + 400, y + 8, 30, 32)
            self.rows.append((item, row_rect, minus_rect, plus_rect))
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.center = (surface.get_width() // 2 - 90, surface.get_height() - 38)
        self.next_button = pygame.Rect(0, 0, 150, 45)
        self.next_button.center = (surface.get_width() // 2 + 90, surface.get_height() - 38)
        button_font = pygame.font.Font(font_file, 28)
        self.back_label = button_font.render("Back", True, "white")
        self.next_label = button_font.render("Next", True, "white")

    def quantities(self):
        values = self.game_state.mission_customizations.setdefault(self.STATE_KEY, {})
        if isinstance(values, list):
            values = {name: 1 for name in values}
            self.game_state.mission_customizations[self.STATE_KEY] = values
        return values

    @staticmethod
    def mission_total_cost(game_state):
        part_values = game_state.mission_customizations.get("rocket_parts", {})
        instrument_values = game_state.mission_customizations.get("instruments", {})
        if isinstance(part_values, list):
            part_values = {name: 1 for name in part_values}
        if isinstance(instrument_values, list):
            instrument_values = {name: 1 for name in instrument_values}
        part_prices = {name: price for name, price, _ in ROCKET_PART_ITEMS}
        instrument_prices = {name: price for name, price, _ in INSTRUMENT_ITEMS}
        rocket_cost = game_state.rocket.price if game_state.rocket else 0
        propellant_cost = 0
        propellant_name = game_state.mission_customizations.get("propellant_type")
        propellants = {name: price for name, _, price in PROPELLANT_OPTIONS}
        if propellant_name in propellants:
            propellant_cost = MISSION_FUEL_KG * propellants[propellant_name]
        instrument_cost = sum(instrument_prices.get(name, 0) * int(count) *
                              (4 if name == "Food" else 1) for name, count in instrument_values.items())
        return rocket_cost + propellant_cost + sum(
            part_prices.get(name, 0) * int(count) for name, count in part_values.items()
        ) + instrument_cost

    def total_cost(self):
        return self.mission_total_cost(self.game_state)

    @staticmethod
    def current_dry_mass_kg(game_state):
        parts = game_state.mission_customizations.get("rocket_parts", {})
        instruments = game_state.mission_customizations.get("instruments", {})
        if isinstance(parts, list):
            parts = {name: 1 for name in parts}
        if isinstance(instruments, list):
            instruments = {name: 1 for name in instruments}
        part_mass = sum(ROCKET_PART_WEIGHTS_KG.get(name, 0) * int(count) for name, count in parts.items())
        instrument_mass = sum(INSTRUMENT_WEIGHTS_KG.get(name, 0) * int(count)
                              for name, count in instruments.items())
        return part_mass + instrument_mass

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None
        if self.back_button.collidepoint(event.pos):
            return self.BACK_SCREEN
        if self.next_button.collidepoint(event.pos):
            return self.NEXT_SCREEN
        values = self.quantities()
        for (name, price, _), row_rect, minus_rect, plus_rect in self.rows:
            count = int(values.get(name, 0))
            if minus_rect.collidepoint(event.pos) and count > 0:
                values[name] = count - 1
            elif plus_rect.collidepoint(event.pos):
                values[name] = count + 1
            elif row_rect.collidepoint(event.pos):
                return None
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        remaining = mission_budget(self.game_state) - self.total_cost()
        budget = self.budget_font.render(f"Budget remaining: ${remaining:,.0f}", True, "white")
        self.surface.blit(budget, budget.get_rect(topright=(935, 64)))
        if self.game_state.rocket is not None:
            mass = self.current_dry_mass_kg(self.game_state)
            capacity = self.game_state.rocket.max_dry_mass_kg
            is_heavy = mass > capacity
            label = "TOO HEAVY" if is_heavy else f"Dry mass: {mass:,.1f} / {capacity:,.0f} kg"
            color = (255, 75, 75) if is_heavy else "white"
            self.surface.blit(self.budget_font.render(label, True, color), (30, 68))
        values = self.quantities()
        mouse = pygame.mouse.get_pos()
        hovered_description = ""
        for (name, price, description), row_rect, minus_rect, plus_rect in self.rows:
            pygame.draw.rect(self.surface, "black", row_rect)
            pygame.draw.rect(self.surface, "white", row_rect, 1)
            quantity = int(values.get(name, 0))
            label = self.font.render(name, True, "white")
            price_text = f"${price:,.0f} p/kg" if name == "Food" else f"${price:,.0f}"
            price_label = self.price_item_font.render(price_text, True, (220, 220, 220))
            self.surface.blit(label, (row_rect.left + 9, row_rect.top + 3))
            self.surface.blit(price_label, (row_rect.left + 9, row_rect.top + 26))
            quantity_text = f"{quantity} days" if name == "Food" else str(quantity)
            quantity_label = self.small_font.render(quantity_text, True, "white")
            self.surface.blit(quantity_label, quantity_label.get_rect(center=(row_rect.left + 380, row_rect.centery)))
            for rect, symbol in ((minus_rect, "-"), (plus_rect, "+")):
                pygame.draw.rect(self.surface, (55, 55, 55) if rect.collidepoint(mouse) else (20, 20, 20), rect)
                pygame.draw.rect(self.surface, "white", rect, 1)
                text = self.small_font.render(symbol, True, "white")
                self.surface.blit(text, text.get_rect(center=rect.center))
            if row_rect.collidepoint(mouse):
                hovered_description = description
        if hovered_description:
            description_image = self.small_font.render(hovered_description, True, "white")
            pygame.draw.rect(self.surface, "black", (30, 395, 900, 28))
            self.surface.blit(description_image, (40, 400))
        self.draw_button(self.back_button, self.back_label)
        self.draw_button(self.next_button, self.next_label)


class InstrumentationScreen(ItemBudgetScreen):
    ITEM_LIST = INSTRUMENT_ITEMS
    STATE_KEY = "instruments"
    TITLE = "Instruments and resources"
    BACK_SCREEN = "rocket_configuration"
    NEXT_SCREEN = "spacecraft_setup"


class LaunchScreen(Screen):
    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.title = pygame.font.Font(font_file, 38).render("Launch", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 45))
        self.font = pygame.font.Font(font_file, 17)
        self.status = ""
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.centerx = surface.get_width() // 2 - 250
        self.back_button.bottom = surface.get_rect().bottom - 15
        self.back_label = pygame.font.Font(font_file, 28).render("Back", True, "white")
        self.launch_button = pygame.Rect(0, 0, 150, 45)
        self.launch_button.centerx = surface.get_width() // 2 - 70
        self.launch_button.bottom = surface.get_rect().bottom - 15
        self.launch_label = pygame.font.Font(font_file, 27).render("Launch", True, "white")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "spacecraft_setup"
            if self.launch_button.collidepoint(event.pos):
                if self.game_state.mission_customizations.get("simulation_mode") == "Demo":
                    return "run_demo"
                return "run_simulation"
        return None

    def draw(self):
        self.draw_background()
        panel = pygame.Surface((900, 365), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 175))
        self.surface.blit(panel, (30, 80))
        self.surface.blit(self.title, self.title_rect)
        rocket_name = self.game_state.rocket.name if self.game_state.rocket else "Not selected"
        spacecraft = self.game_state.mission_customizations.get("spacecraft", {})
        spacecraft_summary = "Not entered"
        if spacecraft:
            spacecraft_summary = (
                f"{spacecraft.get('dry_mass_kg', '?')} kg dry, "
                f"{spacecraft.get('tank_count', '?')} tanks, "
                f"{spacecraft.get('fuel_per_tank_kg', '?')} kg fuel per tank"
            )
        summary = [
            "Difficulty: " + (self.game_state.difficulty or "Not selected"),
            "Players: " + str(self.game_state.player_count or 0),
        ]
        summary.extend(
            f"Player {player.number} role: {player.role or 'Not selected'}"
            for player in self.game_state.players
        )
        summary.extend([
            "Rocket: " + rocket_name,
            "Spacecraft: " + spacecraft_summary,
            "Roster: " + (", ".join(self.game_state.roster) or "Not selected"),
        ])
        y = 100
        for value in summary:
            words = value.split()
            line = ""
            lines = []
            for word in words:
                candidate = (line + " " + word).strip()
                if line and self.font.size(candidate)[0] > self.surface.get_width() - 100:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            if line:
                lines.append(line)
            for part in lines:
                image = self.font.render(part, True, "white")
                self.surface.blit(image, (50, y))
                y += 20
            y += 3
        self.draw_button(self.back_button, self.back_label)
        self.draw_button(self.launch_button, self.launch_label)
        if self.status:
            status_image = self.font.render(self.status, True, "white")
            self.surface.blit(status_image, (50, 445))


class TrajectoryScreen(Screen):
    def __init__(self, surface, background, font_file):
        super().__init__(surface, background, font_file)
        self.title = pygame.font.Font(font_file, 36).render("GMAT trajectory", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 45))
        self.font = pygame.font.Font(font_file, 19)
        self.result = {"status": "idle"}
        self.started_at = None
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.centerx = surface.get_width() // 2
        self.back_button.bottom = surface.get_rect().bottom - 15
        self.back_label = pygame.font.Font(font_file, 28).render("Back", True, "white")

    def handle_event(self, event):
        if self.result["status"] != "running" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "launch"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        status = self.result["status"]
        if status == "running":
            message = self.font.render("Calculating trajectory with GMAT...", True, "white")
            self.surface.blit(message, message.get_rect(center=self.surface.get_rect().center))
            return
        if status == "error":
            message = self.font.render("GMAT could not calculate this mission.", True, "white")
            self.surface.blit(message, message.get_rect(center=(self.surface.get_width() // 2, 230)))
            detail = self.font.render(self.result["message"][:85], True, "white")
            self.surface.blit(detail, detail.get_rect(center=(self.surface.get_width() // 2, 270)))
            self.draw_button(self.back_button, self.back_label)
            return
        if status != "ready":
            self.draw_button(self.back_button, self.back_label)
            return

        trajectory = self.result["trajectory"]
        if self.started_at is None:
            self.started_at = pygame.time.get_ticks()
        elapsed = pygame.time.get_ticks() - self.started_at
        progress = min(1, elapsed / 20000)
        current_index = min(len(trajectory) - 1, int(progress * (len(trajectory) - 1)))
        pygame.draw.rect(self.surface, "black", (25, 95, 440, 320))
        pygame.draw.rect(self.surface, "black", (495, 95, 440, 320))
        earth_title = self.font.render("Earth view (XY projection)", True, "white")
        moon_title = self.font.render("Moon view (within 50,000 km)", True, "white")
        self.surface.blit(earth_title, (45, 108))
        self.surface.blit(moon_title, (515, 108))

        moon_positions = [(point[1] - point[4], point[2] - point[5]) for point in trajectory]
        all_x = [0] + [point[1] for point in trajectory] + [position[0] for position in moon_positions]
        all_y = [0] + [point[2] for point in trajectory] + [position[1] for position in moon_positions]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        earth_scale = min(390 / max(max_x - min_x, 1), 240 / max(max_y - min_y, 1))
        world_center_x = (min_x + max_x) / 2
        world_center_y = (min_y + max_y) / 2

        def earth_pixel(x, y):
            return (round(245 + (x - world_center_x) * earth_scale),
                    round(270 - (y - world_center_y) * earth_scale))

        moon_path = [earth_pixel(*position) for position in moon_positions[:current_index + 1]]
        if len(moon_path) > 1:
            pygame.draw.lines(self.surface, (110, 110, 145), False, moon_path, 1)
        craft_path = [earth_pixel(point[1], point[2]) for point in trajectory[:current_index + 1]]
        if len(craft_path) > 1:
            pygame.draw.lines(self.surface, "white", False, craft_path, 2)
        earth_center = earth_pixel(0, 0)
        pygame.draw.circle(self.surface, (45, 120, 220), earth_center, max(6, min(20, round(6378 * earth_scale))))
        pygame.draw.circle(self.surface, (180, 180, 190), moon_path[-1], 7)
        pygame.draw.circle(self.surface, (255, 190, 45), craft_path[-1], 6)
        self.surface.blit(self.font.render("Earth", True, "white"), (earth_center[0] + 10, earth_center[1] - 14))
        self.surface.blit(self.font.render("Moon", True, "white"), (moon_path[-1][0] + 10, moon_path[-1][1] - 14))

        moon_center = (715, 270)
        moon_scale = min(190 / 50000, 120 / 50000)
        pygame.draw.circle(self.surface, (180, 180, 190), moon_center, max(7, round(1737 * moon_scale)))
        previous = None
        for point in trajectory[:current_index + 1]:
            relative_x, relative_y = point[4], point[5]
            if point[7] <= 50000:
                pixel = (round(moon_center[0] + relative_x * moon_scale),
                         round(moon_center[1] - relative_y * moon_scale))
                if previous is not None:
                    pygame.draw.line(self.surface, "white", previous, pixel, 2)
                previous = pixel
            else:
                previous = None
        current = trajectory[current_index]
        if current[7] <= 50000:
            pygame.draw.circle(self.surface, (255, 190, 45),
                               (round(moon_center[0] + current[4] * moon_scale),
                                round(moon_center[1] - current[5] * moon_scale)), 6)
        else:
            message = self.font.render("Spacecraft outside close-up", True, "white")
            self.surface.blit(message, message.get_rect(center=(715, 385)))

        moon_distance = current[7]
        closest_distance = min(point[7] for point in trajectory[:current_index + 1])
        detail = self.font.render(
            f"Moon distance: {moon_distance:,.0f} km    Closest: {closest_distance:,.0f} km", True, "white"
        )
        self.surface.blit(detail, detail.get_rect(center=(self.surface.get_width() // 2, 445)))
        self.draw_button(self.back_button, self.back_label)


class RocketBuilderScreen(Screen):
    ROCKET_TYPES = (CheapRocket, MediumRocket, ExpensiveRocket)

    def __init__(self, surface, background, font_file, game_state, price_coins, rocket_images):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.price_coins = price_coins
        self.rocket_images = rocket_images
        self.title = pygame.font.Font(font_file, 36).render("Rocket Options", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 55))
        self.budget_font = pygame.font.Font(font_file, 18)
        button_font = pygame.font.Font(font_file, 23)
        self.price_font = pygame.font.Font(font_file, 21)
        self.rocket_buttons = []
        for index, rocket_type in enumerate(self.ROCKET_TYPES):
            rect = pygame.Rect(0, 0, 270, 350)
            rect.topleft = (30 + index * 300, 105)
            label = button_font.render(rocket_type.name, True, "white")
            self.rocket_buttons.append((rocket_type, rect, label))
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.centerx = surface.get_width() // 2 - 90
        self.back_button.bottom = surface.get_rect().bottom - 15
        self.back_label = pygame.font.Font(font_file, 28).render("Back", True, "white")
        self.next_button = pygame.Rect(0, 0, 150, 45)
        self.next_button.centerx = surface.get_width() // 2 + 90
        self.next_button.bottom = surface.get_rect().bottom - 15
        self.next_label = pygame.font.Font(font_file, 28).render("Next", True, "white")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rocket_type, rect, _ in self.rocket_buttons:
                if rect.collidepoint(event.pos):
                    self.game_state.rocket = rocket_type()
                    return None
            if self.back_button.collidepoint(event.pos):
                return "roster"
            if self.next_button.collidepoint(event.pos) and self.game_state.rocket is not None:
                return "rocket_configuration"
        return None

    def draw(self):
        self.draw_background()
        self.surface.blit(self.title, self.title_rect)
        remaining = mission_budget(self.game_state) - ItemBudgetScreen.mission_total_cost(self.game_state)
        budget = self.budget_font.render(f"Budget remaining: ${remaining:,.0f}", True, "white")
        self.surface.blit(budget, budget.get_rect(topright=(935, 76)))
        for rocket_type, rect, label in self.rocket_buttons:
            selected = isinstance(self.game_state.rocket, rocket_type)
            pygame.draw.rect(self.surface, (40, 40, 40), rect)
            pygame.draw.rect(self.surface, "white" if selected else (160, 160, 160), rect, 4 if selected else 2)
            rocket_image = self.rocket_images[rocket_type.price_tier]
            self.surface.blit(rocket_image, rocket_image.get_rect(center=(rect.centerx, rect.top + 155)))
            self.surface.blit(label, label.get_rect(center=(rect.centerx, rect.top + 285)))
            price_label = self.price_font.render(f"${rocket_type.price:,.0f}", True, "white")
            self.surface.blit(price_label, price_label.get_rect(center=(rect.centerx, rect.top + 320)))
        self.draw_button(self.back_button, self.back_label)
        if self.game_state.rocket is not None:
            self.draw_button(self.next_button, self.next_label)
        else:
            pygame.draw.rect(self.surface, (35, 35, 35), self.next_button)
            self.surface.blit(self.next_label, self.next_label.get_rect(center=self.next_button.center))


class RocketConfigurationScreen(ItemBudgetScreen):
    ITEM_LIST = ROCKET_PART_ITEMS
    STATE_KEY = "rocket_parts"
    TITLE = "Rocket Configuration"
    BACK_SCREEN = "rocket_builder"
    NEXT_SCREEN = "instrumentation"
    ROW_START_Y = 140

    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file, game_state)
        self.propellant_font = pygame.font.Font(font_file, 17)
        self.propellant_button = pygame.Rect(30, 98, 290, 36)
        self.propellant_open = False
        self.propellant_option_rects = []

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.propellant_open:
                for option, rect in zip(PROPELLANT_OPTIONS, self.propellant_option_rects):
                    if rect.collidepoint(event.pos):
                        self.game_state.mission_customizations["propellant_type"] = option[0]
                        self.propellant_open = False
                        return None
                self.propellant_open = False
            if self.propellant_button.collidepoint(event.pos):
                self.propellant_open = not self.propellant_open
                return None
        return super().handle_event(event)

    def draw(self):
        super().draw()
        selected = self.game_state.mission_customizations.get("propellant_type", "Select propellant")
        pygame.draw.rect(self.surface, "black", self.propellant_button)
        pygame.draw.rect(self.surface, "white", self.propellant_button, 2)
        label = self.propellant_font.render(f"Propellant: {selected}  ▼", True, "white")
        self.surface.blit(label, (self.propellant_button.left + 8, self.propellant_button.top + 9))
        self.propellant_option_rects = []
        mouse = pygame.mouse.get_pos()
        hovered = None
        if self.propellant_open:
            for index, (name, density, price) in enumerate(PROPELLANT_OPTIONS):
                rect = pygame.Rect(self.propellant_button.left, self.propellant_button.bottom + index * 34,
                                   self.propellant_button.width, 34)
                self.propellant_option_rects.append(rect)
                pygame.draw.rect(self.surface, (60, 60, 60) if rect.collidepoint(mouse) else "black", rect)
                pygame.draw.rect(self.surface, "white", rect, 1)
                option_label = self.propellant_font.render(name, True, "white")
                self.surface.blit(option_label, (rect.left + 8, rect.top + 8))
                if rect.collidepoint(mouse):
                    hovered = (density, price)
        if hovered:
            detail = self.small_font.render(f"{hovered[0]:g} kg/gas  |  ${hovered[1]:g} per kg", True, "white")
            pygame.draw.rect(self.surface, "black", (330, 82, 360, 38))
            self.surface.blit(detail, (340, 93))


class SpacecraftSetupScreen(Screen):
    INPUTS = (
        ("thruster_count", "Thrusters (1-4)", "Number of identical thrusters used for the maneuver."),
        ("thrust_per_thruster_n", "Thrust / thruster (N)", "Force produced by each thruster while it is firing."),
        ("specific_impulse_s", "Specific impulse (s)", "Measure of how efficiently the thruster uses fuel."),
        ("duty_cycle_percent", "Duty cycle (%)", "Percentage of the burn time when the thrusters are firing."),
        ("burn_duration_s", "Burn duration (s)", "Length of the powered maneuver in seconds."),
        ("orbit_altitude_km", "Start orbit (km)", "Altitude of the starting circular Earth orbit."),
        ("burn_angle_deg", "Burn angle (deg)", "Thrust angle from forward orbital motion, where zero means prograde."),
    )
    OPTIONS = {
        "thruster_count": ("1", "2", "3", "4"),
        "thrust_per_thruster_n": ("1000", "5000", "10000", "25000"),
        "specific_impulse_s": ("200", "300", "350", "450"),
        "duty_cycle_percent": ("25", "50", "75", "100"),
        "burn_duration_s": ("600", "1800", "3600", "7200"),
        "orbit_altitude_km": ("200", "300", "400", "500"),
        "burn_angle_deg": ("0", "45", "90", "180"),
    }

    def __init__(self, surface, background, font_file, game_state):
        super().__init__(surface, background, font_file)
        self.game_state = game_state
        self.active_field = None
        self.simulation_mode = "Player spacecraft"
        self.mode_rect = pygame.Rect(720, 20, 205, 38)
        self.mode_options = []
        self.title = pygame.font.Font(font_file, 34).render("Spacecraft configuration", True, "white")
        self.title_rect = self.title.get_rect(center=(surface.get_width() // 2, 55))
        self.label_font = pygame.font.Font(font_file, 19)
        self.value_font = pygame.font.Font(font_file, 22)
        self.help_font = pygame.font.Font(font_file, 17)
        self.fields = []
        self.option_rects = []
        self.option_font = pygame.font.Font(font_file, 20)
        for index, (key, label, description) in enumerate(self.INPUTS):
            column = index // 4
            row = index % 4
            x = 35 + column * 465
            y = 165 + row * 57
            label_image = self.label_font.render(label, True, "white")
            field_rect = pygame.Rect(x + 265, y, 145, 40)
            hover_rect = pygame.Rect(x, y, 410, 40)
            self.fields.append((key, label_image, description, field_rect, hover_rect))
        button_font = pygame.font.Font(font_file, 28)
        self.back_button = pygame.Rect(0, 0, 150, 45)
        self.back_button.centerx = surface.get_width() // 2 - 90
        self.back_button.bottom = surface.get_rect().bottom - 15
        self.back_label = button_font.render("Back", True, "white")
        self.next_button = pygame.Rect(0, 0, 150, 45)
        self.next_button.centerx = surface.get_width() // 2 + 90
        self.next_button.bottom = surface.get_rect().bottom - 15
        self.next_label = button_font.render("Next", True, "white")

    def values(self):
        values = self.game_state.mission_customizations.setdefault("spacecraft", {})
        rocket = self.game_state.rocket
        if rocket is not None:
            dry_mass = ItemBudgetScreen.current_dry_mass_kg(self.game_state)
            tank_count = rocket.tank_count
            # GMAT's current reference trajectory does not use player mass, but
            # the input validator expects a positive spacecraft mass.
            values["dry_mass_kg"] = str(max(dry_mass, 0.1))
            values["tank_count"] = str(tank_count)
            values["fuel_per_tank_kg"] = str(MISSION_FUEL_KG / tank_count)
        return values

    def ready_to_continue(self):
        try:
            get_gmat_inputs(self.game_state)
            return True
        except ValueError:
            return False

    def validation_message(self):
        try:
            get_gmat_inputs(self.game_state)
            return ""
        except ValueError as error:
            return str(error)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.active_field == "simulation_mode":
                for value, option_rect in zip(("Player spacecraft", "Demo"), self.mode_options):
                    if option_rect.collidepoint(event.pos):
                        self.game_state.mission_customizations["simulation_mode"] = value
                        self.active_field = None
                        return None
                self.active_field = None
            if self.mode_rect.collidepoint(event.pos):
                self.active_field = "simulation_mode"
                return None
            if self.active_field is not None:
                for option_index, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        key = self.fields[self.active_field][0]
                        self.values()[key] = self.OPTIONS[key][option_index]
                        self.active_field = None
                        return None
                self.active_field = None
            if self.back_button.collidepoint(event.pos):
                return "instrumentation"
            if self.next_button.collidepoint(event.pos):
                return "launch"
            self.active_field = None
            for index, (_, _, _, field_rect, _) in enumerate(self.fields):
                if field_rect.collidepoint(event.pos):
                    self.active_field = index
                    break
        return None

    def draw(self):
        self.draw_background()
        pygame.draw.rect(self.surface, "black", (20, 95, 920, 300))
        self.surface.blit(self.title, self.title_rect)
        mode = self.game_state.mission_customizations.get("simulation_mode", "Player spacecraft")
        pygame.draw.rect(self.surface, "black", self.mode_rect)
        pygame.draw.rect(self.surface, "white", self.mode_rect, 2)
        mode_label = self.help_font.render("Mode: " + mode, True, "white")
        self.surface.blit(mode_label, mode_label.get_rect(center=self.mode_rect.center))
        values = self.values()
        if self.game_state.rocket is not None:
            dry_mass = ItemBudgetScreen.current_dry_mass_kg(self.game_state)
            capacity = self.game_state.rocket.max_dry_mass_kg
            mass_text = ("TOO HEAVY" if dry_mass > capacity else f"Dry mass: {dry_mass:,.1f} / {capacity:,.0f} kg")
            mass_color = (255, 75, 75) if dry_mass > capacity else "white"
            tank_text = f"Fuel tanks: {self.game_state.rocket.tank_count}    Mission fuel: {MISSION_FUEL_KG:,.0f} kg ({MISSION_DAYS} days)"
            self.surface.blit(self.label_font.render(mass_text, True, mass_color), (40, 105))
            self.surface.blit(self.label_font.render(tank_text, True, "white"), (40, 133))
        hovered_description = "Hover over an input for a one-sentence explanation."
        mouse_position = pygame.mouse.get_pos()
        for index, (key, label, description, field_rect, hover_rect) in enumerate(self.fields):
            self.surface.blit(label, (hover_rect.left, hover_rect.top + 9))
            color = (55, 55, 55) if hover_rect.collidepoint(mouse_position) else "black"
            pygame.draw.rect(self.surface, color, field_rect)
            pygame.draw.rect(self.surface, "white" if index == self.active_field else (160, 160, 160), field_rect, 2)
            value_image = self.value_font.render(values.get(key, "Select"), True, "white")
            self.surface.blit(value_image, (field_rect.left + 8, field_rect.top + 7))
            if hover_rect.collidepoint(mouse_position):
                hovered_description = description
        pygame.draw.rect(self.surface, "black", (30, 405, 900, 57))
        pygame.draw.rect(self.surface, "white", (30, 405, 900, 57), 2)
        help_image = self.help_font.render(hovered_description, True, "white")
        self.surface.blit(help_image, (45, 423))
        self.draw_button(self.back_button, self.back_label)
        self.draw_button(self.next_button, self.next_label)
        self.option_rects = []
        if self.active_field is not None:
            key = self.fields[self.active_field][0]
            _, _, _, field_rect, _ = self.fields[self.active_field]
            menu = pygame.Rect(field_rect.left - 20, field_rect.bottom + 2, 185, 4 * 30 + 8)
            if menu.bottom > 490:
                menu.bottom = field_rect.top - 2
            pygame.draw.rect(self.surface, "black", menu)
            pygame.draw.rect(self.surface, "white", menu, 2)
            for option_index, option in enumerate(self.OPTIONS[key]):
                option_rect = pygame.Rect(menu.left + 4, menu.top + 4 + option_index * 30, menu.width - 8, 30)
                self.option_rects.append(option_rect)
                pygame.draw.rect(self.surface, (55, 55, 55) if option_rect.collidepoint(mouse_position) else "black", option_rect)
                option_image = self.option_font.render(option, True, "white")
                self.surface.blit(option_image, option_image.get_rect(center=option_rect.center))
        self.mode_options = []
        if self.active_field == "simulation_mode":
            for index, value in enumerate(("Player spacecraft", "Demo")):
                option_rect = pygame.Rect(self.mode_rect.left, self.mode_rect.bottom + index * 30, self.mode_rect.width, 30)
                self.mode_options.append(option_rect)
                pygame.draw.rect(self.surface, "black", option_rect)
                pygame.draw.rect(self.surface, "white", option_rect, 1)
                option_image = self.help_font.render(value, True, "white")
                self.surface.blit(option_image, option_image.get_rect(center=option_rect.center))
        validation_message = self.validation_message()
        if validation_message:
            message = self.help_font.render(validation_message[:95], True, (255, 210, 120))
            self.surface.blit(message, message.get_rect(center=(self.surface.get_width() // 2, 480)))
