#!/usr/bin/env python
from argparse import ArgumentParser
import sys


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--foo', default='empty')
    parser.add_argument('--bar', default='empty')
    args = parser.parse_args()

    print(args.foo, file=sys.stdout)
    print(args.bar, file=sys.stderr)
