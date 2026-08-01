import eel
import random
import math
import numpy as np
import time

eel.init('web')

WIDTH = 1000
HEIGHT = 1000

NUM_PREY = 120
NUM_PREDATORS = 15
NUM_FOOD = 250

# Prey Inputs: [fd, fa, pd, pa, nearest_prey_d, nearest_prey_a, flock_d, flock_a, bias] = 9
PREY_INPUTS = 9
# Pred Inputs: [pd, pa, nearest_pred_d, nearest_pred_a, bias] = 5
PRED_INPUTS = 5

HIDDEN_SIZE = 12
OUTPUT_SIZE = 2

def create_model(input_size):
    return {
        'W1': np.random.randn(input_size, HIDDEN_SIZE) * 0.1,
        'b1': np.zeros(HIDDEN_SIZE),
        'W2': np.random.randn(HIDDEN_SIZE, OUTPUT_SIZE) * 0.1,
        'b2': np.zeros(OUTPUT_SIZE)
    }

def mutate(model, mutation_rate=0.1):
    new_model = {}
    for k in model:
        mutation = np.random.randn(*model[k].shape) * mutation_rate
        new_model[k] = model[k] + mutation
    return new_model

def forward(model, x):
    z1 = np.dot(x, model['W1']) + model['b1']
    a1 = np.tanh(z1)
    z2 = np.dot(a1, model['W2']) + model['b2']
    return np.tanh(z2)

class Entity:
    def __init__(self, x, y, input_size, model=None):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 0.0
        self.angle = random.uniform(0, 2 * math.pi)
        self.energy = 1.0
        self.model = model if model else create_model(input_size)
        self.alive = True
        
    def move(self, thrust, turn, top_speed_accel, max_turn):
        self.angle += turn * max_turn
        self.vx += math.cos(self.angle) * thrust * top_speed_accel
        self.vy += math.sin(self.angle) * thrust * top_speed_accel
        
        self.vx *= 0.95
        self.vy *= 0.95
        self.speed = math.sqrt(self.vx**2 + self.vy**2)
        
        self.x = (self.x + self.vx) % WIDTH
        self.y = (self.y + self.vy) % HEIGHT

class Prey(Entity):
    def __init__(self, x, y, model=None):
        super().__init__(x, y, PREY_INPUTS, model)
        
    def update(self, nearest_food, nearest_predator, alive_prey):
        if not self.alive: return
        
        fd, fa = 1.0, 0.0
        if nearest_food:
            dx = nearest_food[0] - self.x
            dy = nearest_food[1] - self.y
            fd = math.sqrt(dx**2 + dy**2) / WIDTH
            fa = math.atan2(dy, dx) - self.angle
            
        pd, pa = 1.0, 0.0
        if nearest_predator:
            dx = nearest_predator.x - self.x
            dy = nearest_predator.y - self.y
            pd = math.sqrt(dx**2 + dy**2) / WIDTH
            pa = math.atan2(dy, dx) - self.angle
            
        # Flocking logic
        flock_x = 0
        flock_y = 0
        flock_count = 0
        nearest_pr_d = 1.0
        nearest_pr_a = 0.0
        
        min_d_sq = float('inf')
        
        for pr in alive_prey:
            if pr is self: continue
            dx = pr.x - self.x
            dy = pr.y - self.y
            d_sq = dx**2 + dy**2
            if d_sq < 25000: # Radius ~150 for flocking
                flock_x += pr.x
                flock_y += pr.y
                flock_count += 1
                if d_sq < min_d_sq:
                    min_d_sq = d_sq
                    nearest_pr_d = math.sqrt(d_sq) / WIDTH
                    nearest_pr_a = math.atan2(dy, dx) - self.angle
                    
        flock_d, flock_a = 1.0, 0.0
        if flock_count > 0:
            cx = (flock_x / flock_count) - self.x
            cy = (flock_y / flock_count) - self.y
            flock_d = math.sqrt(cx**2 + cy**2) / WIDTH
            flock_a = math.atan2(cy, cx) - self.angle

        inputs = np.array([fd, math.sin(fa), pd, math.sin(pa), nearest_pr_d, math.sin(nearest_pr_a), flock_d, math.sin(flock_a), 1.0])
        outputs = forward(self.model, inputs)
        
        thrust = (outputs[0] + 1) / 2.0
        turn = outputs[1]
        
        self.move(thrust, turn, 0.5, 0.25)
        self.energy -= 0.002 + (thrust * 0.001)
        if self.energy <= 0:
            self.alive = False

class Predator(Entity):
    def __init__(self, x, y, model=None):
        super().__init__(x, y, PRED_INPUTS, model)
        
    def update(self, nearest_prey, alive_predators):
        if not self.alive: return
        
        pd, pa = 1.0, 0.0
        if nearest_prey:
            dx = nearest_prey.x - self.x
            dy = nearest_prey.y - self.y
            pd = math.sqrt(dx**2 + dy**2) / WIDTH
            pa = math.atan2(dy, dx) - self.angle
            
        npd, npa = 1.0, 0.0
        min_d_sq = float('inf')
        for pr in alive_predators:
            if pr is self: continue
            dx = pr.x - self.x
            dy = pr.y - self.y
            d_sq = dx**2 + dy**2
            if d_sq < min_d_sq:
                min_d_sq = d_sq
                npd = math.sqrt(d_sq) / WIDTH
                npa = math.atan2(dy, dx) - self.angle
                
        inputs = np.array([pd, math.sin(pa), npd, math.sin(npa), 1.0])
        outputs = forward(self.model, inputs)
        
        thrust = (outputs[0] + 1) / 2.0
        turn = outputs[1]
        
        self.move(thrust, turn, 0.65, 0.15)
        self.energy -= 0.003 + (thrust * 0.0015)
        if self.energy <= 0:
            self.alive = False

class Ecosystem:
    def __init__(self):
        self.prey = [Prey(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_PREY)]
        self.predators = [Predator(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_PREDATORS)]
        self.food = [(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_FOOD)]
        self.ticks = 0

    def step(self):
        self.ticks += 1
        
        alive_prey = [p for p in self.prey if p.alive]
        alive_predators = [p for p in self.predators if p.alive]
        
        new_prey = []
        new_predators = []
        
        while len(self.food) < NUM_FOOD:
            self.food.append((random.uniform(0, WIDTH), random.uniform(0, HEIGHT)))

        # Update Prey
        for p in alive_prey:
            nf = min(self.food, key=lambda f: (f[0]-p.x)**2 + (f[1]-p.y)**2, default=None)
            np_pred = min(alive_predators, key=lambda pred: (pred.x-p.x)**2 + (pred.y-p.y)**2, default=None)
            
            p.update(nf, np_pred, alive_prey)
            
            if nf and (nf[0]-p.x)**2 + (nf[1]-p.y)**2 < 100:
                p.energy += 0.3
                self.food.remove(nf)
                self.food.append((random.uniform(0, WIDTH), random.uniform(0, HEIGHT)))
                
            if p.energy > 1.5:
                p.energy = 0.75
                child = Prey(p.x, p.y, mutate(p.model, 0.1))
                child.energy = 0.75
                new_prey.append(child)

        # Update Predators
        for p in alive_predators:
            np_prey = min(alive_prey, key=lambda prey: (prey.x-p.x)**2 + (prey.y-p.y)**2, default=None)
            
            p.update(np_prey, alive_predators)
            
            if np_prey and (np_prey.x-p.x)**2 + (np_prey.y-p.y)**2 < 200:
                p.energy += 0.8
                np_prey.alive = False
                alive_prey.remove(np_prey)
                
            if p.energy > 1.5:
                p.energy = 0.75
                child = Predator(p.x, p.y, mutate(p.model, 0.1))
                child.energy = 0.75
                new_predators.append(child)

        self.prey = [p for p in self.prey if p.alive] + new_prey
        self.predators = [p for p in self.predators if p.alive] + new_predators
        
        if len(self.prey) < 10:
            self.prey.extend([Prey(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(15)])
        if len(self.predators) == 0 and len(self.prey) > 30:
            self.predators.extend([Predator(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(2)])

eco = Ecosystem()

@eel.expose
def step_sim():
    eco.step()
    
    avg_prey_energy = sum(p.energy for p in eco.prey) / len(eco.prey) if eco.prey else 0
    avg_pred_energy = sum(p.energy for p in eco.predators) / len(eco.predators) if eco.predators else 0
    
    avg_prey_spd = sum(p.speed for p in eco.prey) / len(eco.prey) if eco.prey else 0
    avg_pred_spd = sum(p.speed for p in eco.predators) / len(eco.predators) if eco.predators else 0

    data = {
        'prey': [{'x': p.x, 'y': p.y, 'angle': p.angle, 'energy': p.energy} for p in eco.prey],
        'predators': [{'x': p.x, 'y': p.y, 'angle': p.angle, 'energy': p.energy} for p in eco.predators],
        'food': [{'x': f[0], 'y': f[1]} for f in eco.food],
        'stats': {
            'ticks': eco.ticks,
            'prey_count': len(eco.prey),
            'pred_count': len(eco.predators),
            'avg_prey_energy': avg_prey_energy,
            'avg_pred_energy': avg_pred_energy,
            'avg_prey_spd': avg_prey_spd,
            'avg_pred_spd': avg_pred_spd
        }
    }
    return data

@eel.expose
def init_sim():
    global eco
    eco = Ecosystem()
    return step_sim()

if __name__ == '__main__':
    eel.start('index.html', size=(1400, 1000), port=0)
