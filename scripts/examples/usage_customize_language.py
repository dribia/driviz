import altair as alt
from vega_datasets import data  # type: ignore[import-untyped]

from driviz.theme import Language, Theme

# Enable the theme
theme = Theme(language=Language.ca)
# Choose this over enable because it is more complete and can only do it for Altair
theme.set_basic_colors()

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

chart.save("language_example.html")
