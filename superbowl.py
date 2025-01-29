from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SQUARES_FILE = "squares.json"

# Ensure squares.json exists with an empty dictionary if not found
if not os.path.exists(SQUARES_FILE):
    with open(SQUARES_FILE, "w") as f:
        json.dump({}, f)

def load_squares():
    """Load the current squares from the JSON file."""
    with open(SQUARES_FILE, "r") as f:
        return json.load(f)

def save_squares(squares):
    """Save the updated squares to the JSON file."""
    with open(SQUARES_FILE, "w") as f:
        json.dump(squares, f, indent=4)

@app.route("/")
def home():
    """Render the main page with squares data."""
    squares = load_squares()
    return render_template("index.html", squares=json.dumps(squares))

@app.route("/select", methods=["POST"])
def select_square():
    """Handle square selection."""
    squares = load_squares()
    data = request.json
    row, col = data["row"], data["col"]

    # Check if the square is already taken
    if f"{row},{col}" in squares:
        return jsonify({"error": "This square is already taken!"}), 400

    # Save the selected square
    squares[f"{row},{col}"] = data["name"]
    save_squares(squares)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
