import pytest
from project import select_country_by_level, get_flag_description, check_answer


@pytest.fixture
def sample_flags_data():
    # Minimal in-memory data similar to flags.json structure.
    return {
        "easy": [
            {"country": "France", "description": "Blue, white, and red."},
            {"country": "Japan", "description": "White with red circle."}
        ],
        "medium": [
            {"country": "Brazil", "description": "Green with yellow diamond."}
        ],
        "hard": [
            {"country": "Nepal", "description": "Two stacked triangles."}
        ],
    }


# --- Tests for select_country_by_level ---


def test_select_country_by_level(sample_flags_data):
    # Basic test that returned entry is from the correct level.
    entry = select_country_by_level(1, sample_flags_data)
    countries_easy = {f["country"] for f in sample_flags_data["easy"]}
    assert entry["country"] in countries_easy


def test_select_country_by_level_medium(sample_flags_data):
    entry = select_country_by_level(2, sample_flags_data)
    assert entry["country"] == "Brazil"


def test_select_country_by_level_invalid_level_raises(sample_flags_data):
    with pytest.raises(ValueError):
        select_country_by_level(0, sample_flags_data)


# --- Tests for get_flag_description ---


def test_get_flag_description(sample_flags_data):
    desc = get_flag_description("France", sample_flags_data)
    assert desc == "Blue, white, and red."


def test_get_flag_description_case_insensitive(sample_flags_data):
    desc = get_flag_description("japan", sample_flags_data)
    assert desc == "White with red circle."


def test_get_flag_description_not_found(sample_flags_data):
    desc = get_flag_description("Nonexistent Country", sample_flags_data)
    assert desc is None


# --- Tests for check_answer ---


def test_check_answer():
    assert check_answer("France", "France") is True


def test_check_answer_case_insensitive_and_spaces():
    assert check_answer("  frAnCe  ", "France") is True


def test_check_answer_incorrect():
    assert check_answer("Spain", "France") is False
