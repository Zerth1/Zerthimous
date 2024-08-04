from enum import Enum, auto
from typing import Any, List, Dict, TypeVar, Generic
import math
import random
import string
import copy
import threading
import pyray
import raylib
import pyttsx3
from framework_import import *

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675


class GameState(Enum):
    LOBBY = auto()
    PLAYING = auto()
    SETTINGS = auto()


game_state = GameState.LOBBY
night_mode = True

sound_engine = pyttsx3.init()
sound_engine.setProperty("rate", 115)


def map_ranges(a: float, b: float, c: float, d: float, n: float) -> float:
    return c + ((n - a) / (b - a)) * (d - c)


def color_wrapper(color: pyray.Color) -> pyray.Color:
    new_color = color
    if night_mode:
        if new_color == pyray.BLACK:
            new_color = pyray.WHITE
    else:
        if new_color == pyray.WHITE:
            new_color = pyray.BLACK
    return pyray.Color(new_color[0], new_color[1], new_color[2], new_color[3])


def get_theme_color() -> pyray.Color:
    if night_mode:
        return pyray.BLACK
    return pyray.WHITE


def change_theme() -> None:
    global night_mode
    night_mode = not night_mode
    zerth_ui.is_night_theme = night_mode


def toggle_settings_ui() -> None:
    global game_state
    pyray.draw_text("Settings", 20, 20, 20, color_wrapper(pyray.WHITE))
    settings_interactable = zerth_ui.Interactable(
        pyray.Rectangle(
            20,
            0,
            pyray.measure_text("Settings", 20),
            40,
        )
    )
    if settings_interactable.check_boundaries():
        if game_state == GameState.SETTINGS:
            game_state = GameState.LOBBY
        else:
            game_state = GameState.SETTINGS


settings_frame = None

shape_stimuli_active = False
color_stimuli_active = False
audio_stimuli_active = False

updated_difficulty = 95


def settings_init(is_init: bool) -> None:
    global settings_frame
    diagonal_distance = 0.125 * math.sqrt((SCREEN_WIDTH**2) + (SCREEN_HEIGHT**2))
    leg = diagonal_distance / math.sqrt(2)
    pyray.draw_rectangle_lines(
        int(leg),
        int(leg),
        SCREEN_WIDTH - int(leg * 2),
        SCREEN_HEIGHT - int(leg * 2),
        color_wrapper(pyray.WHITE),
    )
    pyray.draw_rectangle_lines(
        int(leg / 2),
        int(leg / 2),
        SCREEN_WIDTH - int(leg),
        SCREEN_HEIGHT - int(leg),
        color_wrapper(pyray.WHITE),
    )
    offset = pyray.Vector2(leg * 1.25, leg * 1.25)
    if is_init:

        def enabled_func(name: str, is_enabled: bool) -> None:
            global shape_stimuli_active
            global color_stimuli_active
            global audio_stimuli_active
            if is_enabled:
                match name:
                    case "Shape":
                        shape_stimuli_active = True
                    case "Color":
                        color_stimuli_active = True
                    case "Audio":
                        audio_stimuli_active = True
            else:
                match name:
                    case "Shape":
                        shape_stimuli_active = False
                    case "Color":
                        color_stimuli_active = False
                    case "Audio":
                        audio_stimuli_active = False

        def text_updated_func(updated_text: str) -> None:
            global updated_difficulty
            if updated_text == "":
                return
            updated_difficulty = int(updated_text)

        settings_frame = zerth_ui.ScrollingFrame(
            "Settings",
            pyray.Rectangle(
                int(leg),
                int(leg),
                SCREEN_WIDTH - int(leg * 2),
                SCREEN_HEIGHT - int(leg * 2),
            ),
        )
        settings_frame.enabled = True
        inabstract_stimuli = zerth_ui.OrganizedText(
            "Inabstract Stimuli", offset.x, offset.y, 20, "Rainbow"
        )
        settings_frame.insert_text(inabstract_stimuli)
        shape_stimuli = zerth_ui.OrganizedText(
            "Shape:", offset.x, offset.y + 25, 20, "Blue-Purple"
        )
        shape_check = zerth_ui.CheckButton(
            "Shape",
            pyray.Rectangle(
                offset.x + pyray.measure_text("Shape:", 25) + 5,
                offset.y + 25,
                20,
                20,
            ),
            enabled_func,
        )
        settings_frame.insert_text(shape_stimuli)
        settings_frame.insert_check_button(shape_check)
        color_stimuli = zerth_ui.OrganizedText(
            "Color:", offset.x, offset.y + 50, 20, "Blue-Purple"
        )
        color_check = zerth_ui.CheckButton(
            "Color",
            pyray.Rectangle(
                offset.x + pyray.measure_text("Shape:", 25) + 5,
                offset.y + 50,
                20,
                20,
            ),
            enabled_func,
        )
        settings_frame.insert_text(color_stimuli)
        settings_frame.insert_check_button(color_check)
        audio_stimuli = zerth_ui.OrganizedText(
            "Audio:", offset.x, offset.y + 75, 20, "Blue-Purple"
        )
        audio_check = zerth_ui.CheckButton(
            "Audio",
            pyray.Rectangle(
                offset.x + pyray.measure_text("Shape:", 25) + 5,
                offset.y + 75,
                20,
                20,
            ),
            enabled_func,
        )
        settings_frame.insert_text(audio_stimuli)
        settings_frame.insert_check_button(audio_check)
        abstract_stimuli = zerth_ui.OrganizedText(
            "Abstract Stimuli", offset.x + 200, offset.y, 20, "Rainbow"
        )
        settings_frame.insert_text(abstract_stimuli)
        reflection_stimuli = zerth_ui.OrganizedText(
            "Reflection:", offset.x + 200, offset.y + 25, 20, "Red-Purple"
        )
        reflection_check = zerth_ui.CheckButton(
            "Reflection",
            pyray.Rectangle(
                offset.x + 200 + pyray.measure_text("Reflection:", 25) + 5,
                offset.y + 25,
                20,
                20,
            ),
            enabled_func,
        )
        settings_frame.insert_text(reflection_stimuli)
        settings_frame.insert_check_button(reflection_check)
        rotation_stimuli = zerth_ui.OrganizedText(
            "Rotation:", offset.x + 200, offset.y + 50, 20, "Red-Purple"
        )
        rotation_check = zerth_ui.CheckButton(
            "Rotation",
            pyray.Rectangle(
                offset.x + 200 + pyray.measure_text("Reflection:", 25) + 5,
                offset.y + 50,
                20,
                20,
            ),
            enabled_func,
        )
        settings_frame.insert_text(rotation_stimuli)
        settings_frame.insert_check_button(rotation_check)
        difficulty_text = zerth_ui.OrganizedText(
            "Difficulty[0-100]: ", offset.x, offset.y + 100, 20, "Orange-Yellow"
        )
        difficulty_input = zerth_ui.TextInput(
            "Difficulty",
            "20",
            color_wrapper(pyray.WHITE),
            pyray.Rectangle(
                offset.x + pyray.measure_text("Difficulty[0-100]: ", 20) + 5,
                offset.y + 100,
                100,
                25,
            ),
            text_updated_func,
        )
        settings_frame.insert_text(difficulty_text)
        settings_frame.insert_text_input(difficulty_input)
    toggle_settings_ui()


T = TypeVar("T")


class StaticQueue(Generic[T]):
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.is_full = False
        self.items: list[T] = []

    def enqueue(self, item: T) -> T:
        if len(self.items) == self.capacity:
            items_copy = copy.deepcopy(self.items)
            del items_copy[0]
            items_copy.append(item)
            self.items = items_copy
            return item
        elif len(self.items) == self.capacity - 1:
            self.is_full = True
        self.items.append(item)
        return item

    def clear(self):
        self.items = []
        self.is_full = False


class RandomWithPity:
    def __init__(self, percentage: int, pity: int) -> None:
        self.seed = random.random() * (10 ** random.randint(0, 6))
        self.roll_count = 0
        self.pity_count = 1
        self.percentage = percentage
        self.pity = pity or math.inf

    def roll(self) -> bool:
        self.roll_count += 1
        if self.pity_count % self.pity == 0:
            self.pity_count = 1
            return True
        spin = random.random() < (self.percentage / 100)
        if spin:
            self.pity_count = 1
        else:
            self.pity_count += 1
        return spin

    def continue_sequence(self):
        random.seed(self.seed)
        for _ in range(self.roll_count):
            random.random()

    def reset_seed(self):
        self.seed = random.random() * (10 ** random.randint(0, 6))


def generate_square(center: pyray.Vector2, color: pyray.Color) -> None:
    pyray.draw_rectangle(int(center.x - 30), int(center.y + 30), 60, 60, color)


def generate_circle(center: pyray.Vector2, color: pyray.Color) -> None:
    pyray.draw_circle(int(center.x), int(center.y + 60), 30, color)


def generate_square_lines(center: pyray.Vector2, color: pyray.Color) -> None:
    pyray.draw_rectangle(int(center.x - 30), int(center.y + 30), 60, 60, color)
    pyray.draw_rectangle(
        int(center.x - 20), int(center.y + 40), 40, 40, get_theme_color()
    )


def generate_circle_lines(center: pyray.Vector2, color: pyray.Color) -> None:
    pyray.draw_circle(int(center.x), int(center.y + 60), 30, color)
    pyray.draw_circle(int(center.x), int(center.y + 60), 20, get_theme_color())


def draw_grid():
    left_most = (SCREEN_WIDTH / 2) - 180
    right_most = (SCREEN_WIDTH / 2) + 180
    top_most = (SCREEN_HEIGHT / 2) - 180
    bottom_most = (SCREEN_HEIGHT / 2) + 180
    for i in range(7):
        pyray.draw_line(
            int(left_most),
            int(top_most + (i * 60)),
            int(right_most),
            int(top_most + (i * 60)),
            color_wrapper(pyray.WHITE),
        )
    for j in range(7):
        pyray.draw_line(
            int(left_most + (j * 60)),
            int(top_most),
            int(left_most + (j * 60)),
            int(bottom_most),
            color_wrapper(pyray.WHITE),
        )


def generate_grid() -> list[list[pyray.Vector2]]:
    left_most = (SCREEN_WIDTH / 2) - 180
    right_most = (SCREEN_WIDTH / 2) + 180
    top_most = (SCREEN_HEIGHT / 2) - 180
    bottom_most = (SCREEN_HEIGHT / 2) + 180
    grid = []
    for i in range(6):
        grid.append([])
        for j in range(6):
            grid[i].append(
                pyray.Vector2(
                    int(left_most + (j * 60) + 30), int(top_most + (i * 60) - 30)
                )
            )
    return grid


shapes = ["Square", "Circle", "Square_Lines", "Circle_Lines"]
game_colors = [pyray.RED, pyray.GREEN, pyray.BLUE]


def regenerate_random_cell_count(
    squares_left: int, max_cells_per_row: float, i: int
) -> int:
    choice = random.randint(0, min(math.ceil(max_cells_per_row) + 1, 6))
    average_cells_per_row = (squares_left - choice) / (6 - (i + 1))
    if average_cells_per_row > max_cells_per_row:
        return regenerate_random_cell_count(squares_left, max_cells_per_row, i)
    return choice


class TrialCacheTypes(Enum):
    TRIAL_GRID = auto()
    SHAPE_MAP = auto()
    COLOR_MAP = auto()
    AUDIO_MAP = auto()


trial_cache = StaticQueue[Dict[TrialCacheTypes, List[Any]]](3)
current_trial_grid = []
current_shape_map = []
current_color_map = []
current_audio_map = []
grid_cooldown = zerth_cooldown.Cooldown("Grid", 3.0)
appear_cooldown = zerth_cooldown.Cooldown("Appear", 3.0 - 2.0)

random_position_object = RandomWithPity(33, 5)
random_shape_object = RandomWithPity(33, 3)
random_color_object = RandomWithPity(33, 5)
random_audio_object = RandomWithPity(15, 6)
was_previous_position = False

grid_enabled = True


def play_sound_wrapper(word: str) -> None:
    sound_engine.say(word)
    sound_engine.runAndWait()


last_key = ""


def get_raw_key_bind(serialized: str) -> int:
    if serialized == "a":
        return raylib.KEY_A
    elif serialized == "s":
        return raylib.KEY_S
    elif serialized == "d":
        return raylib.KEY_D
    elif serialized == "f":
        return raylib.KEY_F
    elif serialized == "g":
        return raylib.KEY_G
    elif serialized == "h":
        return raylib.KEY_H
    elif serialized == "j":
        return raylib.KEY_J
    elif serialized == "k":
        return raylib.KEY_K
    elif serialized == "l":
        return raylib.KEY_L
    return 0


position_light_up = False
shape_light_up = False
color_light_up = False
audio_light_up = False


def draw_game_buttons() -> None:
    global position_light_up
    global shape_light_up
    global color_light_up
    global audio_light_up
    stimuli_display_order = ["Position"]
    stimuli_key_binds = "asdfghjkl"
    if shape_stimuli_active:
        stimuli_display_order.append("Shape")
    if color_stimuli_active:
        stimuli_display_order.append("Color")
    if audio_stimuli_active:
        stimuli_display_order.append("Audio")
    for index in range(len(stimuli_display_order)):
        to_display = stimuli_display_order[index]
        to_bind = stimuli_key_binds[index]
        stimuli_text = to_display + "[" + to_bind.upper() + "]"
        display_color = color_wrapper(pyray.WHITE)
        if pyray.is_key_pressed(get_raw_key_bind(to_bind)):
            if is_replicate_position and to_display == "Position":
                position_light_up = True
                display_color = pyray.GREEN
            if is_replicate_shape and to_display == "Shape":
                shape_light_up = True
                display_color = pyray.GREEN
            if is_replicate_color and to_display == "Color":
                color_light_up = True
                display_color = pyray.GREEN
            if is_replicate_audio and to_display == "Audio":
                audio_light_up = True
                display_color = pyray.GREEN
        if (
            (position_light_up and to_display == "Position")
            or (shape_light_up and to_display == "Shape")
            or (color_light_up and to_display == "Color")
            or (audio_light_up and to_display == "Audio")
        ):
            display_color = pyray.GREEN
        pyray.draw_text(
            stimuli_text,
            int((SCREEN_WIDTH / 7) * 1),
            int((SCREEN_HEIGHT / 2) * 1) + (index * 40),
            25,
            display_color,
        )


is_replicate_position = False
is_replicate_shape = False
is_replicate_color = False
is_replicate_audio = False


def game_init() -> None:
    global current_trial_grid
    global current_shape_map
    global current_color_map
    global current_audio_map
    global last_key

    global is_replicate_position
    global is_replicate_shape
    global is_replicate_color
    global is_replicate_audio
    global position_light_up
    global shape_light_up
    global color_light_up
    global audio_light_up
    global was_previous_position
    global grid_enabled
    grid = generate_grid()
    if grid_cooldown.is_not_enabled():
        if grid_enabled:
            is_replicate_position = False
            is_replicate_shape = False
            is_replicate_color = False
            if trial_cache.is_full:
                if not was_previous_position:
                    random_position_object.continue_sequence()
                    is_replicate_position = random_position_object.roll()
                    if is_replicate_position:
                        if shape_stimuli_active:
                            random_shape_object.continue_sequence()
                            is_replicate_shape = random_shape_object.roll()
                        if color_stimuli_active:
                            random_color_object.continue_sequence()
                            is_replicate_color = random_color_object.roll()
            actual_number_of_squares = 0
            if not is_replicate_position:
                number_of_squares = int(
                    map_ranges(0, 100, 4, 12, updated_difficulty)
                ) - random.randint(0, 2)
                actual_number_of_squares = number_of_squares
                max_cells_per_row = number_of_squares / 6
                organization = []
                squares_left = number_of_squares
                for i in range(6):
                    if i == 5:
                        organization.append(squares_left)
                        continue
                    cell_count = regenerate_random_cell_count(
                        squares_left, max_cells_per_row, i
                    )
                    if squares_left - cell_count < 0:
                        organization.append(squares_left)
                        squares_left = 0
                    else:
                        organization.append(cell_count)
                        squares_left -= cell_count
                random.shuffle(organization)
                current_trial_grid = []
                for i in range(6):
                    row = organization[i]
                    indices = []
                    six_elements = [i for i in range(6)]
                    if row > 0:
                        while len(six_elements) > 0:
                            random_index = random.randint(0, 5)
                            if random_index not in indices:
                                indices.append(random_index)
                                six_elements.remove(random_index)
                                if len(indices) == row:
                                    break
                    current_trial_grid.append(indices)
            else:
                current_trial_grid = trial_cache.items[0][TrialCacheTypes.TRIAL_GRID]
                actual_number_of_squares = sum([len(i) for i in current_trial_grid])
            if shape_stimuli_active:
                if not is_replicate_shape:
                    original_shapes_size = len(shapes)
                    current_shape_map = []
                    for i in range(len(shapes)):
                        current_shape_map = current_shape_map + [
                            shapes[i]
                        ] * math.floor(actual_number_of_squares / original_shapes_size)
                    remainder = actual_number_of_squares - len(current_shape_map)
                    if remainder > 0:
                        for i in range(remainder):
                            current_shape_map.append(random.choice(shapes))
                    random.shuffle(current_shape_map)
                else:
                    current_shape_map = trial_cache.items[0][TrialCacheTypes.SHAPE_MAP]
            else:
                current_shape_map = ["Square"] * actual_number_of_squares
            if color_stimuli_active:
                if not is_replicate_color:
                    original_colors_size = len(game_colors)
                    current_color_map = []
                    for i in range(len(game_colors)):
                        current_color_map = current_color_map + [
                            game_colors[i]
                        ] * math.floor(actual_number_of_squares / original_colors_size)
                    remainder = actual_number_of_squares - len(current_color_map)
                    if remainder > 0:
                        for i in range(remainder):
                            current_color_map.append(random.choice(game_colors))
                    random.shuffle(current_color_map)
                else:
                    current_color_map = trial_cache.items[0][TrialCacheTypes.COLOR_MAP]
            else:
                current_color_map = [pyray.RED] * actual_number_of_squares
            if audio_stimuli_active:
                current_audio_map = []
                current_audio_map.append(last_key)
            trial_cache.enqueue(
                {
                    TrialCacheTypes.TRIAL_GRID: copy.deepcopy(current_trial_grid),
                    TrialCacheTypes.SHAPE_MAP: copy.deepcopy(current_shape_map),
                    TrialCacheTypes.COLOR_MAP: copy.deepcopy(current_color_map),
                    TrialCacheTypes.AUDIO_MAP: copy.deepcopy(current_audio_map),
                }
            )
            if was_previous_position:
                was_previous_position = False
            else:
                if is_replicate_position:
                    was_previous_position = True
    if grid_enabled:
        if grid_cooldown.is_not_enabled():
            grid_enabled = False
            position_light_up = False
            shape_light_up = False
            color_light_up = False
            audio_light_up = False
            appear_cooldown.reset()
        iteration = 0
        for i in range(6):
            row = current_trial_grid[i]
            for j in range(6):
                if j in row:
                    match current_shape_map[iteration]:
                        case "Square":
                            generate_square(grid[i][j], current_color_map[iteration])
                        case "Circle":
                            generate_circle(grid[i][j], current_color_map[iteration])
                        case "Square_Lines":
                            generate_square_lines(
                                grid[i][j], current_color_map[iteration]
                            )
                        case "Circle_Lines":
                            generate_circle_lines(
                                grid[i][j], current_color_map[iteration]
                            )
                    iteration += 1
    else:
        if appear_cooldown.is_not_enabled():
            grid_cooldown.reset()
            grid_enabled = True
            if audio_stimuli_active:
                random_audio_object.continue_sequence()
                is_replicate_audio = random_audio_object.roll()
                if trial_cache.is_full and is_replicate_audio:
                    last_key = trial_cache.items[0][TrialCacheTypes.AUDIO_MAP][0]
                    if not last_key:
                        last_key = random.choice(string.ascii_lowercase)
                else:
                    last_key = random.choice(string.ascii_lowercase)
                playback = threading.Thread(
                    target=play_sound_wrapper,
                    args=(last_key),
                )
                playback.start()
    draw_game_buttons()
    draw_grid()


def vector2_is_greater(v1: pyray.Vector2, v2: pyray.Vector2) -> bool:
    return (v1.x > v2.x) and (v1.y > v2.y)


def remove_vector_duplicates(vector_list: list[pyray.Vector2]) -> list[pyray.Vector2]:
    list_copy = []
    hash_map = {}
    for vector in vector_list:
        if not hash_map.get(vector.x):
            hash_map[vector.x] = {}
        if not hash_map[vector.x].get(vector.y):
            hash_map[vector.x][vector.y] = True
    for vector in vector_list:
        if hash_map[vector.x].get(vector.y):
            list_copy.append(vector)
            del hash_map[vector.x][vector.y]
    return list_copy


def keep_vector_duplicates(vector_list: list[pyray.Vector2]) -> list[pyray.Vector2]:
    list_copy = []
    hash_map = {}
    for vector in vector_list:
        if not hash_map.get(vector.x):
            hash_map[vector.x] = {}
        if hash_map[vector.x].get(vector.y) is None:
            hash_map[vector.x][vector.y] = False
        else:
            hash_map[vector.x][vector.y] = True
    for vector in vector_list:
        if hash_map[vector.x][vector.y]:
            list_copy.append(vector)
            hash_map[vector.x][vector.y] = False
    return list_copy


def vector_intersection(
    v1: list[pyray.Vector2], v2: list[pyray.Vector2]
) -> list[pyray.Vector2]:
    return keep_vector_duplicates(v1 + v2)


def vector3_to_vector2(vector: pyray.Vector3) -> pyray.Vector2:
    return pyray.Vector2(vector.x, vector.y)


initialization = True
initialization_text = "Welcome to Zerthimous. This is a brain training app."
initialization_dialogue = None

settings_initialization = True
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Zerthimous")
camera = pyray.Camera2D(
    (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 0, 1
)
camera_box = pyray.Rectangle(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100, 200, 200)
camera_box_edges = {
    "Top": [
        pyray.Vector2((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) - 100),
        pyray.Vector2((SCREEN_WIDTH / 2) + 100, (SCREEN_HEIGHT / 2) - 100),
    ],
    "Bottom": [
        pyray.Vector2((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) + 100),
        pyray.Vector2((SCREEN_WIDTH / 2) + 100, (SCREEN_HEIGHT / 2) + 100),
    ],
    "Left": [
        pyray.Vector2((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) + 100),
        pyray.Vector2((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) - 100),
    ],
    "Right": [
        pyray.Vector2((SCREEN_WIDTH / 2) + 100, (SCREEN_HEIGHT / 2) + 100),
        pyray.Vector2((SCREEN_WIDTH / 2) + 100, (SCREEN_HEIGHT / 2) - 100),
    ],
}
camera_offset = pyray.Vector2(0, 0)
last_camera_origin = pyray.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
camera_direction = pyray.Vector2(-0.25, 1)
camera_speed = 0.05
# change_theme()
while not pyray.window_should_close():
    pyray.begin_drawing()
    pyray.clear_background(get_theme_color())
    zerth_ui.ScrollingFrame.update()
    zerth_ui.TextInput.update()
    zerth_ui.CheckButton.update()
    zerth_ui.Dialogue.update()
    if pyray.get_time() > 3:
        match game_state:
            case GameState.LOBBY:
                if settings_frame:
                    settings_frame.enabled = False
                if initialization:
                    initialization = False
                    initialization_dialogue = zerth_ui.Dialogue(
                        initialization_text,
                        zerth_ui.clean_color_permutation(
                            zerth_ui.PRESET_COLOR_RANGES["Green-Yellow"],
                            night_mode,
                        ),
                        pyray.Vector2(0, 0),
                        pyray.Vector2(
                            (SCREEN_WIDTH / 2)
                            - (pyray.measure_text(initialization_text, 20) / 2),
                            (SCREEN_HEIGHT / 6) * 5,
                        ),
                    )
                elif initialization_dialogue and not initialization_dialogue.enabled:
                    if pyray.is_key_pressed(raylib.KEY_SPACE):
                        game_state = GameState.PLAYING
                    else:
                        pyray.draw_text(
                            "Zerthimous",
                            int(
                                SCREEN_WIDTH / 2
                                - (pyray.measure_text("Zerthimous", 50) / 2)
                            ),
                            int((SCREEN_HEIGHT / 8) * 1),
                            50,
                            color_wrapper(pyray.YELLOW),
                        )
                        pyray.draw_text(
                            "Press [Space] to train",
                            int(
                                SCREEN_WIDTH / 2
                                - (pyray.measure_text("Press [Space] to train", 25) / 2)
                            ),
                            int((SCREEN_HEIGHT / 6) * 5),
                            25,
                            color_wrapper(pyray.YELLOW),
                        )
                        toggle_settings_ui()
                        pyray.begin_mode_2d(camera)
                        camera_speed -= 0.0000075
                        camera_speed = max(camera_speed, 0.015)
                        camera_offset = pyray.vector2_add(
                            camera_offset,
                            pyray.vector2_scale(
                                pyray.vector2_normalize(camera_direction), camera_speed
                            ),
                        )
                        new_target = pyray.Vector2(
                            last_camera_origin.x + camera_offset.x,
                            last_camera_origin.y + camera_offset.y,
                        )
                        horizontal_vertices = []
                        vertical_vertices = []
                        if pyray.check_collision_point_rec(new_target, camera_box):
                            camera.target = new_target
                        else:
                            for edge in camera_box_edges.values():
                                if camera_direction.x < 0:
                                    for vertex in edge:
                                        if vertex.x < SCREEN_WIDTH / 2:
                                            horizontal_vertices.append(vertex)
                                else:
                                    for vertex in edge:
                                        if vertex.x > SCREEN_WIDTH / 2:
                                            horizontal_vertices.append(vertex)
                                if camera_direction.y < 0:
                                    for vertex in edge:
                                        if vertex.y > SCREEN_HEIGHT / 2:
                                            vertical_vertices.append(vertex)
                                else:
                                    for vertex in edge:
                                        if vertex.y < SCREEN_HEIGHT / 2:
                                            vertical_vertices.append(vertex)
                            vertex_link = vector_intersection(
                                remove_vector_duplicates(horizontal_vertices),
                                remove_vector_duplicates(vertical_vertices),
                            )[0]
                            potential_edges = {}
                            for i, edge in camera_box_edges.items():
                                for vertex in edge:
                                    if pyray.vector2_equals(vertex, vertex_link):
                                        potential_edges[i] = edge
                                        break
                            for i, edge in potential_edges.copy().items():
                                complement_height_origin = (
                                    SCREEN_HEIGHT - last_camera_origin.y
                                )
                                complement_height_target = (
                                    SCREEN_HEIGHT - camera.target.y
                                )
                                slope = (
                                    complement_height_origin - complement_height_target
                                ) / (last_camera_origin.x - camera.target.x)
                                y_intercept = complement_height_origin - (
                                    slope * last_camera_origin.x
                                )
                                intersection_x = 0.0
                                intersection_y = 0.0
                                if i == "Top" or i == "Bottom":
                                    intersection_y = edge[0].y
                                    intersection_x = (1 / slope) * (
                                        intersection_y - y_intercept
                                    )
                                else:
                                    intersection_x = edge[0].x
                                    intersection_y = (
                                        slope * intersection_x
                                    ) + y_intercept
                                transformed = pyray.vector2_add(
                                    pyray.vector2_scale(
                                        pyray.Vector2(
                                            (intersection_x) - last_camera_origin.x,
                                            (SCREEN_HEIGHT - intersection_y)
                                            - last_camera_origin.y,
                                        ),
                                        0.999,
                                    ),
                                    last_camera_origin,
                                )
                                if pyray.check_collision_point_rec(
                                    transformed, camera_box
                                ):
                                    last_camera_origin = transformed
                                    camera_offset = pyray.vector2_zero()
                                    camera_direction = pyray.vector2_normalize(
                                        vector3_to_vector2(
                                            pyray.vector3_cross_product(
                                                pyray.Vector3(
                                                    -camera_direction.x,
                                                    -camera_direction.y,
                                                    0,
                                                ),
                                                pyray.Vector3(0, 0, 1),
                                            )
                                        )
                                    )
                                    camera_speed = 0.05
                                    break
                                    # print(camera_direction.x, camera_direction.y)
                        pyray.rl_push_matrix()
                        pyray.rl_translatef(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0)
                        pyray.rl_rotatef(pyray.get_time() * 0.25 * 45.0, 0, 0, -1)
                        pyray.draw_ellipse_lines(
                            0,
                            0,
                            50,
                            200,
                            pyray.RED,
                        )
                        for _ in range(3):
                            pyray.rl_rotatef(45.0, 0, 0, -1)
                            pyray.draw_ellipse_lines(
                                0,
                                0,
                                50,
                                200,
                                pyray.RED,
                            )
                        pyray.rl_pop_matrix()
                        pyray.end_mode_2d()
            case GameState.SETTINGS:
                settings_init(settings_initialization)
                if settings_frame:
                    settings_frame.enabled = True
                if settings_initialization:
                    settings_initialization = False
            case GameState.PLAYING:
                if settings_frame:
                    settings_frame.enabled = False
                if pyray.is_key_pressed(raylib.KEY_SLASH):
                    game_state = GameState.LOBBY
                    is_replicate_position = False
                    is_replicate_shape = False
                    is_replicate_color = False
                    is_replicate_audio = False
                    position_light_up = False
                    shape_light_up = False
                    color_light_up = False
                    audio_light_up = False
                    grid_enabled = True
                    trial_cache = StaticQueue[Dict[TrialCacheTypes, List[Any]]](3)
                else:
                    game_init()
    pyray.end_drawing()
    zerth_cooldown.Cooldown.update()
pyray.close_window()
