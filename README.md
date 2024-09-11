# Declarative argparse for Python

The `argparse` module, is, in fact, declarative, but "declaring" the arguments
are done in Python. All that declaration needs to be repeated when the developer
wants to provide alternative ways of providing the value of an argument, e.g.
through a configuration file or environment variables.

Wouldn't it be great if we had a single source of truth?

```yaml
arg-defs:
- name: --option
    action: store
    default: null
    type: str
    required: false
    help: "Path to the configuration file"
- name: positional
    type: str
    help: "Positional argument"
    default: null
```

And from that, we derive all the necessary information?

In our Python code we just need to read this file to build an
`ArgumentParser`:

```python
import declargs

def main():
    args = declargs.parse()
```

And the user can call your program like this:

```sh
$ my-program --option value positional-value
```

like this:

```sh
$ MY_PROGRAM_OPTION=value my-program
```

or even like this

`config.yaml`
```
option: value
```

```
$ my-program
```

## Configuration files

### Static configuration files
#not-implemented

If the user always uses `--option value`, you can allow them to create static
configuration files:

```yaml
static-config:
- ~/.config/my-program/config.yaml
- /etc/my-program/config.yaml

args-defs:
- name: --option
...
```

With that in place, the user **may** create the files
`~/.config/my-program/config.yaml`, and/or `/etc/my-program/config.yaml`
containing:

```yaml
option: value
```

If both configuration files are defined, the last one defined takes precedence.

### Local-scope configuration files
#not-implemented

You can also allow your user to define custom behaviour depending on their
current location in the file system by adding the following to the schema:

```yaml
static-config:
- ~/.config/my-program/config.yaml
- /etc/my-program/config.yaml

local-config: .my-program

args-defs:
- name: --option
...
```

So the user can create a file called `.my-program` anywhere they wish in their
file system, and any values it defines, take precedence over the static
configuration.

And the local-scope configuration cascade like this:

```
/
    home/
        user/
            .my-program
            program/
                .my-program
                sub-folder/
                    .my-program
```

So if the user is inside `/home/user/prgram/sub-folder`, declargs will find 3
local-scope configuration files:

1. `/home/user/.my-program`
2. `/home/user/program/.my-program`
3. `/home/user/program/sub-folder/.my-program`

They are read in this order, and the last one overrides the previous ones.

## Environment variable overrides
#not-implemented

The last way you can allow your users to configure the application is via
environment variables. Environment variables take precedence over any
configuration file, but can be overriden by providing a cli argument directly.

```yaml
static-config:
- ~/.config/my-program/config.yaml
- /etc/my-program/config.yaml

local-config: .my-program

environment-prefix: MY_PROGRAM

args-defs:
- name: --option
...
```

Environment variables take the following form:

```
<environment-prefix>(_<subparser>)*_<option>
```

There is an open question on how to encode lists and other data structures in
an environment variable so that it fully integrates with argparse.

Going further, we could provide a mini-syntax for environment variable naming.


## Hooks

## Type coertion

Environment variables and cli arguments are always strings, so coercing those
to the appropriate type can prevent problems in the future. Pydantic-style
validation would be a plus. Maybe this library should be able to interface with
Pydantic nicely so people can use their data structures as `BaseModel`s. Feels
like this is a bit of an overengineering, but essential to the _coolness factor_
of the project.
