import altair as alt
from vega_datasets import data  # type: ignore[import-untyped]

from driviz.theme import Theme

theme = Theme(locale="ca-ES")  # Set Catalan language
theme.set_basic_colors()

source = data.stocks().sort_values(by="date").iloc[-100:]
chart = (
    alt.Chart(source)
    .mark_line()
    .encode(
        x=alt.X("date:T", title="Data"),
        y=alt.Y("price:Q", title="Preu"),
        color=alt.Color("symbol:N", title="Símbol"),
    )
    .properties(title="Estocs", width=600, height=300)
)
