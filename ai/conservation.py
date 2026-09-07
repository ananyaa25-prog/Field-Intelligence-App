"""
Conservation Intelligence Module.

This module provides structured conservation information
using the verified botanical knowledge base.

The module does not invent conservation facts.
All plant-specific information is retrieved from the
curated knowledge base.
"""

from retrieval import PlantKnowledgeBase


class ConservationIntelligence:
    """
    Provides conservation-focused information for plants.
    """

    def __init__(self):

        self.knowledge_base = PlantKnowledgeBase()

    # --------------------------------------------------
    # GET CONSERVATION PROFILE
    # --------------------------------------------------

    def get_conservation_profile(self, plant_name):
        """
        Return the complete conservation profile
        for a plant.
        """

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:
            return None

        return {
            "plant": plant.get(
                "common_name"
            ),

            "scientific_name": plant.get(
                "scientific_name"
            ),

            "conservation_status": plant.get(
                "conservation_status"
            ),

            "threats": plant.get(
                "threats",
                []
            ),

            "conservation_actions": plant.get(
                "conservation_actions",
                []
            ),

            "biodiversity_role": plant.get(
                "biodiversity_role"
            )
        }

    # --------------------------------------------------
    # THREATS
    # --------------------------------------------------

    def get_threats(self, plant_name):
        """
        Return known threats affecting the plant.
        """

        profile = self.get_conservation_profile(
            plant_name
        )

        if profile is None:
            return None

        return profile["threats"]

    # --------------------------------------------------
    # CONSERVATION ACTIONS
    # --------------------------------------------------

    def get_conservation_actions(
        self,
        plant_name
    ):
        """
        Return recommended conservation actions.
        """

        profile = self.get_conservation_profile(
            plant_name
        )

        if profile is None:
            return None

        return profile[
            "conservation_actions"
        ]

    # --------------------------------------------------
    # BIODIVERSITY ROLE
    # --------------------------------------------------

    def get_biodiversity_role(
        self,
        plant_name
    ):
        """
        Return the plant's biodiversity role.
        """

        profile = self.get_conservation_profile(
            plant_name
        )

        if profile is None:
            return None

        return profile[
            "biodiversity_role"
        ]

    # --------------------------------------------------
    # CONSERVATION SUMMARY
    # --------------------------------------------------

    def get_summary(self, plant_name):
        """
        Build a concise conservation summary
        suitable for the application.
        """

        profile = self.get_conservation_profile(
            plant_name
        )

        if profile is None:
            return None

        return {
            "plant": profile["plant"],
            "scientific_name": profile[
                "scientific_name"
            ],
            "status": profile[
                "conservation_status"
            ],
            "biodiversity_role": profile[
                "biodiversity_role"
            ],
            "threat_count": len(
                profile["threats"]
            ),
            "action_count": len(
                profile["conservation_actions"]
            )
        }

    # --------------------------------------------------
    # AI CONSERVATION CONTEXT
    # --------------------------------------------------

    def build_ai_context(self, plant_name):
        """
        Construct a grounded conservation context
        that can be supplied to the Botanical AI.
        """

        profile = self.get_conservation_profile(
            plant_name
        )

        if profile is None:
            return None

        threats = "\n".join(
            f"- {item}"
            for item in profile["threats"]
        )

        actions = "\n".join(
            f"- {item}"
            for item in profile[
                "conservation_actions"
            ]
        )

        return (
            "CONSERVATION CONTEXT\n\n"

            f"Plant:\n"
            f"{profile['plant']}\n\n"

            f"Scientific Name:\n"
            f"{profile['scientific_name']}\n\n"

            f"Conservation Status:\n"
            f"{profile['conservation_status']}\n\n"

            f"Biodiversity Role:\n"
            f"{profile['biodiversity_role']}\n\n"

            f"Known Threats:\n"
            f"{threats}\n\n"

            f"Conservation Actions:\n"
            f"{actions}\n\n"

            "Use only the information above when "
            "answering conservation-related questions."
        )


# ======================================================
# BASIC MODULE DEMONSTRATION
# ======================================================

if __name__ == "__main__":

    conservation = ConservationIntelligence()

    print("========================================")
    print("      CONSERVATION INTELLIGENCE")
    print("========================================")

    plant_name = "Neem"

    profile = conservation.get_conservation_profile(
        plant_name
    )

    if profile is None:

        print()
        print(
            f"Plant '{plant_name}' not found."
        )

    else:

        print()
        print(
            f"Plant: {profile['plant']}"
        )

        print(
            f"Scientific name: "
            f"{profile['scientific_name']}"
        )

        print()
        print("Conservation Status")
        print("----------------------------------------")
        print(
            profile["conservation_status"]
        )

        print()
        print("Known Threats")
        print("----------------------------------------")

        for threat in profile["threats"]:

            print(
                f"- {threat}"
            )

        print()
        print("Conservation Actions")
        print("----------------------------------------")

        for action in profile[
            "conservation_actions"
        ]:

            print(
                f"- {action}"
            )

        print()
        print("Biodiversity Role")
        print("----------------------------------------")
        print(
            profile["biodiversity_role"]
        )

        print()
        print("AI Context")
        print("----------------------------------------")

        context = conservation.build_ai_context(
            plant_name
        )

        print(
            context
        )

        print()
        print("========================================")
        print("  CONSERVATION MODULE READY")
        print("========================================")