import pygame
import random
import copy
import time
import math

# TODO: change sound when changing n/scramble
# TODO: ensure puzzle is not solved before game even starts (esp when changing n/scramble)
# TODO: make scoreboard tab in menu
# TODO: make online leaderboard
# TODO: add volume control in menu
# TODO: make position of move counter and timer dependent on gap size
# TODO: add computer algorithm to solve puzzle
# TODO: add new game mode: images as tiles

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Sliding Puzzle")

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GRAY_BACKGROUND = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
GOLD = (255, 200, 105)
FPS = 400
NAVY_SQUARE_X, NAVY_SQUARE_Y = 275, 60
NAVY_SQUARE_WIDTH, NAVY_SQUARE_HEIGHT = 600, 600

NAVY_SQUARE = pygame.image.load("venv/navy_blue.png")
NAVY_SQUARE = pygame.transform.scale(NAVY_SQUARE, (NAVY_SQUARE_WIDTH, NAVY_SQUARE_HEIGHT))

ICON_BLUE_BOX = pygame.image.load("venv/icon_blue_80.jpeg")
ICON_BLUE_BOX = pygame.transform.scale(ICON_BLUE_BOX, (80, 80))
ICON_BLUE_BOX_LARGE = pygame.image.load("venv/icon_blue_90.jpeg")
ICON_BLUE_BOX_LARGE = pygame.transform.scale(ICON_BLUE_BOX_LARGE, (90, 90))
ICON_NAVY_BOX = pygame.image.load("venv/icon_navy_80.jpeg")
ICON_NAVY_BOX = pygame.transform.scale(ICON_NAVY_BOX, (80, 80))
ICON_NAVY_BOX_LARGE = pygame.image.load("venv/icon_navy_90.jpeg")
ICON_NAVY_BOX_LARGE = pygame.transform.scale(ICON_NAVY_BOX_LARGE, (90, 90))

SKY_BLUE_BOX = pygame.image.load("venv/sky_blue_text_box_190_90.jpeg")
SKY_BLUE_BOX_LARGE = pygame.image.load("venv/sky_blue_text_box_200_96.jpeg")
INPUT_TEXT_BOX_WIDTH, INPUT_TEXT_BOX_HEIGHT = 190, 90
INPUT_TEXT_BOX = pygame.transform.scale(SKY_BLUE_BOX, (INPUT_TEXT_BOX_WIDTH, INPUT_TEXT_BOX_HEIGHT))
INPUT_TEXT_BOX_LARGE_WIDTH, INPUT_TEXT_BOX_LARGE_HEIGHT = 200, 96
INPUT_TEXT_BOX_LARGE = pygame.transform.scale(SKY_BLUE_BOX_LARGE, (INPUT_TEXT_BOX_LARGE_WIDTH,
                                                                   INPUT_TEXT_BOX_LARGE_HEIGHT))

TRIANGLE_LEFT = pygame.image.load("venv/triangle_left_30x90.png")
TRIANGLE_RIGHT = pygame.image.load("venv/triangle_right_30x90.png")
TRIANGLE_LEFT_LARGE = pygame.image.load("venv/triangle_left_34x102.png")
TRIANGLE_RIGHT_LARGE = pygame.image.load("venv/triangle_right_34x102.png")

N_TEXT_BOX_X, N_TEXT_BOX_Y = 590, 165
N_TEXT_BOX_LARGE_X, N_TEXT_BOX_LARGE_Y = 585, 162
SCRAMBLE_TEXT_BOX_X, SCRAMBLE_TEXT_BOX_Y = 590, 435
SCRAMBLE_TEXT_BOX_LARGE_X, SCRAMBLE_TEXT_BOX_LARGE_Y = 585, 432

TEXT_BOX = pygame.image.load("venv/blue_text_box.png")
TEXT_BOX = pygame.transform.scale(TEXT_BOX, (554, 70))
MENU_ICON = pygame.image.load("venv/menu/three_lines_settings_icon.png")
MENU_ICON_WIDTH, MENU_ICON_HEIGHT = 35, 31
MENU_ICON_LARGE_WIDTH, MENU_ICON_LARGE_HEIGHT = 41, 37
MENU_ICON = pygame.transform.scale(MENU_ICON, (MENU_ICON_WIDTH, MENU_ICON_HEIGHT))
MENU_ICON_GRAY = pygame.image.load("venv/menu/three_lines_gray_36.png")  # (128, 128, 128)
MENU_ICON_GRAY = pygame.transform.scale(MENU_ICON_GRAY, (MENU_ICON_WIDTH, MENU_ICON_HEIGHT))
MENU_WHITE_LARGE = pygame.image.load("venv/menu/menu_white_41.png")
MENU_WHITE_LARGE = pygame.transform.scale(MENU_WHITE_LARGE, (MENU_ICON_LARGE_WIDTH, MENU_ICON_LARGE_HEIGHT))
MENU_GRAY_LARGE = pygame.image.load("venv/menu/menu_gray_41.png")
MENU_GRAY_LARGE = pygame.transform.scale(MENU_GRAY_LARGE, (MENU_ICON_LARGE_WIDTH, MENU_ICON_LARGE_HEIGHT))
RESTART_ICON = pygame.image.load("venv/restart/restart_white_long_34.png")
RESTART_ICON = pygame.transform.scale(RESTART_ICON, (34, 34))
RESTART_ICON_GRAY = pygame.image.load("venv/restart/restart_gray_34.png")
RESTART_ICON_GRAY = pygame.transform.scale(RESTART_ICON_GRAY, (34, 34))
RESTART_WHITE_LARGE = pygame.image.load("venv/restart/restart_white_40.png")
RESTART_WHITE_LARGE = pygame.transform.scale(RESTART_WHITE_LARGE, (40, 40))
OBJECTIVE_ICON = pygame.image.load("venv/menu/target_61.png")
OBJECTIVE_ICON = pygame.transform.scale(OBJECTIVE_ICON, (61, 61))
OBJECTIVE_ICON_LARGE = pygame.image.load("venv/menu/target_71.png")
OBJECTIVE_ICON_LARGE = pygame.transform.scale(OBJECTIVE_ICON_LARGE, (71, 71))
CONTROLS_ICON = pygame.image.load("venv/menu/controller_64.png")
CONTROLS_ICON = pygame.transform.scale(CONTROLS_ICON, (64, 64))
CONTROLS_ICON_LARGE = pygame.image.load("venv/menu/controller_74.png")
CONTROLS_ICON_LARGE = pygame.transform.scale(CONTROLS_ICON_LARGE, (74, 74))
COG_ICON = pygame.image.load("venv/menu/cog_59.png")
COG_ICON = pygame.transform.scale(COG_ICON, (59, 59))
COG_ICON_LARGE = pygame.image.load("venv/menu/cog_69.png")
COG_ICON_LARGE = pygame.transform.scale(COG_ICON_LARGE, (69, 69))
LEADERBOARD_ICON = pygame.image.load("venv/menu/leaderboard_63.png")
LEADERBOARD_ICON = pygame.transform.scale(LEADERBOARD_ICON, (63, 63))
LEADERBOARD_ICON_LARGE = pygame.image.load("venv/menu/leaderboard_73.png")
LEADERBOARD_ICON_LARGE = pygame.transform.scale(LEADERBOARD_ICON_LARGE, (73, 73))

TILE_LANDING_SOUND = pygame.mixer.Sound("venv/tile/tile_land_sound.wav")
TILE_LANDING_SOUND.set_volume(0.6)
VICTORY_SOUND = pygame.mixer.Sound("venv/victory_sound.wav")
VICTORY_SOUND.set_volume(1)
SLIDE_SOUND1 = pygame.mixer.Sound("venv/tile/slide_sound1.wav")
SLIDE_SOUND1.set_volume(0.25)
SLIDE_SOUND2 = pygame.mixer.Sound("venv/tile/slide_sound2.wav")
SLIDE_SOUND2.set_volume(0.8)
SLIDE_SOUND3 = pygame.mixer.Sound("venv/tile/slide_sound3.wav")
SLIDE_SOUND3.set_volume(0.23)
SLIDE_SOUND4 = pygame.mixer.Sound("venv/tile/slide_sound4.wav")
SLIDE_SOUND4.set_volume(0.07)
RESTART_SOUND = pygame.mixer.Sound("venv/restart/minecraft_plank_sound.wav")
RESTART_SOUND.set_volume(1)
MENU_OPEN_SOUND = pygame.mixer.Sound("venv/menu/open_menu.wav")
MENU_OPEN_SOUND.set_volume(0.7)
MENU_CLOSE_SOUND = pygame.mixer.Sound("venv/menu/menu_close.wav")
MENU_CLOSE_SOUND.set_volume(0.3)
CLICK_SOUND = pygame.mixer.Sound("venv/click_sound.wav")
CLICK_SOUND.set_volume(0.3)
ERROR_SOUND = pygame.mixer.Sound("venv/error_sound.wav")
ERROR_SOUND.set_volume(0.5)

INPUT_N_INSTRUCTIONS = ["Puzzle",
                        "Size"]
INPUT_SCRAMBLE_INSTRUCTIONS = ["Scramble",
                               "Number"]
ERROR_N_TOO_SMALL = "Error: must be greater than or equal to 2"
ERROR_NO_INPUT = "Error: no value entered"
ERROR_SCRAMBLE_TOO_SMALL = "Error: must be greater than or equal to 1"

INSTRUCTIONS_LIST = ["Objective", "", "Move tiles until the numbers are", "arranged in ascending order from",
                     "top-left to bottom-right with the",  "empty square in the bottom-right", "corner"]

CONTROLS_LIST = ["Controls", "", "Use the arrow keys or left click to", "move a tile into the empty square", "",
                 "Press R to restart", "", "Press esc to open the menu"]

FONT_GOLD = pygame.font.Font("freesansbold.ttf", 30)
FONT_TEXT_INPUT = pygame.font.Font("freesansbold.ttf", 80)
FONT_TEXT_INPUT_LARGE = pygame.font.Font("freesansbold.ttf", 85)
FONT_STATS = pygame.font.Font("freesansbold.ttf", 30)
FONT_INTRO = pygame.font.Font("freesansbold.ttf", 35)
FONT_INSTRUCTIONS = pygame.font.Font("freesansbold.ttf", 17)
FONT_HEADING = pygame.font.Font("freesansbold.ttf", 24)
FONT_SCOREBOARD = FONT_INSTRUCTIONS
FONT_TAB_TITLE = pygame.font.Font("freesansbold.ttf", 50)
FONT_TAB_TEXT = pygame.font.Font("freesansbold.ttf", 30)

INSTRUCTION_NEWLINE_SIZE = 40
SCOREBOARD_NEWLINE_SIZE = 33
INPUT_NEWLINE_SIZE = 42
brightness = 255
move_count = 0
tile_num = None
last_keypress = None
time_formatted = None
tile_landing_sound_played = False
victory_sound_played = False
game_started = False
tile_landed = False
first_score_recorded = False
menu_open = False
inputting_n = False
inputting_scramble = False
current_time = 0
button_press_time = 0
cooldown = 150  # minimum time between keypress
pixel_counter = 0  # used for sliding animation
time_since_button_press = 0
scoreboard = []
user_input_n = "3"
user_input_scramble = "20"


class Button:
    def __init__(self, box_x, box_y, box, box_large, image, image_large):
        self.box_x = box_x
        self.box_y = box_y
        self.box_large_x = box_x - 5
        self.box_large_y = box_y - 5
        self.box = box
        self.box_width = box.get_width()
        self.box_height = box.get_height()
        self.box_large = box_large
        self.box_large_width = box_large.get_width()
        self.box_large_height = box_large.get_height()
        self.image = image
        self.image_width = image.get_width()
        self.image_height = image.get_height()
        self.image_large = image_large
        self.image_large_width = image_large.get_width()
        self.image_large_height = image_large.get_height()
        self.image_x = box_x + (self.box_width - self.image_width)/2
        self.image_y = box_y + (self.box_height - self.image_height)/2
        self.image_large_x = self.image_x - 5
        self.image_large_y = self.image_y - 5


class IconButton(Button):
    def __init__(self, bool_key, box_x, box_y, box, box_large, image, image_large):
        super().__init__(box_x, box_y, box, box_large, image, image_large)
        self.bool_key = bool_key
        self.box_navy = ICON_NAVY_BOX
        self.box_navy_large = ICON_NAVY_BOX_LARGE
        self.sound_played = False

    def blit_button(self, tab_open):
        mouse_pos = pygame.mouse.get_pos()

        if tab_open[self.bool_key]:
            box = self.box
            box_large = self.box_large

        else:
            box = ICON_NAVY_BOX
            box_large = ICON_NAVY_BOX_LARGE

        if menu_open:
            if mouse_in(mouse_pos, pressed=False, left=self.box_x, right=self.box_x + self.box_width,
                        top=self.box_y, bottom=self.box_y + self.box_height):
                WIN.blit(box_large, (self.box_large_x, self.box_large_y))
                WIN.blit(self.image_large, (self.image_large_x, self.image_large_y))

            else:
                WIN.blit(box, (self.box_x, self.box_y))
                WIN.blit(self.image, (self.image_x, self.image_y))

    def check_tab_open(self, tab_open):
        mouse_pos = pygame.mouse.get_pos()

        if menu_open:
            if mouse_in(mouse_pos, pressed=True, left=self.box_x, right=self.box_x + self.box_width,
                        top=self.box_y, bottom=self.box_y + self.box_height):
                for key in tab_open:
                    if key == self.bool_key:
                        tab_open[self.bool_key] = True
                        continue

                    tab_open[key] = False

                if not self.sound_played:
                    CLICK_SOUND.play()

                    self.sound_played = True


class Arrow:
    def __init__(self, x, y, image, image_large):
        self.x = x
        self.y = y
        self.x_large = x - 2
        self.y_large = y - 6
        self.image = image
        self.image_large = image_large
        self.mask = pygame.mask.from_surface(self.image)
        self.mouse_in_arrow = False
        self.pressed = False

    def blit_arrow(self):
        if self.mouse_in_arrow and self.pressed is False:
            WIN.blit(self.image_large, (self.x_large, self.y_large))

        else:
            WIN.blit(self.image, (self.x, self.y))

    def check_mouse_in_arrow(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        try:
            if self.mask.get_at((mouse_x - self.x, mouse_y - self.y)):
                self.mouse_in_arrow = True
                return True

        except IndexError:
            self.mouse_in_arrow = False
            return False


def move_tile(tile_to_move_num, array):
    empty_row, empty_col = find_tile_index(0)
    tile_row, tile_col = find_tile_index(tile_to_move_num)

    # Define permissible moves
    tile_can_be_moved = False
    if tile_row == empty_row:
        if tile_col == empty_col - 1 or tile_col == empty_col + 1:
            tile_can_be_moved = True

    elif tile_col == empty_col:
        if tile_row == empty_row - 1 or tile_row == empty_row + 1:
            tile_can_be_moved = True

    # Move the tile i.e. swap the values on the puzzle array
    if tile_can_be_moved:
        array[tile_row][tile_col], array[empty_row][empty_col] = \
            array[empty_row][empty_col], array[tile_row][tile_col]

    return tile_can_be_moved


def scramble(num_of_moves, array_to_scramble):
    last_tile_moved = None
    while num_of_moves > 0:
        rand_tile = random.randint(1, n * n - 1)
        if rand_tile == last_tile_moved:
            continue

        if move_tile(rand_tile, array_to_scramble):
            last_tile_moved = rand_tile
            num_of_moves -= 1


def find_tile_index(tile_num):
    for row in range(len(puzzle_array)):
        if tile_num in puzzle_array[row]:
            tile_row, tile_col = row, puzzle_array[row].index(tile_num)
            break

    return tile_row, tile_col


def convert_time(sec):
    global time_formatted
    minutes = sec // 60
    seconds = sec % 60

    if minutes == 0 and seconds < 10:
        time_formatted = f"00:0{str(seconds)}"

    elif minutes == 0 and seconds >= 10:
        time_formatted = f"00:{str(seconds)}"

    elif minutes < 10 and seconds < 10:
        time_formatted = f"0{str(minutes)}:0{str(seconds)}"

    elif minutes < 10 and seconds >= 10:
        time_formatted = f"0{str(minutes)}:{str(seconds)}"

    return time_formatted


def draw_user_input(n_text_box, scramble_text_box, n_arrow_left, n_arrow_right, scramble_arrow_left,
                    scramble_arrow_right):
    global TEXT_BOX, inputting_n, inputting_scramble

    for i, line in enumerate(INPUT_N_INSTRUCTIONS):
        n_instructions = FONT_INTRO.render(line, True, WHITE)
        WIN.blit(n_instructions, (325, 169 + i * INPUT_NEWLINE_SIZE))

    for i, line in enumerate(INPUT_SCRAMBLE_INSTRUCTIONS):
        scramble_instructions = FONT_INTRO.render(line, True, WHITE)
        WIN.blit(scramble_instructions, (325, 440 + i * INPUT_NEWLINE_SIZE))

    n_arrow_left.blit_arrow()
    n_arrow_right.blit_arrow()
    scramble_arrow_left.blit_arrow()
    scramble_arrow_right.blit_arrow()

    mouse_pos = pygame.mouse.get_pos()

    if n_text_box.collidepoint(mouse_pos):
        WIN.blit(INPUT_TEXT_BOX_LARGE, (N_TEXT_BOX_LARGE_X, N_TEXT_BOX_LARGE_Y))

        if inputting_n:
            n_text_large = FONT_TEXT_INPUT_LARGE.render(user_input_n, True, WHITE)

        else:
            n_text_large = FONT_TEXT_INPUT_LARGE.render(user_input_n, True, GOLD)

        n_text_width, n_text_height = FONT_TEXT_INPUT_LARGE.size(user_input_n)
        n_text_x = N_TEXT_BOX_LARGE_X + (INPUT_TEXT_BOX_LARGE_WIDTH - n_text_width) / 2
        n_text_y = N_TEXT_BOX_LARGE_Y + (INPUT_TEXT_BOX_LARGE_HEIGHT - n_text_height) / 2
        WIN.blit(n_text_large, (n_text_x + 1, n_text_y + 5))

        # Display text cursor for n
        if inputting_n and (time.time() % 1) < 0.5:
            pygame.draw.rect(WIN, WHITE, pygame.Rect(n_text_x + n_text_width + 1, 174, 3, 74))

    else:
        WIN.blit(INPUT_TEXT_BOX, (N_TEXT_BOX_X, N_TEXT_BOX_Y))

        if inputting_n:
            n_text = FONT_TEXT_INPUT.render(user_input_n, True, WHITE)

        else:
            n_text = FONT_TEXT_INPUT.render(user_input_n, True, GOLD)

        n_text_width, n_text_height = FONT_TEXT_INPUT.size(user_input_n)
        n_text_x = N_TEXT_BOX_X + (INPUT_TEXT_BOX_WIDTH - n_text_width) / 2
        WIN.blit(n_text, (n_text_x, N_TEXT_BOX_Y + 10))

        if inputting_n and (time.time() % 1) < 0.5:
            pygame.draw.rect(WIN, WHITE, pygame.Rect(n_text_x + n_text_width, 177, 3, 68))

    if scramble_text_box.collidepoint(mouse_pos):
        WIN.blit(INPUT_TEXT_BOX_LARGE, (SCRAMBLE_TEXT_BOX_LARGE_X, SCRAMBLE_TEXT_BOX_LARGE_Y))

        if inputting_scramble:
            scramble_text_large = FONT_TEXT_INPUT_LARGE.render(user_input_scramble, True, WHITE)

        else:
            scramble_text_large = FONT_TEXT_INPUT_LARGE.render(user_input_scramble, True, GOLD)

        scramble_text_width, scramble_text_height = FONT_TEXT_INPUT_LARGE.size(user_input_scramble)
        scramble_text_x = SCRAMBLE_TEXT_BOX_LARGE_X + (INPUT_TEXT_BOX_LARGE_WIDTH - scramble_text_width) / 2
        scramble_text_y = SCRAMBLE_TEXT_BOX_LARGE_Y + (INPUT_TEXT_BOX_LARGE_HEIGHT - scramble_text_height) / 2
        WIN.blit(scramble_text_large, (scramble_text_x + 1, scramble_text_y + 5))

        # Display text cursor for scramble num
        if inputting_scramble and (time.time() % 1) < 0.5:
            pygame.draw.rect(WIN, WHITE, pygame.Rect(scramble_text_x + scramble_text_width + 1, 444, 3, 74))

    else:
        WIN.blit(INPUT_TEXT_BOX, (SCRAMBLE_TEXT_BOX_X, SCRAMBLE_TEXT_BOX_Y))

        if inputting_scramble:
            scramble_text = FONT_TEXT_INPUT.render(user_input_scramble, True, WHITE)

        else:
            scramble_text = FONT_TEXT_INPUT.render(user_input_scramble, True, GOLD)

        scramble_text_width, scramble_text_height = FONT_TEXT_INPUT.size(user_input_scramble)
        scramble_text_x = SCRAMBLE_TEXT_BOX_X + (INPUT_TEXT_BOX_WIDTH - scramble_text_width) / 2
        WIN.blit(scramble_text, (scramble_text_x, SCRAMBLE_TEXT_BOX_Y + 10))

        # Display text cursor for scramble num
        if inputting_scramble and (time.time() % 1) < 0.5:
            pygame.draw.rect(WIN, WHITE, pygame.Rect(scramble_text_x + scramble_text_width, 447, 3, 68))


def draw_window(obj_icon, ctrl_icon, cog_icon, leaderboard_icon, tab_open, gray_restart_button, n_text_box,
                scramble_text_box, n_arrow_left, n_arrow_right, scramble_arrow_left, scramble_arrow_right):
    global tile_num, time_since_button_press, cooldown, brightness, scoreboard, gap_width, \
        sliding_square_size, FONT_NUM
    WIN.fill(GRAY_BACKGROUND)
    WIN.blit(NAVY_SQUARE, (NAVY_SQUARE_X, NAVY_SQUARE_Y))
    move_count_text = FONT_STATS.render("Moves: " + str(move_count), True, WHITE)
    WIN.blit(move_count_text, (293, 20))
    timer_text = FONT_STATS.render(convert_time(time_elapsed), True, WHITE)
    WIN.blit(timer_text, (772, 20))

    mouse_pos = pygame.mouse.get_pos()

    # Icons
    if menu_open:
        if mouse_in(mouse_pos, pressed=False, left=1140, right=1175, top=16, bottom=50):
            WIN.blit(MENU_GRAY_LARGE, (1137, 12))

        else:
            WIN.blit(MENU_ICON_GRAY, (1140, 15))

        obj_icon.check_tab_open(tab_open)
        ctrl_icon.check_tab_open(tab_open)
        cog_icon.check_tab_open(tab_open)
        leaderboard_icon.check_tab_open(tab_open)

        obj_icon.blit_button(tab_open)
        ctrl_icon.blit_button(tab_open)
        cog_icon.blit_button(tab_open)
        leaderboard_icon.blit_button(tab_open)

    else:
        if mouse_in(mouse_pos, pressed=False, left=1140, right=1175, top=16, bottom=50):
            WIN.blit(MENU_WHITE_LARGE, (1137, 12))

        else:
            WIN.blit(MENU_ICON, (1140, 15))

    if mouse_in_restart_unpressed(mouse_pos) and not gray_restart_button:
        WIN.blit(RESTART_WHITE_LARGE, (1082, 10))

    elif restart_pressed(mouse_pos) or gray_restart_button:
        WIN.blit(RESTART_ICON_GRAY, (1085, 13))

    else:
        WIN.blit(RESTART_ICON, (1085, 13))

    if menu_open:
        # Instructions tab
        if tab_open["obj_tab_open"]:
            for i, text in enumerate(INSTRUCTIONS_LIST):
                if INSTRUCTIONS_LIST[i] == "Objective":
                    instructions_text = FONT_TAB_TITLE.render(text, True, WHITE)

                else:
                    instructions_text = FONT_TAB_TEXT.render(text, True, WHITE)

                WIN.blit(instructions_text, (320, 100 + i * INSTRUCTION_NEWLINE_SIZE))

        # Controls tab
        if tab_open["ctrl_tab_open"]:
            for i, text in enumerate(CONTROLS_LIST):
                if CONTROLS_LIST[i] == "Controls":
                    instructions_text = FONT_TAB_TITLE.render(text, True, WHITE)

                else:
                    instructions_text = FONT_TAB_TEXT.render(text, True, WHITE)

                WIN.blit(instructions_text, (320, 100 + i * INSTRUCTION_NEWLINE_SIZE))

        # Cog tab
        if tab_open["cog_tab_open"]:
            draw_user_input(n_text_box, scramble_text_box, n_arrow_left, n_arrow_right, scramble_arrow_left,
                            scramble_arrow_right)

    # Scoreboard text
    rank_list = [x + 1 for x in range(len(scoreboard))]
    scoreboard_text = FONT_STATS.render("Scoreboard", True, (brightness, brightness, brightness))
    rank_heading = FONT_HEADING.render("Rank", True, (brightness, brightness, brightness))
    move_heading = FONT_HEADING.render("Moves", True, (brightness, brightness, brightness))
    time_heading = FONT_HEADING.render("Time", True, (brightness, brightness, brightness))

    # if first_score_recorded:
    #     WIN.blit(scoreboard_text, (947, 20))
    #     WIN.blit(rank_heading, (900, 80))
    #     WIN.blit(move_heading, (995, 80))
    #     WIN.blit(time_heading, (1100, 80))
    #
    # for i, tple in enumerate(scoreboard):
    #     rank_text = FONT_SCOREBOARD.render(str(rank_list[i]), True, (brightness, brightness, brightness))
    #     WIN.blit(rank_text, (905, 130 + i * scoreboard_newline_size))
    #
    #     move_text = FONT_SCOREBOARD.render(str(tple[0]), True, (brightness, brightness, brightness))
    #     WIN.blit(move_text, (1000, 130 + i * scoreboard_newline_size))
    #
    #     time_text = FONT_SCOREBOARD.render(str(convert_time(tple[1])), True, (brightness, brightness, brightness))
    #     WIN.blit(time_text, (1105, 130 + i * scoreboard_newline_size))
    #
    # # decrease font brightness after game has started
    # if game_started and brightness > 40:
    #     brightness -= 2.5

    # Tiles and numbers
    for row in range(len(puzzle_array)):

        if menu_open:
            break

        for col in range(len(puzzle_array[row])):
            if puzzle_array[row][col] == 0:
                continue

            if puzzle_array[row][col] == tile_num:
                continue

            WIN.blit(SLIDING_SQUARE, (NAVY_SQUARE_X + gap_width + col * (gap_width + sliding_square_size),
                                      NAVY_SQUARE_Y + gap_width + row * (gap_width + sliding_square_size)))

            num_to_blit = FONT_NUM.render(str(puzzle_array[row][col]), True, WHITE)
            text_width, text_height = FONT_NUM.size(str(puzzle_array[row][col]))

            WIN.blit(num_to_blit, (NAVY_SQUARE_X + gap_width - text_width / 2 + sliding_square_size / 2
                                   + col * (gap_width + sliding_square_size),
                                   NAVY_SQUARE_Y + gap_width - text_height / 2 + sliding_square_size / 2
                                   + row * (gap_width + sliding_square_size)))

    time_since_button_press = current_time - button_press_time
    draw_sliding_animation()
    draw_puzzle_solved()

    pygame.display.update()


def draw_puzzle_solved():
    global puzzle_solved, time_since_button_press

    if puzzle_solved and time_since_button_press > cooldown:
        solved_text = FONT_GOLD.render("PUZZLE SOLVED!", True, GOLD)
        move_text_width = FONT_STATS.size("Moves: " + str(move_count))[0]
        solved_text_width = FONT_STATS.size("PUZZLE SOLVED!")[0]

        # The solved_text should be in the middle of the move counter and the time
        solved_text_x = (293 + move_text_width) + (772 - (293 + move_text_width) - solved_text_width) / 2
        WIN.blit(solved_text, (solved_text_x, 20))


def draw_sliding_animation():
    global tile_num, pixel_counter, cooldown, time_since_button_press, \
        empty_row_list, empty_col_list, tile_landing_sound_played, tile_landed

    distance = math.floor(sliding_square_size + gap_width)  # distance tile needs to move

    try:
        tile_row, tile_col = find_tile_index(0)  # the original tile is now the empty tile
        tile_row_original, tile_col_original = find_tile_index(tile_num)
        tile_x = NAVY_SQUARE_X + gap_width + tile_col * (gap_width + sliding_square_size)
        tile_y = NAVY_SQUARE_Y + gap_width + tile_row * (gap_width + sliding_square_size)
        last_empty_x = NAVY_SQUARE_X + gap_width + empty_col_list[-2] * (gap_width + sliding_square_size)
        last_empty_y = NAVY_SQUARE_Y + gap_width + empty_row_list[-2] * (gap_width + sliding_square_size)

        num_to_blit = FONT_NUM.render(str(puzzle_array[tile_row_original][tile_col_original]), True, WHITE)
        text_width, text_height = FONT_NUM.size(str(puzzle_array[tile_row_original][tile_col_original]))

        num_x = (NAVY_SQUARE_X + gap_width - text_width / 2 + sliding_square_size / 2
                 + tile_col * (gap_width + sliding_square_size))
        num_y = (NAVY_SQUARE_Y + gap_width - text_height / 2 + sliding_square_size / 2
                 + tile_row * (gap_width + sliding_square_size))
        last_num_x = (NAVY_SQUARE_X + gap_width - text_width / 2 + sliding_square_size / 2
                      + empty_col_list[-2] * (gap_width + sliding_square_size))
        last_num_y = (NAVY_SQUARE_Y + gap_width - text_height / 2 + sliding_square_size / 2
                      + empty_row_list[-2] * (gap_width + sliding_square_size))

        time_since_button_press = current_time - button_press_time

        if pixel_counter <= distance:

            if last_keypress == "up":
                WIN.blit(SLIDING_SQUARE, (tile_x, tile_y - pixel_counter))
                WIN.blit(num_to_blit, (num_x, num_y - pixel_counter))

            elif last_keypress == "down":
                WIN.blit(SLIDING_SQUARE, (tile_x, tile_y + pixel_counter))
                WIN.blit(num_to_blit, (num_x, num_y + pixel_counter))

            elif last_keypress == "left":
                WIN.blit(SLIDING_SQUARE, (tile_x - pixel_counter, tile_y))
                WIN.blit(num_to_blit, (num_x - pixel_counter, num_y))

            elif last_keypress == "right":
                WIN.blit(SLIDING_SQUARE, (tile_x + pixel_counter, tile_y))
                WIN.blit(num_to_blit, (num_x + pixel_counter, num_y))

            if n == 2:
                pixel_counter += 14

            elif n == 3:
                pixel_counter += 12

            else:
                pixel_counter += 10

        else:
            if not menu_open:
                WIN.blit(SLIDING_SQUARE, (last_empty_x, last_empty_y))
                WIN.blit(num_to_blit, (last_num_x, last_num_y))
                tile_landed = True
                SLIDE_SOUND1.stop()
                SLIDE_SOUND2.stop()
                SLIDE_SOUND3.stop()
                SLIDE_SOUND4.stop()

                if not tile_landing_sound_played:
                    TILE_LANDING_SOUND.play()
                    tile_landing_sound_played = True

    except UnboundLocalError:
        pass


def key_up(array):
    global tile_num
    empty_row, empty_col = find_tile_index(0)
    tile_moved = False

    try:
        tile_num = array[empty_row + 1][empty_col]
        if move_tile(tile_num, array):
            tile_moved = True

    except IndexError:
        pass

    return tile_moved, tile_num


def key_down(array):
    global tile_num
    empty_row, empty_col = find_tile_index(0)
    tile_moved = False

    try:
        if empty_row != 0:
            tile_num = array[empty_row - 1][empty_col]
            if move_tile(tile_num, array):
                tile_moved = True

    except IndexError:
        pass

    return tile_moved, tile_num


def key_left(array):
    global tile_num
    empty_row, empty_col = find_tile_index(0)
    tile_moved = False

    try:
        tile_num = array[empty_row][empty_col + 1]
        if move_tile(tile_num, array):
            tile_moved = True

    except IndexError:
        pass

    return tile_moved, tile_num


def key_right(array):
    global tile_num
    empty_row, empty_col = find_tile_index(0)
    tile_moved = False

    try:
        if empty_col != 0:
            tile_num = array[empty_row][empty_col - 1]
            if move_tile(tile_num, array):
                tile_moved = True

    except IndexError:
        pass

    return tile_moved, tile_num


def find_tile_clicked(mouse_pos, n, gap_width, sliding_square_size):
    mouse_x, mouse_y = mouse_pos
    row_clicked, col_clicked = None, None

    # Click must be in the navy square
    if mouse_x < NAVY_SQUARE_X or mouse_x > NAVY_SQUARE_X + NAVY_SQUARE_WIDTH:
        return None, None

    if mouse_y < NAVY_SQUARE_Y or mouse_y > NAVY_SQUARE_Y + NAVY_SQUARE_HEIGHT:
        return None, None

    # Find row
    for row in range(n - 1, -1, -1):
        if mouse_y > (NAVY_SQUARE_Y + gap_width + row * (gap_width + sliding_square_size)):
            if mouse_y > (NAVY_SQUARE_Y + gap_width + row * (gap_width + sliding_square_size) +
                          sliding_square_size):  # Click is in the gap
                pass

            else:
                row_clicked = row

    # Find col
    for col in range(n - 1, -1, -1):
        if mouse_x > (NAVY_SQUARE_X + gap_width + col * (gap_width + sliding_square_size)):
            if mouse_x > (NAVY_SQUARE_X + gap_width + col * (gap_width + sliding_square_size) +
                          sliding_square_size):  # Click is in the gap
                pass

            else:
                col_clicked = col

    return row_clicked, col_clicked


def mouse_in_restart_icon(mouse_pos):
    mouse_x, mouse_y = mouse_pos

    if 1086 <= mouse_x <= 1118 and 14 <= mouse_y <= 50:
        return True

    return False


def mouse_in_restart_unpressed(mouse_pos):
    left_mouse = pygame.mouse.get_pressed()[0]
    if (not left_mouse) and mouse_in_restart_icon(mouse_pos):
        return True

    return False


def restart_pressed(mouse_pos):
    left_mouse = pygame.mouse.get_pressed()[0]
    if left_mouse and mouse_in_restart_icon(mouse_pos):
        return True

    return False


def mouse_restart(mouse_pos):
    if mouse_in_restart_icon(mouse_pos):
        restart()


def menu_button(mouse_pos):
    mouse_x, mouse_y = mouse_pos
    menu_pressed = False

    if 1140 <= mouse_x <= 1175 and 16 <= mouse_y <= 50:
        menu_pressed = True

        if menu_open:
            MENU_CLOSE_SOUND.play()

        else:
            MENU_OPEN_SOUND.play()

    return menu_pressed


def mouse_in(mouse_pos, pressed, left, right, top, bottom):
    left_mouse = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = mouse_pos

    if pressed:
        if left_mouse and (left <= mouse_x <= right and top <= mouse_y <= bottom):
            return True

    if not pressed:
        if (not left_mouse) and (left <= mouse_x <= right and top <= mouse_y <= bottom):
            return True

    return False


def mouse_in_navy_square(mouse_pos):
    mouse_x, mouse_y = mouse_pos
    mouse_in_square = (NAVY_SQUARE_X < mouse_x < NAVY_SQUARE_X + NAVY_SQUARE_WIDTH and
                       NAVY_SQUARE_Y < mouse_y < NAVY_SQUARE_HEIGHT + NAVY_SQUARE_HEIGHT)

    return mouse_in_square


def restart():
    global puzzle_solved, first_score_recorded, tile_num, last_keypress, \
        time_formatted, tile_landing_sound_played, victory_sound_played, \
        game_started, brightness, move_count, empty_row_list, empty_col_list, \
        puzzle_array, solved_puzzle_array, time_elapsed

    # if puzzle_solved:
    #     first_score_recorded = True
    #
    #     scoreboard.append((move_count, time_elapsed))
    #     scoreboard.sort()
    #
    #     if len(scoreboard) > 15:
    #         scoreboard.pop(-1)

    tile_num = None
    last_keypress = None
    time_formatted = None
    tile_landing_sound_played = False
    victory_sound_played = False
    game_started = False
    puzzle_solved = False
    brightness = 255
    move_count = 0
    empty_row_list = []
    empty_col_list = []
    puzzle_array = []
    num_list = [x + 1 for x in range(n * n - 1)] + [0]

    for i in range(n):
        puzzle_array.append(num_list[i * n:i * n + n])

    solved_puzzle_array = copy.deepcopy(puzzle_array)
    scramble(scramble_num, puzzle_array)
    empty_row_list.append(find_tile_index(0)[0])
    empty_col_list.append(find_tile_index(0)[1])
    time_elapsed = 0

    RESTART_SOUND.play()


def main():
    global puzzle_array, move_count, puzzle_solved, time_elapsed, \
        empty_row_list, empty_col_list, current_time, button_press_time, \
        last_keypress, time_since_button_press, pixel_counter, \
        tile_landing_sound_played, game_started, victory_sound_played, \
        tile_num, time_formatted, brightness, tile_landed, scoreboard, \
        first_score_recorded, user_input_n, user_input_scramble, n, scramble_num, \
        SLIDING_SQUARE, gap_width, sliding_square_size, FONT_NUM, cooldown, \
        solved_puzzle_array, menu_open, pause_time, inputting_n, inputting_scramble

    # Initial values
    n = 3
    scramble_num = 20

    restart()
    RESTART_SOUND.stop()

    clock = pygame.time.Clock()

    # Classes
    objective_icon = IconButton("obj_tab_open", 178, 65, box=ICON_BLUE_BOX, box_large=ICON_BLUE_BOX_LARGE,
                                image=OBJECTIVE_ICON, image_large=OBJECTIVE_ICON_LARGE)
    controls_icon = IconButton("ctrl_tab_open", 178, 165, box=ICON_BLUE_BOX, box_large=ICON_BLUE_BOX_LARGE,
                               image=CONTROLS_ICON, image_large=CONTROLS_ICON_LARGE)
    cog_icon = IconButton("cog_tab_open", 178, 265, box=ICON_BLUE_BOX, box_large=ICON_BLUE_BOX_LARGE,
                          image=COG_ICON, image_large=COG_ICON_LARGE)
    leaderboard_icon = IconButton("ldb_tab_open", 178, 365, box=ICON_BLUE_BOX, box_large=ICON_BLUE_BOX_LARGE,
                                  image=LEADERBOARD_ICON, image_large=LEADERBOARD_ICON_LARGE)

    tab_open = {"obj_tab_open": True,
                "ctrl_tab_open": False,
                "cog_tab_open": False,
                "ldb_tab_open": False}

    # Text input boxes
    n_text_box = pygame.Rect(N_TEXT_BOX_X + 2, N_TEXT_BOX_Y + 3, 188, 89)
    scramble_text_box = pygame.Rect(SCRAMBLE_TEXT_BOX_X + 2, SCRAMBLE_TEXT_BOX_Y + 3, 188, 89)

    # Arrows
    n_arrow_left = Arrow(548, 162, TRIANGLE_LEFT, TRIANGLE_LEFT_LARGE)
    n_arrow_right = Arrow(792, 167, TRIANGLE_RIGHT, TRIANGLE_RIGHT_LARGE)
    scramble_arrow_left = Arrow(548, 433, TRIANGLE_LEFT, TRIANGLE_LEFT_LARGE)
    scramble_arrow_right = Arrow(792, 438, TRIANGLE_RIGHT, TRIANGLE_RIGHT_LARGE)

    gray_restart_button = None
    puzzle_solved = False
    run = True
    time_elapsed = 0

    while run:
        # Variables using n:
        gap_width = 60 / n
        sliding_square_size = (NAVY_SQUARE_WIDTH - (n + 1) * gap_width) / n
        FONT_NUM = pygame.font.Font("freesansbold.ttf", int(160 / n * 1.2))

        SLIDING_SQUARE = pygame.image.load("venv/sky_blue.png")
        SLIDING_SQUARE = pygame.transform.scale(SLIDING_SQUARE,
                                                (sliding_square_size, sliding_square_size))

        # Adjust cooldown depending on n
        if n == 2:
            cooldown = 180

        elif n >= 6:
            cooldown = 100

        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        time_since_button_press = current_time - button_press_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                tile_landed = False

                if event.key == pygame.K_r:
                    restart()
                    gray_restart_button = True

                if event.key == pygame.K_ESCAPE:
                    if not menu_open:
                        menu_open = True
                        inputting_n = False
                        inputting_scramble = False
                        user_input_n = str(n)
                        user_input_scramble = str(scramble_num)
                        pause_time = time.time()
                        MENU_OPEN_SOUND.play()

                    else:
                        menu_open = False
                        MENU_CLOSE_SOUND.play()

                        # Increase start_time so that time_elapsed is same after menu closed as before menu opened
                        # Only if game has not been restarted
                        if game_started:
                            start_time += time.time() - pause_time

                # Text input
                if tab_open["cog_tab_open"]:

                    if inputting_n:
                        if event.key == pygame.K_BACKSPACE:
                            user_input_n = user_input_n[:-1]

                        elif event.key == pygame.K_RETURN:
                            if len(user_input_n) == 0:
                                pass

                            else:
                                n_tmp = int(user_input_n)
                                if n_tmp < 2:
                                    user_input_n = ""

                                else:
                                    n = n_tmp
                                    inputting_n = False
                                    restart()

                        elif event.unicode in "0123456789" and len(user_input_n) <= 2:
                            user_input_n += event.unicode

                    if inputting_scramble:
                        if event.key == pygame.K_BACKSPACE:
                            user_input_scramble = user_input_scramble[:-1]

                        elif event.key == pygame.K_RETURN:
                            if len(user_input_scramble) == 0:
                                pass

                            else:
                                scramble_num_tmp = int(user_input_scramble)
                                if scramble_num_tmp < 1:
                                    user_input_scramble = ""

                                else:
                                    scramble_num = scramble_num_tmp
                                    inputting_scramble = False
                                    restart()

                        elif event.unicode in "0123456789" and len(user_input_scramble) <= 2:
                            user_input_scramble += event.unicode

                # Keyboard input
                if not puzzle_solved and not menu_open:

                    if not game_started and (event.key == pygame.K_UP or
                                             event.key == pygame.K_DOWN or
                                             event.key == pygame.K_LEFT or
                                             event.key == pygame.K_RIGHT or
                                             event.key == pygame.K_w or
                                             event.key == pygame.K_s or
                                             event.key == pygame.K_a or
                                             event.key == pygame.K_d):
                        start_time = time.time()
                        game_started = True

                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and \
                            time_since_button_press > cooldown:
                        if key_up(puzzle_array)[0]:
                            last_keypress = "up"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND1.play()
                            tile_landing_sound_played = False

                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and \
                            time_since_button_press > cooldown:
                        if key_down(puzzle_array)[0]:
                            last_keypress = "down"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND2.play()
                            tile_landing_sound_played = False

                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and \
                            time_since_button_press > cooldown:
                        if key_left(puzzle_array)[0]:
                            last_keypress = "left"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND3.play()
                            tile_landing_sound_played = False

                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and \
                            time_since_button_press > cooldown:
                        if key_right(puzzle_array)[0]:
                            last_keypress = "right"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND4.play()
                            tile_landing_sound_played = False

            if event.type == pygame.KEYUP:
                gray_restart_button = False

            if tab_open["cog_tab_open"]:
                n_arrow_left.check_mouse_in_arrow()
                n_arrow_right.check_mouse_in_arrow()
                scramble_arrow_left.check_mouse_in_arrow()
                scramble_arrow_right.check_mouse_in_arrow()

            # Mouse input
            left_mouse = pygame.mouse.get_pressed()[0]
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN and left_mouse:
                mouse_pos = pygame.mouse.get_pos()
                row_clicked, col_clicked = find_tile_clicked(mouse_pos, n, gap_width, sliding_square_size)

                if (row_clicked is not None) and (col_clicked is not None):
                    start_time = time.time()
                    game_started = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if tab_open["cog_tab_open"]:

                    # If mouse click is not in either of the text boxes
                    if not (n_text_box.collidepoint(event.pos) or scramble_text_box.collidepoint(event.pos)):
                        inputting_n = False
                        inputting_scramble = False
                        user_input_n = str(n)
                        user_input_scramble = str(scramble_num)

                    if n_text_box.collidepoint(event.pos):
                        inputting_scramble = False
                        inputting_n = not inputting_n

                    elif scramble_text_box.collidepoint(event.pos):
                        inputting_n = False
                        inputting_scramble = not inputting_scramble

                    # Check for mouse click in arrows and change n/scramble
                    if n_arrow_left.check_mouse_in_arrow():
                        if n > 2:
                            n_arrow_left.pressed = True
                            n -= 1
                            user_input_n = str(int(user_input_n) - 1)
                            restart()
                            RESTART_SOUND.stop()
                            CLICK_SOUND.play()
                        else:
                            ERROR_SOUND.play()

                    elif n_arrow_right.check_mouse_in_arrow():
                        n_arrow_right.pressed = True
                        n += 1
                        user_input_n = str(int(user_input_n) + 1)
                        restart()
                        RESTART_SOUND.stop()
                        CLICK_SOUND.play()

                    elif scramble_arrow_left.check_mouse_in_arrow():
                        if scramble_num > 1:
                            scramble_arrow_left.pressed = True

                            scramble_num -= 1
                            user_input_scramble = str(int(user_input_scramble) - 1)
                            restart()
                            RESTART_SOUND.stop()
                            CLICK_SOUND.play()

                        else:
                            ERROR_SOUND.play()

                    elif scramble_arrow_right.check_mouse_in_arrow():
                        scramble_arrow_right.pressed = True
                        scramble_num += 1
                        user_input_scramble = str(int(user_input_scramble) + 1)
                        restart()
                        RESTART_SOUND.stop()
                        CLICK_SOUND.play()

                if time_since_button_press > cooldown:

                    left_mouse = pygame.mouse.get_pressed()[0]

                    if left_mouse:
                        mouse_pos = pygame.mouse.get_pos()

                        # print(mouse_pos)

                        row_clicked, col_clicked = find_tile_clicked(mouse_pos, n, gap_width, sliding_square_size)
                        empty_row, empty_col = find_tile_index(0)

                        # Check which tab open
                        objective_icon.check_tab_open(tab_open)
                        controls_icon.check_tab_open(tab_open)
                        cog_icon.check_tab_open(tab_open)
                        leaderboard_icon.check_tab_open(tab_open)

                        if not puzzle_solved:
                            button_press_time = pygame.time.get_ticks()

                        # Check if restart button pressed
                        mouse_restart(mouse_pos)

                        # Check if menu button pressed
                        if menu_button(mouse_pos):
                            if not menu_open:
                                menu_open = True
                                inputting_n = False
                                inputting_scramble = False
                                user_input_n = str(n)
                                user_input_scramble = str(scramble_num)
                                pause_time = time.time()

                            else:
                                menu_open = False

                                # Increase start_time so that time_elapsed is same after menu closed as before menu opened
                                # Only if game has not been restarted
                                if game_started:
                                    start_time += time.time() - pause_time

                        if not puzzle_solved and row_clicked is not None and col_clicked is not None and not menu_open:
                            # Determine which way, if any, to move tile
                            if col_clicked == empty_col:
                                # Move up -- empty tile is above clicked tile
                                if empty_row == row_clicked - 1:
                                    key_up(puzzle_array)
                                    last_keypress = "up"
                                    move_count += 1
                                    pixel_counter = 0
                                    empty_row_list.append(find_tile_index(0)[0])
                                    empty_col_list.append(find_tile_index(0)[1])
                                    SLIDE_SOUND1.play()
                                    tile_landing_sound_played = False

                                # Move down -- empty tile is below clicked tile
                                if empty_row == row_clicked + 1:
                                    key_down(puzzle_array)
                                    last_keypress = "down"
                                    move_count += 1
                                    pixel_counter = 0
                                    empty_row_list.append(find_tile_index(0)[0])
                                    empty_col_list.append(find_tile_index(0)[1])
                                    SLIDE_SOUND2.play()
                                    tile_landing_sound_played = False

                            if row_clicked == empty_row:
                                # Move left -- empty tile is to the left of clicked tile
                                if empty_col == col_clicked - 1:
                                    key_left(puzzle_array)
                                    last_keypress = "left"
                                    move_count += 1
                                    pixel_counter = 0
                                    empty_row_list.append(find_tile_index(0)[0])
                                    empty_col_list.append(find_tile_index(0)[1])
                                    SLIDE_SOUND3.play()
                                    tile_landing_sound_played = False

                                # Move right -- empty tile is to the right of clicked tile
                                if empty_col == col_clicked + 1:
                                    key_right(puzzle_array)
                                    last_keypress = "right"
                                    move_count += 1
                                    pixel_counter = 0
                                    empty_row_list.append(find_tile_index(0)[0])
                                    empty_col_list.append(find_tile_index(0)[1])
                                    SLIDE_SOUND4.play()
                                    tile_landing_sound_played = False

            if event.type == pygame.MOUSEBUTTONUP:
                objective_icon.sound_played = False
                controls_icon.sound_played = False
                cog_icon.sound_played = False
                leaderboard_icon.sound_played = False
                n_arrow_left.pressed = False
                n_arrow_right.pressed = False
                scramble_arrow_left.pressed = False
                scramble_arrow_right.pressed = False

        # Check end condition
        if puzzle_array == solved_puzzle_array:
            puzzle_solved = True

        if not puzzle_solved:
            end_time = time.time()

        if puzzle_solved:
            if not victory_sound_played and tile_landed:
                VICTORY_SOUND.play()
                victory_sound_played = True

        if game_started and not menu_open:
            time_elapsed = round(end_time - start_time)

            if time_elapsed < 0:
                time_elapsed = 0
                end_time = start_time

        draw_window(objective_icon, controls_icon, cog_icon, leaderboard_icon, tab_open, gray_restart_button,
                    n_text_box, scramble_text_box, n_arrow_left, n_arrow_right, scramble_arrow_left,
                    scramble_arrow_right)

    pygame.quit()


if __name__ == "__main__":
    main()
