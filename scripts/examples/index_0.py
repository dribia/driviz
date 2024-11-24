import altair as alt
import pandas as pd

from driviz import theme

theme.enable()

source = pd.DataFrame({"values": [12, 23, 47, 6, 52, 19]})
base = alt.Chart(source).encode(
    alt.Theta("values:Q").stack(True),  # noqa: PD013
    alt.Radius("values").scale(type="sqrt", zero=True, rangeMin=20),
    color="values:N",
)
c1 = base.mark_arc(innerRadius=20, stroke="#fff")
c2 = base.mark_text(radiusOffset=10).encode(text="values:Q")
chart = c1 + c2
