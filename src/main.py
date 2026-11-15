import threading

import pygame

from game_state import GameState
from gmat_simulation import run_gmat_simulation, run_lunar_transfer_demo
from load import load_game
from save import save_before_simulation, save_game
from screens import DifficultyScreen, InstrumentationScreen, ItemBudgetScreen, LaunchScreen, MainScreen, MenuScreen, RocketBuilderScreen, RocketConfigurationScreen, RoleSelectionScreen, RosterSelectionScreen, RoverIntroScreen, SpacecraftSetupScreen, TrajectoryScreen, mission_budget


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

    workshop_bg = pygame.image.load("../Assets/images/workshop.png")
    workshop_bg = pygame.transform.scale(workshop_bg, screen.get_size())
    launch_bg = pygame.image.load("../Assets/images/Kennedy_Space_Center_Moonlit_Launch.png")
    launch_bg = pygame.transform.scale(launch_bg, screen.get_size())

    price_coins = {}
    for tier, count in (("cheap", 3), ("medium", 6), ("expensive", 9)):
        coin = pygame.image.load(f"../Assets/images/Coins_Gold_Shadow_{count}.png").convert_alpha()
        price_coins[tier] = pygame.transform.scale(coin, (48, 48))
    money_coin = pygame.image.load("../Assets/images/Coins_Gold_Shadow_0.png").convert_alpha()
    money_coin = pygame.transform.scale(money_coin, (32, 32))
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
        "difficulty": DifficultyScreen(screen, space_background, font_file, game_state),
        "menu": MenuScreen(screen, space_background, font_file, game_state),
        "rover_intro": RoverIntroScreen(
            screen, "../Assets/images/moonbreakers_rover_crystal_6s.gif", font_file
        ),
        "roles": RoleSelectionScreen(screen, space_background, font_file, game_state),
        "roster": RosterSelectionScreen(screen, mission_control_bg, font_file, game_state, crew_icons),
        "rocket_builder": RocketBuilderScreen(screen, mission_control_bg, font_file, game_state, price_coins, rocket_images),
        "rocket_configuration": RocketConfigurationScreen(screen, workshop_bg, font_file, game_state),
        "instrumentation": InstrumentationScreen(screen, workshop_bg, font_file, game_state),
        "spacecraft_setup": SpacecraftSetupScreen(screen, workshop_bg, font_file, game_state),
        "launch": LaunchScreen(screen, launch_bg, font_file, game_state),
        "trajectory": TrajectoryScreen(screen, space_background, font_file),
    }
    current_screen = "main"
    save_screens = ("rocket_builder", "rocket_configuration", "instrumentation", "spacecraft_setup", "launch")
    save_button = pygame.Rect(20, screen.get_height() - 60, 150, 45)
    save_label = pygame.font.Font(font_file, 28).render("Save", True, "white")
    money_font = pygame.font.Font(font_file, 19)
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
                elif next_screen is not None:
                    current_screen = next_screen
                    save_notice = ""

        screens[current_screen].draw()
        if current_screen in save_screens and game_state.rocket is not None:
            pygame.draw.rect(screen, "black", (730, 15, 210, 44))
            money_label = money_font.render(
                f"${mission_budget(game_state) - ItemBudgetScreen.mission_total_cost(game_state):,.0f}", True, "white"
            )
            screen.blit(money_label, (742, 27))
            screen.blit(money_coin, (895, 21))
            screens[current_screen].draw_button(save_button, save_label)
            if save_notice:
                notice = notice_font.render(save_notice, True, "white")
                screen.blit(notice, (20, 75))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
