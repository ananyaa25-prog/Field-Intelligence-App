from retrieval import PlantKnowledgeBase


class BotanicalAssistant:
    """
    Grounded botanical assistant.

    The assistant retrieves verified information from the
    botanical knowledge base and uses that information to
    construct plant-specific responses.
    """

    def __init__(self):

        self.knowledge_base = PlantKnowledgeBase()

    def classify_question(self, question):
        """
        Identify the main intent of the user's question.
        """

        if not question:
            return "general"

        question = question.lower().strip()

        conservation_keywords = [
            "conservation",
            "protect",
            "protection",
            "threat",
            "threats",
            "endangered",
            "save",
            "preserve"
        ]

        ecology_keywords = [
            "ecology",
            "ecological",
            "biodiversity",
            "environment",
            "habitat",
            "ecosystem",
            "wildlife",
            "pollinator"
        ]

        botanical_keywords = [
            "scientific name",
            "family",
            "characteristic",
            "characteristics",
            "features",
            "description",
            "identify",
            "what is"
        ]

        fact_keywords = [
            "fact",
            "facts",
            "interesting"
        ]

        if any(
            keyword in question
            for keyword in conservation_keywords
        ):
            return "conservation"

        if any(
            keyword in question
            for keyword in ecology_keywords
        ):
            return "ecology"

        if any(
            keyword in question
            for keyword in fact_keywords
        ):
            return "facts"

        if any(
            keyword in question
            for keyword in botanical_keywords
        ):
            return "botanical"

        return "general"

    def answer(self, plant_name, question):
        """
        Generate a grounded response for a plant-related question.
        """

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:

            return {
                "status": "not_found",
                "plant": plant_name,
                "answer": (
                    f"I could not find '{plant_name}' "
                    "in the botanical knowledge base."
                )
            }

        question_type = self.classify_question(
            question
        )

        context = self.knowledge_base.build_context(
            plant_name
        )

        response = self._generate_response(
            plant,
            question_type,
            context
        )

        return {
            "status": "success",
            "plant": plant["common_name"],
            "question_type": question_type,
            "answer": response,
            "grounded": True
        }

    def _generate_response(
        self,
        plant,
        question_type,
        context
    ):
        """
        Generate a response using only information
        available in the retrieved botanical context.
        """

        if question_type == "botanical":

            characteristics = "\n".join(
                f"- {item}"
                for item in plant.get(
                    "characteristics",
                    []
                )
            )

            return (
                f"{plant['common_name']} "
                f"({plant['scientific_name']}) belongs "
                f"to the {plant['family']} family.\n\n"
                f"{plant['description']}\n\n"
                f"Key characteristics:\n"
                f"{characteristics}"
            )

        if question_type == "ecology":

            ecological_importance = "\n".join(
                f"- {item}"
                for item in plant.get(
                    "ecological_importance",
                    []
                )
            )

            return (
                f"{plant['common_name']} plays a role "
                f"in its local environment.\n\n"
                f"Habitat:\n"
                f"{plant['habitat']}\n\n"
                f"Ecological importance:\n"
                f"{ecological_importance}\n\n"
                f"Biodiversity role:\n"
                f"{plant['biodiversity_role']}"
            )

        if question_type == "conservation":

            threats = "\n".join(
                f"- {item}"
                for item in plant.get(
                    "threats",
                    []
                )
            )

            actions = "\n".join(
                f"- {item}"
                for item in plant.get(
                    "conservation_actions",
                    []
                )
            )

            return (
                f"Conservation status:\n"
                f"{plant['conservation_status']}\n\n"
                f"Potential threats:\n"
                f"{threats}\n\n"
                f"Conservation actions:\n"
                f"{actions}"
            )

        if question_type == "facts":

            facts = "\n".join(
                f"- {item}"
                for item in plant.get(
                    "interesting_facts",
                    []
                )
            )

            return (
                f"Interesting facts about "
                f"{plant['common_name']}:\n"
                f"{facts}"
            )

        return (
            f"{plant['common_name']} "
            f"({plant['scientific_name']}) belongs "
            f"to the {plant['family']} family.\n\n"
            f"{plant['description']}\n\n"
            f"Habitat:\n"
            f"{plant['habitat']}\n\n"
            f"Conservation status:\n"
            f"{plant['conservation_status']}"
        )

    def get_context(self, plant_name):
        """
        Expose the verified botanical context for
        downstream AI or application components.
        """

        return self.knowledge_base.build_context(
            plant_name
        )


if __name__ == "__main__":

    assistant = BotanicalAssistant()

    print("========================================")
    print("       GROUNDED BOTANICAL AI")
    print("========================================")

    plant = "Neem"

    question = (
        "Why is Neem important for biodiversity?"
    )

    print(f"\nPlant: {plant}")
    print(f"Question: {question}")

    result = assistant.answer(
        plant,
        question
    )

    print(
        "\nQuestion type:",
        result["question_type"]
    )

    print(
        "Grounded:",
        result["grounded"]
    )

    print("\nAnswer:")
    print(result["answer"])

    print("\n----------------------------------------")
    print("AI CONTEXT PREVIEW")
    print("----------------------------------------")

    context = assistant.get_context(
        "Neem"
    )

    print(context[:1000])

    print("\n...")