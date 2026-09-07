"""
End-to-End Botanical AI Pipeline Tests.

This module validates the complete Member 3 AI pipeline:

1. Plant retrieval
2. Question classification
3. Evidence retrieval
4. Confidence evaluation
5. Grounded prompt construction
6. Grounded response generation
7. Response formatting

The purpose is to ensure that the individual AI components
work correctly together as one application-ready pipeline.
"""

from botanical_assistant import BotanicalAssistant
from response_formatter import BotanicalResponseFormatter


def print_header(title):
    """Print a consistent test section header."""

    print()
    print("=" * 50)
    print(title)
    print("=" * 50)


def test_end_to_end_ecology():
    """
    Test a complete ecology question.

    Example:
        Why is Neem important for biodiversity?
    """

    print()
    print("[TEST 1] End-to-end ecology pipeline")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "Neem",
        "Why is Neem important for biodiversity?"
    )

    formatted = formatter.format(result)

    assert formatted["status"] == "success"
    assert formatted["plant"] == "Neem"
    assert formatted["question_type"] == "ecology"
    assert formatted["grounded"] is True
    assert formatted["evidence_available"] is True

    assert "Neem" in formatted["answer"]

    print("PASS - Ecology pipeline")


def test_end_to_end_conservation():
    """
    Test a complete conservation question.
    """

    print()
    print("[TEST 2] End-to-end conservation pipeline")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "Banyan",
        "What are the threats to Banyan?"
    )

    formatted = formatter.format(result)

    assert formatted["status"] == "success"
    assert formatted["plant"] == "Banyan"
    assert formatted["question_type"] == "conservation"
    assert formatted["grounded"] is True
    assert formatted["evidence_available"] is True

    print("PASS - Conservation pipeline")


def test_botanical_question():
    """
    Test botanical information retrieval.
    """

    print()
    print("[TEST 3] Botanical information pipeline")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "Tulsi",
        "What is the scientific name and family of Tulsi?"
    )

    formatted = formatter.format(result)

    assert formatted["status"] == "success"
    assert formatted["plant"] == "Tulsi"
    assert formatted["question_type"] == "botanical"
    assert formatted["grounded"] is True

    print("PASS - Botanical pipeline")


def test_facts_question():
    """
    Test interesting-facts handling.
    """

    print()
    print("[TEST 4] Interesting facts pipeline")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "Rose",
        "Tell me some interesting facts about Rose."
    )

    formatted = formatter.format(result)

    assert formatted["status"] == "success"
    assert formatted["plant"] == "Rose"
    assert formatted["question_type"] == "facts"
    assert formatted["grounded"] is True

    print("PASS - Facts pipeline")


def test_unknown_plant():
    """
    Test safe handling of an unknown plant.
    """

    print()
    print("[TEST 5] Unknown plant handling")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "XYZPlant",
        "What is this plant?"
    )

    formatted = formatter.format(result)

    assert formatted["status"] == "not_found"
    assert formatted["grounded"] is False
    assert formatted["evidence_available"] is False

    print("PASS - Unknown plant handling")


def test_case_insensitive_pipeline():
    """
    Test that plant recognition remains case-insensitive
    throughout the complete pipeline.
    """

    print()
    print("[TEST 6] Case-insensitive pipeline")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "nEeM",
        "Why is Neem important for biodiversity?"
    )

    formatted = formatter.format(result)

    assert formatted["status"] == "success"
    assert formatted["plant"] == "Neem"
    assert formatted["grounded"] is True

    print("PASS - Case-insensitive pipeline")


def test_display_output():
    """
    Test conversion of structured output into
    application-friendly display text.
    """

    print()
    print("[TEST 7] Application display formatting")

    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    result = assistant.answer(
        "Aloe Vera",
        "What are the characteristics of Aloe Vera?"
    )

    formatted = formatter.format(result)

    display = formatter.format_for_display(
        formatted
    )

    assert "Aloe Vera" in display
    assert "Knowledge grounded: True" in display

    print("PASS - Application display formatting")


def run_all_tests():
    """
    Run the complete end-to-end test suite.
    """

    print_header(
        "BOTANICAL AI END-TO-END PIPELINE TESTS"
    )

    test_end_to_end_ecology()
    test_end_to_end_conservation()
    test_botanical_question()
    test_facts_question()
    test_unknown_plant()
    test_case_insensitive_pipeline()
    test_display_output()

    print()
    print("=" * 50)
    print("              TEST SUMMARY")
    print("=" * 50)

    print()
    print("Pipeline tests: 7/7 PASS")

    print()
    print("Validated components:")
    print("- Plant retrieval")
    print("- Question classification")
    print("- Evidence integration")
    print("- Grounded response generation")
    print("- Response formatting")
    print("- Error handling")
    print("- Application-ready output")

    print()
    print("=" * 50)
    print("     END-TO-END PIPELINE VERIFIED")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()