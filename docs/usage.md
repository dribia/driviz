The most basic example for usage is:
```python
from driviz import theme

theme.enable()
```

### Examples
```python
import altair as alt
import numpy as np
import pandas as pd
import random

from driviz import theme

theme.enable()

variety =  [f"V{i}" for i in range(10)]
site = [f"site{i:02d}" for i in range(14)]
k = 10000
df = pd.DataFrame(
    data={
        "yield": np.random.rand(k,),
        "variety": random.choices(variety, k=k),
        "site": random.choices(site, k=k),
    }
)

selection = alt.selection_point(fields=["site"], bind="legend")

bars = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("sum(yield):Q", stack="zero"),
        y=alt.Y("variety:N"),
        color=alt.Color("site"),
        opacity=alt.condition(
            selection, alt.value(1), alt.value(0.2)
        )
    )
    .properties(title="Example chart")
    .add_params(selection)
)

text = (
    alt.Chart(df)
    .mark_text(dx=-15, dy=3, color="white")
    .encode(
        x=alt.X("sum(yield):Q", stack="zero"),
        y=alt.Y("variety:N"),
        detail="site:N",
        text=alt.Text("sum(yield):Q", format=".1f")
    )
)

chart = bars + text
chart.save(
    "altair_example_barh.html"
)
```
