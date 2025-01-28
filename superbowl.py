from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Define grid size
gridSize = 10
grid = [[None for _ in range(gridSize)] for _ in range(gridSize)]

# Ensure directory and file exist
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            for _ in range(gridSize):
                f.write(','.join(['' for _ in range(gridSize)]) + '\n')

# Define file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
saved_data_dir = os.path.join(current_dir, 'saved_data')
grid_file_path = os.path.join(saved_data_dir, 'grid.txt')

# Ensure folder and file exist
ensure_directory_exists(saved_data_dir)
ensure_file_exists(grid_file_path)

# Load grid from the file
def load_grid():
    with open(grid_file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            grid[i] = [cell if cell else None for cell in line.strip().split(',')]

# Save grid to the file
def save_grid_to_file():
    with open(grid_file_path, 'w') as f:
        for row in grid:
            f.write(','.join([cell if cell else '' for cell in row]) + '\n')

# Route to render the home page
@app.route('/')
def home():
    load_grid()
    return render_template('index.html', grid=grid)

# Save grid when user selects a square
@app.route('/save-grid', methods=['POST'])
def save_grid():
    data = request.json
    row, col, name = data['row'], data['col'], data['name']
    if grid[row][col]:  # Check if the square is already claimed
        return jsonify({'message': 'This square is already claimed by someone else!'}), 400

    grid[row][col] = name
    save_grid_to_file()  # Save updated grid to file
    return jsonify({'message': 'Square claimed successfully! Please send payment to PayPal: your-email@example.com or Venmo: @your-venmo-username.'})

if __name__ == '__main__':
    app.run(debug=True)
