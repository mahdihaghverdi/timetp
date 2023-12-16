import sys

from .timetp import parse, tokenize

if __name__ == "__main__":
    time = sys.argv[1]
    verbose = False
    try:
        verbose = True if sys.argv[2] == "-v" else False
    except IndexError:
        pass

    if verbose:
        print(repr(parse(tokenize(time))))
    else:
        print(parse(tokenize(time)))
