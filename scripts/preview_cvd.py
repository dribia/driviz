"""Render colorblind simulations of the theme palettes and a demo chart.

Development utility to preview how charts styled with the Dribia theme look
to people with red-green color vision deficiency (deuteranopia and
protanopia), using the Machado et al. (2009) severity-1.0 model. It is not
part of the test suite.

For each theme mode (default, and `color_blind=True` for the Okabe-Ito
palette) it writes the palette swatches under normal, deutan
and protan simulated vision, plus the demo chart rendered with the theme and
simulated the same way. It also writes a Markdown report
(`colorblind_preview.md`, next to the output directory) embedding the
generated images.

Usage:

    uv run python scripts/preview_cvd.py [--output-dir cvd_preview]

"""

import argparse
import os
from pathlib import Path

import altair as alt
import matplotlib.image as mpl_image
import matplotlib.pyplot as plt
import numpy as np

from driviz import theme

# Machado, Oliveira & Fernandes (2009) severity-1.0 matrices, applied on
# linear RGB.
_MACHADO = {
    "deutan": np.array(
        [
            [0.367322, 0.860646, -0.227968],
            [0.280085, 0.672501, 0.047281],
            [-0.011820, 0.042940, 0.968881],
        ]
    ),
    "protan": np.array(
        [
            [0.152286, 1.052583, -0.204868],
            [0.114503, 0.786281, 0.099216],
            [-0.003882, -0.048116, 1.051998],
        ]
    ),
}

_VISIONS = ("normal", "deutan", "protan")


def _srgb_to_linear(c: np.ndarray) -> np.ndarray:
    """Convert sRGB values in [0, 1] to linear RGB."""
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c: np.ndarray) -> np.ndarray:
    """Convert linear RGB values to sRGB in [0, 1]."""
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


def _simulate_rgb(rgb: np.ndarray, vision: str) -> np.ndarray:
    """Simulate a vision deficiency on an RGB array in [0, 1].

    Args:
        rgb: Array of RGB colors, with the color axis last.
        vision: One of "normal", "deutan" or "protan".

    Returns: Array with the same shape as `rgb`.

    """
    if vision == "normal":
        return rgb
    rgb = np.asarray(rgb)
    sim = _srgb_to_linear(rgb[..., :3]) @ _MACHADO[vision].T
    return np.concatenate([_linear_to_srgb(sim), rgb[..., 3:]], axis=-1)


def _hex_to_rgb(hexes: list[str]) -> np.ndarray:
    """Convert a list of hex color strings to an (N, 3) RGB array in [0, 1]."""

    def parse(hex_color: str) -> list[float]:
        digits = hex_color.lstrip("#")
        if len(digits) == 3:
            digits = "".join(2 * digit for digit in digits)
        return [int(digits[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    return np.array([parse(hex_color) for hex_color in hexes])


def _palettes() -> list[tuple[str, list[str]]]:
    """Get the palettes to preview, from the theme definition."""
    return [
        ("Dribia (CVD-safe)", [c.as_hex() for c in theme.category_palettes.palette]),
        ("Okabe-Ito", [c.as_hex() for c in theme.category_palettes.okabe]),
    ]


def _save_swatch_grid(output_dir: Path) -> Path:
    """Save the palette swatches under each simulated vision.

    Args:
        output_dir: Directory where the PNG is written.

    Returns: Path to the written PNG.

    """
    palettes = _palettes()
    fig, axes = plt.subplots(len(palettes), len(_VISIONS), figsize=(15, 6.5))
    for row, (name, hexes) in enumerate(palettes):
        rgb = _hex_to_rgb(hexes)
        for col, vision in enumerate(_VISIONS):
            ax = axes[row, col]
            colors = _simulate_rgb(rgb, vision)
            for k, color in enumerate(colors):
                ax.add_patch(plt.Rectangle((k, 0), 0.92, 1, color=color))
                ax.text(
                    k + 0.46,
                    -0.16,
                    hexes[k].upper(),
                    ha="center",
                    va="top",
                    fontsize=6.3,
                    rotation=90,
                )
            ax.set_xlim(-0.05, len(hexes))
            ax.set_ylim(-0.75, 1.05)
            ax.axis("off")
            if col == 0:
                ax.text(
                    -0.15,
                    0.5,
                    name,
                    ha="right",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                )
            if row == 0:
                ax.text(
                    len(hexes) / 2 - 0.4,
                    1.12,
                    f"{vision} vision",
                    ha="center",
                    fontsize=10,
                )
    fig.suptitle("Dribia palettes under simulated color vision deficiencies")
    fig.tight_layout()
    path = output_dir / "palettes.png"
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return path


def _demo_chart() -> alt.Chart:
    """Build the demo chart used for the simulated renders."""
    values = [
        {"category": f"C{i + 1:02d}", "value": value}
        for i, value in enumerate([8, 6, 10, 3, 7, 8, 5, 6, 9, 4, 7, 5])
    ]
    return (
        alt.Chart(alt.Data(values=values))
        .mark_bar()
        .encode(
            x=alt.X("category:N", sort=None, title="Category"),
            y=alt.Y("value:Q", title="Value"),
            color=alt.Color("category:N", title="Category"),
        )
        .properties(title="Demo chart", height=300)
    )


def _save_demo_charts(output_dir: Path) -> list[Path]:
    """Render the demo chart in each theme mode and simulate each vision.

    Args:
        output_dir: Directory where the PNGs are written.

    Returns: Paths to the written PNGs.

    """
    chart = _demo_chart()
    modes: tuple[bool, ...] = (False, True)
    paths = []
    for color_blind in modes:
        theme.enable(color_blind=color_blind)
        mode = "okabe" if color_blind else "normal"
        rendered = output_dir / f"chart_{mode}_render.png"
        chart.save(str(rendered))
        image = mpl_image.imread(rendered)
        for vision in _VISIONS:
            path = output_dir / f"chart_{mode}_{vision}.png"
            mpl_image.imsave(path, _simulate_rgb(image, vision))
            paths.append(path)
    theme.enable()
    return paths


def _write_report(output_dir: Path) -> Path:
    """Write a Markdown report showcasing the generated previews.

    The report is written next to the output directory (with the default
    `--output-dir`, the repository root) and embeds the generated PNGs with
    relative links.

    Args:
        output_dir: Directory containing the generated PNGs.

    Returns: Path to the written Markdown report.

    """
    path = output_dir.parent / "colorblind_preview.md"
    modes = (
        ("normal", "Default (CVD-safe Dribia)"),
        ("okabe", "Okabe-Ito"),
    )
    vision_labels = {
        "normal": "Normal vision",
        "deutan": "Deuteranopia (simulated)",
        "protan": "Protanopia (simulated)",
    }

    def _link(name: str, width: int | None = None) -> str:
        relative = os.path.relpath(output_dir / name, output_dir.parent)
        src = Path(relative).as_posix()
        if width is None:
            return f"![]({src})"
        return f'<img src="{src}" width="{width}">'

    table_header = f"| Mode | {' | '.join(vision_labels[v] for v in _VISIONS)} |"
    table_rows = "\n".join(
        "| {label} | {cells} |".format(
            label=label,
            cells=" | ".join(
                _link(f"chart_{mode}_{vision}.png", width=240) for vision in _VISIONS
            ),
        )
        for mode, label in modes
    )
    content = (
        "# Colorblind palette preview\n"
        "\n"
        "How the Dribia theme palettes look under simulated color vision\n"
        "deficiencies (deuteranopia and protanopia, Machado et al. 2009,\n"
        "severity 1.0). Generated by `scripts/preview_cvd.py`; this file is a\n"
        "local artifact, not meant to be committed.\n"
        "\n"
        "Regenerate with:\n"
        "\n"
        "```console\n"
        "uv run python scripts/preview_cvd.py\n"
        "```\n"
        "\n"
        "## Palette swatches\n"
        "\n"
        "Rows: the default Dribia palette (colorblind-safe) and the\n"
        "Okabe-Ito palette (`color_blind=True`).\n"
        "Columns: vision type.\n"
        "\n"
        f"{_link('palettes.png')}\n"
        "\n"
        "## Demo chart under each mode and vision\n"
        "\n"
        f"{table_header}\n"
        "| --- | --- | --- | --- |\n"
        f"{table_rows}\n"
        "\n"
        "Images are displayed at a fixed width so that every viewer renders\n"
        "the columns identically.\n"
        "\n"
        "The default palette keeps the original Dribia blues and re-tunes\n"
        "the remaining colors for red-green color vision deficiency;\n"
        "`color_blind=True` selects the Okabe-Ito palette for maximum\n"
        "separability.\n"
    )
    path.write_text(content)
    return path


def main() -> None:
    """Generate the preview images and the Markdown report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("cvd_preview"),
        help="Directory where the preview PNGs are written.",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = [_save_swatch_grid(args.output_dir), *_save_demo_charts(args.output_dir)]
    report = _write_report(args.output_dir)
    print(report)
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
