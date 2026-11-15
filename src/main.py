import threading

import pygame

from game_state import GameState
from gmat_simulation import run_gmat_simulation, run_lunar_transfer_demo
from load import load_game
from save import save_before_simulation, save_game
from screens import AnalysisResultsScreen, DifficultyScreen, EndingScreen, InstrumentationScreen, JournalScreen, LaunchScreen, MainScreen, MenuScreen, MissionChoiceScreen, RocketBuilderScreen, RocketConfigurationScreen, RoleSelectionScreen, RosterSelectionScreen, RoverIntroScreen, SpacecraftSetupScreen, StoryScreen, TrajectoryScreen
from story import JOURNAL_ENTRIES, STORY_WINDOWS


def main():
    pygame.init()
    try:
        pygame.mixer.music.load("../Assets/audio/absounds-80s-montage-256202.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except (pygame.error, OSError):
        pass
    screen = pygame.display.set_mode((1028, 620))
    pygame.display.set_caption("Moonbreakers")


    pygame.font.Font("../Assets/font/RasterForgeRegular-JpBgm.ttf", 58)
    font_file = "../Assets/font/RasterForgeRegular-JpBgm.ttf"

    icon = pygame.image.load("../Assets/images/Moon_Rotating.gif")
    pygame.display.set_icon(icon)
    space_background = pygame.image.load("../Assets/images/blue-expanded.png")
    space_background = pygame.transform.scale(space_background, screen.get_size())

    mission_control_bg = pygame.image.load("../Assets/images/Mission Control.png")
    mission_control_bg = pygame.transform.scale(mission_control_bg, screen.get_size())

    computer_bg = pygame.image.load("../Assets/images/Computer_screen.png")
    computer_bg = pygame.transform.scale(computer_bg, screen.get_size())

    board_room_bg = pygame.image.load("../Assets/images/Board_room.png")
    board_room_bg = pygame.transform.scale(board_room_bg, screen.get_size())

    drawing_board_bg = pygame.image.load("../Assets/images/White_board.png")
    drawing_board_bg = pygame.transform.scale(drawing_board_bg, screen.get_size())

    destroyed_earth_bg = pygame.image.load("../Assets/images/destroyed earth.png")
    destroyed_earth_bg = pygame.transform.scale(destroyed_earth_bg, screen.get_size())

    workshop_bg = pygame.image.load("../Assets/images/workshop.png")
    workshop_bg = pygame.transform.scale(workshop_bg, screen.get_size())
    launch_bg = pygame.image.load("../Assets/images/Kennedy_Space_Center_Moonlit_Launch.png")
    launch_bg = pygame.transform.scale(launch_bg, screen.get_size())

    price_coins = {}
    for tier, count in (("cheap", 3), ("medium", 6), ("expensive", 9)):
        coin = pygame.image.load(f"../Assets/images/Coins_Gold_Shadow_{count}.png").convert_alpha()
        price_coins[tier] = pygame.transform.scale(coin, (48, 48))
    rocket_files = {
        "cheap": "../Assets/images/Pixel Art Rocket on Transparent Background-1.png",
        "medium": "../Assets/images/Retro Pixel Art Rocket Launch-2.png",
        "expensive": "../Assets/images/Pixel-Art Heavy-Lift Rocket-3.png",
    }
    rocket_images = {}
    for tier, filename in rocket_files.items():
        image = pygame.image.load(filename).convert_alpha()
        bounds = image.get_bounding_rect(min_alpha=20)
        image = image.subsurface(bounds).copy()
        width = min(200, round(image.get_width() * 220 / image.get_height()))
        height = round(image.get_height() * width / image.get_width())
        rocket_images[tier] = pygame.transform.scale(image, (width, height))

    crew_icon_files = {
        "Geologist": "01_geologist.png",
        "Physicists": "02_physicist.png",
        "Astrobiologist": "03_astrobiologist.png",
        "Signal Engineer": "04_signal_engineer.png",
        "Astronaut": "05_astronaut.png",
        "Doctor": "06_doctor.png",
        "Psychologist": "07_psychologist.png",
        "Geneticist": "08_geneticist.png",
        "Epidemiologist": "09_epidemiologist.png",
        "Computer Scientist/Engineer": "10_computer_scientist-engineer.png",
        "Linguist": "11_linguist.png",
        "Flight Director": "12_flight_director.png",
        "Propulsion Engineer": "13_propulsion_engineer.png",
    }
    crew_icons = {}
    for profession, filename in crew_icon_files.items():
        image = pygame.image.load(f"../Assets/images/{filename}").convert_alpha()
        crew_icons[profession] = pygame.transform.smoothscale(image, (56, 56))

    game_state = GameState()
    screens = {
        "main": MainScreen(screen, space_background, font_file),
        "difficulty": DifficultyScreen(screen, computer_bg, font_file, game_state),
        "menu": MenuScreen(screen, computer_bg, font_file, game_state),
        "rover_intro": RoverIntroScreen(
            screen, "../Assets/images/moonbreakers_rover_crystal_6s.gif", font_file
        ),
        "roles": RoleSelectionScreen(screen, computer_bg, font_file, game_state),
        "roster": RosterSelectionScreen(screen, computer_bg, font_file, game_state, crew_icons),
        "rocket_builder": RocketBuilderScreen(screen, mission_control_bg, font_file, game_state, price_coins, rocket_images),
        "rocket_configuration": RocketConfigurationScreen(screen, workshop_bg, font_file, game_state),
        "instrumentation": InstrumentationScreen(screen, workshop_bg, font_file, game_state),
        "spacecraft_setup": SpacecraftSetupScreen(screen, workshop_bg, font_file, game_state),
        "launch": LaunchScreen(screen, launch_bg, font_file, game_state),
        "trajectory": TrajectoryScreen(screen, launch_bg, font_file),
        "analysis_results": AnalysisResultsScreen(screen, mission_control_bg, font_file, game_state),
        "mission_choice": MissionChoiceScreen(screen, board_room_bg, font_file),
        "game_over_final": EndingScreen(screen, destroyed_earth_bg, font_file, "GAME OVER"),
        "to_be_continued": EndingScreen(screen, space_background, font_file, "To be continued..."),
    }
    for name, (title, dialogue, back_screen, next_screen) in STORY_WINDOWS.items():
        if name in ("opening_call", "invite_team", "doubt", "who_team"):
            background = computer_bg
        elif name in ("secure_location", "boss_briefing", "mission_offer", "mission_plan"):
            background = board_room_bg
        elif name == "analysis_success":
            background = drawing_board_bg
        else:
            background = mission_control_bg
        screens[name] = StoryScreen(
            screen, background, font_file, title, dialogue, back_screen, next_screen,
            compact=name in ("invite_team", "doubt", "who_team"),
        )
    for index, entry in enumerate(JOURNAL_ENTRIES, start=1):
        screens[f"journal_{index}"] = JournalScreen(
            screen, mission_control_bg, font_file, index, entry,
            "trajectory" if index == 1 else f"journal_{index - 1}",
            "results_prompt" if index == len(JOURNAL_ENTRIES) else f"journal_{index + 1}",
        )
    current_screen = "main"
    save_screens = ("rocket_builder", "rocket_configuration", "instrumentation", "spacecraft_setup", "launch")
    save_button = pygame.Rect(20, screen.get_height() - 60, 150, 45)
    save_label = pygame.font.Font(font_file, 28).render("Save", True, "white")
    notice_font = pygame.font.Font(font_file, 18)
    save_notice = ""

    def calculate_trajectory(inputs, result, demo=False):
        try:
            simulation = run_lunar_transfer_demo() if demo else run_gmat_simulation(inputs)
            result["trajectory"] = simulation["trajectory"]
            result["assessment"] = simulation["assessment"]
            result["outcome"] = simulation["outcome"]
            result["status"] = "ready"
        except (OSError, ValueError, RuntimeError, ImportError, KeyError) as error:
            result["message"] = str(error)
            result["status"] = "error"

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                can_save = current_screen in save_screens and game_state.rocket is not None
                if can_save and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and save_button.collidepoint(event.pos):
                    next_screen = "save_game"
                else:
                    next_screen = screens[current_screen].handle_event(event)
                if next_screen == "save_game":
                    try:
                        save_game(game_state, current_screen)
                        save_notice = "Mission saved"
                    except (OSError, TypeError):
                        save_notice = "Could not save mission"
                elif next_screen in ("run_simulation", "run_demo"):
                    try:
                        demo = next_screen == "run_demo"
                        inputs = None if demo else save_before_simulation(game_state, current_screen)
                        screens["launch"].status = ""
                        screens["analysis_results"].reset()
                        trajectory_screen = screens["trajectory"]
                        trajectory_screen.result = {"status": "running"}
                        trajectory_screen.started_at = None
                        current_screen = "trajectory"
                        threading.Thread(
                            target=calculate_trajectory,
                            args=(inputs, trajectory_screen.result, demo),
                            daemon=True,
                        ).start()
                    except (OSError, ValueError, TypeError) as error:
                        screens["launch"].status = str(error)
                elif next_screen == "load_game":
                    try:
                        current_screen = load_game(game_state)
                        save_notice = "Mission loaded"
                    except (OSError, ValueError):
                        screens["main"].notice = "No valid save found"
                elif next_screen == "new_game":
                    game_state.reset()
                    screens["analysis_results"].reset()
                    screens["trajectory"].result = {"status": "idle"}
                    screens["trajectory"].started_at = None
                    screens["launch"].status = ""
                    screens["main"].notice = ""
                    screens["roles"].open_player = None
                    screens["roles"].scroll_offset = 0
                    screens["spacecraft_setup"].active_field = None
                    screens["rocket_configuration"].propellant_open = False
                    for name in (*STORY_WINDOWS, *(f"journal_{i}" for i in range(1, len(JOURNAL_ENTRIES) + 1))):
                        screens[name].page = 0
                    current_screen = "main"
                    save_notice = ""
                elif next_screen is not None:
                    if next_screen == "analysis_results":
                        screens["analysis_results"].prepare()
                    current_screen = next_screen
                    save_notice = ""

        screens[current_screen].draw()
        if current_screen in save_screens and game_state.rocket is not None:
            screens[current_screen].draw_button(save_button, save_label)
            if save_notice:
                notice = notice_font.render(save_notice, True, "white")
                screen.blit(notice, (20, 75))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
