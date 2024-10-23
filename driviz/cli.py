"""DriViz Command Line Interface."""

from rich.console import Console
from typer import Option, Typer

from driviz import __version__

app = Typer()

console = Console(tab_size=4)


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main_callback(version: bool = Option(False, help="Show the package version.")):
    """DriViz command line interface."""
    if version:
        console.print(f", version {__version__}")


if __name__ == "__main__":
    app()
