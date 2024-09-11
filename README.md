# Declarative argparse for Python

The `argparse` module, is, in fact, declarative, but the declaration of the
arguments is done in Python. All that declaration needs to be repeated when the
developer wants to provide alternative ways of providing the value of an
argument, e.g. through a configuration file or environment variables.

Wouldn't it be great if we had a single source of truth? For example:

```yaml
arg-defs:
- name: positional
  type: str
  help: "Positional argument"
  default: 'Some cool default value'
- name: --option
  action: store
  default: False
  type: str
  required: false
  help: "Path to the configuration file"
```

And from that, we derive all the necessary information?

## Uncluttered source code

In our Python code we just need to read this file to build an `ArgumentParser`.
We're actually building a `Declargs` class, which simple inherits from
`ArgumentParser`:

```python
import declargs
import yaml

def main():
    with open('schema', 'r') as f:
        schema = yaml.safe_load(f)

    parser = declargs.Declargs(schema)

    args = parser.parse_args()
```

It is nice to not have to call `parser.add_argument` over and over, but the real
power of Declargs comes from the ability to override defaults.

## Overriding defaults

Programs usually provide a few ways of overriding defaults:

- Configuration files: these can be static, for example `~/.config/my-app/config`
  or location specific, like a `.my-app` file located in the user's current
  directory.
- Environment variables

Declargs aims to _automatically_ provide the user of your app with the ability
to override defaults using these methods.

### Static configuration files

If the user always uses `--option value`, they could define them in a
configuration file that lives in a known (static) location, e.g.
`~/.config/my-app/config.yaml`

You, as the app developer, can define that location in the schema file:

```yaml
config:
  static_configs:
    - path: /etc/my-app/config.yaml
      required: true
    - path: ./tests/resources/dummy-config.yaml
      required: true

args-defs:
- name: --option
...
```

With that in place, the user **may** create the files
`~/.config/my-program/config.yaml`, and/or `/etc/my-app/config.yaml`
containing the new desired default value for the option:

```yaml
option: value
```

If both configuration files are defined, the last one defined takes precedence.

### Local-scope configuration files

You can also allow your user to define custom behavior depending on their
current location in the file system by adding the following to the schema:

```yaml
config:
  local_config: .my-app.yaml

args-defs:
- name: --option
...
```

So the user can create a file called `.my-app.yaml` anywhere they wish in their
file system, and any values it defines, take precedence over the static
configuration.

And the local-scope configuration cascade like this:

```
/
    home/
        user/
            .my-app.yaml
            program/
                .my-app.yaml
                sub-folder/
                    .my-yaml
```

So if the user is inside `/home/user/program/sub-folder`, Declargs will find 3
local-scope configuration files:

1. `/home/user/.my-program`
2. `/home/user/program/.my-program`
3. `/home/user/program/sub-folder/.my-program`

They are read in this order, and the last one is the only one taken into
consideration

## Environment variable overrides
#not-implemented

Now that we have a single source of truth for the configuration items of our
app, it would be a shame to not be able to override them with environment
variables. This will be implemented soon.

## Type coertion

Environment variables and cli arguments are always strings, so coercing those
to the appropriate type can prevent problems in the future. Pydantic-style
validation would be a plus. Maybe this library should be able to interface with
Pydantic nicely so people can use their data structures as `BaseModel`s. Feels
like this is a bit of an overengineering, but essential to the _coolness factor_
of the project. Might be implemented.
