import random

import altair as alt
import numpy as np
import pandas as pd

from driviz import theme

alt.data_transformers.disable_max_rows()

theme.enable()

variety = [f"V{i}" for i in range(10)]
site = [f"site{i:02d}" for i in range(14)]
k = 10000
rng = np.random.default_rng()
random_df = pd.DataFrame(
    data={
        "yield": rng.random(k),
        "variety": random.choices(variety, k=k),
        "site": random.choices(site, k=k),
    }
)
selection = alt.selection_point(fields=["site"], bind="legend")
bars = (
    alt.Chart(random_df)
    .mark_bar()
    .encode(
        x=alt.X("sum(yield):Q", stack="zero"),
        y=alt.Y("variety:N", title="Variety"),
        color=alt.Color("site", title="Site"),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    )
    .add_params(selection)
)
text = (
    alt.Chart(random_df)
    .mark_text(dx=-15, dy=3, color="white")
    .encode(
        x=alt.X("sum(yield):Q", stack="zero"),
        y=alt.Y("variety:N"),
        detail="site:N",
        text=alt.Text("sum(yield):Q", format=".1f"),
    )
)
chart = (bars + text).properties(title="Example chart", height=300)
