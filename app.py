from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        n = int(request.form.get('n', 5))  # Default size is 5x5 if not specified
        return render_template('grid.html', size=n)
    return render_template('index.html')

@app.route('/validate_grid', methods=['POST'])
def validate_grid():
    cell_states = request.json.get('states')
    # Here, you can process the cell_states as needed
    print(cell_states)  # Example action
    return jsonify({"message": "Data received!"})

if __name__ == '__main__':
    app.run(debug=True)

