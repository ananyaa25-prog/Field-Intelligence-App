import json
from pathlib import Path


class PlantKnowledgeBase:
    """
    Structured botanical knowledge base.

    Loads plant information from plants.json and provides:
    - plant lookup
    - normalized name matching
    - keyword search
    - ecological information
    - conservation information
    - AI-ready botanical context
    """

    def __init__(self, data_path=None):

        if data_path is None:
            data_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "plants.json"
            )

        self.data_path = Path(data_path)
        self.plants = self._load_data()

    def _load_data(self):
        """Load plant information from the JSON knowledge base."""

        try:

            with open(
                self.data_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    "Plant knowledge base must be a JSON object."
                )

            return data

        except FileNotFoundError:

            raise FileNotFoundError(
                f"Plant knowledge base not found: {self.data_path}"
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid JSON in plant knowledge base: {error}"
            )

    def normalize_name(self, plant_name):
        """
        Normalize plant names for flexible matching.
        """

        if not plant_name:
            return ""

        normalized = plant_name.strip().lower()

        removable_words = {
            "plant",
            "tree",
            "flower",
            "herb"
        }

        words = normalized.split()

        cleaned_words = [
            word
            for word in words
            if word not in removable_words
        ]

        return " ".join(cleaned_words)

    def get_plant(self, plant_name):
        """
        Retrieve a plant using:
        - plant ID
        - common name
        - scientific name
        - normalized name
        """

        search_name = self.normalize_name(plant_name)

        if not search_name:
            return None

        for plant_id, plant_data in self.plants.items():

            common_name = self.normalize_name(
                plant_data.get("common_name", "")
            )

            scientific_name = self.normalize_name(
                plant_data.get("scientific_name", "")
            )

            normalized_id = self.normalize_name(
                plant_id
            )

            if (
                search_name == common_name
                or search_name == scientific_name
                or search_name == normalized_id
            ):
                return plant_data

        return None

    def list_plants(self):
        """Return all available plant common names."""

        plant_names = []

        for plant_id, plant_data in self.plants.items():

            plant_names.append(
                plant_data.get(
                    "common_name",
                    plant_id
                )
            )

        return plant_names

    def search(self, keyword):
        """
        Search the complete botanical record using a keyword.
        """

        if not keyword:
            return []

        keyword = keyword.strip().lower()

        if not keyword:
            return []

        results = []

        for plant_data in self.plants.values():

            searchable_content = json.dumps(
                plant_data,
                ensure_ascii=False
            ).lower()

            if keyword in searchable_content:
                results.append(plant_data)

        return results

    def get_by_family(self, family_name):
        """
        Retrieve all plants belonging to a botanical family.
        """

        if not family_name:
            return []

        family_name = family_name.strip().lower()

        results = []

        for plant_data in self.plants.values():

            family = plant_data.get(
                "family",
                ""
            ).lower()

            if family_name == family:
                results.append(plant_data)

        return results

    def get_conservation_information(self, plant_name):
        """
        Retrieve conservation-related information.
        """

        plant = self.get_plant(plant_name)

        if plant is None:
            return None

        return {
            "common_name": plant.get("common_name"),
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
            )
        }

    def get_ecological_information(self, plant_name):
        """
        Retrieve ecological information.
        """

        plant = self.get_plant(plant_name)

        if plant is None:
            return None

        return {
            "common_name": plant.get("common_name"),
            "habitat": plant.get(
                "habitat"
            ),
            "ecological_importance": plant.get(
                "ecological_importance",
                []
            ),
            "biodiversity_role": plant.get(
                "biodiversity_role"
            )
        }

    def build_context(self, plant_name):
        """
        Build a clean AI-ready context from the plant knowledge base.

        This converts structured botanical information into a
        readable context that can later be supplied to an AI
        response-generation layer.
        """

        plant = self.get_plant(plant_name)

        if plant is None:
            return None

        characteristics = "\n".join(
            f"- {item}"
            for item in plant.get(
                "characteristics",
                []
            )
        )

        ecological_importance = "\n".join(
            f"- {item}"
            for item in plant.get(
                "ecological_importance",
                []
            )
        )

        threats = "\n".join(
            f"- {item}"
            for item in plant.get(
                "threats",
                []
            )
        )

        conservation_actions = "\n".join(
            f"- {item}"
            for item in plant.get(
                "conservation_actions",
                []
            )
        )

        interesting_facts = "\n".join(
            f"- {item}"
            for item in plant.get(
                "interesting_facts",
                []
            )
        )

        context = f"""
PLANT PROFILE

Common Name:
{plant.get("common_name", "Unknown")}

Scientific Name:
{plant.get("scientific_name", "Unknown")}

Family:
{plant.get("family", "Unknown")}

Native Region:
{plant.get("native_region", "Unknown")}

Description:
{plant.get("description", "No description available.")}

Characteristics:
{characteristics}

Habitat:
{plant.get("habitat", "Unknown")}

Ecological Importance:
{ecological_importance}

Biodiversity Role:
{plant.get("biodiversity_role", "Unknown")}

Conservation Status:
{plant.get("conservation_status", "Unknown")}

Threats:
{threats}

Conservation Actions:
{conservation_actions}

Interesting Facts:
{interesting_facts}
""".strip()

        return context


if __name__ == "__main__":

    knowledge_base = PlantKnowledgeBase()

    print("========================================")
    print("      BOTANICAL KNOWLEDGE BASE")
    print("========================================")

    print(
        f"\nTotal plants: "
        f"{len(knowledge_base.plants)}"
    )

    print("\nAvailable plants:")

    for plant in knowledge_base.list_plants():
        print(f"- {plant}")

    print("\n----------------------------------------")
    print("Testing normalized lookup")
    print("----------------------------------------")

    result = knowledge_base.get_plant("NEEM TREE")

    if result:
        print("PASS - 'NEEM TREE' matched successfully")
    else:
        print("FAIL - Normalized lookup failed")

    print("\n----------------------------------------")
    print("Testing ecological retrieval")
    print("----------------------------------------")

    ecological_data = (
        knowledge_base.get_ecological_information(
            "Banyan"
        )
    )

    if ecological_data:
        print(
            "PASS - Ecological information retrieved"
        )
    else:
        print(
            "FAIL - Ecological information not retrieved"
        )

    print("\n----------------------------------------")
    print("Testing conservation retrieval")
    print("----------------------------------------")

    conservation_data = (
        knowledge_base.get_conservation_information(
            "Neem"
        )
    )

    if conservation_data:
        print(
            "PASS - Conservation information retrieved"
        )
    else:
        print(
            "FAIL - Conservation information not retrieved"
        )

    print("\n----------------------------------------")
    print("Testing AI-ready context")
    print("----------------------------------------")

    context = knowledge_base.build_context("Neem")

    if context:

        print("PASS - AI context successfully created")

        print("\nPreview:")
        print(context[:800])
        print("\n...")

    else:

        print(
            "FAIL - AI context could not be created"
        )

    print("\n========================================")
    print("       KNOWLEDGE BASE READY")
    print("========================================")