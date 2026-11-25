import altair as alt
import pandas as pd

from driviz import theme

theme.enable()

source = pd.DataFrame(
    data={
        "category": [f"C{i + 1:02d}" for i in range(12)],
        "value": [8, 6, 10, 3, 7, 8, 5, 6, 9, 4, 7, 5],
    },
)
chart = (
    alt.Chart(source)
    .mark_bar()
    .encode(
        x=alt.X("category:N", sort=None, title="Category"),
        y=alt.Y("value:Q", title="Value"),
        color=alt.Color("category:N", title="Category"),
    )
    .properties(title="Colorblind-safe Dribia palette", height=300)
)
