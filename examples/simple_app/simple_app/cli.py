import importlib.resources
import declargs

import yaml


def main():
    with importlib.resources.open_text('simple_app', 'schema.yaml') as f:
        schema = yaml.safe_load(f)

    config = declargs.load_config(**schema['config'])
    parser = declargs.Declargs(schema['argument_parser'], config=config)

    args = parser.parse_args()

    print(args.positional)
    print(args.some_kwarg)


if __name__ == '__main__':
    main()
