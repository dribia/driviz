import altair as alt
from vega_datasets import data

from driviz import theme

theme.set_basic_colors()

source = data.iowa_electricity()
chart = (
    alt.Chart(source)
    .mark_area()
    .encode(
        x="year:T",
        y=alt.Y("net_generation:Q").stack("normalize"),  # noqa: PD013
        color="source:N",
    )
)
