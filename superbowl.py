from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SQUARES_FILE = "squares.json"

# Ensure squares.json exists
if not os.path.exists(SQUARES_FILE):
    with open(SQUARES_FILE, "w") as f:
        json.dump({}, f)

def load_squares():
    with open(SQUARES_FILE, "r") as f:
        return json.load(f)

def save_squares(squares):
    with open(SQUARES_FILE, "w") as f:
        json.dump(squares, f, indent=4)

@app.route("/")
def home():
    squares = load_squares()
    return render_template("index.html", squares=json.dumps(squares))

@app.route("/select", methods=["POST"])
def select_square():
    squares = load_squares()
    data = request.json
    row, col = data["row"], data["col"]

    if f"{row},{col}" in squares:
        return jsonify({"error": f"This square is already taken by {squares[f'{row},{col}']}!"}), 400

    squares[f"{row},{col}"] = data["name"]
    save_squares(squares)
    
    return jsonify({"success": True, "name": data["name"]})

if __name__ == "__main__":
    app.run(debug=True)
