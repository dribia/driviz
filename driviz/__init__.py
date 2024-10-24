"""DriViz."""

from importlib.metadata import PackageNotFoundError, version

from .theme import theme

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__", "theme"]
