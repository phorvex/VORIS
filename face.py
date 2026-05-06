import curses
import time
import random
import threading
import math

# VORIS state
STATE_IDLE = "idle"
STATE_SPEAKING = "speaking"
STATE_THINKING = "thinking"
STATE_LISTENING = "listening"
STATE_SHOWING = "showing"

current_state = STATE_IDLE
current_text = ""
show_content = ""
running = True

# Matrix rain characters
MATRIX_CHARS = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# VORIS face frames - built to scale but base design
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
                'brightness': random.choice(['bright', 'dim', 'dim']),
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

def draw_face(stdscr, state, matrix, tick, status_text=""):
    try:
        height, width = stdscr.getmaxyx()
        stdscr.erase()

        # Colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)      # matrix bright
        curses.init_pair(2, curses.COLOR_GREEN, -1)      # matrix dim
        curses.init_pair(3, curses.COLOR_WHITE, -1)      # face
        curses.init_pair(4, curses.COLOR_CYAN, -1)       # accent
        curses.init_pair(5, curses.COLOR_GREEN, -1)      # status
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)  # highlight

        # Draw matrix rain background
        matrix.update()
        for y in range(height):
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

        # Select face based on state
        if state == STATE_SPEAKING:
            face = FACE_SPEAKING if (tick // 3) % 2 == 0 else FACE_IDLE
        elif state == STATE_THINKING:
            face = FACE_THINKING
        elif state == STATE_LISTENING:
            face = FACE_LISTENING
        else:
            face = FACE_IDLE

        # Eye blink
        blink = (tick % 80 > 77)
        if blink:
            face = list(face)
            if len(face) > 7:
                face[7] = face[7].replace("██", "--")

        # Center face
        face_width = max(len(l) for l in face)
        face_height = len(HAIR_LINES) + len(face)
        start_x = max(0, (width - face_width) // 2)
        start_y = max(1, (height - face_height) // 2 - 2)

        # Subtle float animation
        float_offset = int(math.sin(tick * 0.05) * 1)
        start_y += float_offset

        # Draw hair
        for i, line in enumerate(HAIR_LINES):
            y = start_y + i
            if 0 <= y < height - 1:
                x = max(0, (width - len(line)) // 2)
                try:
                    stdscr.addstr(y, x, line, curses.color_pair(1) | curses.A_BOLD)
                except:
                    pass

        # Draw face
        for i, line in enumerate(face if not blink else face):
            y = start_y + len(HAIR_LINES) + i
            if 0 <= y < height - 1:
                x = max(0, (width - len(line)) // 2)
                try:
                    stdscr.addstr(y, x, line, curses.color_pair(3) | curses.A_BOLD)
                except:
                    pass

        # VORIS name
        name_y = start_y + len(HAIR_LINES) + len(face) + 1
        name = "V O R I S"
        if 0 <= name_y < height - 1:
            nx = max(0, (width - len(name)) // 2)
            try:
                stdscr.addstr(name_y, nx, name, curses.color_pair(4) | curses.A_BOLD)
            except:
                pass

        # Status bar at bottom
        status = STATUS_MESSAGES.get(state, "● STANDBY")
        bar_y = height - 2
        if bar_y > 0:
            bar = f" {status} "
            if status_text:
                bar += f"│ {status_text[:width - len(bar) - 10]} "
            bx = max(0, (width - len(bar)) // 2)
            try:
                stdscr.addstr(bar_y, bx, bar, curses.color_pair(5) | curses.A_BOLD)
            except:
                pass

        # Scan line effect
        scan_y = tick % height
        if 0 <= scan_y < height - 1:
            try:
                for x in range(width - 1):
                    ch = stdscr.inch(scan_y, x)
                    stdscr.addch(scan_y, x, ch & 0xFF, curses.color_pair(1))
            except:
                pass

        stdscr.refresh()
    except curses.error:
        pass

def run_face(stdscr):
    global running, current_state, current_text
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

        draw_face(stdscr, current_state, matrix, tick, current_text)
        tick += 1
        time.sleep(0.05)

        key = stdscr.getch()
        if key == ord('q'):
            running = False
            break

def set_state(state, text=""):
    global current_state, current_text
    current_state = state
    current_text = text

def start_face():
    global running
    running = True
    t = threading.Thread(target=lambda: curses.wrapper(run_face), daemon=True)
    t.start()

def stop_face():
    global running
    running = False