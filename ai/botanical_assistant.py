"""
Grounded Botanical AI Assistant.

This module provides:
- plant retrieval
- question classification
- botanical context generation
- conservation intelligence
- prompt construction
- grounded responses
- interactive command-line usage

The core BotanicalAssistant class can also be imported
by the application layer without using the CLI.
"""

from retrieval import PlantKnowledgeBase
from prompts import BotanicalPromptBuilder
from conservation import ConservationIntelligence


class BotanicalAssistant:
    """
    Main botanical intelligence component.

    The assistant connects the structured botanical
    knowledge base with question classification,
    conservation intelligence, prompt engineering,
    and grounded response generation.
    """

    def __init__(self):

        self.knowledge_base = PlantKnowledgeBase()

        self.conservation = ConservationIntelligence()

        self.prompt_builder = BotanicalPromptBuilder()

    # --------------------------------------------------
    # QUESTION CLASSIFICATION
    # --------------------------------------------------

    def classify_question(self, question):
        """
        Classify the user's question into an intent category.

        Supported categories:
        - botanical
        - ecology
        - conservation
        - facts
        - general
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

    # --------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------

    def retrieve_context(self, plant_name):
        """
        Retrieve verified botanical context for a plant.
        """

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:
            return None

        return self.knowledge_base.build_context(
            plant_name
        )

    # --------------------------------------------------
    # CONSERVATION CONTEXT
    # --------------------------------------------------

    def get_conservation_context(self, plant_name):
        """
        Retrieve grounded conservation information
        for the selected plant.

        Conservation information is obtained from the
        dedicated ConservationIntelligence layer.
        """

        return self.conservation.build_ai_context(
            plant_name
        )

    # --------------------------------------------------
    # COMBINED AI CONTEXT
    # --------------------------------------------------

    def build_ai_context(self, plant_name):
        """
        Build the complete grounded AI context.

        The context combines:
        - botanical knowledge
        - conservation knowledge

        Both are retrieved from the verified
        knowledge base.
        """

        plant_context = self.retrieve_context(
            plant_name
        )

        if plant_context is None:
            return None

        conservation_context = (
            self.get_conservation_context(
                plant_name
            )
        )

        if conservation_context is None:
            return plant_context

        return (
            plant_context
            + "\n\n"
            + conservation_context
        )

    # --------------------------------------------------
    # PROMPT CONSTRUCTION
    # --------------------------------------------------

    def build_grounded_prompt(
        self,
        plant_name,
        question
    ):
        """
        Retrieve plant information and construct a
        category-specific grounded AI prompt.
        """

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:
            return None

        context = self.build_ai_context(
            plant_name
        )

        question_type = self.classify_question(
            question
        )

        if question_type == "ecology":

            prompt = (
                self.prompt_builder
                .build_ecology_prompt(
                    plant_context=context,
                    question=question
                )
            )

        elif question_type == "conservation":

            prompt = (
                self.prompt_builder
                .build_conservation_prompt(
                    plant_context=context,
                    question=question
                )
            )

        elif question_type == "botanical":

            prompt = (
                self.prompt_builder
                .build_botanical_prompt(
                    plant_context=context,
                    question=question
                )
            )

        elif question_type == "facts":

            prompt = (
                self.prompt_builder
                .build_facts_prompt(
                    plant_context=context,
                    question=question
                )
            )

        else:

            prompt = (
                self.prompt_builder
                .build_prompt(
                    plant_context=context,
                    question=question,
                    question_type=question_type
                )
            )

        return {
            "plant": plant,
            "question_type": question_type,
            "context": context,
            "prompt": prompt
        }

    # --------------------------------------------------
    # GROUNDED RESPONSE
    # --------------------------------------------------

    def generate_grounded_response(
        self,
        plant,
        question_type
    ):
        """
        Generate a response directly from the verified
        botanical knowledge base.

        This deterministic response layer is used until
        an external LLM is connected.
        """

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

            conservation_profile = (
                self.conservation
                .get_conservation_profile(
                    plant["common_name"]
                )
            )

            if conservation_profile is not None:

                threats = "\n".join(
                    f"- {item}"
                    for item in
                    conservation_profile[
                        "threats"
                    ]
                )

                actions = "\n".join(
                    f"- {item}"
                    for item in
                    conservation_profile[
                        "conservation_actions"
                    ]
                )

                return (
                    f"Conservation status:\n"
                    f"{conservation_profile['conservation_status']}\n\n"
                    f"Potential threats:\n"
                    f"{threats}\n\n"
                    f"Conservation actions:\n"
                    f"{actions}"
                )

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

    # --------------------------------------------------
    # COMPLETE ANSWER PIPELINE
    # --------------------------------------------------

    def answer(
        self,
        plant_name,
        question
    ):
        """
        Execute the complete grounded AI pipeline.

        Pipeline:
            1. Plant retrieval
            2. Question classification
            3. Botanical context construction
            4. Conservation context construction
            5. Combined grounded context
            6. Prompt construction
            7. Grounded response generation
        """

        pipeline = self.build_grounded_prompt(
            plant_name,
            question
        )

        if pipeline is None:

            return {
                "status": "not_found",
                "plant": plant_name,
                "question_type": "unknown",
                "answer": (
                    f"I could not find '{plant_name}' "
                    "in the botanical knowledge base."
                ),
                "grounded": False,
                "prompt": None,
                "context": None
            }

        response = self.generate_grounded_response(
            pipeline["plant"],
            pipeline["question_type"]
        )

        return {
            "status": "success",
            "plant": pipeline["plant"][
                "common_name"
            ],
            "question_type": pipeline[
                "question_type"
            ],
            "answer": response,
            "grounded": True,
            "prompt": pipeline["prompt"],
            "context": pipeline["context"]
        }

    # --------------------------------------------------
    # CONTEXT ACCESS
    # --------------------------------------------------

    def get_context(self, plant_name):
        """
        Return the complete verified botanical and
        conservation context for downstream components.
        """

        return self.build_ai_context(
            plant_name
        )


# ======================================================
# INTERACTIVE COMMAND-LINE INTERFACE
# ======================================================

def run_interactive_assistant():
    """
    Run the Botanical Assistant interactively.

    This function is intentionally separate from the
    BotanicalAssistant class so that application code
    can import the class without triggering input().
    """

    assistant = BotanicalAssistant()

    print()
    print("========================================")
    print("       BOTANICAL INTELLIGENCE AI")
    print("========================================")

    print()
    print(
        "Welcome to the Botanical Intelligence Assistant."
    )

    print(
        "Ask questions about plants, ecology, "
        "biodiversity, and conservation."
    )

    print()
    print("----------------------------------------")
    print("AVAILABLE PLANTS")
    print("----------------------------------------")

    plants = assistant.knowledge_base.list_plants()

    for index, plant in enumerate(
        plants,
        start=1
    ):
        print(
            f"{index}. {plant}"
        )

    print()
    print(
        "Type 'exit' at any time to quit."
    )

    while True:

        print()
        print("----------------------------------------")

        plant_name = input(
            "Enter plant name: "
        ).strip()

        if plant_name.lower() == "exit":

            print()
            print(
                "Thank you for using the "
                "Botanical Intelligence Assistant."
            )

            break

        if not plant_name:

            print(
                "Please enter a plant name."
            )

            continue

        plant = assistant.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:

            print()
            print(
                f"Plant '{plant_name}' was not found."
            )

            print(
                "Please choose a plant from the "
                "available list."
            )

            continue

        print()
        print(
            f"Selected plant: "
            f"{plant['common_name']}"
        )

        print(
            f"Scientific name: "
            f"{plant['scientific_name']}"
        )

        print()

        question = input(
            "Ask your question: "
        ).strip()

        if question.lower() == "exit":

            print()
            print(
                "Thank you for using the "
                "Botanical Intelligence Assistant."
            )

            break

        if not question:

            print(
                "Please enter a question."
            )

            continue

        result = assistant.answer(
            plant_name,
            question
        )

        print()
        print("----------------------------------------")
        print("AI ANALYSIS")
        print("----------------------------------------")

        print(
            f"Question type: "
            f"{result['question_type']}"
        )

        print(
            f"Knowledge grounded: "
            f"{result['grounded']}"
        )

        print()
        print("ANSWER")
        print("----------------------------------------")

        print(
            result["answer"]
        )

        print()
        print("----------------------------------------")

        print(
            "The response was generated from "
            "the verified botanical knowledge base."
        )


# ======================================================
# PROGRAM ENTRY POINT
# ======================================================

if __name__ == "__main__":

    run_interactive_assistant()