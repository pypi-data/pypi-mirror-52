import re


SPECIAL_CHARS_RE = re.compile("([@()])")


def escape_special_chars(match_string):
    if match_string:
        if SPECIAL_CHARS_RE.search(match_string):
            match_string = SPECIAL_CHARS_RE.sub(r"\\\\\1", match_string)
    return match_string
