def tokenizer(string):
    """Tokenize and return a namedtuple of the time string to numbers-letters"""
    string = string.lower()
    tokens = []
    if not string:
        return tokens

    if string[0].isalpha():
        raise SyntaxError(
            f"A pair cannot start with a letter.\n"
            f"  -> {string[0]!r} needs a number behind it."
        )

    digits = ''
    i = 0
    try:
        while string[i].isdigit():
            digits += string[i]
            i += 1
        letter = string[i]
    except IndexError:
        raise SyntaxError(
            f"A pair of  a number and a letter is needed.\n"
            f"  -> '{string[i-1]}' needs a letter after it."
        ) from None

    if letter not in list('dwhms'):
        raise SyntaxError("Time convention letters should be one of d, w, h, m or s.")

    tokens.append((int(digits), letter))
    string = string[i+1:]
    return tokens + tokenizer(string)
