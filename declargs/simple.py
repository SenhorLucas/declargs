import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
subparsers = parser.add_subparsers(dest='command')
foo_parser = subparsers.add_parser('foo')
foo_parser.add_argument('--bar', help='bar help')

foo_parser.set_defaults(bar='default bar')

args = parser.parse_args()
print(args)
