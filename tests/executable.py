#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import time


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--foo', default='empty')
    parser.add_argument('--bar', default='empty')
    parser.add_argument('--delay', default=0)
    args = parser.parse_args()

    print(args.foo, file=sys.stdout)
    print(args.bar, file=sys.stderr)

    time.sleep(args.delay)
