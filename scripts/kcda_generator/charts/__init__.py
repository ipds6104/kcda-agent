"""
KCDA Charts Module Package.
Mengekspor seluruh fungsi dari svg_engine dan extractors.
"""

from .svg_engine import (
    parse_number,
    format_id_number,
    format_figure_header,
    generate_horizontal_bar_chart,
    generate_grouped_horizontal_bar_chart,
)
from .extractors import (
    get_chapter1_charts,
    get_chapter2_charts,
    get_chapter3_charts,
    get_chapter4_charts,
    get_chapter5_charts,
)

__all__ = [
    "parse_number",
    "format_id_number",
    "format_figure_header",
    "generate_horizontal_bar_chart",
    "generate_grouped_horizontal_bar_chart",
    "get_chapter1_charts",
    "get_chapter2_charts",
    "get_chapter3_charts",
    "get_chapter4_charts",
    "get_chapter5_charts",
]
