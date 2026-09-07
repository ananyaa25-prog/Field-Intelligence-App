from retrieval import PlantKnowledgeBase


def run_tests():
    knowledge_base = PlantKnowledgeBase()

    print("========================================")
    print("   BOTANICAL RETRIEVAL ENGINE TESTS")
    print("========================================")

    # Test 1: Common name
    print("\n[TEST 1] Common name lookup")
    result = knowledge_base.get_plant("Neem")

    if result:
        print("PASS - Neem found")
    else:
        print("FAIL - Neem not found")

    # Test 2: Case-insensitive lookup
    print("\n[TEST 2] Case-insensitive lookup")
    result = knowledge_base.get_plant("neem")

    if result:
        print("PASS - Lowercase 'neem' found")
    else:
        print("FAIL - Lowercase 'neem' not found")

    # Test 3: Scientific name
    print("\n[TEST 3] Scientific name lookup")
    result = knowledge_base.get_plant("Azadirachta indica")

    if result:
        print("PASS - Scientific name found")
    else:
        print("FAIL - Scientific name not found")

    # Test 4: Another plant
    print("\n[TEST 4] Multiple plant retrieval")
    result = knowledge_base.get_plant("Tulsi")

    if result:
        print(f"PASS - Retrieved {result['common_name']}")
    else:
        print("FAIL - Tulsi not found")

    # Test 5: Unknown plant
    print("\n[TEST 5] Unknown plant handling")
    result = knowledge_base.get_plant("Dragon Tree XYZ")

    if result is None:
        print("PASS - Unknown plant handled safely")
    else:
        print("FAIL - Unknown plant returned a result")

    # Test 6: Empty input
    print("\n[TEST 6] Empty input handling")
    result = knowledge_base.get_plant("")

    if result is None:
        print("PASS - Empty input handled safely")
    else:
        print("FAIL - Empty input returned a result")

    # Test 7: Keyword search
    print("\n[TEST 7] Keyword search")
    results = knowledge_base.search("pollinator")

    if results:
        print(f"PASS - Found {len(results)} plant record(s)")
    else:
        print("FAIL - No results found")

    print("\n========================================")
    print("          TESTING COMPLETE")
    print("========================================")


if __name__ == "__main__":
    run_tests()