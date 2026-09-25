import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Y-Axis div to add ID
y_axis_pattern = r'<div class="flex flex-col justify-between text-\[10px\] text-slate-500 pr-4 h-full pb-6">\s*<span>40</span><span>30</span><span>20</span><span>10</span><span>0</span>\s*</div>'
y_axis_new = r'<div class="flex flex-col justify-between text-[10px] text-slate-500 pr-4 h-full pb-6" id="y-axis-labels"><span>40</span><span>30</span><span>20</span><span>10</span><span>0</span></div>'
content = re.sub(y_axis_pattern, y_axis_new, content)

# Add loadConsultasSemana() function
js_logic = """
async function loadConsultasSemana() {
    try {
        const res = await window.api.getConsultas(0, 1000);
        const counts = [0, 0, 0, 0, 0, 0, 0];
        
        const today = new Date();
        const startOfWeek = new Date(today);
        startOfWeek.setDate(today.getDate() - today.getDay());
        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);
        
        const startStr = startOfWeek.toISOString().split('T')[0];
        const endStr = endOfWeek.toISOString().split('T')[0];

        if(res.items) {
            res.items.forEach(c => {
                if(c.data >= startStr && c.data <= endStr) {
                    const day = new Date(c.data + "T00:00:00").getDay();
                    counts[day]++;
                }
            });
        }
        
        const daysToShow = [1, 2, 3, 4, 5, 6];
        const maxCount = Math.max(1, ...daysToShow.map(d => counts[d]));
        const max10 = Math.ceil(maxCount / 10) * 10 || 10;
        
        const chartArea = document.getElementById('grafico-semana');
        if(chartArea) {
            let html = '';
            daysToShow.forEach(day => {
                const count = counts[day];
                const percent = count === 0 ? 0 : (count / max10) * 100;
                
                html += `
                <div class="w-12 bg-gradient-to-t from-blue-600 to-cyan-400 rounded-t-sm flex justify-center relative shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-500" style="height: ${percent}%">
                    <span class="absolute -top-5 text-[10px] text-white font-bold">${count}</span>
                </div>
                `;
            });
            chartArea.innerHTML = html;
        }
        
        const yAxis = document.getElementById('y-axis-labels');
        if(yAxis) {
            yAxis.innerHTML = `<span>${max10}</span><span>${Math.round(max10 * 0.75)}</span><span>${Math.round(max10 * 0.5)}</span><span>${Math.round(max10 * 0.25)}</span><span>0</span>`;
        }

    } catch (e) { console.error("Erro gráfico", e); }
}
"""

content = content.replace('async function loadAgenda() {', js_logic + '\nasync function loadAgenda() {')

# Call it in init_calls
content = content.replace('loadProximasConsultas();', 'loadProximasConsultas();\n    loadConsultasSemana();')


with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Chart dynamic logic added.")
