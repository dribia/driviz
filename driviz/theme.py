"""**Custom visualization themes**.

Here we define a custom theme for
`Altair <https://altair-viz.github.io/index.html>`_ and
`Matplotlib <https://matplotlib.org/stable/index.html>`_.
We export a :data:`~.theme` object that should be used across the code
to activate and deactivate the custom theme:

.. doctest::

    >>> from driviz import theme

    >>> theme.enable()

This theme uses Google's
`Roboto <https://fonts.google.com/specimen/Roboto>`_ font,
**it should be installed in your OS**.
You can install it in Ubuntu with:

.. code-block:: console

    $ sudo apt install fonts-roboto

The following example generates the interactive plot
``data/results/altair_example_barh.html``:

.. doctest::

    >>> import altair as alt
    >>> import numpy as np
    >>> import pandas as pd
    >>> import random

    >>> from driviz import theme

    >>> theme.enable()

    >>> variety =  [f"V{i}" for i in range(10)]
    >>> site = [f"site{i:02d}" for i in range(14)]
    >>> k = 10000
    >>> df = pd.DataFrame(
    ...     data={
    ...         "yield": np.random.rand(k,),
    ...         "variety": random.choices(variety, k=k),
    ...         "site": random.choices(site, k=k),
    ...     }
    ... )

    >>> selection = alt.selection_point(fields=["site"], bind="legend")

    >>> bars = (
    ...     alt.Chart(df)
    ...     .mark_bar()
    ...     .encode(
    ...         x=alt.X("sum(yield):Q", stack="zero"),
    ...         y=alt.Y("variety:N"),
    ...         color=alt.Color("site"),
    ...         opacity=alt.condition(
    ...             selection, alt.value(1), alt.value(0.2)
    ...         )
    ...     )
    ...     .properties(title="Example chart")
    ...     .add_params(selection)
    ... )

    >>> text = (
    ...     alt.Chart(df)
    ...     .mark_text(dx=-15, dy=3, color="white")
    ...     .encode(
    ...         x=alt.X("sum(yield):Q", stack="zero"),
    ...         y=alt.Y("variety:N"),
    ...         detail="site:N",
    ...         text=alt.Text("sum(yield):Q", format=".1f")
    ...     )
    ... )

    >>> chart = bars + text
    >>> chart.save(
    ...     "altair_example_barh.html"
    ... )

For more examples, visit the
`Example Gallery <https://altair-viz.github.io/gallery/index.html>`_.

"""

from copy import deepcopy
from typing import Any, Literal, no_type_check

import altair as alt
import matplotlib as mpl
from cycler import cycler
from pydantic import BaseModel, ConfigDict
from pydantic_extra_types.color import Color

WHICH_PACKAGE = Literal["all", "alt", "mpl"]


class _Base(BaseModel):
    """Base class."""

    model_config = ConfigDict(
        validate_default=True,
    )


class CategoryPalettes(_Base):
    """Discrete color palettes for categories."""

    palette: list[Color] = [
        Color("#00004E"),
        Color("#0043AF"),
        Color("#3D97F2"),
        Color("#73BAFF"),
        Color("#A8C2AA"),
        Color("#CBC771"),
        Color("#FFCD1B"),
        Color("#FF9424"),
        Color("#FF6D2A"),
        Color("#FF3333"),
        Color("#A0213E"),
        Color("#601445"),
    ]


class CustomColors(_Base):
    """Custom theme colors."""

    dark_blue: Color = Color("#00004E")
    blue: Color = Color("#0043AF")
    light_blue: Color = Color("#73BAFF")
    grey: Color = Color("#DFE6EA")
    red: Color = Color("#FF3333")
    yellow: Color = Color("#FFCD1B")
    black: Color = Color("#000000")
    white: Color = Color("#fff")


class VegaActions(_Base):
    """Vega actions options."""

    export: bool = True
    """Export as PNG and SVG."""
    source: bool = False
    """View the Vega source code."""
    compiled: bool = False
    """View the Vega compiled code."""
    editor: bool = False
    """Open in Vega Editor."""


class Theme(_Base):
    """Custom Altair visualization theme.

    This class defines a custom Altair theme and provides methods
    to :meth:`~.enable` and :meth:`~.disable` it.

    """

    _default_theme: str = "default"
    _default_renderer: str = "default"
    _default_mpl_params: mpl.RcParams = deepcopy(mpl.rcParams)
    """Altair's default theme name."""
    theme_name: str = "dribia"
    """Name under which the theme is registered."""
    color: CustomColors = CustomColors()
    """Custom colors."""
    category_palettes: CategoryPalettes = CategoryPalettes()
    """Category palettes."""
    font: str = "Roboto"
    """Custom font."""
    font_weight: str = "normal"
    """Custom font weight."""
    legend_font_weight: str = "normal"
    """Custom font weight legend."""
    font_size_base: int = 18
    """Custom font size."""
    font_size_xl: float = font_size_base * 1.5
    """Custom font large size."""
    font_size_sm: float = font_size_base * 0.9
    """Custom font small size."""
    font_color: Color = color.dark_blue
    """Custom font color."""
    height: int = 400
    """Custom window height."""
    width: int = 711
    """Custom window width."""
    dpi: int = 50
    """Custom DPI."""
    actions: VegaActions = VegaActions()
    """Actions displayed in the actions menu."""
    locale: str = "en-GB"
    """
    Locale options for the theme (ISO 639-1 two-letter codes). It works for Altair only.
    Available options in: https://github.com/d3/d3-format/tree/main/locale
    """

    def _get_alt_theme(self) -> dict[str, Any]:
        """Build and get the theme's configuration dictionary.

        Returns: Theme's configurations.

        """
        _hex_categories_palette = [c.as_hex() for c in self.category_palettes.palette]
        return {
            "config": {
                "background": "white",
                "view": {
                    "continuousHeight": self.height,
                    "continuousWidth": self.width,
                },
                "title": {
                    "fontSize": self.font_size_xl,
                    "anchor": "start",
                    "color": self.font_color.as_hex(),
                    "font": self.font,
                    "fontWeight": self.font_weight,
                    "offset": 15,
                    "subtitleFont": self.font,
                    "subtitleFontWeight": self.font_weight,
                    "subtitleFontSize": self.font_size_sm,
                    "subtitleFontStyle": self.legend_font_weight,
                },
                "axis": {
                    "titleFont": self.font,
                    "titleColor": self.font_color.as_hex(),
                    "titleFontSize": self.font_size_sm,
                    "titleFontWeight": self.font_weight,
                    "labelFont": self.font,
                    "labelColor": self.font_color.as_hex(),
                    "labelFontSize": self.font_size_base,
                    "labelFontWeight": self.legend_font_weight,
                    "grid": True,
                    "gridColor": self.color.grey.as_hex(),
                    "gridOpacity": 1,
                    "domain": False,
                    "tickColor": self.font_color.as_hex(),
                },
                "legend": {
                    "titleFont": self.font,
                    "titleColor": self.font_color.as_hex(),
                    "titleFontSize": self.font_size_base,
                    "titleFontWeight": self.font_weight,
                    "labelFont": self.font,
                    "labelColor": self.font_color.as_hex(),
                    "labelFontSize": self.font_size_sm,
                    "labelFontWeight": self.legend_font_weight,
                },
                "header": {
                    "titleFont": self.font,
                    "titleColor": self.font_color.as_hex(),
                    "titleFontSize": self.font_size_base,
                    "titleFontWeight": self.font_weight,
                    "labelFont": self.font,
                    "labelColor": self.font_color.as_hex(),
                    "labelFontSize": self.font_size_base,
                    "labelFontWeight": self.font_weight,
                },
                "line": {"stroke": self.color.blue.as_hex()},
                "circle": {"fill": self.color.blue.as_hex(), "stroke": None},
                "point": {
                    "stroke": self.color.blue.as_hex(),
                    "fill": self.color.light_blue.as_hex(),
                },
                "rect": {"fill": self.color.blue.as_hex()},
                "range": {
                    "category": _hex_categories_palette,
                    "ramp": _hex_categories_palette,
                    "diverging": [
                        self.color.blue.as_hex(),
                        self.color.white.as_hex(),
                        self.color.red.as_hex(),
                    ],
                    "heatmap": _hex_categories_palette[0:10],
                },
            }
        }

    @staticmethod
    def _get_cmap(_hex_categories_palette: list[str]) -> str:
        """Build and get the theme's color map."""
        if "dribia" not in mpl.colormaps:
            mpl.colormaps.register(
                cmap=mpl.colors.LinearSegmentedColormap.from_list(
                    name="dribia", colors=_hex_categories_palette[0:10]
                ),
                name="dribia",
            )
        return "dribia"

    def _get_mpl_theme(self) -> dict[str, Any]:
        """Build and get the Matplotlib theme's configuration dict.

        Returns: Matplotlib theme's configurations.

        """
        _hex_categories_palette = [c.as_hex() for c in self.category_palettes.palette]
        return {
            "axes.prop_cycle": cycler("color", _hex_categories_palette),
            "axes.edgecolor": self.color.grey.as_hex(),
            "axes.grid": True,
            "axes.labelcolor": self.font_color.as_hex(),
            "axes.labelsize": self.font_size_xl,
            "axes.labelweight": "bold",
            "axes.titlecolor": self.font_color.as_hex(),
            "axes.titlelocation": "left",
            "axes.titlepad": 15.0,
            "axes.titlesize": self.font_size_xl,
            "axes.titleweight": "normal",
            "figure.dpi": self.dpi,
            "figure.figsize": [self.width / self.dpi, self.height / self.dpi],
            "figure.titlesize": self.font_size_xl,
            "font.family": self.font,
            "font.size": self.font_size_base,
            "font.weight": "normal",
            "grid.color": self.color.grey.as_hex(),
            "image.cmap": self._get_cmap(_hex_categories_palette),
            "legend.fontsize": self.font_size_base,
            "legend.labelcolor": self.font_color.as_hex(),
            "legend.loc": "upper right",
            "legend.title_fontsize": self.font_size_base,
            "lines.color": self.color.blue.as_hex(),
            "patch.facecolor": self.color.blue.as_hex(),
            "text.color": self.font_color.as_hex(),
            "xtick.color": self.font_color.as_hex(),
            "ytick.color": self.font_color.as_hex(),
            "xtick.labelsize": self.font_size_base,
            "ytick.labelsize": self.font_size_base,
        }

    @no_type_check
    def enable(self, which: WHICH_PACKAGE = "all") -> None:
        """Enable the custom theme.

        1. If the theme is not yet registered in Altair, we register it.
        2. We enable the theme.
        3. We set the actions we want to show in the actions menu.
        4. We set the configurations for Matplotlib.

        Args:
            which: Graphics environment to enable the theme on.

        """
        if which in ["all", "alt"]:

            @alt.theme.register(self.theme_name, enable=True)
            def dribia_theme():
                return alt.theme.ThemeConfig(
                    **self._get_alt_theme()
                )  # pragma: no cover

            alt.renderers.set_embed_options(
                actions=self.actions.model_dump(),
                time_format_locale=self.locale,
                format_locale=self.locale,
            )

        if which in ["all", "mpl"]:
            mpl.rcParams.update(self._get_mpl_theme())

    @no_type_check
    def disable(self, which: WHICH_PACKAGE = "all") -> None:
        """Disable the custom theme.

        Disabling the theme is just enabling back the default one.

        Args:
            which: Graphics environment to disable the theme on.

        """
        if which in ["all", "alt"]:
            alt.theme.enable(self._default_theme)
            alt.renderers.enable(self._default_renderer)
        if which in ["all", "mpl"]:
            mpl.rcParams.update(self._default_mpl_params)

    @no_type_check
    def set_basic_colors(self, six: bool = False, first_grey: bool = False) -> None:
        """Set the theme's configuration with four basic colors.

        Args:
            six: whether to set the palette to six colors, otherwise, it
              will be set up with four colors.
            first_grey: whether to set the first color to grey.

        .. doctest::

            >>> import altair as alt
            >>> from driviz import theme

            >>> theme.set_basic_colors()

        """
        if six:
            colors = [
                Color("#00004E"),
                Color("#3D97F2"),
                Color("#A8C2AA"),
                Color("#FFCD1B"),
                Color("#FF6D2A"),
                Color("#A0213E"),
            ]
            name = "basic_colors_six"
        else:
            colors = [
                Color("#00004E"),
                Color("#73BAFF"),
                Color("#FFCD1B"),
                Color("#FF3333"),
            ]
            name = "basic_colors"
        if first_grey:
            colors = [Color("#BABFC2"), *colors]
            name += "_grey"

        new_theme = self._get_alt_theme()
        new_theme["config"]["range"]["category"] = [c.as_hex() for c in colors]

        @alt.theme.register(name, enable=True)
        def dribia_basic_colors_theme():
            return alt.theme.ThemeConfig(**new_theme)  # pragma: no cover

        alt.renderers.set_embed_options(
            actions=self.actions.model_dump(),
            time_format_locale=self.locale,
            format_locale=self.locale,
        )

        mpl_theme = self._get_mpl_theme()
        mpl_theme["axes.prop_cycle"] = cycler("color", [c.as_hex() for c in colors])
        mpl.rcParams.update(mpl_theme)


theme = Theme()
"""This is the object that should be used to enable and disable the
theme across the code.

.. doctest::

    >>> from driviz import theme

    >>> theme.enable()

:meta hide-value:
"""

__all__ = ["Theme", "theme"]
