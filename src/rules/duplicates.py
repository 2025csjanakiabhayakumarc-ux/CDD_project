"""Rule: duplicates

Checks whether the DataFrame contains duplicate rows or duplicate
values within the configured subset of columns.
"""

from __future__ import annotations

import pandas as pd

from src.rules._base import Finding

RULE_ID = "duplicates"


def check(df: pd.DataFrame, subset: list[str] | None = None, **_) -> list[Finding]:
    """Return a Finding if duplicate rows are found, otherwise []."""
    duplicate_mask = df.duplicated(subset=subset or None, keep="first")
    duplicate_count = int(duplicate_mask.sum())

    if duplicate_count == 0:
        return []

    columns = subset or list(df.columns)
    return [
        Finding(
            rule=RULE_ID,
            message=f"Found {duplicate_count} duplicate row(s).",
            hint=f"Remove duplicate entries based on these columns: {', '.join(columns)}",
        )
    ]