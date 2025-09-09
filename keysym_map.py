from Xlib import XK


def get_keysym_for_char(char: str):
    # Handle special characters and punctuation
    special_map = {
        "\n": XK.XK_Return,
        "\t": XK.XK_Tab,
        " ": XK.XK_space,
        "/": XK.XK_slash,
        "'": XK.XK_apostrophe,
        ".": XK.XK_period,
        ",": XK.XK_comma,
        "—": XK.XK_minus,
        "-": XK.XK_minus,
        ":": XK.XK_colon,
        ";": XK.XK_semicolon,
        "<": XK.XK_less,
        ">": XK.XK_greater,
        "&": XK.XK_ampersand,
        '"': XK.XK_quotedbl,
    }
    if char in special_map:
        return special_map[char]
    # Try to get keysym for normal characters
    keysym = XK.string_to_keysym(char)
    if keysym != 0:
        return keysym

    # return None on error
    return None
