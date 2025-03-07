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

    output_dir = Path(__file__).parents[1] / "docs" / "plots"
    output_dir.mkdir(exist_ok=True)

    img_format = "png"
    output_path = output_dir / f"{name}.{img_format}"

    chart.save(str(output_path))

    return f"```python\n{code}\n```\n\n![Plot](plots/{name}.{img_format})\n"


if __name__ == "__main__":
    jinja_env = JinjaEnvironment(
        loader=FileSystemLoader(Path(__file__).parents[1] / "docs" / "templates")
    )

    for name in jinja_env.list_templates():
        template = jinja_env.get_template(name)
        render = template.render(
            **{
                f.name.replace(".py", ""): add_plot(f.name.replace(".py", ""))
                for f in (Path(__file__).parents[0] / "examples").glob("*.py")
                if f.name.startswith(name[0 : name.find(".")])
            }
        )
        with Path(Path(__file__).parents[1] / "docs" / name.replace(".jinja", "")).open(
            mode="w"
        ) as f:
            f.write(render)
