import click

from . import __version__, Uninstaller, is_windows


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'v{__version__}')
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help="Show version and exit.")
def cli():
    pass


@cli.command(help="Remove .Net Core SDK and runtime")
@click.option('--no-input', is_flag=True, help='Deletes the files without asking the user')
@click.option('--sdk', help='Removes SDK')
@click.option('--runtime', help='Removes Runtime. Not supported in Windows')
def remove(no_input, sdk, runtime):

    if sdk is None and runtime is None:
        click.echo("No SDK or runtime version provided.")
        raise click.Abort()

    if not no_input:
        click.confirm('Do you want to continue?', abort=True)

    if is_windows():
        if sdk:
            Uninstaller().delete_sdk_runtime_windows(sdk)

        if runtime:
            raise click.exceptions.BadOptionUsage('runtime', 'Removing runtime is not supported in Windows.')
    else:
        if sdk:
            Uninstaller().delete_sdk(sdk)

        if runtime:
            Uninstaller().delete_runtime(runtime)


@cli.command('list', help="List all the version of .Net Core SDK and runtime installed")
def list_dotnet():
    Uninstaller().list_dotnet()
