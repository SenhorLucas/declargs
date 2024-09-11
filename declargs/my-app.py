#!/usr/bin/env python3

from declargs import Declargs

def main():
    parser = Declargs('dummy-schema.yaml')
    args = parser.parse_args()
    print(vars(args))

if __name__ == '__main__':
    main()
