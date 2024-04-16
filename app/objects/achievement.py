from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.objects.score import Score

__all__ = ("Achievement",)


class Achievement:
    """A class to represent a single osu! achievement."""

    def __init__(
        self,
        id: int,
        file: str,
        name: str,
        desc: str,
        cond: Callable[[Score, int], bool],  # (score, mode) -> unlocked
    ) -> None:
        self.id = id
        self.file = file
        self.name = name
        self.desc = desc

        self.cond = cond

    def __repr__(self) -> str:
        return f"{self.file}+{self.name}+{self.desc}"
