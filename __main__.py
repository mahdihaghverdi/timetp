import sys

from .timetp import parse, tokenize, letters

keys = ', '.join(letters.keys())
values = ', '.join(letters.values())

if __name__ == "__main__":
    usage = f"""timetp. Little tokenizer and parser with finite automata studies
USAGE: python -m timetp "TIME-STRING" [-v]
       python -m timetp help

help:
    TIME-STRING:    a sequence of digitletters like: 4w5d16h99m10s
                    - first digit must not be 0
                    - letters can be chosen from: {keys!r} 
                      which correspond to {values!r}
    help:           show this message and exit
    -v:             enable verbose mode"""

    time_or_help = sys.argv[1]
    if time_or_help == 'help':
        print(usage)
        sys.exit(0)

    time = time_or_help
    verbose = False
    try:
        verbose = True if sys.argv[2] == "-v" else False
    except IndexError:
        pass

    if verbose:
        print(repr(parse(tokenize(time))))
    else:
        print(parse(tokenize(time)))
