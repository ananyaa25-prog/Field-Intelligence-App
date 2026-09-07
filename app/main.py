import os
import sys

# Make the AI module directory available for the existing
# botanical AI imports.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

AI_DIRECTORY = os.path.join(
    PROJECT_ROOT,
    "ai"
)

if AI_DIRECTORY not in sys.path:
    sys.path.insert(0, AI_DIRECTORY)


from ai.botanical_assistant import BotanicalAssistant
from ai.response_formatter import BotanicalResponseFormatter


def main():
    assistant = BotanicalAssistant()
    formatter = BotanicalResponseFormatter()

    print("=" * 50)
    print("       FIELD INTELLIGENCE APP")
    print("=" * 50)
    print()
    print("Botanical AI Assistant")
    print("Ask about Indian native flora.")
    print("Type 'exit' to quit.")
    print()

    while True:
        plant = input("Enter plant name: ").strip()

        if plant.lower() == "exit":
            print("Thank you for using Field Intelligence App.")
            break

        if not plant:
            print("Please enter a plant name.")
            continue

        question = input("Ask your question: ").strip()

        if question.lower() == "exit":
            print("Thank you for using Field Intelligence App.")
            break

        if not question:
            print("Please enter a question.")
            continue

        result = assistant.answer(
            plant,
            question
        )

        formatted = formatter.format(
            result
        )

        print()
        print("-" * 50)
        print(
            formatter.format_for_display(
                formatted
            )
        )
        print("-" * 50)
        print()


if __name__ == "__main__":
    main()