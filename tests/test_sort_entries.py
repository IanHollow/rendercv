import pytest

from rendercv.data import (
    ExperienceEntry,
    EducationEntry,
    PublicationEntry,
)
from rendercv.data.models.computers import sort_entries


@pytest.fixture
def sample_entries():
    """Return a heterogeneous list of entries with various date configurations."""
    return [
        # Ongoing role – should be considered the newest
        ExperienceEntry(
            company="Company A",
            position="Engineer",
            start_date="2023-01",
            end_date="present",
        ),
        # Entry with only a single date
        PublicationEntry(
            title="Paper 1",
            authors=["Doe"],
            date="2022-06",
        ),
        # Entry with both start / end in the past
        EducationEntry(
            institution="Uni",
            area="Area",
            start_date="2010-09",
            end_date="2014-06",
        ),
    ]


@pytest.mark.parametrize("order, expected_first_cls", [
    ("reverse", ExperienceEntry),
    ("chronological", EducationEntry),
    ("none", ExperienceEntry),  # original list keeps its order
])
def test_sort_entries_orders(sample_entries, order, expected_first_cls):
    sorted_list = sort_entries(sample_entries, order)
    assert isinstance(sorted_list[0], expected_first_cls)


def test_sort_entries_preserves_original(sample_entries):
    original_copy = list(sample_entries)
    _ = sort_entries(sample_entries, "reverse")
    # ensure original list not mutated
    assert sample_entries == original_copy


@pytest.mark.parametrize("invalid_order", ["ascending", "desc", "", None])
def test_sort_entries_invalid_order(sample_entries, invalid_order):
    with pytest.raises(ValueError):
        sort_entries(sample_entries, invalid_order)  # type: ignore[arg-type]


def test_sort_entries_missing_dates_raises():
    entries = [
        "Just a string",  # TextEntry without any date information
    ]
    with pytest.raises(ValueError):
        sort_entries(entries, "reverse")


# Malformed or non-ISO date strings should raise ValueError when sorting is requested.
def test_sort_entries_malformed_date_raises():
    entries = [
        PublicationEntry(
            title="Paper with funky date",
            authors=["Doe"],
            date="Fall 2023",  # not parseable by RenderCV
        )
    ]

    with pytest.raises(ValueError):
        sort_entries(entries, "reverse")