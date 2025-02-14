#
# Copyright (c) 2025 by Abertis.
# This file is part of the project driviz,
# developed by Dribia Data Research, Barcelona.
#
import altair as alt
from vega_datasets import data  # type: ignore[import-untyped]

from driviz.theme import Theme, Language

# Enable the theme
theme = Theme(language=Language.ca)
theme.set_basic_colors()

theme.enable()

# Generate synthetic time series data
source = data.stocks().sort_values(by="date").iloc[-100:]
# Create the chart
chart = (
    alt.Chart(source)
    .mark_line()
    .encode(
        x="date:T",
        y="price:Q",
        color="symbol:N",
    )
    .properties(title="Stocks", width=600, height=400)
)
