#!/usr/bin/env python3.7
import argparse
import re
from ripgrepy import Ripgrepy


def trim_prefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):]
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')
    parser.add_argument('repository')
    args = parser.parse_args()

    symbol = args.symbol
    repository = args.repository

    if re.fullmatch('[A-Z_]+', symbol):
        search = rf'{symbol}\s=\s'
    elif symbol[0].isupper():
        search = f'class {symbol}'
    else:
        search = f'def {symbol}'

    result = Ripgrepy(search, repository).json().run().as_dict[0]

    absolute_path = result['data']['path']['text']


    relative_path = trim_prefix(absolute_path, repository)

    import_path = trim_prefix(relative_path, '/').replace('.py', '').replace('/', '.')

    print(f'from {import_path} import {symbol}')

if __name__ == '__main__':
    main()
