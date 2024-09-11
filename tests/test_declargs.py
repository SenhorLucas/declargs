from pathlib import Path
import declargs

import pytest
import yaml


@pytest.fixture
def simple_schema():
    with open(Path('tests') / 'resources' / 'dummy-schema.yaml', 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture
def subparser_schema():
    with open(Path('tests') / 'resources' / 'schema-subparsers.yaml') as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize(
    ('argv', 'first_positional_value', 'some_kwarg_value'),
    [
        ([], 'positional from file', True),
        (['test', '--some-kwarg'], 'test', True),
    ],
)
def test_declargs_simple(simple_schema, argv, first_positional_value, some_kwarg_value):
    config = declargs.load_config(**simple_schema['config'])
    parser = declargs.Declargs(simple_schema['argument_parser'], config=config)

    args = parser.parse_args(argv)

    assert args.first_positional == first_positional_value
    assert args.some_kwarg == some_kwarg_value


@pytest.mark.parametrize(
    ('argv', 'first_positional_value', 'kwarg_value'),
    [
        (['sub-command-a', 'cli-pos'], 'cli-pos', True),
        (['sub-command-a', 'cli-pos-b', '-s'], 'cli-pos-b', True),
        (['sub-command-a', '-s'], 'Override default a', True),
    ],
)
def test_declargs_subparser(subparser_schema,  argv, first_positional_value, kwarg_value):
    config = declargs.load_config(**subparser_schema['config'])
    parser = declargs.Declargs(subparser_schema['argument_parser'], config=config)

    args = parser.parse_args(argv)

    assert args.sub_command_positional == first_positional_value
    assert args.sub_command_a_kwarg == kwarg_value



#     data_file = tmp_path / 'config.yaml'
#     data_file.write_text(yaml.dump(config))
#     return data_file


# def test_parse(monkeypatch, schema_file):
#     """Parse function should return an argparse.Namespace object."""
#     args = declargs.parse(config_file)
#     assert isinstance(args, argparse.Namespace)
#     # TODO: Add more assertions...
# 
# 
# def test_read_config(config_file):
# 
#     config = declargs.read_config(config_file)
#     assert isinstance(config, dict)
#     assert 'key1' in config
#     assert 'key2' in config
#     # Add more assertions...
# 
# 
# def test_cascade_override_args(config_file):
#     # Test the cascade_override_args function
#     args = {'key1': 'default1', 'key3': 'default3'}
#     configs = [config_file]
#     overridden_args = declargs.cascade_override_args(args, configs)
#     assert overridden_args['key1'] == 'value1'
#     assert overridden_args['key2'] == 'value2'
#     assert overridden_args['key3'] == 'default3'
#     # Add more assertions...
# 
# 
# def test_override_from_env(monkeypatch):
#     """Args should be overridden by environment variables with the prefix."""
#     args = {'key1': 'default1', 'key2': 'default2'}
#     prefix = 'MYAPP'
# 
#     monkeypatch.setenv('MYAPP_KEY1', 'env_value1')
# 
#     overridden_args = declargs.override_from_env(args, prefix)
#     assert overridden_args['key1'] == 'env_value1'
#     assert overridden_args['key2'] == 'default2'
# 
