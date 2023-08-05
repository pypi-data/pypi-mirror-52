#!/usr/bin/env python3

"""Run set operations on files."""

import argparse
import sys
from typing import Callable

import onset

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("steps", nargs="+", help="Syntax: file (oper file)+")


def from_oper(oper: str) -> Callable[[set, set], None]:
    """Convert a string to a set operator."""
    func = None
    oper = oper.lower()

    if oper in {"u", "union"}:
        func = onset.union
    elif oper in {"d", "diff", "difference"}:
        func = onset.difference
    elif oper in {"j", "disj", "disjunction"}:
        func = onset.disjunction
    elif oper in {"i", "inter", "intersection"}:
        func = onset.intersection

    if func is None:
        raise ValueError("Unknown set operation: {}".format(oper))

    return func


def from_file(path: str) -> set:
    """Return a set of lines from a file path."""
    with open(path, "r") as r:
        return set(r.read().splitlines())


def main(args=None):
    """Execute the main script."""
    opts = parser.parse_args(args)
    steps = opts.steps

    if (len(steps) % 2) != 1:
        sys.exit("Error: the number of steps should be odd. Got: {}".format(len(steps)))

    state = from_file(steps.pop(0))

    for soper, sfile in zip(steps, steps[1:]):
        oper = from_oper(soper)
        file = from_file(sfile)

        oper(state, file)

    sys.stdout.write("\n".join(state))


if __name__ == "__main__":
    main()
