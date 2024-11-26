import altair as alt
import pandas as pd

from driviz import theme

theme.set_basic_colors(six=True)

source = pd.DataFrame(
    data={"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]},
)
chart = (
    alt.Chart(source)
    .mark_arc()
    .encode(theta="value", color=alt.Color("category:N", title="Category"))
)
