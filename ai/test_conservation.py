"""
Automated tests for the Conservation Intelligence module.

The test suite verifies:
- Conservation profile retrieval
- Threat retrieval
- Conservation action retrieval
- Biodiversity information
- Summary generation
- AI context generation
- Case-insensitive lookup
- Unknown plant handling
- Consistency with the botanical knowledge base
"""

from conservation import ConservationIntelligence


PLANTS = [
    "Neem",
    "Tulsi",
    "Aloe Vera",
    "Banyan",
    "Hibiscus",
    "Rose",
    "Sunflower"
]


def test_conservation_profiles():
    """Verify conservation profiles for all plants."""

    engine = ConservationIntelligence()

    for plant_name in PLANTS:

        profile = engine.get_conservation_profile(
            plant_name
        )

        assert profile is not None
        assert profile["plant"]
        assert profile["scientific_name"]
        assert profile["conservation_status"]
        assert isinstance(
            profile["threats"],
            list
        )
        assert isinstance(
            profile["conservation_actions"],
            list
        )
        assert profile["biodiversity_role"]


def test_threat_retrieval():
    """Verify that threats can be retrieved."""

    engine = ConservationIntelligence()

    for plant_name in PLANTS:

        threats = engine.get_threats(
            plant_name
        )

        assert threats is not None
        assert isinstance(
            threats,
            list
        )


def test_conservation_actions():
    """Verify conservation actions."""

    engine = ConservationIntelligence()

    for plant_name in PLANTS:

        actions = (
            engine.get_conservation_actions(
                plant_name
            )
        )

        assert actions is not None
        assert isinstance(
            actions,
            list
        )


def test_biodiversity_role():
    """Verify biodiversity information."""

    engine = ConservationIntelligence()

    for plant_name in PLANTS:

        role = engine.get_biodiversity_role(
            plant_name
        )

        assert role is not None
        assert len(role.strip()) > 0


def test_conservation_summaries():
    """Verify concise conservation summaries."""

    engine = ConservationIntelligence()

    for plant_name in PLANTS:

        summary = engine.get_summary(
            plant_name
        )

        assert summary is not None
        assert summary["plant"]
        assert summary["scientific_name"]
        assert summary["status"]
        assert summary["biodiversity_role"]

        assert isinstance(
            summary["threat_count"],
            int
        )

        assert isinstance(
            summary["action_count"],
            int
        )


def test_ai_context_generation():
    """Verify grounded AI conservation context."""

    engine = ConservationIntelligence()

    for plant_name in PLANTS:

        context = engine.build_ai_context(
            plant_name
        )

        assert context is not None

        assert (
            "CONSERVATION CONTEXT"
            in context
        )

        assert (
            "Scientific Name:"
            in context
        )

        assert (
            "Conservation Status:"
            in context
        )

        assert (
            "Biodiversity Role:"
            in context
        )

        assert (
            "Known Threats:"
            in context
        )

        assert (
            "Conservation Actions:"
            in context
        )


def test_case_insensitive_lookup():
    """Verify normalized plant lookup."""

    engine = ConservationIntelligence()

    profile = (
        engine.get_conservation_profile(
            "neem"
        )
    )

    assert profile is not None
    assert profile["plant"] == "Neem"


def test_unknown_plant_handling():
    """Verify safe handling of unknown plants."""

    engine = ConservationIntelligence()

    assert (
        engine.get_conservation_profile(
            "UnknownPlant"
        )
        is None
    )

    assert (
        engine.get_threats(
            "UnknownPlant"
        )
        is None
    )

    assert (
        engine.get_conservation_actions(
            "UnknownPlant"
        )
        is None
    )

    assert (
        engine.get_biodiversity_role(
            "UnknownPlant"
        )
        is None
    )

    assert (
        engine.get_summary(
            "UnknownPlant"
        )
        is None
    )

    assert (
        engine.build_ai_context(
            "UnknownPlant"
        )
        is None
    )


def test_grounded_context_consistency():
    """
    Verify that the AI context contains the same
    verified conservation information returned by
    the structured profile.
    """

    engine = ConservationIntelligence()

    profile = (
        engine.get_conservation_profile(
            "Neem"
        )
    )

    context = engine.build_ai_context(
        "Neem"
    )

    assert profile is not None
    assert context is not None

    assert (
        profile["plant"]
        in context
    )

    assert (
        profile["scientific_name"]
        in context
    )

    assert (
        profile["conservation_status"]
        in context
    )

    assert (
        profile["biodiversity_role"]
        in context
    )

    for threat in profile["threats"]:

        assert threat in context

    for action in profile[
        "conservation_actions"
    ]:

        assert action in context


def run_tests():
    """Run the complete conservation test suite."""

    tests = [
        (
            "Conservation profiles",
            test_conservation_profiles
        ),
        (
            "Threat retrieval",
            test_threat_retrieval
        ),
        (
            "Conservation actions",
            test_conservation_actions
        ),
        (
            "Biodiversity role",
            test_biodiversity_role
        ),
        (
            "Conservation summaries",
            test_conservation_summaries
        ),
        (
            "AI context generation",
            test_ai_context_generation
        ),
        (
            "Case-insensitive lookup",
            test_case_insensitive_lookup
        ),
        (
            "Unknown plant handling",
            test_unknown_plant_handling
        ),
        (
            "Grounded context consistency",
            test_grounded_context_consistency
        )
    ]

    print("========================================")
    print("   CONSERVATION INTELLIGENCE TESTS")
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

    failed = len(tests) - passed

    print()
    print("========================================")
    print("             TEST SUMMARY")
    print("========================================")

    print(
        f"Passed: {passed}/{len(tests)}"
    )

    print(
        f"Failed: {failed}/{len(tests)}"
    )

    print()

    if passed == len(tests):

        print(
            "ALL CONSERVATION TESTS PASSED"
        )

    else:

        print(
            "SOME CONSERVATION TESTS FAILED"
        )

    print()
    print("========================================")


if __name__ == "__main__":

    run_tests()