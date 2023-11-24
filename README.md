# timetp

## Introduction
In a Python User Group (@PyFarsi in telegram), a problem was asked:
> How can I get a string like `4d5w16h78m65s` and parse it to get information out of it?

Then I started to explain that you can write a little tokenizer
with this DFA (Deterministic Finite Automata) and then parse it easily

This is the DFA:
![dfa](https://github.com/mahdihaghverdi/timetp/blob/main/docs/images/dfa.jpg)

Well I implemented it myself :-)

It was quite easy but this is how it works
```python
time = '4d5w'
print(parse(tokenize(time)))        # 39 days, 0:00:00
print(repr(parse(tokenize(time))))  # datetime.timedelta(days=39)
```

In the terminal as a module:
```commandline
python -m timetp "4d5w"
# 39 days, 0:00:00

python -m timetp "4d5w" -v
# datetime.timedelta(days=39)
```

## Implementation
### `tokenize` - The tokenizer
```python
from typing import TypeAlias

token: TypeAlias = tuple[str, int]


def tokenize(string: str) -> list[token]:
    """Tokenize and return a two tuple of the time string

    >>> tokenize('4d5w')
    [('days', 4) ,('weeks', 5)]
    """
    letters = {
        'd': 'days',
        'w': 'weeks',
        'h': 'hours',
        'm': 'minutes',
        's': 'seconds'
    }

    string = string.lower()
    tokens: list[token] = []
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
            f"  -> '{string[i - 1]}' needs a letter after it."
        ) from None

    if letter not in list('dwhms'):
        raise SyntaxError("Time convention letters should be one of d, w, h, m or s.")

    tokens.append((letters[letter], int(digits)))
    string = string[i + 1:]
    return tokens + tokenize(string)
```

Let's break down the function to see each state of the DFA
#### State 0
```python
if string[0].isalpha():
    raise SyntaxError(
        f"A pair cannot start with a letter.\n"
        f"  -> {string[0]!r} needs a number behind it."
    )
```

This `if` statement acts the two ways of the 0 state, it check if the string passed to it starts with a letter or not.

This point is in the programming environment we have raised `SyntaxError` but in DFA we had to write a loop to say this is an error state

Let's see how it works
```python
print(tokenize('d4'))

# SyntaxError: A pair cannot start with a letter.
#  -> 'd' needs a number behind it.
```

```python
print(tokenize('4dw13'))

# SyntaxError: A pair cannot start with a letter.
#  -> 'w' needs a number behind it.
```

You can clearly see that it raises `SyntaxError` when it encounters an invalid pair.
