"""Docs generation module."""

import importlib
from pathlib import Path

from jinja2 import Environment as JinjaEnvironment
from jinja2 import FileSystemLoader


def add_plot(name: str) -> str:
    """Add the plot to the code."""
    with (Path(__file__).parents[0] / "examples" / f"{name}.py").open() as file:
        code = file.read()
    chart = importlib.import_module(f"scripts.examples.{name}").chart
    if "png" in name:
        output_dir = Path(__file__).parents[1] / "docs" / "plots"
        output_dir.mkdir(exist_ok=True)
        chart.save(str(output_dir / f"{name}.png"))
        embedded_plot = f"![Plot](plots/{name}.png)\n"
    else:
        embedded_plot = f"```vegalite\n{chart.to_json(indent=2)}\n```\n"
    return f"```python\n{code}\n```\n\n{embedded_plot}"


if __name__ == "__main__":
    jinja_env = JinjaEnvironment(
        loader=FileSystemLoader(Path(__file__).parents[1] / "docs" / "templates")
    )

    for name_ in jinja_env.list_templates():
        template = jinja_env.get_template(name_)
        render = template.render(
            **{
                f.name.replace(".py", ""): add_plot(f.name.replace(".py", ""))
                for f in (Path(__file__).parents[0] / "examples").glob("*.py")
                if f.name.startswith(name_[0 : name_.find(".")])
            }
        )
        with Path(
            Path(__file__).parents[1] / "docs" / name_.replace(".jinja", "")
        ).open(mode="w") as f:
            f.write(render)
