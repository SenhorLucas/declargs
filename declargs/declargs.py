import argparse
import pathlib
from typing import Any, Callable, Dict, List, Mapping, Optional, Union
import os
import logging
import sys

# TODO: Remove external dependencies, let the user decide the markup language
import yaml

Pathlike = Union[str, os.PathLike]
log = logging.getLogger(__name__)


class Declargs(argparse.ArgumentParser):
    """
    """
    def __init__(
            self,
            schema: Dict[str, Any],
            config: Dict[str, Any] = None,
            **kwargs,
    ):
        self.schema = schema
        arg_defs = self.schema.pop('arg_defs', None)
        subparsers_def = self.schema.pop('subparsers', None)
        parents = self.schema.pop('parents', None)

        super().__init__(**self.schema, **kwargs)

        if subparsers_def is not None:
            parsers = subparsers_def.pop('parsers', {})
            self.subparsers = self.add_subparsers(**subparsers_def)
            for subschema in parsers:
                name = subschema.pop('name')
                help = subschema.pop('help', None)
                config = config.pop(name, None) if config is not None else None
                self.subparsers.add_parser(name, help=help, schema=subschema, config=config)

        # TODO: Implement parent parsers
        # TODO: Implement groups

        self._add_all_arguments(arg_defs)
        if config is not None:
            self.set_defaults(**config)

    def _add_all_arguments(self, arg_defs):
        """
        Call `add_argument` for each definition in `arg_defs`.
        """
        for kwargs in arg_defs:
            self._add_arg_def(kwargs)

    def _add_arg_def(self, arg_def: Dict[str, Any]):
        """
        Add an argument definition to the parser.
        """
        args = arg_def.pop('names')
        self.add_argument(*args, **arg_def)


class ConfigLoader:
    def __init__(
            self,
            local_config = None,
            static_configs = None,
            config_parser: Callable = yaml.safe_load,
            environment_prefix: str = None,
            exit_on_error: bool = False
    ):
        self.local_config_path = self._search_local_config(local_config) or None
        self.static_configs = static_configs or []
        self.config_parser = config_parser
        self.exit_on_error = exit_on_error
        self.environment_prefix = environment_prefix

        self.config = None
        # TODO: Implement environment variables

    def get_config(self):
        if self.config is not None:
            return self.config

        self.config = {}
        for path, required in [
                (self.local_config_path, False),
                *[(cfg['path'], cfg.get('required', False)) for cfg in self.static_configs],
        ]:
            if path is not None:
                try:
                    with open(path, 'r') as file:
                        config_content = self.config_parser(file)
                except Exception as e:
                    if self.exit_on_error and required:
                        raise e
                else:
                    self.config = self.deep_update(config_content, self.config)
        return self.config


    def deep_update(self, source: Dict, destination: Dict):
        """
        Update the destination dictionary with the source dictionary.
        """
        for key, value in source.items():
            if isinstance(value, Mapping):
                destination[key] = self.deep_update(value, destination.get(key, {}))
            else:
                destination[key] = value
        return destination

    def _search_local_config(self, file_name: Optional[Pathlike]) -> Optional[Pathlike]:
        """
        Search for `file_name` in the current directory and its parents.

        Return the first file found, or None if no file is found.
        """
        if file_name is None:
            return None
        current_dir = pathlib.Path.cwd()
        # We probably don't want `/.my_config.yaml` at the root level, like, ever?
        while current_dir != current_dir.parent:
            file_path = current_dir / file_name
            if file_path.exists():
                return file_path
            current_dir = current_dir.parent


def load_config(
    local_config = None,
    static_configs = None,
    config_parser: Callable = yaml.safe_load,
    environment_prefix: str = None,
    exit_on_error: bool = False
):
    loader = ConfigLoader(
        local_config=local_config,
        static_configs=static_configs,
        config_parser=config_parser,
        environment_prefix=environment_prefix,
        exit_on_error=exit_on_error
    )
    return loader.get_config()
