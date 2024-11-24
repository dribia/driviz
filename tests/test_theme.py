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
