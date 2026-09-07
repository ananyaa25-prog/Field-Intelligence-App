"""
Field Plant Profile Layer.

This module converts verified botanical knowledge into a
structured field-ready profile.

The profile is designed for:
- the Botanical AI assistant
- conservation guidance
- the mobile/AR application
- future API integration

No botanical facts are generated here.
All information comes from the verified knowledge base.
"""

from retrieval import PlantKnowledgeBase


class FieldPlantProfile:
    """
    Creates structured plant profiles from the
    botanical knowledge base.
    """

    def __init__(self):

        self.knowledge_base = PlantKnowledgeBase()

    # --------------------------------------------------
    # BUILD PROFILE
    # --------------------------------------------------

    def get_profile(self, plant_name):
        """
        Retrieve a complete structured profile.

        Returns None if the plant is not present
        in the knowledge base.
        """

        plant = self.knowledge_base.get_plant(
            plant_name
        )

        if plant is None:
            return None

        return {
            "identity": {
                "common_name": plant.get(
                    "common_name"
                ),
                "scientific_name": plant.get(
                    "scientific_name"
                ),
                "family": plant.get(
                    "family"
                )
            },

            "origin": {
                "native_region": plant.get(
                    "native_region"
                )
            },

            "description": plant.get(
                "description"
            ),

            "characteristics": plant.get(
                "characteristics",
                []
            ),

            "habitat": plant.get(
                "habitat"
            ),

            "ecology": {
                "ecological_importance": plant.get(
                    "ecological_importance",
                    []
                ),
                "biodiversity_role": plant.get(
                    "biodiversity_role"
                )
            },

            "conservation": {
                "status": plant.get(
                    "conservation_status"
                ),
                "threats": plant.get(
                    "threats",
                    []
                ),
                "recommended_actions": plant.get(
                    "conservation_actions",
                    []
                )
            },

            "interesting_facts": plant.get(
                "interesting_facts",
                []
            )
        }

    # --------------------------------------------------
    # FIELD SUMMARY
    # --------------------------------------------------

    def get_field_summary(self, plant_name):
        """
        Create a concise field-oriented summary.

        This is useful for displaying information
        inside the mobile/AR application.
        """

        profile = self.get_profile(
            plant_name
        )

        if profile is None:
            return None

        identity = profile["identity"]
        ecology = profile["ecology"]
        conservation = profile["conservation"]

        return {
            "plant_name": identity["common_name"],
            "scientific_name": identity[
                "scientific_name"
            ],
            "family": identity["family"],
            "habitat": profile["habitat"],
            "ecological_importance": (
                ecology["ecological_importance"]
            ),
            "biodiversity_role": (
                ecology["biodiversity_role"]
            ),
            "conservation_status": (
                conservation["status"]
            ),
            "threats": conservation["threats"],
            "conservation_actions": (
                conservation["recommended_actions"]
            )
        }

    # --------------------------------------------------
    # AI CONTEXT
    # --------------------------------------------------

    def get_ai_context(self, plant_name):
        """
        Return the verified context used by the
        Botanical AI system.
        """

        profile = self.get_profile(
            plant_name
        )

        if profile is None:
            return None

        identity = profile["identity"]
        ecology = profile["ecology"]
        conservation = profile["conservation"]

        return (
            f"PLANT PROFILE\n\n"

            f"Common Name:\n"
            f"{identity['common_name']}\n\n"

            f"Scientific Name:\n"
            f"{identity['scientific_name']}\n\n"

            f"Family:\n"
            f"{identity['family']}\n\n"

            f"Native Region:\n"
            f"{profile['origin']['native_region']}\n\n"

            f"Description:\n"
            f"{profile['description']}\n\n"

            f"Habitat:\n"
            f"{profile['habitat']}\n\n"

            f"Ecological Importance:\n"
            f"{self._format_list(ecology['ecological_importance'])}\n\n"

            f"Biodiversity Role:\n"
            f"{ecology['biodiversity_role']}\n\n"

            f"Conservation Status:\n"
            f"{conservation['status']}\n\n"

            f"Threats:\n"
            f"{self._format_list(conservation['threats'])}\n\n"

            f"Conservation Actions:\n"
            f"{self._format_list(conservation['recommended_actions'])}"
        )

    # --------------------------------------------------
    # DISPLAY PROFILE
    # --------------------------------------------------

    def display_profile(self, plant_name):
        """
        Print a human-readable field profile.
        """

        profile = self.get_profile(
            plant_name
        )

        if profile is None:

            print(
                f"Plant '{plant_name}' "
                "was not found."
            )

            return

        identity = profile["identity"]
        ecology = profile["ecology"]
        conservation = profile["conservation"]

        print()
        print("========================================")
        print("          FIELD PLANT PROFILE")
        print("========================================")

        print()
        print(
            f"Plant: {identity['common_name']}"
        )

        print(
            f"Scientific name: "
            f"{identity['scientific_name']}"
        )

        print(
            f"Family: {identity['family']}"
        )

        print(
            f"Native region: "
            f"{profile['origin']['native_region']}"
        )

        print()
        print("Description")
        print("----------------------------------------")
        print(profile["description"])

        print()
        print("Habitat")
        print("----------------------------------------")
        print(profile["habitat"])

        print()
        print("Ecological Importance")
        print("----------------------------------------")

        for item in ecology[
            "ecological_importance"
        ]:
            print(f"- {item}")

        print()
        print("Biodiversity Role")
        print("----------------------------------------")
        print(
            ecology["biodiversity_role"]
        )

        print()
        print("Conservation Status")
        print("----------------------------------------")
        print(
            conservation["status"]
        )

        print()
        print("Threats")
        print("----------------------------------------")

        for item in conservation[
            "threats"
        ]:
            print(f"- {item}")

        print()
        print("Conservation Actions")
        print("----------------------------------------")

        for item in conservation[
            "recommended_actions"
        ]:
            print(f"- {item}")

        print()
        print("========================================")

    # --------------------------------------------------
    # INTERNAL HELPER
    # --------------------------------------------------

    @staticmethod
    def _format_list(items):
        """
        Convert a list into readable bullet points.
        """

        if not items:
            return "- No information available"

        return "\n".join(
            f"- {item}"
            for item in items
        )


# ======================================================
# DEMONSTRATION
# ======================================================

