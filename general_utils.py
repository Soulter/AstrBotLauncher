import datetime
import os

PLATFORM_GOCQ = 'gocq'
PLATFORM_QQCHAN = 'qqchan'

FG_COLORS = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "purple": "35",
    "cyan": "36",
    "white": "37",
    "default": "39",
}

BG_COLORS = {
    "black": "40",
    "red": "41",
    "green": "42",
    "yellow": "43",
    "blue": "44",
    "purple": "45",
    "cyan": "46",
    "white": "47",
    "default": "49",
}

LEVEL_DEBUG = "DEBUG"
LEVEL_INFO = "INFO"
LEVEL_WARNING = "WARNING"
LEVEL_ERROR = "ERROR"
LEVEL_CRITICAL = "CRITICAL"

level_codes = {
    LEVEL_DEBUG: 0,
    LEVEL_INFO: 1,
    LEVEL_WARNING: 2,
    LEVEL_ERROR: 3,
    LEVEL_CRITICAL: 4
}

level_colors = {
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "purple",
}

def log(
        msg: str,
        level: str = "INFO",
        tag: str = "System",
        fg: str = None,
        bg: str = None,
        max_len: int = 10000):
    """
    日志记录函数
    """
    _set_level_code = level_codes[LEVEL_INFO]
    if 'LOG_LEVEL' in os.environ and os.environ['LOG_LEVEL'] in level_codes:
        _set_level_code = level_codes[os.environ['LOG_LEVEL']]


    if level in level_codes and level_codes[level] < _set_level_code:
        return

    if len(msg) > max_len:
        msg = msg[:max_len] + "..."
    now = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
    pre = f"[{now}] [{level}] [{tag}]: {msg}"
    if level == "INFO":
        if fg is None:
            fg = FG_COLORS["green"]
        if bg is None:
            bg = BG_COLORS["default"]
    elif level == "WARNING":
        if fg is None:
            fg = FG_COLORS["yellow"]
        if bg is None:
            bg = BG_COLORS["default"]
    elif level == "ERROR":
        if fg is None:
            fg = FG_COLORS["red"]
        if bg is None:
            bg = BG_COLORS["default"]
    elif level == "CRITICAL":
        if fg is None:
            fg = FG_COLORS["purple"]
        if bg is None:
            bg = BG_COLORS["default"]
    
    print(f"\033[{fg};{bg}m{pre}\033[0m")
