"""
Botanical Evidence and Confidence Layer.

This module provides:
- evidence tracking
- grounded field identification
- evidence summaries
- confidence estimation
- source transparency for AI responses

The module does not generate new botanical facts.
It only evaluates and reports the structured
knowledge already available in the project.
"""


class BotanicalEvidence:
    """
    Evidence and confidence manager for the
    Botanical Intelligence AI pipeline.
    """

    def __init__(self):
        self.source_types = [
            "botanical_knowledge_base",
            "conservation_knowledge_base"
        ]

    # --------------------------------------------------
    # EVIDENCE COLLECTION
    # --------------------------------------------------

    def collect_evidence(self, plant):
        """
        Collect all available evidence fields from
        a verified botanical plant record.
        """

        if not plant:
            return {
                "available": False,
                "fields": [],
                "sources": []
            }

        botanical_fields = [
            "common_name",
            "scientific_name",
            "family",
            "native_region",
            "description",
            "characteristics",
            "habitat",
            "ecological_importance",
            "biodiversity_role",
            "interesting_facts"
        ]

        conservation_fields = [
            "conservation_status",
            "threats",
            "conservation_actions"
        ]

        fields = []

        for field in botanical_fields:
            if plant.get(field):
                fields.append(field)

        for field in conservation_fields:
            if plant.get(field):
                fields.append(field)

        sources = []

        if any(
            field in fields
            for field in botanical_fields
        ):
            sources.append(
                "botanical_knowledge_base"
            )

        if any(
            field in fields
            for field in conservation_fields
        ):
            sources.append(
                "conservation_knowledge_base"
            )

        return {
            "available": len(fields) > 0,
            "fields": fields,
            "sources": sources
        }

    # --------------------------------------------------
    # QUESTION-SPECIFIC EVIDENCE
    # --------------------------------------------------

    def get_relevant_fields(
        self,
        plant,
        question_type
    ):
        """
        Identify the evidence fields relevant to
        the user's question category.
        """

        if not plant:
            return []

        mapping = {
            "botanical": [
                "common_name",
                "scientific_name",
                "family",
                "description",
                "characteristics"
            ],

            "ecology": [
                "habitat",
                "ecological_importance",
                "biodiversity_role"
            ],

            "conservation": [
                "conservation_status",
                "threats",
                "conservation_actions"
            ],

            "facts": [
                "interesting_facts"
            ],

            "general": [
                "common_name",
                "scientific_name",
                "family",
                "description",
                "habitat",
                "conservation_status"
            ]
        }

        fields_to_check = mapping.get(
            question_type,
            mapping["general"]
        )

        relevant_fields = []

        for field in fields_to_check:
            if plant.get(field):
                relevant_fields.append(field)

        return relevant_fields

    # --------------------------------------------------
    # CONFIDENCE ESTIMATION
    # --------------------------------------------------

    def calculate_confidence(
        self,
        plant,
        question_type
    ):
        """
        Calculate deterministic confidence based
        on the availability of relevant structured
        evidence.
        """

        if not plant:
            return {
                "level": "low",
                "score": 0.0,
                "reason": (
                    "No verified plant record found."
                )
            }

        mapping = {
            "botanical": [
                "common_name",
                "scientific_name",
                "family",
                "description",
                "characteristics"
            ],

            "ecology": [
                "habitat",
                "ecological_importance",
                "biodiversity_role"
            ],

            "conservation": [
                "conservation_status",
                "threats",
                "conservation_actions"
            ],

            "facts": [
                "interesting_facts"
            ],

            "general": [
                "common_name",
                "scientific_name",
                "family",
                "description",
                "habitat",
                "conservation_status"
            ]
        }

        expected_fields = mapping.get(
            question_type,
            mapping["general"]
        )

        relevant_fields = self.get_relevant_fields(
            plant,
            question_type
        )

        total_possible = len(expected_fields)

        if total_possible == 0:
            score = 0.0
        else:
            score = (
                len(relevant_fields)
                / total_possible
            )

        if score >= 0.8:
            level = "high"
        elif score >= 0.5:
            level = "medium"
        else:
            level = "low"

        return {
            "level": level,
            "score": round(score, 2),
            "reason": (
                f"{len(relevant_fields)} of "
                f"{total_possible} relevant evidence "
                f"fields are available."
            )
        }

    # --------------------------------------------------
    # EVIDENCE REPORT
    # --------------------------------------------------

    def build_evidence_report(
        self,
        plant,
        question_type
    ):
        """
        Build a structured evidence report that can
        be consumed by the AI/application layer.
        """

        if not plant:
            return {
                "grounded": False,
                "sources": [],
                "evidence_fields": [],
                "confidence": {
                    "level": "low",
                    "score": 0.0,
                    "reason": (
                        "No verified plant record found."
                    )
                }
            }

        evidence = self.collect_evidence(plant)

        relevant_fields = self.get_relevant_fields(
            plant,
            question_type
        )

        confidence = self.calculate_confidence(
            plant,
            question_type
        )

        return {
            "grounded": evidence["available"],
            "sources": evidence["sources"],
            "evidence_fields": relevant_fields,
            "confidence": confidence
        }

    # --------------------------------------------------
    # HUMAN-READABLE SUMMARY
    # --------------------------------------------------

    def build_summary(
        self,
        plant,
        question_type
    ):
        """
        Create a readable grounding report for
        debugging, demonstrations, and application UI.
        """

        report = self.build_evidence_report(
            plant,
            question_type
        )

        if not report["grounded"]:
            return (
                "Grounding status: Not grounded\n"
                "No verified botanical evidence available."
            )

        sources = "\n".join(
            f"- {source}"
            for source in report["sources"]
        )

        fields = "\n".join(
            f"- {field}"
            for field in report["evidence_fields"]
        )

        confidence = report["confidence"]

        return (
            "GROUNDING REPORT\n"
            "----------------------------------------\n"
            "Grounded: True\n\n"
            "Evidence sources:\n"
            f"{sources}\n\n"
            "Relevant evidence fields:\n"
            f"{fields}\n\n"
            "Confidence:\n"
            f"- Level: {confidence['level']}\n"
            f"- Score: {confidence['score']}\n"
            f"- Reason: {confidence['reason']}"
        )


# ======================================================
# BACKWARD COMPATIBILITY
# ======================================================

EvidenceManager = BotanicalEvidence


# ======================================================
# DEMONSTRATION
# ======================================================

if __name__ == "__main__":

    from retrieval import PlantKnowledgeBase

    print("========================================")
    print("       BOTANICAL EVIDENCE LAYER")
    print("========================================")

    knowledge_base = PlantKnowledgeBase()
    evidence = BotanicalEvidence()

    plant = knowledge_base.get_plant("Neem")

    print()
    print("Testing Neem evidence...")

    report = evidence.build_evidence_report(
        plant,
        "ecology"
    )

    if report["grounded"]:
        print(
            "PASS - Evidence successfully collected"
        )
    else:
        print(
            "FAIL - Evidence collection failed"
        )

    print()
    print(
        evidence.build_summary(
            plant,
            "ecology"
        )
    )

    print()
    print("========================================")
    print("       EVIDENCE LAYER READY")
    print("========================================")
    