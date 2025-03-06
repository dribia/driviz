DriViz
==========================

<p align="center">
    <a href="https://dribia.github.io/driviz">
    <picture style="display: block; margin-left: auto; margin-right: auto; width: 40%;">
            <source
                media="(prefers-color-scheme: dark)"
                srcset="./docs/img/logo_dribia_blanc_cropped.png"
            >
            <source
                media="(prefers-color-scheme: light)"
                srcset="./docs/img/logo_dribia_blau_cropped.png"
            >
            <img
                alt="driviz"
                src="./docs/img/logo_dribia_blau_cropped.png"
            >
        </picture>
    </a>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Tests](https://github.com/dribia/driviz/actions/workflows/test.yml/badge.svg)](https://github.com/dribia/driviz/actions/workflows/test.yml) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/driviz)](https://codecov.io/gh/dribia/driviz) [![Tests](https://github.com/dribia/driviz/actions/workflows/lint.yml/badge.svg)](https://github.com/dribia/driviz/actions/workflows/lint.yml) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/driviz)](https://pypi.org/project/driviz/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/driviz?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/driviz?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/dribia/driviz?color=blue)](LICENSE)                                                                                                                                                                                                                                                                                                         |
---
**Documentation**: <a href="https://dribia.github.io/driviz" target="_blank">https://dribia.github.io/driviz</a>

**Source Code**: <a href="https://github.com/dribia/driviz" target="_blank">https://github.com/dribia/driviz</a>

---

## Installation

This project resides in the Python Package Index (PyPI), so it can easily be installed with pip:
```console
pip install driviz
```

## Usage

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

## Contributing
[Poetry](https://python-poetry.org) is the best way to interact with this project, to install it,
follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation).

With `poetry` installed, one can install the project dependencies with:
```console
make setup
```

Then, to run the project unit tests:
```console
make test-unit
```

To run the linters (`ruff` and `mypy`):
```console
make lint
```

To apply all code formatting:
```console
make format
```

## License
`driviz` is distributed under the terms of the
[MIT](https://opensource.org/license/mit) license.
Check the [LICENSE](./LICENSE) file for further details.
