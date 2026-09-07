"""
Grounded Botanical AI Assistant.

This module provides the complete botanical intelligence pipeline:

    Plant Retrieval
          ↓
    Question Classification
          ↓
    Evidence Collection
          ↓
    Confidence Evaluation
          ↓
    Grounded Prompt Construction
          ↓
    Grounded Response Generation
          ↓
    Application-Ready Result

The assistant is designed so that the application layer can
import BotanicalAssistant without triggering the CLI.

All factual responses are grounded in the structured botanical
and conservation knowledge bases.
"""

from retrieval import PlantKnowledgeBase
from prompts import BotanicalPromptBuilder
from conservation import ConservationIntelligence
from evidence import BotanicalEvidence


class BotanicalAssistant:
    """
    Main botanical intelligence component.

    Connects:
    - botanical knowledge
    - conservation knowledge
    - evidence collection
    - confidence evaluation
    - prompt engineering
    - grounded response generation
    """

    def __init__(self):

        self.knowledge_base = PlantKnowledgeBase()

        self.conservation = ConservationIntelligence()

        self.evidence = BotanicalEvidence()

        self.prompt_builder = BotanicalPromptBuilder()

    # ==================================================
    # QUESTION CLASSIFICATION
    # ==================================================

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
            "preserve",
            "preservation"
        ]

        ecology_keywords = [
            "ecology",
            "ecological",
            "biodiversity",
            "environment",
            "habitat",
            "ecosystem",
            "wildlife",
            "pollinator",
            "pollination"
        ]

        botanical_keywords = [
            "scientific name",
            "family",
            "characteristic",
            "characteristics",
            "feature",
            "features",
            "description",
            "identify",
            "identification",
            "what is",
            "native region"
        ]

        fact_keywords = [
            "fact",
            "facts",
            "interesting",
            "interesting fact",
            "did you know"
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

    # ==================================================
    # PLANT RETRIEVAL
    # ==================================================

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

    # ==================================================
    # EVIDENCE COLLECTION
    # ==================================================

    def collect_evidence(self, plant_name, question_type):
        """
        Collect grounded evidence for the selected plant.

        The evidence layer determines:
        - whether sufficient evidence exists
        - which knowledge sources were used
        - which fields are relevant
        - confidence level
        - confidence score
        - confidence reasoning
        """

        try:

            return self.evidence.collect_evidence(
                plant_name,
                question_type
            )

        except TypeError:

            try:

                return self.evidence.collect_evidence(
                    plant_name
                )

            except Exception:

                return None

        except Exception:

            return None

    # ==================================================
    # PROMPT CONSTRUCTION
    # ==================================================

    def build_grounded_prompt(
        self,
        plant_name,
        question
    ):
        """
        Retrieve plant information, collect evidence,
        classify the question and construct a grounded prompt.
        """

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:
            return None

        context = self.knowledge_base.build_context(
            plant_name
        )

        question_type = self.classify_question(
            question
        )

        evidence = self.collect_evidence(
            plant_name,
            question_type
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
            "evidence": evidence,
            "prompt": prompt
        }

    # ==================================================
    # GROUNDED RESPONSE GENERATION
    # ==================================================

    def generate_grounded_response(
        self,
        plant,
        question_type
    ):
        """
        Generate a deterministic response directly from
        the verified botanical knowledge base.

        This layer intentionally avoids inventing information.
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

    # ==================================================
    # COMPLETE AI PIPELINE
    # ==================================================

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
        3. Evidence collection
        4. Confidence evaluation
        5. Context construction
        6. Grounded prompt construction
        7. Grounded response generation
        8. Application-ready result
        """

        pipeline = self.build_grounded_prompt(
            plant_name,
            question
        )

        # ----------------------------------------------
        # UNKNOWN PLANT
        # ----------------------------------------------

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
                "evidence": None,
                "confidence": {
                    "level": "none",
                    "score": 0.0,
                    "reason": "Plant was not found."
                },
                "prompt": None,
                "context": None
            }

        # ----------------------------------------------
        # GROUNDED RESPONSE
        # ----------------------------------------------

        response = self.generate_grounded_response(
            pipeline["plant"],
            pipeline["question_type"]
        )

        # ----------------------------------------------
        # EVIDENCE
        # ----------------------------------------------

        evidence = pipeline.get(
            "evidence"
        )

        # ----------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------

        confidence = {
            "level": "unknown",
            "score": 0.0,
            "reason": "Confidence information unavailable."
        }

        if evidence:

            if isinstance(evidence, dict):

                if "confidence" in evidence:

                    confidence = evidence[
                        "confidence"
                    ]

                elif "grounding" in evidence:

                    grounding = evidence[
                        "grounding"
                    ]

                    if isinstance(
                        grounding,
                        dict
                    ):

                        confidence = grounding.get(
                            "confidence",
                            confidence
                        )

        # ----------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------

        return {
            "status": "success",

            "plant": pipeline[
                "plant"
            ][
                "common_name"
            ],

            "question_type": pipeline[
                "question_type"
            ],

            "answer": response,

            "grounded": True,

            "evidence": evidence,

            "confidence": confidence,

            "prompt": pipeline[
                "prompt"
            ],

            "context": pipeline[
                "context"
            ]
        }

    # ==================================================
    # CONTEXT ACCESS
    # ==================================================

    def get_context(
        self,
        plant_name
    ):
        """
        Return verified botanical context for downstream
        application or AI components.
        """

        return self.knowledge_base.build_context(
            plant_name
        )

    # ==================================================
    # EVIDENCE REPORT
    # ==================================================

    def get_evidence_report(
        self,
        plant_name,
        question
    ):
        """
        Return the evidence and confidence report for
        a specific botanical question.
        """

        question_type = self.classify_question(
            question
        )

        evidence = self.collect_evidence(
            plant_name,
            question_type
        )

        return {
            "plant": plant_name,
            "question_type": question_type,
            "evidence": evidence
        }


# ======================================================
# INTERACTIVE COMMAND-LINE INTERFACE
# ======================================================

def run_interactive_assistant():
    """
    Run the Botanical Intelligence Assistant interactively.

    The CLI demonstrates:
    - plant selection
    - question classification
    - grounded answers
    - evidence availability
    - confidence
    - safe error handling
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

    plants = (
        assistant
        .knowledge_base
        .list_plants()
    )

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

        plant = (
            assistant
            .knowledge_base
            .get_plant(
                plant_name
            )
        )

        if plant is None:

            print()

            print(
                f"Plant '{plant_name}' "
                "was not found."
            )

            print(
                "Please choose a plant from "
                "the available list."
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

        confidence = result.get(
            "confidence",
            {}
        )

        print(
            f"Confidence level: "
            f"{confidence.get('level', 'unknown')}"
        )

        print(
            f"Confidence score: "
            f"{confidence.get('score', 0.0)}"
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
            "Evidence available: "
            f"{result.get('evidence') is not None}"
        )

        print(
            "The response was generated from "
            "the verified botanical knowledge base."
        )


# ======================================================
# PROGRAM ENTRY POINT
# ======================================================

if __name__ == "__main__":

    run_interactive_assistant()