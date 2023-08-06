# Uninstall .Net Core SDK and Runtime

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

To list all installed .Net Core libraries

```
> dotnetcore list
```

#### Using with POSIX systems

To remove a version of .Net Core SDK or Runtimes:

```
> dotnetcore remove --sdk 1.0.0
> dotnetcore remove --runtime 1.0.0
```

#### Using with Windows systems

> Note: Windows doesn't support removing runtime libraries individually from the uninstaller.

To remove a version of .Net Core SDK or Runtime:

```
> dotnetcore remove --sdk 1.0.0
```

### Using as a Module

```python
from dot_net_core_uninstaller import Uninstaller

remove_dotnet = Uninstaller()
remove_dotnet.delete_runtime("1.0.0")  # Does not work on Windows
remove_dotnet.delete_sdk("1.0.0")  # Does not work on Windows
remove_dotnet.delete_sdk_runtime_windows("1.0.0")  # Does not work on POSIX
```
