import curses
import time
import random
import threading
import math
import socket
import json

STATE_IDLE = "idle"
STATE_SPEAKING = "speaking"
STATE_THINKING = "thinking"
STATE_LISTENING = "listening"
STATE_SHOWING = "showing"

current_state = STATE_IDLE
current_text = ""
current_input = ""
last_user = ""
last_voris = ""
running = True

MATRIX_CHARS = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

FACE_IDLE = [
    "          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ",
    "       ▓▓▓░░░░░░░░░░░░░░░░░░░▓▓▓       ",
    "     ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░▓▓     ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▀▀▓▓░░░░░░░░░░░▓▓▀▀▓▓░░░░░░▓  ",
    "  ▓░░░▓▓██▓▓░░░░░░░░░░░▓▓██▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "   ▓░░░░░░░░░░░░▓░░░░░░░░░░░░░░░░░▓   ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "    ▓░░░░░░░░░▓▓▓▓▓▓▓░░░░░░░░░░░▓    ",
    "     ▓░░░░░░░░░░░░░░░░░░░░░░░░░▓     ",
    "      ▓▓░░░░░░░░░░░░░░░░░░░░░▓▓      ",
    "        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ",
]

FACE_SPEAKING = [
    "          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ",
    "       ▓▓▓░░░░░░░░░░░░░░░░░░░▓▓▓       ",
    "     ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░▓▓     ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▄▄▓▓░░░░░░░░░░░▓▓▄▄▓▓░░░░░░▓  ",
    "  ▓░░░▓▓██▓▓░░░░░░░░░░░▓▓██▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "   ▓░░░░░░░░░░░░▓░░░░░░░░░░░░░░░░░▓   ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "    ▓░░░░░░░░▓░▓░▓░▓░▓░░░░░░░░░░▓    ",
    "     ▓░░░░░░░░░░░░░░░░░░░░░░░░░▓     ",
    "      ▓▓░░░░░░░░░░░░░░░░░░░░░▓▓      ",
    "        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ",
]

FACE_THINKING = [
    "          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ",
    "       ▓▓▓░░░░░░░░░░░░░░░░░░░▓▓▓       ",
    "     ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░▓▓     ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "  ▓░░░▓▓──▓▓░░░░░░░░░░░▓▓▀▀▓▓░░░░░░▓  ",
    "  ▓░░░▓▓██▓▓░░░░░░░░░░░▓▓██▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "   ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓   ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "    ▓░░░░░░░░░▓▓░░░▓▓░░░░░░░░░░░▓    ",
    "     ▓░░░░░░░░░░░░░░░░░░░░░░░░░▓     ",
    "      ▓▓░░░░░░░░░░░░░░░░░░░░░▓▓      ",
    "        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ",
]

FACE_LISTENING = [
    "          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ",
    "       ▓▓▓░░░░░░░░░░░░░░░░░░░▓▓▓       ",
    "     ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░▓▓     ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▲▲▓▓░░░░░░░░░░░▓▓▲▲▓▓░░░░░░▓  ",
    "  ▓░░░▓▓██▓▓░░░░░░░░░░░▓▓██▓▓░░░░░░▓  ",
    "  ▓░░░▓▓▓▓▓▓░░░░░░░░░░░▓▓▓▓▓▓░░░░░░▓  ",
    "   ▓░░░▓▓▓▓░░░░░░░░░░░░░▓▓▓▓░░░░░░▓   ",
    "   ▓░░░░░░░░░░░░▓░░░░░░░░░░░░░░░░░▓   ",
    "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓    ",
    "    ▓░░░░░░░░░▓▓▓▓▓▓▓░░░░░░░░░░░▓    ",
    "     ▓░░░░░░░░░░░░░░░░░░░░░░░░░▓     ",
    "      ▓▓░░░░░░░░░░░░░░░░░░░░░▓▓      ",
    "        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        ",
]

HAIR_LINES = [
    "    ≋≋≋≋╔══════════════════════╗≋≋≋≋    ",
    "  ≋≋≋≋≋║                      ║≋≋≋≋≋  ",
    " ≋≋≋≋≋═╝                      ╚═≋≋≋≋≋ ",
    "≋≋≋≋≋▓                          ▓≋≋≋≋≋",
    "≋≋≋≋▓▓                          ▓▓≋≋≋≋",
]

STATUS_MESSAGES = {
    STATE_IDLE:      "● STANDBY",
    STATE_SPEAKING:  "◉ SPEAKING",
    STATE_THINKING:  "◎ PROCESSING",
    STATE_LISTENING: "◈ LISTENING",
    STATE_SHOWING:   "◆ DISPLAYING",
}

class MatrixRain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.columns = []
        for _ in range(width):
            self.columns.append({
                'pos': random.randint(-height, 0),
                'speed': random.uniform(0.3, 1.0),
                'chars': [random.choice(MATRIX_CHARS) for _ in range(height)],
            })

    def update(self):
        for col in self.columns:
            col['pos'] += col['speed']
            if col['pos'] > self.height + 5:
                col['pos'] = random.randint(-self.height, -5)
                col['speed'] = random.uniform(0.3, 1.0)
                col['chars'] = [random.choice(MATRIX_CHARS) for _ in range(self.height)]
            if random.random() < 0.05:
                idx = random.randint(0, self.height - 1)
                col['chars'][idx] = random.choice(MATRIX_CHARS)

    def get_char(self, x, y):
        if x >= len(self.columns):
            return ' ', False, False
        col = self.columns[x]
        pos = int(col['pos'])
        if y == pos:
            return col['chars'][y % len(col['chars'])], True, True
        elif 0 <= y < pos and pos - y < 20:
            fade = pos - y
            if fade < 3:
                return col['chars'][y % len(col['chars'])], True, False
            elif fade < 10:
                return col['chars'][y % len(col['chars'])], False, False
        return ' ', False, False


def draw_screen(stdscr, state, matrix, tick):
    global current_input, last_user, last_voris
    try:
        height, width = stdscr.getmaxyx()
        stdscr.erase()

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, curses.COLOR_GREEN, -1)

        # Reserve bottom 4 rows for UI
        face_height_limit = height - 5

        # Matrix rain only in face area
        matrix.update()
        for y in range(face_height_limit):
            for x in range(width - 1):
                char, visible, head = matrix.get_char(x, y)
                if visible:
                    try:
                        if head:
                            stdscr.addch(y, x, char, curses.color_pair(1) | curses.A_BOLD)
                        else:
                            stdscr.addch(y, x, char, curses.color_pair(2))
                    except:
                        pass

        # Select face
        if state == STATE_SPEAKING:
            face = FACE_SPEAKING if (tick // 3) % 2 == 0 else FACE_IDLE
        elif state == STATE_THINKING:
            face = FACE_THINKING
        elif state == STATE_LISTENING:
            face = FACE_LISTENING
        else:
            face = FACE_IDLE

        # Blink
        blink = (tick % 80 > 77)
        if blink:
            face = list(face)
            if len(face) > 7:
                face[7] = face[7].replace("██", "--")

        face_width = max(len(l) for l in face)
        total_face_h = len(HAIR_LINES) + len(face)
        start_x = max(0, (width - face_width) // 2)
        start_y = max(1, (face_height_limit - total_face_h) // 2)
        float_offset = int(math.sin(tick * 0.05) * 1)
        start_y += float_offset

        # Hair
        for i, line in enumerate(HAIR_LINES):
            y = start_y + i
            if 0 <= y < face_height_limit:
                x = max(0, (width - len(line)) // 2)
                try:
                    stdscr.addstr(y, x, line, curses.color_pair(1) | curses.A_BOLD)
                except:
                    pass

        # Face
        for i, line in enumerate(face):
            y = start_y + len(HAIR_LINES) + i
            if 0 <= y < face_height_limit:
                x = max(0, (width - len(line)) // 2)
                try:
                    stdscr.addstr(y, x, line, curses.color_pair(3) | curses.A_BOLD)
                except:
                    pass

        # VORIS name
        name_y = start_y + len(HAIR_LINES) + len(face) + 1
        name = "V O R I S"
        if 0 <= name_y < face_height_limit:
            nx = max(0, (width - len(name)) // 2)
            try:
                stdscr.addstr(name_y, nx, name, curses.color_pair(4) | curses.A_BOLD)
            except:
                pass

        # Bottom UI area
        divider_y = height - 5
        status_y = height - 4
        user_y = height - 3
        voris_y = height - 2
        input_y = height - 1

        # Divider
        try:
            stdscr.addstr(divider_y, 0, "─" * (width - 1), curses.color_pair(1))
        except:
            pass

        # Status
        status = STATUS_MESSAGES.get(state, "● STANDBY")
        try:
            stdscr.addstr(status_y, 2, status, curses.color_pair(5) | curses.A_BOLD)
        except:
            pass

        # Last user message
        if last_user:
            user_line = f"You: {last_user}"[:width - 3]
            try:
                stdscr.addstr(user_y, 2, user_line, curses.color_pair(3))
            except:
                pass

        # Last VORIS response
        if last_voris:
            voris_line = f"VORIS: {last_voris}"[:width - 3]
            try:
                stdscr.addstr(voris_y, 2, voris_line, curses.color_pair(4))
            except:
                pass

        # Input line
        prompt = "> "
        input_display = f"{prompt}{current_input}"[:width - 2]
        try:
            stdscr.addstr(input_y, 0, input_display, curses.color_pair(1) | curses.A_BOLD)
        except:
            pass

        stdscr.refresh()
    except curses.error:
        pass


def run_face(stdscr):
    global running, current_state, current_input, last_user, last_voris
    curses.curs_set(0)
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()
    matrix = MatrixRain(width, height)
    tick = 0

    while running:
        h, w = stdscr.getmaxyx()
        if h != height or w != width:
            height, width = h, w
            matrix = MatrixRain(width, height)

        draw_screen(stdscr, current_state, matrix, tick)
        tick += 1
        time.sleep(0.05)

        key = stdscr.getch()
        if key == curses.KEY_BACKSPACE or key == 127:
            current_input = current_input[:-1]
        elif key == ord('\n') or key == curses.KEY_ENTER or key == 10:
            if current_input.strip():
                last_user = current_input.strip()
                submitted_input = current_input.strip()
                current_input = ""
                # Signal that input is ready
                _input_ready.set()
                _pending_input[0] = submitted_input
        elif key == 27:
            running = False
            break
        elif 32 <= key <= 126:
            current_input += chr(key)

    curses.endwin()


_input_ready = threading.Event()
_pending_input = [None]


def get_input_from_face():
    global last_user
    _input_ready.clear()
    _input_ready.wait()
    return _pending_input[0]


def set_state(state, text=""):
    global current_state, last_voris
    current_state = state
    if text:
        last_voris = text


def start_face():
    global running
    running = True
    t = threading.Thread(target=lambda: curses.wrapper(run_face), daemon=True)
    t.start()


def stop_face():
    global running
    running = False