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

This `if` statement decides between the two ways of the state 0, it check if the string passed to it starts with a letter or not.

Here, in the programming environment, we have raised `SyntaxError` but in DFA we had to write a loop to say this is an error state

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


#### State 1 and 2
```python
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
```

This piece of code acts as the state 1 and one side of state 2 of our DFA.

it starts at the first index of the argument (we are sure that it is a digit), then iterates until we ran out of the sequence of digits.

If you look at the DFA, we have two loops. The loop on the state 2 has two meanings, one: it loops to get all the numbers
 and two: it says there is no letter after this numbers -> so you have to raise a `SyntaxError`. 

So this is the reason of the `try except` block and `raise` statement.

Let's see how it works
```python
print(tokenize('444d'))

# [('days', 444)]
```

```python
print(tokenize('444'))

# SyntaxError: A pair of  a number and a letter is needed.
#  -> '444' needs a letter after it.
```

```python
print(tokenize('12d5w4'))

# SyntaxError: A pair of  a number and a letter is needed.
#  -> '4' needs a letter after it.
```

#### Syntax Checking
```python
if letter not in list('dwhms'):
    raise SyntaxError("Time convention letters should be one of d, w, h, m or s.")
```

This if statement ensures that user has used one of `d` , `w`, `h`, `m` or `s` letters and not anything else


#### State 2
```python
tokens.append((letters[letter], int(digits)))
string = string[i + 1:]
return tokens + tokenize(string)
```

Now we have reached the fun part

Here we have our number and letter and we append it to the tokens list.

Then, we shrink the argument to pass it to the `tokenize` function it self. Why?

Because all we had done above are done for just one pair, and all the work should be done for all the pairs in the string and a recursive solution fits best here.

Here's what happens:
```
tokenize('4d5w')
  |- local tokens: [('days', 4)]
  |- shrink the arg: arg -> '5w'
  |- call tokenize('5w')
       |- local tokens: [('weeks', 5)]
  |- the call returns
  |- local tokens: [('days', 4), ('weeks', 5)]
```


### `parse` - The parser
```python
def parse(tokens: list[token]):
    """Return a `timedelta` object out of the tokens"""
    _dict = defaultdict(int)
    for type_, number in tokens:
        _dict[type_] += number

    return timedelta(**_dict)
```

Our parser is a nice and little one. 

All it does is that it sums up the homogeneous keys together and then passes it to `timedelta` and returns it

The reason behind the `for` is this:

Consider an input like this: `4d5d5w12d`, what `tokenize` generates it this:
```
[('days', 4), ('days', 5), ('weeks', 5), ('days', 4)]
```

but the right thing is to sum up all days and then pass the kw arg to `timedelta`, this `for` loop does that.
