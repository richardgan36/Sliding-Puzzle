import pygame
from pygame import mixer
import random
import copy
import time
import math
import sys

# TODO: make option to reselect n and scramble num
# TODO: display options after puzzle solve (r for restart, x to change n and scramble num)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Sliding Puzzle")

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GRAY_BACKGROUND = (40, 40, 40)
WHITE = (255, 255, 255)
GOLD = (255, 200, 105)
FPS = 400
NAVY_SQUARE_X, NAVY_SQUARE_Y = 275, 60
NAVY_SQUARE_WIDTH, NAVY_SQUARE_HEIGHT = 600, 600
NAVY_SQUARE = pygame.image.load("venv/navy_blue.png")
NAVY_SQUARE = pygame.transform.scale(NAVY_SQUARE, (NAVY_SQUARE_WIDTH, NAVY_SQUARE_HEIGHT))
SLIDING_SQUARE = pygame.image.load("venv/sky_blue.png")
TEXT_BOX = pygame.image.load("venv/blue_text_box.png")
TEXT_BOX = pygame.transform.scale(TEXT_BOX, (554, 70))
TILE_LANDING_SOUND = mixer.Sound("venv/tile_land_sound.wav")
TILE_LANDING_SOUND.set_volume(0.6)
VICTORY_SOUND = mixer.Sound("venv/victory_sound.wav")
VICTORY_SOUND.set_volume(1)
SLIDE_SOUND1 = mixer.Sound("venv/slide_sound1.wav")
SLIDE_SOUND1.set_volume(0.25)
SLIDE_SOUND2 = mixer.Sound("venv/slide_sound2.wav")
SLIDE_SOUND2.set_volume(0.8)
SLIDE_SOUND3 = mixer.Sound("venv/slide_sound3.wav")
SLIDE_SOUND3.set_volume(0.23)
SLIDE_SOUND4 = mixer.Sound("venv/slide_sound4.wav")
SLIDE_SOUND4.set_volume(0.07)
FONT_GOLD = pygame.font.Font("freesansbold.ttf", 30)
FONT_GOLD_INPUT = pygame.font.Font("freesansbold.ttf", 48)
FONT_STATS = pygame.font.Font("freesansbold.ttf", 30)
FONT_INTRO = pygame.font.Font("freesansbold.ttf", 23)
INPUT_N_INSTRUCTIONS = "Enter an integer n to create an n by n puzzle grid"
INPUT_SCRAMBLE_INSTRUCTIONS = ["Enter an integer indicating how many times the",
                               "computer should scramble the tiles"]
ERROR_N_TOO_SMALL = "Error: must be greater than or equal to 2"
ERROR_NO_INPUT = "Error: no value entered"
ERROR_SCRAMBLE_TOO_SMALL = "Error: must be greater than or equal to 1"

display_error_n_too_small = False
display_error_no_input = False
display_error_scramble_too_small = False

INSTRUCTIONS_LIST = ["Objective", "", "", "Move tiles until", "the numbers are", "arranged in",
                     "ascending order", "from top-left", "to bottom-right", "with the empty",
                     "square in the", "bottom-right", "corner", "", "",
                     "Controls", "", "", "Use the arrow", "keys to move", "a tile into the",
                     "empty square", "", "Press R to restart", "", "Press any arrow", "key to start"]

FONT_INSTRUCTIONS = pygame.font.Font("freesansbold.ttf", 17)
FONT_HEADING = pygame.font.Font("freesansbold.ttf", 24)
FONT_SCOREBOARD = FONT_INSTRUCTIONS
instruction_newline_size = 23
scoreboard_newline_size = 33
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
n_inputted = False
scramble_inputted = False
current_time = 0
button_press_time = 0
cooldown = 150  # minimum time between keypress
pixel_counter = 0  # used for sliding animation
time_since_button_press = 0
scoreboard = []
user_input_n = ""
user_input_scramble = ""


def move_tile(tile_to_move_num, array):
    empty_row, empty_col = find_tile_index(0)
    tile_row, tile_col = find_tile_index(tile_to_move_num)

    # define permissible moves
    tile_can_be_moved = False
    if tile_row == empty_row:
        if tile_col == empty_col - 1 or tile_col == empty_col + 1:
            tile_can_be_moved = True

    elif tile_col == empty_col:
        if tile_row == empty_row - 1 or tile_row == empty_row + 1:
            tile_can_be_moved = True

    # move the tile i.e. swap the values on the puzzle array
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


def draw_user_input():
    global TEXT_BOX, n_inputted, display_error_no_input, display_error_n_too_small, \
        display_error_scramble_too_small
    WIN.fill(GRAY_BACKGROUND)
    WIN.blit(NAVY_SQUARE, (NAVY_SQUARE_X, NAVY_SQUARE_Y))
    n_instructions = FONT_INTRO.render(INPUT_N_INSTRUCTIONS, True, WHITE)
    WIN.blit(n_instructions, (300, 80))
    WIN.blit(TEXT_BOX, (298, 120))

    n_text = FONT_GOLD_INPUT.render(user_input_n, True, GOLD)
    WIN.blit(n_text, (316, 133))
    n_text_width, n_text_height = FONT_GOLD_INPUT.size(user_input_n)

    # display text cursor
    if not n_inputted and round(time.time(), 0) % 2 == 0:
        # text cursor is a white rectangle
        pygame.draw.rect(WIN, WHITE, pygame.Rect(319 + n_text_width, 133, 3, 47))

    if display_error_n_too_small and not n_inputted:
        display_error_no_input = False
        error_text_1 = FONT_INSTRUCTIONS.render(ERROR_N_TOO_SMALL, True, WHITE)
        WIN.blit(error_text_1, (300, 200))

    if display_error_no_input and not n_inputted:
        display_error_n_too_small = False
        error_text_2 = FONT_INSTRUCTIONS.render(ERROR_NO_INPUT, True, WHITE)
        WIN.blit(error_text_2, (300, 200))

    if n_inputted:

        for i in range(len(INPUT_SCRAMBLE_INSTRUCTIONS)):
            scramble_instructions = FONT_INTRO.render(INPUT_SCRAMBLE_INSTRUCTIONS[i], True, WHITE)
            WIN.blit(scramble_instructions, (300, 300 + i * scoreboard_newline_size))

        WIN.blit(TEXT_BOX, (298, 375))
        scramble_text = FONT_GOLD_INPUT.render(user_input_scramble, True, GOLD)
        WIN.blit(scramble_text, (316, 389))
        scramble_text_width, scramble_text_height = FONT_GOLD_INPUT.size(user_input_scramble)

        if not scramble_inputted and round(time.time(), 0) % 2 == 0:
            # text cursor is a white rectangle
            pygame.draw.rect(WIN, WHITE, pygame.Rect(319 + scramble_text_width, 389, 3, 47))

        if display_error_scramble_too_small:
            display_error_no_input = False
            error_text_3 = FONT_INSTRUCTIONS.render(ERROR_SCRAMBLE_TOO_SMALL, True, WHITE)
            WIN.blit(error_text_3, (300, 454))

        if display_error_no_input:
            display_error_scramble_too_small = False
            error_text_4 = FONT_INSTRUCTIONS.render(ERROR_NO_INPUT, True, WHITE)
            WIN.blit(error_text_4, (300, 454))

    pygame.display.update()


def draw_window():
    global tile_num, time_since_button_press, cooldown, brightness, scoreboard, gap_width, \
        sliding_square_size, FONT_NUM
    WIN.fill(GRAY_BACKGROUND)
    WIN.blit(NAVY_SQUARE, (NAVY_SQUARE_X, NAVY_SQUARE_Y))
    move_count_text = FONT_STATS.render("Moves: " + str(move_count), True, WHITE)
    WIN.blit(move_count_text, (293, 20))
    timer_text = FONT_STATS.render(convert_time(time_elapsed), True, WHITE)
    WIN.blit(timer_text, (772, 20))

    # instructions text
    i = 0  # for creating new lines (incrementing y value of text)
    for text in INSTRUCTIONS_LIST:
        if INSTRUCTIONS_LIST[i] == "Objective" or INSTRUCTIONS_LIST[i] == "Controls":
            instructions_text = FONT_STATS.render(text, True, (brightness, brightness, brightness))

        else:
            instructions_text = FONT_INSTRUCTIONS.render(text, True, (brightness, brightness, brightness))

        WIN.blit(instructions_text, (65, 20 + i * instruction_newline_size))

        i += 1

    # Scoreboard text
    rank_list = [x + 1 for x in range(len(scoreboard))]
    scoreboard_text = FONT_STATS.render("Scoreboard", True, (brightness, brightness, brightness))
    rank_heading = FONT_HEADING.render("Rank", True, (brightness, brightness, brightness))
    move_heading = FONT_HEADING.render("Moves", True, (brightness, brightness, brightness))
    time_heading = FONT_HEADING.render("Time", True, (brightness, brightness, brightness))

    if first_score_recorded:
        WIN.blit(scoreboard_text, (947, 20))
        WIN.blit(rank_heading, (900, 80))
        WIN.blit(move_heading, (995, 80))
        WIN.blit(time_heading, (1100, 80))

    j = 0
    for tple in scoreboard:
        rank_text = FONT_SCOREBOARD.render(str(rank_list[j]), True, (brightness, brightness, brightness))
        WIN.blit(rank_text, (905, 130 + j * scoreboard_newline_size))

        move_text = FONT_SCOREBOARD.render(str(tple[0]), True, (brightness, brightness, brightness))
        WIN.blit(move_text, (1000, 130 + j * scoreboard_newline_size))

        time_text = FONT_SCOREBOARD.render(str(convert_time(tple[1])), True, (brightness, brightness, brightness))
        WIN.blit(time_text, (1105, 130 + j * scoreboard_newline_size))

        j += 1

    # decrease font brightness after game has started
    if game_started and brightness > 40:
        brightness -= 2.5

    for row in range(len(puzzle_array)):
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

    if puzzle_solved and time_since_button_press > cooldown:
        solved_text = FONT_GOLD.render("PUZZLE SOLVED!", True, GOLD)
        move_text_width = FONT_STATS.size("Moves: " + str(move_count))[0]
        solved_text_width = FONT_STATS.size("PUZZLE SOLVED!")[0]

        # The solved_text should be in the middle of the move counter and the time
        solved_text_x = (293 + move_text_width) + (772 - (293 + move_text_width) - solved_text_width) / 2
        WIN.blit(solved_text, (solved_text_x, 20))

    pygame.display.update()


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

            pixel_counter += 10

        else:
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

    except:
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


def main():
    global puzzle_array, move_count, puzzle_solved, time_elapsed, \
        empty_row_list, empty_col_list, current_time, button_press_time, \
        last_keypress, time_since_button_press, pixel_counter, \
        tile_landing_sound_played, game_started, victory_sound_played, \
        tile_num, time_formatted, brightness, tile_landed, scoreboard, \
        first_score_recorded, user_input_n, user_input_scramble, n, n_inputted, \
        scramble_inputted, scramble_num, SLIDING_SQUARE, gap_width, \
        sliding_square_size, FONT_NUM, display_error_n_too_small, \
        display_error_scramble_too_small, display_error_no_input

    # take user input for n and scramble_num
    while not n_inputted:
        input_n_width = FONT_GOLD_INPUT.size(user_input_n)[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input_n = user_input_n[:-1]

                elif event.key == pygame.K_RETURN:
                    if len(user_input_n) == 0:
                        display_error_no_input = True
                        display_error_n_too_small = False

                    else:
                        try:
                            n = int(user_input_n)
                            if n < 2:
                                display_error_n_too_small = True
                                user_input_n = ""

                            else:
                                n_inputted = True
                                display_error_no_input = False
                                display_error_n_too_small = False

                        except:
                            pass

                elif event.unicode in "0123456789" and input_n_width < 500:
                    user_input_n += event.unicode

        draw_user_input()

    while not scramble_inputted:
        input_scramble_width = FONT_GOLD_INPUT.size(user_input_scramble)[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input_scramble = user_input_scramble[:-1]

                elif event.key == pygame.K_RETURN:
                    if len(user_input_scramble) == 0:
                        display_error_no_input = True
                        display_error_scramble_too_small = False

                    else:
                        try:
                            scramble_num = int(user_input_scramble)
                            if scramble_num < 1:
                                display_error_scramble_too_small = True
                                user_input_scramble = ""

                            else:
                                scramble_inputted = True

                        except:
                            pass

                elif event.unicode in "0123456789" and input_scramble_width < 500:
                    user_input_scramble += event.unicode

        draw_user_input()

    # variables using n:
    gap_width = 60 / n
    sliding_square_size = (NAVY_SQUARE_WIDTH - (n + 1) * gap_width) / n
    FONT_NUM = pygame.font.Font("freesansbold.ttf", int(160 / n * 1.2))

    SLIDING_SQUARE = pygame.transform.scale(SLIDING_SQUARE,
                                            (sliding_square_size, sliding_square_size))

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

    clock = pygame.time.Clock()

    puzzle_solved = False
    run = True
    time_elapsed = 0

    while run:

        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        time_since_button_press = current_time - button_press_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                tile_landed = False

                if event.key == pygame.K_r:

                    if puzzle_solved:
                        first_score_recorded = True

                        scoreboard.append((move_count, time_elapsed))
                        scoreboard.sort()

                        if len(scoreboard) > 15:
                            scoreboard.pop(-1)

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

                # Keyboard input
                if not puzzle_solved:

                    if not game_started and (event.key == pygame.K_UP or
                                             event.key == pygame.K_DOWN or
                                             event.key == pygame.K_LEFT or
                                             event.key == pygame.K_RIGHT):
                        start_time = time.time()
                        game_started = True

                    if event.key == pygame.K_UP and time_since_button_press > cooldown:
                        if key_up(puzzle_array)[0]:
                            last_keypress = "up"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND1.play()
                            tile_landing_sound_played = False

                    elif event.key == pygame.K_DOWN and time_since_button_press > cooldown:
                        if key_down(puzzle_array)[0]:
                            last_keypress = "down"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND2.play()
                            tile_landing_sound_played = False

                    elif event.key == pygame.K_LEFT and time_since_button_press > cooldown:
                        if key_left(puzzle_array)[0]:
                            last_keypress = "left"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND3.play()
                            tile_landing_sound_played = False

                    elif event.key == pygame.K_RIGHT and time_since_button_press > cooldown:
                        if key_right(puzzle_array)[0]:
                            last_keypress = "right"
                            button_press_time = pygame.time.get_ticks()
                            move_count += 1
                            pixel_counter = 0
                            empty_row_list.append(find_tile_index(0)[0])
                            empty_col_list.append(find_tile_index(0)[1])
                            SLIDE_SOUND4.play()
                            tile_landing_sound_played = False

            # Mouse input
            if not puzzle_solved:

                if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
                    start_time = time.time()
                    game_started = True

                if event.type == pygame.MOUSEBUTTONDOWN and time_since_button_press > cooldown:
                    left_mouse = pygame.mouse.get_pressed()[0]

                    if left_mouse:
                        button_press_time = pygame.time.get_ticks()
                        mouse_pos = pygame.mouse.get_pos()
                        row_clicked, col_clicked = find_tile_clicked(mouse_pos, n, gap_width, sliding_square_size)
                        empty_row, empty_col = find_tile_index(0)

                        if row_clicked is None or col_clicked is None:
                            break

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

            # Check end condition
            if puzzle_array == solved_puzzle_array:
                puzzle_solved = True

        if not puzzle_solved:
            end_time = time.time()

        if puzzle_solved:

            if not victory_sound_played and tile_landed:
                VICTORY_SOUND.play()
                victory_sound_played = True

        if game_started:
            time_elapsed = round(end_time - start_time)

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
