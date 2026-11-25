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

    # Colorblind-safe palette derived from the Dribia colors, keeping the
    # original blues. Safe for deuteranopia and protanopia.
    palette: list[Color] = [
        Color("#00004E"),
        Color("#0043AF"),
        Color("#3D97F2"),
        Color("#73BAFF"),
        Color("#72D3D9"),
        Color("#C0B667"),
        Color("#F8CD29"),
        Color("#F08617"),
        Color("#CC440E"),
        Color("#F15649"),
        Color("#A4204E"),
        Color("#64204D"),
    ]
    # Okabe-Ito colorblind-safe palette, optimized for maximum
    # color-vision-deficiency separability.
    okabe: list[Color] = [
        Color("#000000"),
        Color("#E69F00"),
        Color("#56B4E9"),
        Color("#009E73"),
        Color("#F0E442"),
        Color("#0072B2"),
        Color("#D55E00"),
        Color("#CC79A7"),
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
    _only_blue_in_gradients: bool = False
    """Altair's default theme name."""
    _color_blind: bool = False
    """Whether the Okabe-Ito palette is active."""
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

    def _get_hex_palette(self) -> list[str]:
        """Get the hex codes of the active category palette.

        The active palette depends on the `color_blind` option passed to
        :meth:`~.enable`.

        Returns: List of hex color strings of the active palette.

        """
        if self._color_blind:
            colors = self.category_palettes.okabe
        else:
            colors = self.category_palettes.palette
        return [c.as_hex() for c in colors]

    def _get_alt_theme(self) -> dict[str, Any]:
        """Build and get the theme's configuration dictionary.

        Returns: Theme's configurations.

        """
        _hex_categories_palette = self._get_hex_palette()
        _blues_palette = [c.as_hex() for c in self.category_palettes.palette][0:4]
        _gradient_palette = (
            _blues_palette if self._only_blue_in_gradients else _hex_categories_palette
        )
        _heatmap_palette = (
            _blues_palette
            if self._only_blue_in_gradients
            else _hex_categories_palette[0:10]
        )
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
                    "ramp": _gradient_palette,
                    "diverging": [
                        self.color.blue.as_hex(),
                        self.color.white.as_hex(),
                        self.color.red.as_hex(),
                    ],
                    "heatmap": _heatmap_palette,
                },
            }
        }

    def _get_cmap(self) -> str:
        """Build and get the theme's color map.

        Returns: Name of the registered Matplotlib colormap.

        """
        if self._only_blue_in_gradients:
            cmap_name = "dribia_blue"
            cmap_colors = [c.as_hex() for c in self.category_palettes.palette][0:4]
        else:
            cmap_colors = self._get_hex_palette()[0:10]
            cmap_name = "okabe_ito" if self._color_blind else "dribia"
        if cmap_name not in mpl.colormaps:
            mpl.colormaps.register(
                cmap=mpl.colors.LinearSegmentedColormap.from_list(
                    name=cmap_name, colors=cmap_colors
                ),
                name=cmap_name,
            )
        return cmap_name

    def _get_mpl_theme(self) -> dict[str, Any]:
        """Build and get the Matplotlib theme's configuration dict.

        Returns: Matplotlib theme's configurations.

        """
        _hex_categories_palette = self._get_hex_palette()
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
            "image.cmap": self._get_cmap(),
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
    def enable(
        self,
        which: WHICH_PACKAGE = "all",
        only_blue_in_gradients: bool = False,
        color_blind: bool = False,
    ) -> None:
        """Enable the custom theme.

        1. If the theme is not yet registered in Altair, we register it.
        2. We enable the theme.
        3. We set the actions we want to show in the actions menu.
        4. We set the configurations for Matplotlib.

        Args:
            which: Graphics environment to enable the theme on.
            only_blue_in_gradients: If True, use only the first four
                palette colors (blues, dark to light) for gradient scales
                (ramp, heatmap, and matplotlib colormap).
            color_blind: If True, use the Okabe-Ito palette for categorical
                colors, optimized for maximum color-vision-deficiency
                separability. The default palette is derived from the
                Dribia colors, keeping the original blues, and is already
                safe for red-green color vision deficiency (deuteranopia
                and protanopia).

        """
        self._only_blue_in_gradients = only_blue_in_gradients
        self._color_blind = color_blind
        if which in ["all", "alt"]:
            _alt_theme = self._get_alt_theme()

            @alt.theme.register(self.theme_name, enable=True)
            def dribia_theme():
                return alt.theme.ThemeConfig(**_alt_theme)  # pragma: no cover

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

    def _get_basic_colors(self, six: bool = False) -> list[str]:
        """Get the basic colors for the active palette.

        Args:
            six: whether to get six colors, otherwise, four colors.

        Returns: List of hex color strings of the basic colors.

        """
        _hex_categories_palette = self._get_hex_palette()
        if self._color_blind:
            return _hex_categories_palette[:6] if six else _hex_categories_palette[:4]
        indices = [0, 2, 4, 6, 8, 10] if six else [0, 3, 6, 9]
        return [_hex_categories_palette[i] for i in indices]

    @no_type_check
    def set_basic_colors(self, six: bool = False, first_grey: bool = False) -> None:
        """Set the theme's configuration with four basic colors.

        The colors are taken from the active palette, which depends on the
        `color_blind` option passed to :meth:`~.enable`.

        Args:
            six: whether to set the palette to six colors, otherwise, it
              will be set up with four colors.
            first_grey: whether to set the first color to grey.

        .. doctest::

            >>> import altair as alt
            >>> from driviz import theme

            >>> theme.set_basic_colors()

        """
        colors = self._get_basic_colors(six=six)
        name = "basic_colors_six" if six else "basic_colors"
        if first_grey:
            colors = ["#BABFC2", *colors]
            name += "_grey"

        new_theme = self._get_alt_theme()
        new_theme["config"]["range"]["category"] = colors

        @alt.theme.register(name, enable=True)
        def dribia_basic_colors_theme():
            return alt.theme.ThemeConfig(**new_theme)  # pragma: no cover

        alt.renderers.set_embed_options(
            actions=self.actions.model_dump(),
            time_format_locale=self.locale,
            format_locale=self.locale,
        )

        mpl_theme = self._get_mpl_theme()
        mpl_theme["axes.prop_cycle"] = cycler("color", colors)
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
