# Evolutionary Neural Ecosystem 🦈🐟

An advanced, interactive, real-time Machine Learning simulation where Predators (sharks) and Prey (fish) evolve inside a continuous 2D physics engine. 

This project explores the intersection of **Genetic Algorithms**, **Neural Networks**, and **Artificial Life**, challenging agents to learn complex social behaviors like Boids flocking and solitary hunting organically over time.

---

## 🚀 Key Features & Architectural Highlights

### 1. Zero-Dependency Neural Networks (NumPy Only)
Rather than relying on heavy frameworks like PyTorch or TensorFlow, the "brains" of every single agent in this simulation are built entirely from scratch using raw matrix math in `numpy`. 
- **Feed-Forward Architecture**: A simple but effective multi-layer perceptron (MLP). 
- **Activation Functions**: Uses `tanh` to map outputs between `-1` and `1`, allowing agents to steer left/right and accelerate/brake smoothly.
- **Fast Execution**: NumPy vectorization allows hundreds of independent neural networks to be evaluated simultaneously in real-time.

### 2. Continuous Organic Evolution (Genetic Algorithm)
Most ML simulations use rigid "Generation" resets where the entire population dies, the fittest are selected, and the simulation restarts. This project uses a **Continuous Evolution** model:
- Agents expend **Energy** to move, turn, and simply exist (baseline metabolic drain).
- When agents consume their respective food source, they gain Energy.
- **Reproduction**: If an agent is successful enough to push its Energy past a critical threshold (`1.5`), it instantly undergoes mitosis. It splits its energy with a new offspring, passing down its neural weights with a slight gaussian mutation applied.
- This creates an organic ecosystem where species adapt dynamically in real-time. 

### 3. Machine-Learned "Boids" Flocking
The Prey agents are capable of evolving complex schooling behaviors to evade predators. They are fed specific environmental inputs inspired by Craig Reynolds' Boids model:
- **Cohesion**: Prey calculate the "Center of Mass" of all neighboring prey within a certain radius. They can use this input to learn to steer towards the flock.
- **Separation**: Prey sense the exact distance and angle of their closest neighbor, allowing them to learn not to collide.
- Through evolutionary pressure (Predators eating isolated prey), the prey naturally learn to school together!

### 4. Continuous Physics Engine
The environment is not a rigid grid (like cellular automata or the classic Wa-Tor model). Agents exist in a continuous 2D plane equipped with:
- **Kinematics**: Angular velocity, forward thrust, and inertial drag/friction.
- **Varying Biological Limits**: Predators have higher top speeds but slower turn rates. Prey are highly agile but have lower top speeds. 

### 5. Advanced Analytical Dashboard
The backend is bridged to a modern web frontend via `Eel`. The dashboard uses `Chart.js` to plot live data streams from the Python backend:
- **Population Tracker**: Watch the predator-prey balance naturally ebb and flow in a classic Lotka-Volterra cycle.
- **Average Energy**: Monitor the metabolic health of both species.
- **Average Speed**: Observe evolutionary selection in real-time as the ecosystem selects for faster and more efficient swimmers.

---

## 🧠 Deep Dive: The Agent Senses

Both species are governed by Neural Networks with a Hidden Layer size of `12`, but their input senses differ based on their ecological niche.

### Prey Neural Network (9 Inputs)
Prey are the gatherers. They eat stationary green "Food" dots and flee from Predators.
1. `Distance to nearest Food`
2. `Angle to nearest Food`
3. `Distance to nearest Predator`
4. `Angle to nearest Predator`
5. `Distance to nearest Prey (Separation)`
6. `Angle to nearest Prey (Separation)`
7. `Distance to Flock Center of Mass (Cohesion)`
8. `Angle to Flock Center of Mass (Cohesion)`
9. `Bias Unit` (Always 1.0)

### Predator Neural Network (5 Inputs)
Predators are apex hunters. They eat moving Prey. They have senses allowing them to detect other predators so they can learn to hunt solitarily and avoid competing for the same meal.
1. `Distance to nearest Prey`
2. `Angle to nearest Prey`
3. `Distance to nearest Predator (Territoriality)`
4. `Angle to nearest Predator (Territoriality)`
5. `Bias Unit` (Always 1.0)

Both networks output exactly 2 values:
- `Thrust`: Mapped from 0 to 1, determining forward acceleration.
- `Turn Rate`: Mapped from -1 to 1, determining angular velocity (steering left or right).

---

## 🛠️ Tech Stack

- **Python 3.x**: Core simulation loop and physics engine.
- **NumPy**: Neural Network matrix multiplication and weight initialization.
- **Eel**: A lightweight Python library for hosting the local web server and establishing a bi-directional WebSocket connection between Python and JS.
- **HTML5 Canvas & JavaScript**: High-performance rendering of the continuous 2D space.
- **Chart.js**: Dynamic, real-time data visualization.

---

## 🎮 Installation and Usage

To run the simulation locally on your machine:

1. **Clone the repository** or download the project files.
2. **Ensure Python is installed** (Python 3.8+ recommended).
3. **Install the dependencies**:
   ```bash
   pip install eel numpy
   ```
4. **Launch the ecosystem**:
   ```bash
   python main.py
   ```
5. A Google Chrome or Microsoft Edge window will automatically launch. 
6. **Watch them learn!** The initial agents will be completely uncoordinated. Over thousands of ticks, you will watch them evolve to swim smoothly, hunt efficiently, and school together!

*(Note: If the simulation slows down, you can reduce the `NUM_PREY` and `NUM_FOOD` constants in `main.py`.)*

---

Made with 💖 and ☕ by Vaibhav Pandey!
