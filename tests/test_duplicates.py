"""Tests for the duplicates rule."""

import pandas as pd

from src.rules.duplicates import RULE_ID, check


def test_no_duplicates_returns_empty_list():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
    })

    assert check(df) == []


def test_duplicate_entire_rows_returns_finding():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Alice"],
        "age": [25, 30, 25],
    })

    findings = check(df)

    assert len(findings) == 1
    assert findings[0].rule == RULE_ID
    assert "1 duplicate row" in findings[0].message


def test_duplicates_using_subset_of_columns():
    df = pd.DataFrame({
        "name": ["Alice", "Alice", "Bob"],
        "age": [25, 26, 30],
    })

    findings = check(df, subset=["name"])

    assert len(findings) == 1
    assert "1 duplicate row" in findings[0].message


def test_empty_dataframe_returns_no_findings():
    df = pd.DataFrame(columns=["name", "age"])

    assert check(df) == []


def test_multiple_duplicate_rows_are_counted():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Alice", "Bob"],
        "age": [25, 30, 25, 30],
    })

    findings = check(df)

    assert len(findings) == 1
    assert "2 duplicate row" in findings[0].message