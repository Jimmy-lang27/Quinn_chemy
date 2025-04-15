from flask import Flask, request, render_template, jsonify
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import threading

app = Flask(__name__)

# Reaction database with temperature and pressure conditions
Reaction_database = {
    ("H2", "O2"): {"product": "H2O", "temp_needed": 500, "pressure_needed": 2},
    ("C", "O2"): {"product": "CO2", "temp_needed": 300, "pressure_needed": 1},
    ("C", "H2"): {"product": "CH4", "temp_needed": 600, "pressure_needed": 2},
    ("Fe", "O2"): {"product": "Fe2O3", "temp_needed": 700, "pressure_needed": 3},
    ("N2", "H2"): {"product": "NH3", "temp_needed": 400, "pressure_needed": 5},
    ("Na", "Cl2"): {"product": "NaCl", "temp_needed": 200, "pressure_needed": 1},
    ("Ca", "O2"): {"product": "CaO", "temp_needed": 800, "pressure_needed": 4},
    ("Mg", "H2"): {"product": "MgH2", "temp_needed": 500, "pressure_needed": 3},
    ("Al", "Br2"): {"product": "AlBr3", "temp_needed": 600, "pressure_needed": 2},
    ("Zn", "S"): {"product": "ZnS", "temp_needed": 700, "pressure_needed": 1}
}

def get_reaction(reactant1, reactant2):
    reactants1 = (reactant1, reactant2)
    reactants2 = (reactant2, reactant1)
    reaction = Reaction_database.get(reactants1) or Reaction_database.get(reactants2)
    return reaction if reaction else {"product": "Unknown", "temp_needed": None, "pressure_needed": None}

@app.route('/')
def home():
    return "Welcome to Quinn Chemy!"

@app.route('/predict', methods=['POST'])
def predict_reaction():
    data = request.json
    reactant1 = data["reactant1"]
    reactant2 = data["reactant2"]
    reaction = get_reaction(reactant1, reactant2)
    return jsonify(reaction)

def simulate_reaction(reactant1, reactant2, product):
    fig, ax = plt.subplots()
    molecules = {reactant1: "blue", reactant2: "red", product: "purple"}
    particles = [{"x": random.uniform(1, 9), "y": random.uniform(1, 9), "type": reactant1} for _ in range(5)] + \
                [{"x": random.uniform(1, 9), "y": random.uniform(1, 9), "type": reactant2} for _ in range(5)]
    
    def update(frame):
        if frame > 30:
            for p in particles:
                p["type"] = product
        ax.clear()
        ax.scatter([p["x"] for p in particles], [p["y"] for p in particles], c=[molecules[p["type"]] for p in particles], s=200)
    
    ani = animation.FuncAnimation(fig, update, frames=60, interval=200)
    plt.show()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


    app.run(debug=True)
