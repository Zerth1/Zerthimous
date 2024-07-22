from enum import Enum, auto
import math
import threading
import json
import openai
import pyray
from pyray import (
    BLACK,
    GREEN,
    RED,
    WHITE,
    YELLOW,
)
from openai import OpenAI
from raylib.defines import raylib

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
CIRCLE_RADIUS = 150

DEFAULT_SCALE = 30
DEFAULT_WORD_COUNT = 4


def lerp(a: float, b: float, t: float) -> float:
    return a + t * (b - a)


class ZerthimousState(Enum):
    LOBBY = auto()
    PLAYING = auto()
    SETTINGS = auto()


class Cooldown:
    def __init__(self, name: str, cooldown_time: float) -> None:
        self.cooldown_time = cooldown_time
        self.acc = pyray.get_time()
        self.enabled = True
        self.name = name

    def update(self) -> None:
        if self.is_not_enabled():
            return
        if pyray.get_time() - self.acc > self.cooldown_time:
            self.acc = pyray.get_time()
            self.enabled = False

    def reset(self) -> None:
        is_not_enabled = self.is_not_enabled()
        if is_not_enabled:
            self.enabled = True

    def is_not_enabled(self) -> bool:
        return not self.enabled


cooldown_objects: dict[str, Cooldown] = {}


def construct_cooldown(name: str, cooldown_time: float) -> Cooldown:
    cooldown_objects[name] = Cooldown(name, cooldown_time)
    return cooldown_objects[name]


camera = pyray.Camera2D(
    (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 0, 1
)
pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Zerthimous")
client = OpenAI()
zerthimous_state = ZerthimousState.LOBBY
lobby_text = "Welcome to Zerthimous! This is a verbal training app."
lobby_text_cooldown = construct_cooldown("lobby_text", 0.125)
lobby_text_index = 0

enter_game_text = "Press [Space] to start training"

RAINBOW = [
    pyray.Color(254, 0, 0, 1),
    pyray.Color(253, 254, 2, 1),
    pyray.Color(11, 255, 1, 1),
    pyray.Color(1, 30, 254, 1),
    pyray.Color(254, 0, 246, 1),
]


def lobby_init(can_dialogue: bool) -> bool:
    global lobby_text_index
    global zerthimous_state
    current_alpha = (pyray.get_time() % 1.5) / 1.5
    current_index = math.floor(((pyray.get_time() / 1.5) % len(RAINBOW)))
    if can_dialogue:
        if not lobby_text_cooldown.is_not_enabled():
            pyray.draw_text(
                lobby_text[0:lobby_text_index],
                int(SCREEN_WIDTH / 2) - int(pyray.measure_text(lobby_text, 20) / 2),
                int(SCREEN_HEIGHT / 2),
                20,
                pyray.Color(
                    int(
                        lerp(
                            RAINBOW[current_index].r,
                            RAINBOW[(current_index + 1) % len(RAINBOW)].r,
                            current_alpha,
                        )
                    ),
                    int(
                        lerp(
                            RAINBOW[current_index].g,
                            RAINBOW[(current_index + 1) % len(RAINBOW)].g,
                            current_alpha,
                        )
                    ),
                    int(
                        lerp(
                            RAINBOW[current_index].b,
                            RAINBOW[(current_index + 1) % len(RAINBOW)].b,
                            current_alpha,
                        )
                    ),
                    255,
                ),
            )
            return False
        lobby_text_cooldown.reset()
        lobby_text_index += 1
        pyray.draw_text(
            lobby_text[0:lobby_text_index],
            int(SCREEN_WIDTH / 2) - int(pyray.measure_text(lobby_text, 20) / 2),
            int(SCREEN_HEIGHT / 2),
            20,
            pyray.Color(
                int(
                    lerp(
                        RAINBOW[current_index].r,
                        RAINBOW[(current_index + 1) % len(RAINBOW)].r,
                        current_alpha,
                    )
                ),
                int(
                    lerp(
                        RAINBOW[current_index].g,
                        RAINBOW[(current_index + 1) % len(RAINBOW)].g,
                        current_alpha,
                    )
                ),
                int(
                    lerp(
                        RAINBOW[current_index].b,
                        RAINBOW[(current_index + 1) % len(RAINBOW)].b,
                        current_alpha,
                    )
                ),
                255,
            ),
        )
        if lobby_text_index == len(lobby_text) + 1:
            return True
        return False
    pyray.draw_text("Settings", 20, 20, 20, WHITE)
    pyray.draw_text(
        enter_game_text,
        int(SCREEN_WIDTH / 2) - int(pyray.measure_text(enter_game_text, 20) / 2),
        int(SCREEN_HEIGHT / 4) * 3,
        20,
        YELLOW,
    )
    pyray.draw_text(
        "Zerthimous",
        int(SCREEN_WIDTH / 2) - int(pyray.measure_text("Zerthimous", 80) / 2),
        int(SCREEN_HEIGHT / 6) * 1,
        80,
        RED,
    )
    toggle_settings_ui()
    return True


game_metadata = None


def game_init() -> None:
    global game_metadata
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a very divergent thinker and have an endless pool of english vocabulary and is a perfect speller. You dont recycle words from previous responses when asked to generate a list of words.",
            },
            {
                "role": "user",
                "content": (
                    "On a scale of 0-100 from most easiest to most difficult, I would like you to generate {word_count} english only words that you can create a story with given the number {scale} on the scale. Do not generate a story. Generate only a json file's contents without file specifiers with 'words' as a field and an array of the words as the value. Do not include any other text in your response."
                ).format(scale=int(scale_text), word_count=int(word_count_text)),
            },
        ],
        temperature=1.75,
    )
    content = response.choices[0].message.content
    if content is not None:
        print(content)
        game_metadata = json.loads(content)
        print(game_metadata["words"])
    else:
        game_init()


def parse_game_metadata() -> None:
    if not game_metadata:
        return
    words_size = len(game_metadata["words"])
    for i, word in enumerate(game_metadata["words"]):
        pyray.draw_line(
            int(SCREEN_WIDTH / 2),
            int(SCREEN_HEIGHT / 2),
            int(SCREEN_WIDTH / 2)
            + int(CIRCLE_RADIUS * math.cos(i * (2 * (math.pi / words_size)))),
            int(SCREEN_HEIGHT / 2)
            + int(CIRCLE_RADIUS * -math.sin(i * (2 * (math.pi / words_size)))),
            GREEN,
        )
        pyray.draw_text(
            word,
            int(SCREEN_WIDTH / 2)
            + int(CIRCLE_RADIUS * math.cos(i * (2 * (math.pi / words_size))))
            - int(pyray.measure_text(word, 20) / 2),
            int(SCREEN_HEIGHT / 2)
            + int(CIRCLE_RADIUS * -math.sin(i * (2 * (math.pi / words_size)))),
            20,
            YELLOW,
        )
    pyray.draw_circle_gradient(
        int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), CIRCLE_RADIUS / 7, GREEN, YELLOW
    )


def toggle_settings_ui() -> None:
    global zerthimous_state
    mouse_position = pyray.get_mouse_position()
    pyray.draw_text("Settings", 20, 20, 20, WHITE)
    if pyray.is_mouse_button_pressed(raylib.MOUSE_BUTTON_LEFT):
        if pyray.check_collision_point_rec(
            mouse_position,
            pyray.Rectangle(
                20,
                0,
                pyray.measure_text("Settings", 20),
                40,
            ),
        ):
            if zerthimous_state == ZerthimousState.SETTINGS:
                zerthimous_state = ZerthimousState.LOBBY
            else:
                zerthimous_state = ZerthimousState.SETTINGS


scale_text = str(DEFAULT_SCALE)
word_count_text = str(DEFAULT_WORD_COUNT)
backspace_detected = False


def settings_init() -> None:
    global scale_text
    global backspace_detected
    global word_count_text
    diagonal_distance = 0.125 * math.sqrt((SCREEN_WIDTH**2) + (SCREEN_HEIGHT**2))
    leg = diagonal_distance / math.sqrt(2)
    pyray.draw_rectangle_lines(
        int(leg),
        int(leg),
        SCREEN_WIDTH - int(leg * 2),
        SCREEN_HEIGHT - int(leg * 2),
        WHITE,
    )
    pyray.draw_rectangle_lines(
        int(leg / 2),
        int(leg / 2),
        SCREEN_WIDTH - int(leg),
        SCREEN_HEIGHT - int(leg),
        WHITE,
    )
    offset = pyray.Vector2(leg * 1.5, leg * 1.5)
    scale_textbox = pyray.Rectangle(offset.x + 200, offset.y, 100, 25)
    mouse_scale_flag = pyray.check_collision_point_rec(
        pyray.get_mouse_position(), scale_textbox
    )
    if mouse_scale_flag:
        if pyray.is_key_up(raylib.KEY_BACKSPACE):
            backspace_detected = False
        if (
            pyray.is_key_down(raylib.KEY_BACKSPACE)
            and len(scale_text) > 0
            and not backspace_detected
        ):
            backspace_detected = True
            scale_text = scale_text[0 : len(scale_text) - 1]
        pressed = pyray.get_char_pressed()
        while pressed > 0:
            scale_text += chr(pressed)
            pressed = pyray.get_char_pressed()
    pyray.draw_rectangle_rec(scale_textbox, WHITE)
    pyray.draw_text(
        "Scale:", int(scale_textbox.x - 200), int(scale_textbox.y), 25, YELLOW
    )
    pyray.draw_text(
        scale_text, int(scale_textbox.x + 10), int(scale_textbox.y), 25, BLACK
    )
    word_textbox = pyray.Rectangle(offset.x + 200, offset.y + 50, 100, 25)
    mouse_word_flag = pyray.check_collision_point_rec(
        pyray.get_mouse_position(), word_textbox
    )
    if mouse_word_flag:
        if pyray.is_key_up(raylib.KEY_BACKSPACE):
            backspace_detected = False
        if (
            pyray.is_key_down(raylib.KEY_BACKSPACE)
            and len(word_count_text) > 0
            and not backspace_detected
        ):
            backspace_detected = True
            word_count_text = word_count_text[0 : len(word_count_text) - 1]
        pressed = pyray.get_char_pressed()
        while pressed > 0:
            word_count_text += chr(pressed)
            pressed = pyray.get_char_pressed()
    pyray.draw_rectangle_rec(word_textbox, WHITE)
    pyray.draw_text(
        "Word Count:", int(word_textbox.x - 200), int(word_textbox.y), 25, YELLOW
    )
    pyray.draw_text(
        word_count_text, int(word_textbox.x + 10), int(word_textbox.y), 25, BLACK
    )
    toggle_settings_ui()


is_in_intermission = True
dialogue_exited = False
game_active = False
camera_offset = pyray.Vector2(0, 0)
while not pyray.window_should_close():
    camera.zoom += pyray.get_mouse_wheel_move() * 0.025
    pyray.begin_drawing()
    pyray.clear_background(BLACK)
    if pyray.is_key_down(raylib.KEY_W):
        camera_offset.y -= 1
    elif pyray.is_key_down(raylib.KEY_A):
        camera_offset.x -= 1
    elif pyray.is_key_down(raylib.KEY_S):
        camera_offset.y += 1
    elif pyray.is_key_down(raylib.KEY_D):
        camera_offset.x += 1
    camera.target = (
        (SCREEN_WIDTH / 2.0) + camera_offset.x,
        (SCREEN_HEIGHT / 2.0) + camera_offset.y,
    )
    if pyray.is_key_down(raylib.KEY_SLASH):
        zerthimous_state = ZerthimousState.LOBBY
    if is_in_intermission:
        if pyray.get_time() > 3.0:
            is_in_intermission = False
    else:
        match zerthimous_state:
            case ZerthimousState.LOBBY:
                camera_offset.x = 0
                camera_offset.y = 0
                dialogue_exited = lobby_init(not dialogue_exited)
                if dialogue_exited and pyray.is_key_down(raylib.KEY_SPACE):
                    zerthimous_state = ZerthimousState.PLAYING
            case ZerthimousState.PLAYING:
                if not game_active:
                    game_active = True
                    thread = threading.Thread(target=game_init)
                    thread.start()
                pyray.begin_mode_2d(camera)
                parse_game_metadata()
                pyray.end_mode_2d()
                pyray.draw_text(
                    "Regenerate",
                    int(SCREEN_WIDTH / 2)
                    - int(pyray.measure_text("Regenerate", 40) / 2),
                    int(SCREEN_HEIGHT / 4) * 3,
                    40,
                    RED,
                )
                if pyray.is_mouse_button_pressed(raylib.MOUSE_BUTTON_LEFT):
                    if pyray.check_collision_point_rec(
                        pyray.get_mouse_position(),
                        pyray.Rectangle(
                            int(SCREEN_WIDTH / 2)
                            - int(pyray.measure_text("Regenerate", 40) / 2),
                            int((SCREEN_HEIGHT / 4) * 3) - 40,
                            pyray.measure_text("Regenerate", 40),
                            80,
                        ),
                    ):
                        game_active = False
            case ZerthimousState.SETTINGS:
                settings_init()
    pyray.end_drawing()
    for i, cooldown in cooldown_objects.items():
        cooldown.update()
pyray.close_window()
