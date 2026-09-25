"""Backcover generator for KCDA."""

from typing import Dict, Any

def render_backcover(cfg: Dict[str, Any]) -> str:
    slug = cfg.get("slug", "")
    cover_belakang = cfg.get("cover_belakang", f"assets/covers/belakang/{slug.title()}.jpg")

    if not cover_belakang.startswith("/"):
        cover_belakang = "/" + cover_belakang

    return f"""// ==========================================
// KOVER BELAKANG (BACK COVER) - DESAIN VISUAL RESMI
// ==========================================
#page(
  paper: "a5",
  margin: 0cm,
  header: none,
  footer: none,
)[
  #image("{cover_belakang}", width: 100%, height: 100%)
]
"""
