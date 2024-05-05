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
    if request.is_json:
        cell_states = request.get_json().get('states')
        print("Received cell states:", cell_states)  # 打印接收到的数据
        return jsonify({"message": "Data received!"})
    else:
        print("No JSON received")  # 如果没有接收到 JSON，打印提示
        return jsonify({"message": "No data received"}), 400

if __name__ == '__main__':
    app.run(debug=True)

