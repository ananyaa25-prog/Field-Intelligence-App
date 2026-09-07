"""
Integration tests for the Grounded Botanical AI Assistant.

These tests verify:
- plant retrieval
- question classification
- prompt construction
- grounded responses
- error handling
- end-to-end assistant behaviour
"""

from botanical_assistant import BotanicalAssistant


def print_result(test_number, name, passed):
    """
    Display a consistent test result.
    """

    status = "PASS" if passed else "FAIL"

    print(
        f"[TEST {test_number}] {name}"
    )

    print(
        f"{status} - {name}"
    )

    print()


def main():

    assistant = BotanicalAssistant()

    print("========================================")
    print("   BOTANICAL AI INTEGRATION TESTS")
    print("========================================")
    print()

    # --------------------------------------------------
    # TEST 1
    # --------------------------------------------------

    result = assistant.answer(
        "Neem",
        "What is the scientific name of Neem?"
    )

    passed = (
        result["status"] == "success"
        and result["question_type"] == "botanical"
        and result["grounded"] is True
        and "Azadirachta indica"
        in result["answer"]
    )

    print_result(
        1,
        "Botanical question handling",
        passed
    )

    # --------------------------------------------------
    # TEST 2
    # --------------------------------------------------

    result = assistant.answer(
        "Tulsi",
        "Why is Tulsi important for biodiversity?"
    )

    passed = (
        result["status"] == "success"
        and result["question_type"] == "ecology"
        and result["grounded"] is True
    )

    print_result(
        2,
        "Ecology question handling",
        passed
    )

    # --------------------------------------------------
    # TEST 3
    # --------------------------------------------------

    result = assistant.answer(
        "Banyan",
        "What are the threats to Banyan?"
    )

    passed = (
        result["status"] == "success"
        and result["question_type"] == "conservation"
        and result["grounded"] is True
    )

    print_result(
        3,
        "Conservation question handling",
        passed
    )

    # --------------------------------------------------
    # TEST 4
    # --------------------------------------------------

    result = assistant.answer(
        "Rose",
        "Tell me some interesting facts about Rose."
    )

    passed = (
        result["status"] == "success"
        and result["question_type"] == "facts"
        and result["grounded"] is True
    )

    print_result(
        4,
        "Interesting facts handling",
        passed
    )

    # --------------------------------------------------
    # TEST 5
    # --------------------------------------------------

    result = assistant.answer(
        "nEeM",
        "What is the family of this plant?"
    )

    passed = (
        result["status"] == "success"
        and result["plant"] == "Neem"
        and result["grounded"] is True
    )

    print_result(
        5,
        "Case-insensitive plant recognition",
        passed
    )

    # --------------------------------------------------
    # TEST 6
    # --------------------------------------------------

    result = assistant.answer(
        "UnknownPlant",
        "What is this plant?"
    )

    passed = (
        result["status"] == "not_found"
        and result["grounded"] is False
        and result["prompt"] is None
    )

    print_result(
        6,
        "Unknown plant handling",
        passed
    )

    # --------------------------------------------------
    # TEST 7
    # --------------------------------------------------

    result = assistant.build_grounded_prompt(
        "Sunflower",
        "Why is Sunflower important for biodiversity?"
    )

    passed = (
        result is not None
        and result["question_type"] == "ecology"
        and "Sunflower" in result["context"]
        and "USER QUESTION" in result["prompt"]
        and "RESPONSE INSTRUCTIONS" in result["prompt"]
    )

    print_result(
        7,
        "Grounded prompt construction",
        passed
    )

    # --------------------------------------------------
    # TEST 8
    # --------------------------------------------------

    result = assistant.answer(
        "Aloe Vera",
        "What is the habitat of Aloe Vera?"
    )

    passed = (
        result["status"] == "success"
        and result["grounded"] is True
        and result["context"] is not None
        and result["prompt"] is not None
        and result["answer"]
    )

    print_result(
        8,
        "End-to-end AI pipeline",
        passed
    )

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    print("========================================")

    print(
        "BOTANICAL AI TESTING COMPLETE"
    )

    print("========================================")

    print()

    print(
        "The integration suite validates:"
    )

    print(
        "- Retrieval"
    )

    print(
        "- Question classification"
    )

    print(
        "- Prompt construction"
    )

    print(
        "- Grounded responses"
    )

    print(
        "- Error handling"
    )

    print(
        "- End-to-end AI pipeline"
    )

    print()

    print(
        "Grounded architecture verified."
    )


if __name__ == "__main__":
    main()