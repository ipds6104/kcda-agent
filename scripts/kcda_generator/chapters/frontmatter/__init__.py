"""
Frontmatter Subpackage for KCDA 2026.
Orchestrator modul-modul pendahuluan: cover, katalog, preface, dan toc.
"""

from typing import Dict, Any
from .cover import render_cover_and_title_page
from .katalog import render_katalog_and_contributors
from .preface import render_prefaces
from .toc import render_toc_and_notes

def render_frontmatter(cfg: Dict[str, Any]) -> str:
    """Menggabungkan seluruh komponen frontmatter berstandar resmi BPS Pusat."""
    return "\n".join([
        render_cover_and_title_page(cfg),
        render_katalog_and_contributors(cfg),
        render_prefaces(cfg),
        render_toc_and_notes(cfg)
    ])

__all__ = ["render_frontmatter"]
