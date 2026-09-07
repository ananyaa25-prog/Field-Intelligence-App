"""
Automated tests for the Field Plant Profile layer.

The tests verify that structured plant profiles,
field summaries, AI contexts, and error handling
work correctly for the complete botanical dataset.
"""

from field_profile import FieldPlantProfile


def test_all_plant_profiles():
    """Verify that all seven plant profiles exist."""

    engine = FieldPlantProfile()

    plants = [
        "Neem",
        "Tulsi",
        "Aloe Vera",
        "Banyan",
        "Hibiscus",
        "Rose",
        "Sunflower"
    ]

    for plant_name in plants:

        profile = engine.get_profile(
            plant_name
        )

        assert profile is not None
        assert profile["identity"]["common_name"]
        assert profile["identity"]["scientific_name"]
        assert profile["identity"]["family"]


def test_field_summaries():
    """Verify that field summaries contain key information."""

    engine = FieldPlantProfile()

    plants = [
        "Neem",
        "Tulsi",
        "Aloe Vera",
        "Banyan",
        "Hibiscus",
        "Rose",
        "Sunflower"
    ]

    for plant_name in plants:

        summary = engine.get_field_summary(
            plant_name
        )

        assert summary is not None
        assert summary["plant_name"]
        assert summary["scientific_name"]
        assert summary["family"]
        assert summary["habitat"]
        assert summary["conservation_status"]


def test_ai_context_generation():
    """Verify AI-ready context generation."""

    engine = FieldPlantProfile()

    plants = [
        "Neem",
        "Tulsi",
        "Aloe Vera",
        "Banyan",
        "Hibiscus",
        "Rose",
        "Sunflower"
    ]

    for plant_name in plants:

        context = engine.get_ai_context(
            plant_name
        )

        assert context is not None
        assert "PLANT PROFILE" in context
        assert "Common Name:" in context
        assert "Scientific Name:" in context
        assert "Ecological Importance:" in context
        assert "Conservation Status:" in context


def test_unknown_plant_handling():
    """Verify safe handling of unknown plants."""

    engine = FieldPlantProfile()

    assert (
        engine.get_profile("UnknownPlant")
        is None
    )

    assert (
        engine.get_field_summary("UnknownPlant")
        is None
    )

    assert (
        engine.get_ai_context("UnknownPlant")
        is None
    )


def test_case_insensitive_lookup():
    """Verify that plant lookup remains normalized."""

    engine = FieldPlantProfile()

    profile = engine.get_profile(
        "neem"
    )

    assert profile is not None

    assert (
        profile["identity"]["common_name"]
        == "Neem"
    )


def test_profile_consistency():
    """
    Verify that the structured profile preserves
    the same verified information used by the AI.
    """

    engine = FieldPlantProfile()

    profile = engine.get_profile(
        "Neem"
    )

    context = engine.get_ai_context(
        "Neem"
    )

    assert profile is not None
    assert context is not None

    assert (
        profile["identity"]["common_name"]
        in context
    )

    assert (
        profile["identity"]["scientific_name"]
        in context
    )

    assert (
        profile["identity"]["family"]
        in context
    )


def run_tests():
    """Run the complete Field Profile test suite."""

    tests = [
        (
            "All plant profiles",
            test_all_plant_profiles
        ),
        (
            "Field summaries",
            test_field_summaries
        ),
        (
            "AI context generation",
            test_ai_context_generation
        ),
        (
            "Unknown plant handling",
            test_unknown_plant_handling
        ),
        (
            "Case-insensitive lookup",
            test_case_insensitive_lookup
        ),
        (
            "Profile consistency",
            test_profile_consistency
        )
    ]

    print("========================================")
    print("     FIELD PROFILE AUTOMATED TESTS")
    print("========================================")

    passed = 0

    for index, (name, test) in enumerate(
        tests,
        start=1
    ):

        print()
        print(
            f"[TEST {index}] {name}"
        )

        try:

            test()

            print(
                f"PASS - {name}"
            )

            passed += 1

        except AssertionError:

            print(
                f"FAIL - {name}"
            )

        except Exception as error:

            print(
                f"FAIL - {name}"
            )

            print(
                f"Error: {error}"
            )

    print()
    print("========================================")
    print("             TEST SUMMARY")
    print("========================================")

    print(
        f"Passed: {passed}/{len(tests)}"
    )

    print(
        f"Failed: {len(tests) - passed}/{len(tests)}"
    )

    print()

    if passed == len(tests):

        print(
            "ALL FIELD PROFILE TESTS PASSED"
        )

    else:

        print(
            "SOME FIELD PROFILE TESTS FAILED"
        )

    print()
    print("========================================")


if __name__ == "__main__":

    run_tests()