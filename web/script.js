const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

const btnInit = document.getElementById('btnInit');
const btnToggle = document.getElementById('btnToggle');

const statPrey = document.getElementById('statPrey');
const statPred = document.getElementById('statPred');
const statTicks = document.getElementById('statTicks');

let running = true;
let chartPop = null;
let chartEnergy = null;
let chartSpeed = null;

function createChart(canvasId, title1, title2) {
    const ctxChart = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctxChart, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: title1,
                    data: [],
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: true,
                    tension: 0.3
                },
                {
                    label: title2,
                    data: [],
                    borderColor: '#f43f5e',
                    backgroundColor: 'rgba(244, 63, 94, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: true,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { beginAtZero: true }
            }
        }
    });
}

function initCharts() {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Fira Code', monospace";

    if (chartPop) chartPop.destroy();
    if (chartEnergy) chartEnergy.destroy();
    if (chartSpeed) chartSpeed.destroy();

    chartPop = createChart('populationChart', 'Prey Pop', 'Pred Pop');
    chartEnergy = createChart('energyChart', 'Prey Energy', 'Pred Energy');
    chartSpeed = createChart('speedChart', 'Prey Speed', 'Pred Speed');
}

function updateChart(chart, val1, val2) {
    chart.data.labels.push("");
    chart.data.datasets[0].data.push(val1);
    chart.data.datasets[1].data.push(val2);

    if (chart.data.labels.length > 100) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }
    chart.update();
}

function updateCharts(data) {
    if (data.stats.ticks % 10 === 0) {
        updateChart(chartPop, data.stats.prey_count, data.stats.pred_count);
        updateChart(chartEnergy, data.stats.avg_prey_energy, data.stats.avg_pred_energy);
        updateChart(chartSpeed, data.stats.avg_prey_spd, data.stats.avg_pred_spd);
    }
}

async function initSimulation() {
    running = false;
    canvas.width = 1000;
    canvas.height = 1000;
    
    // Fill canvas initially
    ctx.fillStyle = '#020617';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    initCharts();
    
    const data = await eel.init_sim()();
    draw(data);
    
    running = true;
    btnToggle.textContent = "Pause";
    loop();
}

function drawAgent(x, y, angle, energy, type) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    
    ctx.beginPath();
    if (type === 'prey') {
        ctx.moveTo(12, 0);
        ctx.lineTo(-6, -5);
        ctx.lineTo(-6, 5);
        ctx.fillStyle = `rgba(56, 189, 248, ${Math.min(1.0, Math.max(0.2, energy))})`;
        ctx.strokeStyle = '#38bdf8';
    } else {
        ctx.moveTo(20, 0);
        ctx.lineTo(-10, -10);
        ctx.lineTo(-10, 10);
        ctx.fillStyle = `rgba(244, 63, 94, ${Math.min(1.0, Math.max(0.2, energy))})`;
        ctx.strokeStyle = '#f43f5e';
    }
    
    ctx.closePath();
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.restore();
}

function draw(data) {
    // Fading trail effect for fluid motion
    ctx.fillStyle = 'rgba(2, 6, 23, 0.3)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#22c55e';
    data.food.forEach(f => {
        ctx.beginPath();
        ctx.arc(f.x, f.y, 3, 0, Math.PI*2);
        ctx.fill();
    });
    
    data.prey.forEach(p => drawAgent(p.x, p.y, p.angle, p.energy, 'prey'));
    data.predators.forEach(p => drawAgent(p.x, p.y, p.angle, p.energy, 'predator'));
    
    statPrey.textContent = data.stats.prey_count;
    statPred.textContent = data.stats.pred_count;
    statTicks.textContent = data.stats.ticks;
}

async function loop() {
    if (!running) return;
    const data = await eel.step_sim()();
    draw(data);
    updateCharts(data);
    requestAnimationFrame(loop);
}

btnInit.addEventListener('click', initSimulation);
btnToggle.addEventListener('click', () => {
    running = !running;
    btnToggle.textContent = running ? "Pause" : "Resume";
    if (running) loop();
});

window.onload = () => setTimeout(initSimulation, 300);
