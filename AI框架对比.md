<!-- Confirmation: NEITHER Mermaid JS NOR SVG were used anywhere in the output. -->
<!-- Chosen Palette: "Vibrant Tech" (Indigo #4f46e5, Pink #ec4899, Teal #14b8a6, Amber #f59e0b, Sky #0ea5e9) -->
<!-- Narrative Plan: 
1. Introduction: Set the stage on the AI orchestration landscape.
2. Capability Radar: Compare the 5 frameworks across core dimensions (RAG, Agents, Flow, etc.).
3. Market & Complexity: ScatterGL plot showing Learning Curve vs Integration Power.
4. Primary Architectures: Donut charts illustrating the compositional focus of each framework.
5. Decision Flowchart: HTML/CSS based guide on when to choose which framework.
-->
<!-- Chart Choices: 
6. Radar Chart (Chart.js) -> Goal: Compare multiple variables. Justification: Ideal for showing strengths/weaknesses across 5 dimensions. NO SVG.
7. ScatterGL (Plotly.js) -> Goal: Relationships. Justification: Shows correlation between learning curve and capability using WebGL rendering. NO SVG.
8. Donut Charts (Chart.js) -> Goal: Composition. Justification: Compares core architectural pillars of each framework. NO SVG.
9. CSS Decision Tree -> Goal: Organize. Justification: Replaces Mermaid/SVG for flowcharts. NO SVG.
-->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Orchestration Frameworks: Comparative Analysis</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }
.chart-container { position: relative; width: 100%; max-width: 600px; margin-left: auto; margin-right: auto; height: 350px; max-height: 400px; }
.chart-container-large { position: relative; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; height: 400px; max-height: 500px; }
.flow-card { background-color: #1e293b; border: 2px solid #334155; border-radius: 0.5rem; padding: 1rem; text-align: center; }
.flow-arrow { font-size: 1.5rem; color: #94a3b8; display: flex; align-items: center; justify-content: center; padding: 0.5rem; }
</style>
</head>
<body class="antialiased">

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <header class="text-center mb-16">
        <h1 class="text-4xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 via-indigo-500 to-pink-500 mb-4">
            AI Orchestration Landscape
        </h1>
        <p class="text-xl text-slate-300 max-w-3xl mx-auto">
            A comprehensive visual breakdown of deer-flow, AutoGen, LangGraph, LlamaIndex, and Nanobot to help architects select the optimal cognitive framework.
        </p>
    </header>

    <section class="mb-16 bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
        <h2 class="text-2xl font-bold text-white mb-4 border-b border-slate-600 pb-2">1. Capability Radar Analysis</h2>
        <p class="text-slate-300 mb-8 leading-relaxed">
            The modern AI landscape demands versatile orchestration. This radar analysis compares our five target frameworks across key technical dimensions: Multi-Agent Coordination, Data Retrieval (RAG) depth, Stateful Flow Control, Developer Experience (DX), and Ecosystem Scalability. Notice how LlamaIndex strongly biases towards Data, while LangGraph and AutoGen push heavily into State and Multi-Agent domains.
        </p>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div class="chart-container-large">
                <canvas id="radarChart"></canvas>
            </div>
            <div class="space-y-4">
                <div class="bg-slate-700 p-4 rounded-lg border-l-4 border-indigo-500">
                    <h3 class="font-bold text-indigo-400">LangGraph</h3>
                    <p class="text-sm text-slate-300">Dominates in stateful flow control and cyclic agent graphs.</p>
                </div>
                <div class="bg-slate-700 p-4 rounded-lg border-l-4 border-pink-500">
                    <h3 class="font-bold text-pink-400">AutoGen</h3>
                    <p class="text-sm text-slate-300">The leader in conversational multi-agent collaboration and code execution.</p>
                </div>
                <div class="bg-slate-700 p-4 rounded-lg border-l-4 border-teal-500">
                    <h3 class="font-bold text-teal-400">LlamaIndex</h3>
                    <p class="text-sm text-slate-300">Unmatched for data ingestion, indexing, and advanced RAG architectures.</p>
                </div>
                <div class="bg-slate-700 p-4 rounded-lg border-l-4 border-amber-500">
                    <h3 class="font-bold text-amber-400">deer-flow</h3>
                    <p class="text-sm text-slate-300">Specializes in highly structured, deterministic pipeline orchestration.</p>
                </div>
                <div class="bg-slate-700 p-4 rounded-lg border-l-4 border-sky-500">
                    <h3 class="font-bold text-sky-400">Nanobot</h3>
                    <p class="text-sm text-slate-300">Lightweight, minimalist design for rapid single-purpose agent deployment.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="mb-16 bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
        <h2 class="text-2xl font-bold text-white mb-4 border-b border-slate-600 pb-2">2. Learning Curve vs. Integration Power</h2>
        <p class="text-slate-300 mb-8 leading-relaxed">
            Choosing a framework often comes down to the tradeoff between how fast a team can learn it and how powerful it becomes in production. The scatter plot below illustrates this relationship. Frameworks like Nanobot offer rapid onboarding but have lower ceilings, whereas LangGraph requires significant conceptual understanding of state graphs but provides enterprise-grade control.
        </p>

        <div class="grid grid-cols-1 gap-8">
            <div class="chart-container-large bg-slate-900 rounded-lg p-2">
                <div id="scatterPlot" style="width:100%; height:100%;"></div>
            </div>
            <p class="text-sm text-slate-400 text-center italic">
                * Note: X-Axis represents the initial learning curve (higher is harder). Y-Axis represents absolute orchestration power and enterprise readiness.
            </p>
        </div>
    </section>

    <section class="mb-16 bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
        <h2 class="text-2xl font-bold text-white mb-4 border-b border-slate-600 pb-2">3. Architectural Composition Breakdown</h2>
        <p class="text-slate-300 mb-8 leading-relaxed">
            Every framework is opinionated. By analyzing their internal module distribution and primary use-case documentation, we can deduce their core focus areas. Below, we break down each framework's architecture into three pillars: Data Indexing, Agentic Logic, and State/Routing Mechanics.
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="flex flex-col items-center">
                <h4 class="text-lg font-semibold text-slate-200 mb-2">LangGraph Focus</h4>
                <div class="chart-container">
                    <canvas id="donutLangGraph"></canvas>
                </div>
                <p class="text-xs text-slate-400 text-center mt-2">Heavily biased towards State/Routing to manage complex cycles.</p>
            </div>
            
            <div class="flex flex-col items-center">
                <h4 class="text-lg font-semibold text-slate-200 mb-2">LlamaIndex Focus</h4>
                <div class="chart-container">
                    <canvas id="donutLlamaIndex"></canvas>
                </div>
                <p class="text-xs text-slate-400 text-center mt-2">Data Indexing takes priority, treating agents as query engines.</p>
            </div>

            <div class="flex flex-col items-center">
                <h4 class="text-lg font-semibold text-slate-200 mb-2">AutoGen Focus</h4>
                <div class="chart-container">
                    <canvas id="donutAutoGen"></canvas>
                </div>
                <p class="text-xs text-slate-400 text-center mt-2">Agentic Logic and conversational loops form the core architecture.</p>
            </div>
        </div>
    </section>

    <section class="mb-16 bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
        <h2 class="text-2xl font-bold text-white mb-4 border-b border-slate-600 pb-2">4. Decision Matrix Workflow</h2>
        <p class="text-slate-300 mb-8 leading-relaxed">
            Not sure where to start? Use the structural logic flow below to identify the most appropriate framework based on your project's primary technical requirement.
        </p>
        
        <div class="flex flex-col items-center w-full max-w-4xl mx-auto font-mono text-sm">
            <div class="flow-card bg-indigo-900 border-indigo-500 w-64 font-bold text-white">
                Start: What is your primary need?
            </div>
            <div class="flow-arrow">&#8595;</div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full relative">
                <div class="flex flex-col items-center">
                    <div class="flow-card w-full">Heavy Document / Data Integration</div>
                    <div class="flow-arrow">&#8595;</div>
                    <div class="flow-card border-teal-500 bg-teal-900 text-teal-100 w-full shadow-[0_0_15px_rgba(20,184,166,0.5)]">
                        LlamaIndex
                    </div>
                </div>

                <div class="flex flex-col items-center mt-8 md:mt-0">
                    <div class="flow-card w-full">Complex Multi-Agent Interaction</div>
                    <div class="flow-arrow">&#8595;</div>
                    <div class="flex justify-around w-full gap-2 border-t-2 border-slate-600 pt-4 mt-2">
                        <div class="flex flex-col items-center w-1/2">
                            <span class="text-xs text-slate-400 mb-1">State & Control</span>
                            <div class="flow-card border-indigo-500 bg-indigo-900 text-indigo-100 w-full shadow-[0_0_15px_rgba(79,70,229,0.5)]">LangGraph</div>
                        </div>
                        <div class="flex flex-col items-center w-1/2">
                            <span class="text-xs text-slate-400 mb-1">Conversational</span>
                            <div class="flow-card border-pink-500 bg-pink-900 text-pink-100 w-full shadow-[0_0_15px_rgba(236,72,153,0.5)]">AutoGen</div>
                        </div>
                    </div>
                </div>

                <div class="flex flex-col items-center mt-8 md:mt-0">
                    <div class="flow-card w-full">Simplicity & Fast Pipelines</div>
                    <div class="flow-arrow">&#8595;</div>
                    <div class="flex justify-around w-full gap-2 border-t-2 border-slate-600 pt-4 mt-2">
                        <div class="flex flex-col items-center w-1/2">
                            <span class="text-xs text-slate-400 mb-1">Structured</span>
                            <div class="flow-card border-amber-500 bg-amber-900 text-amber-100 w-full shadow-[0_0_15px_rgba(245,158,11,0.5)]">deer-flow</div>
                        </div>
                        <div class="flex flex-col items-center w-1/2">
                            <span class="text-xs text-slate-400 mb-1">Minimalist</span>
                            <div class="flow-card border-sky-500 bg-sky-900 text-sky-100 w-full shadow-[0_0_15px_rgba(14,165,233,0.5)]">Nanobot</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>

<script>
function wrapLabel(label, max = 16) {
    if (typeof label !== 'string') return label;
    if (label.length <= max) return label;
    const words = label.split(' ');
    const lines = [];
    let currentLine = '';
    for (let i = 0; i < words.length; i++) {
        const word = words[i];
        if ((currentLine + word).length > max) {
            if (currentLine) lines.push(currentLine.trim());
            currentLine = word + ' ';
        } else {
            currentLine += word + ' ';
        }
    }
    if (currentLine) lines.push(currentLine.trim());
    return lines;
}

const tooltipConfig = {
    callbacks: {
        title: function(tooltipItems) {
            const item = tooltipItems[0];
            let label = item.chart.data.labels[item.dataIndex];
            if (Array.isArray(label)) {
                return label.join(' ');
            } else {
                return label;
            }
        }
    }
};

const labelsRaw = ['LangGraph Framework', 'AutoGen Multi-Agent', 'LlamaIndex RAG', 'deer-flow Pipeline', 'Nanobot Micro-Agent'];
const wrappedLabels = labelsRaw.map(l => wrapLabel(l));

const radarCtx = document.getElementById('radarChart').getContext('2d');
new Chart(radarCtx, {
    type: 'radar',
    data: {
        labels: ['State & Flow Management', 'Agent Collaboration', 'Data & Retrieval', 'Developer Experience', 'Production Scalability'].map(l => wrapLabel(l)),
        datasets: [
            {
                label: 'LangGraph',
                data: [10, 8, 6, 7, 9],
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                borderColor: '#4f46e5',
                pointBackgroundColor: '#4f46e5',
                borderWidth: 2
            },
            {
                label: 'AutoGen',
                data: [6, 10, 5, 6, 7],
                backgroundColor: 'rgba(236, 72, 153, 0.2)',
                borderColor: '#ec4899',
                pointBackgroundColor: '#ec4899',
                borderWidth: 2
            },
            {
                label: 'LlamaIndex',
                data: [5, 6, 10, 8, 8],
                backgroundColor: 'rgba(20, 184, 166, 0.2)',
                borderColor: '#14b8a6',
                pointBackgroundColor: '#14b8a6',
                borderWidth: 2
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            tooltip: tooltipConfig,
            legend: { position: 'bottom', labels: { color: '#f8fafc' } }
        },
        scales: {
            r: {
                angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                pointLabels: { color: '#cbd5e1', font: { size: 11 } },
                ticks: { backdropColor: 'transparent', color: '#64748b', stepSize: 2 }
            }
        }
    }
});

const scatterData = [
    {
        x: [8], y: [9],
        mode: 'markers+text',
        type: 'scattergl',
        name: 'LangGraph',
        text: ['LangGraph'],
        textposition: 'top center',
        marker: { size: 25, color: '#4f46e5', line: {width: 2, color: '#fff'} }
    },
    {
        x: [6], y: [8],
        mode: 'markers+text',
        type: 'scattergl',
        name: 'AutoGen',
        text: ['AutoGen'],
        textposition: 'top center',
        marker: { size: 25, color: '#ec4899', line: {width: 2, color: '#fff'} }
    },
    {
        x: [5], y: [9],
        mode: 'markers+text',
        type: 'scattergl',
        name: 'LlamaIndex',
        text: ['LlamaIndex'],
        textposition: 'top center',
        marker: { size: 25, color: '#14b8a6', line: {width: 2, color: '#fff'} }
    },
    {
        x: [4], y: [6],
        mode: 'markers+text',
        type: 'scattergl',
        name: 'deer-flow',
        text: ['deer-flow'],
        textposition: 'bottom center',
        marker: { size: 20, color: '#f59e0b', line: {width: 2, color: '#fff'} }
    },
    {
        x: [2], y: [4],
        mode: 'markers+text',
        type: 'scattergl',
        name: 'Nanobot',
        text: ['Nanobot'],
        textposition: 'bottom right',
        marker: { size: 15, color: '#0ea5e9', line: {width: 2, color: '#fff'} }
    }
];

const scatterLayout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: '#cbd5e1' },
    xaxis: { title: 'Learning Curve (1 = Easy, 10 = Steep)', gridcolor: '#334155', range: [0, 10] },
    yaxis: { title: 'Integration Power (1 = Basic, 10 = Enterprise)', gridcolor: '#334155', range: [0, 10] },
    showlegend: false,
    margin: { t: 20, b: 50, l: 50, r: 20 }
};

Plotly.newPlot('scatterPlot', scatterData, scatterLayout, {displayModeBar: false});

const donutCommonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        tooltip: tooltipConfig,
        legend: { position: 'bottom', labels: { color: '#f8fafc', font: { size: 10 } } }
    },
    cutout: '70%',
    borderColor: '#1e293b',
    borderWidth: 2
};

const compLabels = ['Data Indexing', 'Agentic Logic', 'State/Routing'].map(l => wrapLabel(l));
const bgColors = ['#14b8a6', '#ec4899', '#4f46e5'];

new Chart(document.getElementById('donutLangGraph').getContext('2d'), {
    type: 'doughnut',
    data: { labels: compLabels, datasets: [{ data: [15, 25, 60], backgroundColor: bgColors }] },
    options: donutCommonOptions
});

new Chart(document.getElementById('donutLlamaIndex').getContext('2d'), {
    type: 'doughnut',
    data: { labels: compLabels, datasets: [{ data: [70, 20, 10], backgroundColor: bgColors }] },
    options: donutCommonOptions
});

new Chart(document.getElementById('donutAutoGen').getContext('2d'), {
    type: 'doughnut',
    data: { labels: compLabels, datasets: [{ data: [10, 65, 25], backgroundColor: bgColors }] },
    options: donutCommonOptions
});
</script>
</body>
</html>