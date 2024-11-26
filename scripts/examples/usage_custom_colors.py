import altair as alt
import pandas as pd

from driviz import theme

theme.enable()

source = pd.DataFrame(
    data={"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]},
)
color_mapping = {
    1: "#FD0100",
    2: "#F76915",
    3: "#EEDE04",
    4: "#A0D636",
    5: "#2FA236",
    6: "#333ED4",
}
chart = (
    alt.Chart(source)
    .mark_arc()
    .encode(
        theta="value",
        color=alt.Color(
            "category:N",
            title="Category",
            scale=alt.Scale(
                domain=list(color_mapping),
                range=list(color_mapping.values()),
            ),
        ),
    )
)
