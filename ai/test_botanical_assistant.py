from botanical_assistant import BotanicalAssistant


def run_tests():
    assistant = BotanicalAssistant()

    print("========================================")
    print("   BOTANICAL ASSISTANT TEST SUITE")
    print("========================================")

    tests = [
        {
            "name": "Botanical information",
            "plant": "Neem",
            "question": "What is the scientific name and family of Neem?",
            "expected_type": "botanical"
        },
        {
            "name": "Ecological information",
            "plant": "Banyan",
            "question": "How does Banyan contribute to biodiversity?",
            "expected_type": "ecology"
        },
        {
            "name": "Conservation information",
            "plant": "Hibiscus",
            "question": "What are the threats and conservation actions for Hibiscus?",
            "expected_type": "conservation"
        },
        {
            "name": "Interesting facts",
            "plant": "Sunflower",
            "question": "Tell me some interesting facts about Sunflower.",
            "expected_type": "facts"
        },
        {
            "name": "General information",
            "plant": "Rose",
            "question": "Tell me about Rose.",
            "expected_type": "general"
        },
        {
            "name": "Unknown plant",
            "plant": "Dragon Tree XYZ",
            "question": "What is the ecological importance of this plant?",
            "expected_type": None
        }
    ]

    passed = 0

    for number, test in enumerate(tests, start=1):

        print(f"\n[TEST {number}] {test['name']}")
        print(f"Plant: {test['plant']}")
        print(f"Question: {test['question']}")

        result = assistant.answer(
            test["plant"],
            test["question"]
        )

        if test["expected_type"] is None:

            if result["status"] == "not_found":
                print("PASS - Unknown plant handled correctly")
                passed += 1
            else:
                print("FAIL - Unknown plant was not handled correctly")

        else:

            if (
                result["status"] == "success"
                and result["question_type"] == test["expected_type"]
            ):
                print(
                    f"PASS - Question classified as "
                    f"{result['question_type']}"
                )
                passed += 1
            else:
                print(
                    f"FAIL - Expected {test['expected_type']}, "
                    f"got {result.get('question_type')}"
                )

    print("\n========================================")
    print(f"RESULT: {passed}/{len(tests)} TESTS PASSED")
    print("========================================")


if __name__ == "__main__":
    run_tests()