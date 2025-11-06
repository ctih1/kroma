from .colors.ansi import ansi_supported as _ansi_supported

ansi_supported = _ansi_supported()


def _get_color_if_supported(color: str) -> str:
    if ansi_supported:
        return color
    return ''
