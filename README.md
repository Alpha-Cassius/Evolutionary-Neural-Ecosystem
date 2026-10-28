<div align="center">

<img src="https://iso.500px.com/wp-content/uploads/2015/02/parting_cover.jpeg" width="700" alt="School of fish underwater representing evolutionary neural ecosystem" style="border-radius: 15px;" />

<br/>
<br/>

<h1>Evolutionary Neural Ecosystem </h1>

**An advanced, interactive, real-time Machine Learning simulation where Predators (sharks) and Prey (fish) evolve inside a continuous 2D physics engine.**

<p>
<a href="https://github.com/alpha-cassius"><img src="https://img.shields.io/badge/AUTHOR-Vaibhav_Pandey-8a2be2?style=for-the-badge&amp;labelColor=0d1117" alt="AUTHOR" /></a> 
<a href="https://github.com/alpha-cassius?tab=repositories"><img src="https://img.shields.io/badge/OPEN_SOURCE-00d2ff?style=for-the-badge&amp;labelColor=0d1117" alt="OPEN SOURCE" /></a> 
<img src="https://img.shields.io/badge/AI-NEURAL_NETWORKS-34d399?style=for-the-badge&amp;labelColor=0d1117" alt="AI NEURAL NETWORKS" />
</p>

<p><b>Exploring the intersection of Genetic Algorithms, Neural Networks, and Artificial Life.</b></p>

---

</div>

## ✨ About The Project

This simulation challenges AI agents to learn complex social behaviors—like Boids flocking and solitary hunting—organically over time. Instead of relying on pre-programmed rules, the agents must survive, eat, and reproduce. Through the pressures of natural selection and continuous evolution, raw matrix math transforms into life-like biological behaviors.

<br/>

## 🚀 Architectural Highlights

<table width="100%">
<tr>
<td width="50%" valign="top">
  <h3>🧠 Zero-Dependency NNs</h3>
  <p>The "brains" of every single agent are built entirely from scratch using raw matrix math in <code>numpy</code> (no PyTorch/TensorFlow). Uses a multi-layer perceptron (MLP) with <code>tanh</code> activation for smooth steering and acceleration.</p>
</td>
<td width="50%" valign="top">
  <h3>🧬 Continuous Evolution</h3>
  <p>Instead of rigid "Generation" resets, this uses a <b>Continuous Evolution</b> model. Agents expend energy to move. If they eat enough to pass a threshold, they instantly undergo mitosis, passing down slightly mutated neural weights.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
  <h3>🐟 Machine-Learned "Boids"</h3>
  <p>Prey are fed environmental inputs inspired by Craig Reynolds' Boids model (Cohesion & Separation). Through evolutionary pressure from predators, they naturally learn to school together to survive.</p>
</td>
<td width="50%" valign="top">
  <h3>🌊 Continuous Physics Engine</h3>
  <p>Agents exist in a continuous 2D plane (not a grid). The engine calculates angular velocity, forward thrust, inertial drag, and biological limits (e.g., Predators are faster but turn slower than Prey).</p>
</td>
</tr>
</table>

### 📊 Advanced Analytical Dashboard
The Python backend is bridged to a modern web frontend via `Eel`. A real-time dashboard uses `Chart.js` to plot live data streams:
*   **Population Tracker:** Watch the predator-prey balance naturally ebb and flow in a classic Lotka-Volterra cycle.
*   **Average Energy:** Monitor the metabolic health of both species.
*   **Average Speed:** Observe evolutionary selection in real-time as the ecosystem selects for faster, more efficient swimmers.

<br/>

## 🔬 Deep Dive: The Agent Senses

Both species are governed by Neural Networks with a Hidden Layer size of `12`, but their input senses differ strictly based on their ecological niche. Both networks output exactly 2 values: **Thrust** (0 to 1) and **Turn Rate** (-1 to 1).

<table width="100%">
<tr>
<td width="50%" valign="top">
  <h3>🟢 Prey Network (9 Inputs)</h3>
  <i>Prey are gatherers. They eat stationary food and flee predators.</i>
  <ol>
    <li>Distance to nearest Food</li>
    <li>Angle to nearest Food</li>
    <li>Distance to nearest Predator</li>
    <li>Angle to nearest Predator</li>
    <li>Distance to nearest Prey <i>(Separation)</i></li>
    <li>Angle to nearest Prey <i>(Separation)</i></li>
    <li>Distance to Flock Center <i>(Cohesion)</i></li>
    <li>Angle to Flock Center <i>(Cohesion)</i></li>
    <li>Bias Unit <i>(Always 1.0)</i></li>
  </ol>
</td>
<td width="50%" valign="top">
  <h3>🔴 Predator Network (5 Inputs)</h3>
  <i>Predators are apex hunters. They eat moving Prey and avoid competing.</i>
  <ol>
    <li>Distance to nearest Prey</li>
    <li>Angle to nearest Prey</li>
    <li>Distance to nearest Predator <i>(Territoriality)</i></li>
    <li>Angle to nearest Predator <i>(Territoriality)</i></li>
    <li>Bias Unit <i>(Always 1.0)</i></li>
  </ol>
  <br/><br/>
</td>
</tr>
</table>

<br/>

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend & Physics** | Python 3.x | Core simulation loop and 2D kinematic physics engine. |
| **AI Math** | NumPy | Neural Network matrix multiplication and weight initialization. |
| **Bridge** | Eel | Lightweight local web server & bi-directional WebSocket connection. |
| **Rendering** | HTML5 Canvas / JS | High-performance visual rendering of the continuous 2D space. |
| **Data Viz** | Chart.js | Dynamic, real-time data visualization on the dashboard. |

<br/>

## 🎮 Installation and Usage

To run the simulation locally on your machine and watch evolution happen in real-time:

1. **Ensure Python is installed** (Python 3.8+ recommended).
2. **Clone the repository** and navigate to the project folder.
3. **Install the dependencies**:
   ```bash
   pip install eel numpy

```

4. **Launch the ecosystem**:
```bash
python main.py

```


5. A Google Chrome or Microsoft Edge window will launch automatically.
6. **Watch them learn!** The initial agents will be completely uncoordinated. Over thousands of ticks, you will watch them evolve to swim smoothly, hunt efficiently, and school together!

> *Note: If the simulation slows down, you can reduce the `NUM_PREY` and `NUM_FOOD` constants in `main.py`.*

---

## 🤝 Let's Connect






Made with 💖 and ☕ by Vaibhav Pandey
