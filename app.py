from flask import Flask, render_template, request, jsonify
import numpy as np
import random
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


def initialize_q_values(n, num_actions):
    return np.zeros((n, n, num_actions))

def get_reward(state, grid):
    if grid[state] == 'end':
        return 100  # Reward for reaching the end
    elif grid[state] == 'obstacle':
        return 0  # No reward or penalty since it's impassable
    elif grid[state] == 'penalty':
        return -10  # Penalty for penalized state
    else:
        return -1  # Small penalty for each move

def is_terminal(state, grid):
    return grid[state] in ['end', 'obstacle']

def is_obstacle(state, grid):
    return grid[state] == 'obstacle'

def q_learning(grid, n, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    num_actions = 4  # up, down, left, right
    q_values = initialize_q_values(n, num_actions)
    actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # left, right, up, down

    for _ in range(episodes):
        state = (random.randint(0, n-1), random.randint(0, n-1))
        while not is_terminal(state, grid):
            # Explore or exploit
            if random.random() < epsilon:
                action_index = random.randint(0, num_actions - 1)
            else:
                action_index = np.argmax(q_values[state])

            next_state = (state[0] + actions[action_index][0], state[1] + actions[action_index][1])
            
            # Stay in grid bounds and avoid obstacles
            if 0 <= next_state[0] < n and 0 <= next_state[1] < n and not is_obstacle(next_state, grid):
                reward = get_reward(next_state, grid)
                next_max = np.max(q_values[next_state])
                q_values[state + (action_index,)] += alpha * (reward + gamma * next_max - q_values[state + (action_index,)])
                state = next_state
            else:
                # Update for staying in the same place if next state is an obstacle or out of bounds
                q_values[state + (action_index,)] += alpha * (get_reward(state, grid) + gamma * np.max(q_values[state]) - q_values[state + (action_index,)])

    policy = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            policy[i, j] = np.argmax(q_values[i, j])

    return q_values, policy

@app.route('/start-q-learning', methods=['POST'])
def start_q_learning():
    n = int(request.form.get('n', 5))  # Grid size
    cell_states = request.get_json().get('states', [])  # Cell states

    # Convert states to a grid
    grid = np.array(cell_states).reshape(n, n)

    # Perform Q-learning
    q_values, policy = q_learning(grid, n)

    # Send back the learned Q-values and policy
    return jsonify({
        'q_values': q_values.tolist(),
        'policy': policy.tolist()
    })





if __name__ == '__main__':
    app.run(debug=True)

