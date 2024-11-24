"""Docs generation module."""

from pathlib import Path

from jinja2 import Environment as JinjaEnvironment
from jinja2 import FileSystemLoader

from scripts.examples import chart


def add_plot(name: str) -> str:
    """Add the plot to the code."""
    with (Path(__file__).parents[0] / "examples" / f"{name}.py").open() as file:
        code = file.read()
    return (
        f"```python\n{code}\n```\n\n"
        f"```vegalite\n{chart[name].to_json(indent=2)}\n```\n"
    )


if __name__ == "__main__":
    jinja_env = JinjaEnvironment(
        loader=FileSystemLoader(Path(__file__).parents[1] / "docs" / "templates")
    )

    for name in jinja_env.list_templates():
        template = jinja_env.get_template(name)
        render = template.render(
            **{k: add_plot(k) for k in chart if k.startswith(name[0 : name.find(".")])}
        )
        with Path(Path(__file__).parents[1] / "docs" / name.replace(".jinja", "")).open(
            mode="w"
        ) as f:
            f.write(render)
