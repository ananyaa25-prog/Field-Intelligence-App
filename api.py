from flask import Flask, request, jsonify
import sys
from pathlib import Path

# Add the ai folder to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent
AI_FOLDER = PROJECT_ROOT / "ai"

sys.path.insert(0, str(AI_FOLDER))

from botanical_assistant import BotanicalAssistant


app = Flask(__name__)

assistant = BotanicalAssistant()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Field Intelligence Botanical API is running."
    })


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "answer": "No request data received."
            }), 400

        plant_name = data.get("plant")
        question = data.get("question")

        if not plant_name:
            return jsonify({
                "status": "error",
                "answer": "Plant name is required."
            }), 400

        if not question:
            return jsonify({
                "status": "error",
                "answer": "Question is required."
            }), 400

        result = assistant.answer(
            plant_name,
            question
        )

        return jsonify(result)

    except Exception as error:
        return jsonify({
            "status": "error",
            "answer": str(error),
            "grounded": False
        }), 500


if __name__ == "__main__":
    print("=" * 50)
    print("       FIELD INTELLIGENCE BOTANICAL API")
    print("=" * 50)
    print()
    print("API running at:")
    print("http://127.0.0.1:5000")
    print()
    print("POST endpoint:")
    print("http://127.0.0.1:5000/ask")
    print()
    print("Press CTRL+C to stop the server.")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )