"""
Botanical AI Response Formatter.

This module converts the internal BotanicalAssistant result
into a clean, structured response that can be consumed by
the application layer.

Responsibilities:
- format AI results consistently
- expose plant identity
- expose question intent
- expose grounded status
- expose evidence/context
- provide user-facing response text
- provide safe error responses

The formatter does not generate new botanical facts.
It only organizes information returned by the grounded
botanical intelligence layer.
"""


class BotanicalResponseFormatter:
    """
    Format grounded botanical AI results into a
    consistent application-ready structure.
    """

    def __init__(self):
        """Initialize the response formatter."""
        pass

    # --------------------------------------------------
    # SUCCESS RESPONSE
    # --------------------------------------------------

    def format_success(self, result):
        """
        Format a successful BotanicalAssistant result.

        Expected result fields:
        - status
        - plant
        - question_type
        - answer
        - grounded
        - prompt
        - context
        """

        if not result:
            return self.format_error(
                "No AI result was provided."
            )

        return {
            "status": "success",
            "plant": result.get("plant"),
            "question_type": result.get(
                "question_type",
                "general"
            ),
            "answer": result.get(
                "answer",
                ""
            ),
            "grounded": result.get(
                "grounded",
                False
            ),
            "evidence_available": bool(
                result.get("context")
            ),
            "context": result.get(
                "context"
            )
        }

    # --------------------------------------------------
    # ERROR RESPONSE
    # --------------------------------------------------

    def format_error(self, message):
        """
        Create a safe and consistent error response.
        """

        return {
            "status": "error",
            "plant": None,
            "question_type": "unknown",
            "answer": message,
            "grounded": False,
            "evidence_available": False,
            "context": None
        }

    # --------------------------------------------------
    # NOT FOUND RESPONSE
    # --------------------------------------------------

    def format_not_found(self, result):
        """
        Format a plant-not-found response.
        """

        if not result:
            return self.format_error(
                "Plant could not be found."
            )

        return {
            "status": "not_found",
            "plant": result.get("plant"),
            "question_type": "unknown",
            "answer": result.get(
                "answer",
                "The requested plant was not found "
                "in the botanical knowledge base."
            ),
            "grounded": False,
            "evidence_available": False,
            "context": None
        }

    # --------------------------------------------------
    # GENERAL FORMATTER
    # --------------------------------------------------

    def format(self, result):
        """
        Automatically format a BotanicalAssistant result.

        This is the main method application code should use.
        """

        if not result:
            return self.format_error(
                "No response was generated."
            )

        status = result.get("status")

        if status == "success":
            return self.format_success(result)

        if status == "not_found":
            return self.format_not_found(result)

        return self.format_error(
            result.get(
                "answer",
                "Unable to generate a botanical response."
            )
        )

    # --------------------------------------------------
    # DISPLAY FORMAT
    # --------------------------------------------------

    def format_for_display(self, formatted_result):
        """
        Convert a structured response into clean
        human-readable text.

        This is useful for CLI or application display.
        """

        if not formatted_result:
            return "No response available."

        status = formatted_result.get("status")

        if status == "not_found":
            return (
                "Plant not found.\n\n"
                + formatted_result.get(
                    "answer",
                    "The requested plant was not found."
                )
            )

        if status == "error":
            return (
                "Unable to process the request.\n\n"
                + formatted_result.get(
                    "answer",
                    "An unknown error occurred."
                )
            )

        plant = formatted_result.get(
            "plant",
            "Unknown plant"
        )

        question_type = formatted_result.get(
            "question_type",
            "general"
        )

        grounded = formatted_result.get(
            "grounded",
            False
        )

        answer = formatted_result.get(
            "answer",
            ""
        )

        return (
            f"Plant: {plant}\n"
            f"Question type: {question_type}\n"
            f"Knowledge grounded: {grounded}\n\n"
            f"Answer:\n"
            f"{answer}"
        )


# ======================================================
# MODULE SELF-TEST
# ======================================================

if __name__ == "__main__":

    formatter = BotanicalResponseFormatter()

    print("=" * 40)
    print("   BOTANICAL RESPONSE FORMATTER")
    print("=" * 40)

    print()
    print("[TEST 1] Successful response")

    success_result = {
        "status": "success",
        "plant": "Neem",
        "question_type": "ecology",
        "answer": (
            "Neem contributes to local plant diversity."
        ),
        "grounded": True,
        "prompt": "Grounded botanical prompt",
        "context": "Verified Neem context"
    }

    formatted = formatter.format(
        success_result
    )

    assert formatted["status"] == "success"
    assert formatted["plant"] == "Neem"
    assert formatted["grounded"] is True
    assert formatted["evidence_available"] is True

    print("PASS - Successful response formatting")

    print()
    print("[TEST 2] Not-found response")

    not_found_result = {
        "status": "not_found",
        "plant": "XYZPlant",
        "answer": (
            "I could not find 'XYZPlant' "
            "in the botanical knowledge base."
        ),
        "grounded": False
    }

    formatted = formatter.format(
        not_found_result
    )

    assert formatted["status"] == "not_found"
    assert formatted["grounded"] is False
    assert formatted["evidence_available"] is False

    print("PASS - Not-found response formatting")

    print()
    print("[TEST 3] Error response")

    formatted = formatter.format(None)

    assert formatted["status"] == "error"
    assert formatted["grounded"] is False

    print("PASS - Error handling")

    print()
    print("[TEST 4] Display formatting")

    display = formatter.format_for_display(
        formatter.format(success_result)
    )

    assert "Neem" in display
    assert "ecology" in display
    assert "Knowledge grounded: True" in display

    print("PASS - Human-readable display formatting")

    print()
    print("=" * 40)
    print(" ALL RESPONSE FORMATTER TESTS PASSED")
    print("=" * 40)