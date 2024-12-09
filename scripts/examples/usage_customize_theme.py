import altair as alt
from pydantic_extra_types.color import Color
from vega_datasets import data  # type: ignore[import-untyped]

from driviz.theme import Theme

theme = Theme(font="Arial", font_color=Color("green"))
theme.set_basic_colors()

source = data.iowa_electricity()
chart = (
    alt.Chart(source)
    .mark_area()
    .encode(
        x="year:T",
        y=alt.Y("net_generation:Q").stack("normalize"),
        color="source:N",
    )
)
