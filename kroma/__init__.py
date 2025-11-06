from .colors.html import HTMLColor, RGB
from .utils import _get_color_if_supported
from enum import Enum, auto


ANSI = "\033["
RESET = f"{ANSI}0m"


class StyleType(Enum):
    FOREGROUND = auto()
    BACKGROUND = auto()


def convert_html_hex_to_ansi(text: str, color: HTMLColor | str, type: StyleType) -> str:
    if isinstance(color, str):
        # color is a HEX code
        if "#" in color:
            color = color.replace("#", "")
        color = color.lower().strip()
    else:
        # color is a HTMLColor enum, get the corresponding hex code
        color = color.value.lower().strip()

    color_chars = [char for char in color]

    rgb = RGB(
        int(color_chars[0] + color_chars[1], 16),
        int(color_chars[2] + color_chars[3], 16),
        int(color_chars[4] + color_chars[5], 16)
    )

    ansi_color = (
        (ANSI + ("38" if type == StyleType.FOREGROUND else "48") + ";2;[r];[g];[b]m")
        .replace("[r]", str(rgb.r))
        .replace("[g]", str(rgb.g))
        .replace("[b]", str(rgb.b))
    )

    return _get_color_if_supported(ansi_color) + text + _get_color_if_supported(RESET)


def style(text: str, foreground: str | HTMLColor | None = None, background: str | HTMLColor | None = None) -> str:
    if foreground is None and background is None:
        return text
    elif foreground is not None and background is None:
        return convert_html_hex_to_ansi(text, foreground, StyleType.FOREGROUND)
    elif foreground is None and background is not None:
        return convert_html_hex_to_ansi(text, background, StyleType.BACKGROUND)
    elif foreground is not None and background is not None:
        return convert_html_hex_to_ansi(convert_html_hex_to_ansi(text, foreground, StyleType.FOREGROUND), background, StyleType.BACKGROUND)

    return text
