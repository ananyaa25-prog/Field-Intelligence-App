"""
Grounded Botanical AI Assistant.

Complete pipeline:

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
"""

from retrieval import PlantKnowledgeBase
from prompts import BotanicalPromptBuilder
from conservation import ConservationIntelligence
from evidence import BotanicalEvidence


class BotanicalAssistant:
    """
    Main botanical intelligence component.
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
            "preservation",
            "danger",
            "risk"
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
            "native region",
            "native to",
            "origin"
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

    def collect_evidence(
        self,
        plant,
        question_type
    ):
        """
        Collect evidence and confidence for the
        specific plant and question category.
        """

        if not plant:
            return self.evidence.build_evidence_report(
                None,
                question_type
            )

        return self.evidence.build_evidence_report(
            plant,
            question_type
        )

    # ==================================================
    # PROMPT CONSTRUCTION
    # ==================================================

    def build_grounded_prompt(
        self,
        plant_name,
        question
    ):

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
            plant,
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
        question,
        question_type
    ):
        """
        Generate a response using only fields
        available in the verified plant record.
        """

        question = question.lower().strip()

        common_name = plant.get(
            "common_name",
            "this plant"
        )

        # ==================================================
        # ECOLOGY
        # ==================================================

        if question_type == "ecology":

            if any(
                word in question
                for word in [
                    "habitat",
                    "where does",
                    "where do",
                    "where can"
                ]
            ):

                habitat = plant.get(
                    "habitat"
                )

                if habitat:
                    return (
                        f"The habitat of "
                        f"{common_name} is:\n\n"
                        f"{habitat}"
                    )

            if any(
                word in question
                for word in [
                    "biodiversity",
                    "biodiversity role",
                    "diversity"
                ]
            ):

                role = plant.get(
                    "biodiversity_role"
                )

                if role:
                    return (
                        f"{common_name} contributes "
                        f"to biodiversity by:\n\n"
                        f"{role}"
                    )

            if any(
                word in question
                for word in [
                    "ecological importance",
                    "ecological role",
                    "ecology",
                    "ecosystem",
                    "environment"
                ]
            ):

                importance = plant.get(
                    "ecological_importance",
                    []
                )

                if importance:

                    formatted = "\n".join(
                        f"- {item}"
                        for item in importance
                    )

                    return (
                        f"The ecological importance "
                        f"of {common_name} includes:\n\n"
                        f"{formatted}"
                    )

            if any(
                word in question
                for word in [
                    "wildlife",
                    "pollinator",
                    "pollination"
                ]
            ):

                role = plant.get(
                    "biodiversity_role"
                )

                if role:
                    return (
                        f"According to the current "
                        f"knowledge base:\n\n"
                        f"{role}"
                    )

            importance = plant.get(
                "ecological_importance",
                []
            )

            if importance:

                formatted = "\n".join(
                    f"- {item}"
                    for item in importance
                )

                return (
                    f"{common_name} plays a role "
                    f"in its local environment.\n\n"
                    f"Ecological importance:\n"
                    f"{formatted}"
                )

            return (
                f"The current knowledge base does "
                f"not contain enough ecological "
                f"information about {common_name}."
            )

        # ==================================================
        # CONSERVATION
        # ==================================================

        if question_type == "conservation":

            if any(
                word in question
                for word in [
                    "threat",
                    "threats",
                    "danger",
                    "risk"
                ]
            ):

                threats = plant.get(
                    "threats",
                    []
                )

                if threats:

                    formatted = "\n".join(
                        f"- {item}"
                        for item in threats
                    )

                    return (
                        f"Potential threats to "
                        f"{common_name} include:\n\n"
                        f"{formatted}"
                    )

            if any(
                word in question
                for word in [
                    "protect",
                    "protection",
                    "save",
                    "preserve",
                    "preservation",
                    "conserve",
                    "conservation action"
                ]
            ):

                actions = plant.get(
                    "conservation_actions",
                    []
                )

                if actions:

                    formatted = "\n".join(
                        f"- {item}"
                        for item in actions
                    )

                    return (
                        f"Conservation actions for "
                        f"{common_name} include:\n\n"
                        f"{formatted}"
                    )

            if any(
                word in question
                for word in [
                    "status",
                    "endangered"
                ]
            ):

                status = plant.get(
                    "conservation_status"
                )

                if status:
                    return (
                        f"The conservation status "
                        f"of {common_name} is:\n\n"
                        f"{status}"
                    )

            status = plant.get(
                "conservation_status"
            )

            if status:
                return (
                    f"The conservation status of "
                    f"{common_name} is:\n\n"
                    f"{status}"
                )

            return (
                f"The current knowledge base does "
                f"not contain enough conservation "
                f"information about {common_name}."
            )

        # ==================================================
        # BOTANICAL
        # ==================================================

        if question_type == "botanical":

            if "scientific name" in question:

                scientific_name = plant.get(
                    "scientific_name"
                )

                if scientific_name:
                    return (
                        f"The scientific name of "
                        f"{common_name} is "
                        f"{scientific_name}."
                    )

            if "family" in question:

                family = plant.get(
                    "family"
                )

                if family:
                    return (
                        f"{common_name} belongs to "
                        f"the {family} family."
                    )

            if any(
                word in question
                for word in [
                    "native region",
                    "native to",
                    "origin",
                    "where is it native"
                ]
            ):

                native_region = plant.get(
                    "native_region"
                )

                if native_region:
                    return (
                        f"{common_name} is native to "
                        f"{native_region}."
                    )

            if any(
                word in question
                for word in [
                    "characteristic",
                    "characteristics",
                    "feature",
                    "features"
                ]
            ):

                characteristics = plant.get(
                    "characteristics",
                    []
                )

                if characteristics:

                    formatted = "\n".join(
                        f"- {item}"
                        for item in characteristics
                    )

                    return (
                        f"Key characteristics of "
                        f"{common_name} are:\n\n"
                        f"{formatted}"
                    )

            if "description" in question:

                description = plant.get(
                    "description"
                )

                if description:
                    return (
                        f"{common_name} "
                        f"({plant.get('scientific_name', '')}) "
                        f"is {description}"
                    )

            scientific_name = plant.get(
                "scientific_name",
                ""
            )

            family = plant.get(
                "family",
                ""
            )

            description = plant.get(
                "description",
                ""
            )

            return (
                f"{common_name} "
                f"({scientific_name}) belongs "
                f"to the {family} family.\n\n"
                f"{description}"
            )

        # ==================================================
        # FACTS
        # ==================================================

        if question_type == "facts":

            facts = plant.get(
                "interesting_facts",
                []
            )

            if facts:

                formatted = "\n".join(
                    f"- {item}"
                    for item in facts
                )

                return (
                    f"Interesting facts about "
                    f"{common_name}:\n\n"
                    f"{formatted}"
                )

            return (
                f"The current knowledge base does "
                f"not contain interesting facts "
                f"about {common_name}."
            )

        # ==================================================
        # GENERAL
        # ==================================================

        if question_type == "general":

            if "scientific name" in question:

                return (
                    f"The scientific name of "
                    f"{common_name} is "
                    f"{plant.get('scientific_name')}."
                )

            if "family" in question:

                return (
                    f"{common_name} belongs to "
                    f"the {plant.get('family')} family."
                )

            if "habitat" in question:

                return (
                    f"The habitat of "
                    f"{common_name} is:\n\n"
                    f"{plant.get('habitat')}"
                )

            if any(
                word in question
                for word in [
                    "what is",
                    "describe",
                    "tell me about"
                ]
            ):

                return (
                    f"{common_name} "
                    f"({plant.get('scientific_name', '')})\n\n"
                    f"{plant.get('description', '')}"
                )

            return (
                f"{common_name} "
                f"({plant.get('scientific_name', '')}) "
                f"belongs to the "
                f"{plant.get('family', '')} family."
            )

        return (
            f"I can answer questions about "
            f"{common_name} using the information "
            f"available in the botanical knowledge base."
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
        Execute the complete grounded pipeline.
        """

        pipeline = self.build_grounded_prompt(
            plant_name,
            question
        )

        # --------------------------------------------------
        # UNKNOWN PLANT
        # --------------------------------------------------

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
                    "level": "low",
                    "score": 0.0,
                    "reason": (
                        "Plant was not found."
                    )
                },
                "prompt": None,
                "context": None
            }

        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        response = self.generate_grounded_response(
            pipeline["plant"],
            question,
            pipeline["question_type"]
        )

        # --------------------------------------------------
        # EVIDENCE REPORT
        # --------------------------------------------------

        evidence_report = pipeline.get(
            "evidence",
            {}
        )

        # --------------------------------------------------
        # CONFIDENCE
        # --------------------------------------------------

        confidence = evidence_report.get(
            "confidence",
            {
                "level": "low",
                "score": 0.0,
                "reason": (
                    "Confidence information unavailable."
                )
            }
        )

        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------

        return {
            "status": "success",

            "plant": pipeline["plant"].get(
                "common_name",
                plant_name
            ),

            "question_type": pipeline[
                "question_type"
            ],

            "answer": response,

            "grounded": evidence_report.get(
                "grounded",
                False
            ),

            "evidence": evidence_report,

            "confidence": confidence,

            "prompt": pipeline["prompt"],

            "context": pipeline["context"]
        }

    # ==================================================
    # CONTEXT ACCESS
    # ==================================================

    def get_context(
        self,
        plant_name
    ):

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:
            return None

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

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:

            return {
                "plant": plant_name,
                "question_type": "unknown",
                "evidence": None
            }

        question_type = self.classify_question(
            question
        )

        evidence = self.collect_evidence(
            plant,
            question_type
        )

        return {
            "plant": plant_name,
            "question_type": question_type,
            "evidence": evidence
        }


# ======================================================
# INTERACTIVE COMMAND LINE
# ======================================================

def run_interactive_assistant():

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

    plants = assistant.knowledge_base.list_plants()

    print("----------------------------------------")
    print("AVAILABLE PLANTS")
    print("----------------------------------------")

    for index, plant in enumerate(
        plants,
        start=1
    ):
        print(
            f"{index}. {plant}"
        )

    print()
    print("Type 'exit' at any time to quit.")

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
            f"{confidence.get('level')}"
        )

        print(
            f"Confidence score: "
            f"{confidence.get('score')}"
        )

        print()
        print("ANSWER")
        print("----------------------------------------")
        print(
            result["answer"]
        )

        print()
        print("----------------------------------------")

        evidence = result.get(
            "evidence",
            {}
        )

        print(
            "Evidence sources: "
            f"{evidence.get('sources', [])}"
        )

        print(
            "Evidence fields: "
            f"{evidence.get('evidence_fields', [])}"
        )


# ======================================================
# PROGRAM ENTRY POINT
# ======================================================

if __name__ == "__main__":
    run_interactive_assistant()