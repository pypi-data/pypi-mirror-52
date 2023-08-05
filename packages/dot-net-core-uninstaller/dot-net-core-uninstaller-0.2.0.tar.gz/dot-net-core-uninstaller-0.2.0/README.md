# Uninstall .Net Core SDK and Runtime

> Note: This can only be used in POSIX type operating systems.

Uninstall previous .Net Core SDK's and its runtime files.

> Note: You might need super user account to use this library. 

## Instillation

```
pip install dot-net-core-uninstaller
```

## Usage

There are to ways to use this:

### Using Command Line Interface (recommended)

```
Usage: dotnetcore [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show version and exit.
  --help     Show this message and exit.

Commands:
  list    List all the version of .Net Core installed.
  remove  Remove the version of .Net Core.

```

To remove a version of .Net Core SDK or Runtimes:

```
> dotnetcore remove --sdk 1.0.0
> dotnetcore remove --runtime 1.0.0
```

To list all installed .Net Core libraries

```
> dotnetcore list
```

### Using as a Module

```python
from dot_net_core_uninstaller import Uninstaller

remove_dotnet = Uninstaller()
remove_dotnet.delete_runtime("1.0.0")
remove_dotnet.delete_sdk("1.0.0")
```
