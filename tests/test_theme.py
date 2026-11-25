"""Viz theme test module."""

from typing import Any

import altair as alt
import matplotlib as mpl

from driviz import theme

_default_mpl_params = mpl.rcParams.copy()
_default_alt_theme = alt.theme.active


def _compare_mpl_params(p1: dict[str, Any], p2: dict[str, Any]) -> bool:
    """Utility to compare matplotlib params excluding the backend."""
    _p1 = dict(p1)
    _p2 = dict(p2)
    _p1.pop("backend")
    _p2.pop("backend")
    return _p1 == _p2


def test_theme():
    """Test the enable method from Theme object."""
    assert isinstance(theme._get_mpl_theme(), dict)
    assert isinstance(theme._get_alt_theme(), dict)
    assert _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    assert alt.theme.active == _default_alt_theme
    theme.enable("alt")
    assert _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    assert alt.theme.active == theme.theme_name
    theme.enable("mpl")
    assert alt.theme.active == theme.theme_name
    assert not _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    theme.disable("alt")
    assert alt.theme.active == _default_alt_theme
    assert not _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    theme.disable("mpl")
    assert _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    assert alt.theme.active == _default_alt_theme
    theme.enable("all")
    assert alt.theme.active == theme.theme_name
    assert not _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    theme.disable("all")
    assert _compare_mpl_params(mpl.rcParams.copy(), _default_mpl_params)
    assert alt.theme.active == _default_alt_theme
    theme.set_basic_colors()
    assert alt.theme.active == "basic_colors"
    theme.set_basic_colors(six=True)
    assert alt.theme.active == "basic_colors_six"
    theme.set_basic_colors(first_grey=True)
    assert alt.theme.active == "basic_colors_grey"
    theme.set_basic_colors(six=True, first_grey=True)
    assert alt.theme.active == "basic_colors_six_grey"
    theme.enable(only_blue_in_gradients=True)
    assert theme._get_cmap() == "dribia_blue"
    theme.disable()
    theme.enable()
    assert theme._get_cmap() == "dribia"


def test_theme_colorblind():
    """Test the colorblind option of the enable method."""

    def _range(key: str) -> list[str]:
        return theme._get_alt_theme()["config"]["range"][key]

    theme.disable()
    theme.enable()
    _default_category = _range("category")
    assert theme._get_cmap() == "dribia"

    # The default palette is derived from the Dribia colors, keeping the
    # blues, and is safe for deuteranopia and protanopia.
    assert _range("category") == [c.as_hex() for c in theme.category_palettes.palette]

    # The Okabe-Ito palette maximizes colorblind separability.
    theme.enable(color_blind=True)
    assert alt.theme.active == theme.theme_name
    assert _range("category") != _default_category
    assert _range("category") == [c.as_hex() for c in theme.category_palettes.okabe]
    assert theme._get_cmap() == "okabe_ito"

    # The diverging scale is kept untouched in colorblind mode.
    assert _range("diverging") == [
        theme.color.blue.as_hex(),
        theme.color.white.as_hex(),
        theme.color.red.as_hex(),
    ]

    # Gradients keep the Dribia blues in colorblind mode.
    theme.enable(color_blind=True, only_blue_in_gradients=True)
    _blues = [c.as_hex() for c in theme.category_palettes.palette][0:4]
    assert _range("ramp") == _blues
    assert _range("heatmap") == _blues
    assert theme._get_cmap() == "dribia_blue"

    # Basic colors are taken from the active palette.
    theme.enable(color_blind=False)
    assert theme._get_basic_colors() == [
        theme.category_palettes.palette[i].as_hex() for i in (0, 3, 6, 9)
    ]
    assert theme._get_basic_colors(six=True) == [
        theme.category_palettes.palette[i].as_hex() for i in (0, 2, 4, 6, 8, 10)
    ]
    theme.set_basic_colors()
    assert alt.theme.active == "basic_colors"
    theme.set_basic_colors(six=True)
    assert alt.theme.active == "basic_colors_six"

    # The Okabe-Ito basic colors are the first ones of the palette.
    theme.enable(color_blind=True)
    assert theme._get_basic_colors() == [
        c.as_hex() for c in theme.category_palettes.okabe[:4]
    ]
    assert theme._get_basic_colors(six=True) == [
        c.as_hex() for c in theme.category_palettes.okabe[:6]
    ]

    # Disabling and enabling again restores the default palette.
    theme.disable()
    theme.enable()
    assert _range("category") == _default_category
    assert theme._get_cmap() == "dribia"
