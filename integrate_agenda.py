import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the script block in dashboard.html completely.
# First, let's find everything from <script> document.addEventListener('DOMContentLoaded', async () => { ... to </body>
pattern = r"<script>\s*document\.addEventListener\('DOMContentLoaded', async \(\) => \{.*?</script>\s*</body>"

new_script = """<script>
function renderCalendar() {
    const today = new Date();
    const month = today.getMonth();
    const year = today.getFullYear();
    const day = today.getDate();
    
    const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    const header = document.getElementById('calendar-header');
    if(header) header.innerHTML = `<span>${monthNames[month]} ${year}</span>`;
    
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    const grid = document.getElementById('calendar-grid');
    if(!grid) return;
    grid.innerHTML = '';
    
    const daysOfWeek = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S'];
    daysOfWeek.forEach(d => {
        grid.innerHTML += `<div class="text-slate-500 font-bold mb-1">${d}</div>`;
    });
    
    for (let i = 0; i < firstDay; i++) {
        grid.innerHTML += `<div></div>`;
    }
    
    for (let i = 1; i <= daysInMonth; i++) {
        const isToday = i === day;
        const activeClass = isToday ? 'active' : '';
        grid.innerHTML += `<div class="calendar-day ${activeClass}">${i}</div>`;
    }
}

async function loadAgenda() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const consultas = await window.api.getConsultas(0, 100, { data: today });
        const agendaBody = document.getElementById('agenda-list-body');
        if(!agendaBody) return;
        
        if (!consultas.items || consultas.items.length === 0) {
            agendaBody.innerHTML = '<p class="text-xs text-slate-400 p-2">Nenhum atendimento para hoje.</p>';
            return;
        }
        
        let html = '';
        consultas.items.forEach(c => {
            const time = c.horario ? c.horario.substring(0, 5) : '--:--';
            const statusColor = c.status === 'Confirmada' ? 'bg-teal-500' : 'bg-blue-500';
            const pNome = c.paciente && c.paciente.user ? c.paciente.user.nome : 'Paciente Desconhecido';
            const mNome = c.medico && c.medico.user ? c.medico.user.nome : 'Médico Desconhecido';
            const esp = c.medico ? c.medico.especialidade : '';
            
            html += `
            <div class="bg-[#131c31] border border-[#1e293b] rounded-xl p-3 flex gap-3 items-center hover:bg-[#1e293b] transition cursor-pointer shadow-md">
              <div class="${statusColor} text-white text-xs font-bold px-2 py-1 rounded-md">${time}</div>
              <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700 shrink-0">
                <i class="ph ph-user text-slate-300 shrink-0"></i>
              </div>
              <div class="flex-1 overflow-hidden">
                <h5 class="text-white text-xs font-bold truncate">${pNome}</h5>
                <p class="text-slate-400 text-[10px] truncate">${mNome} - ${esp}</p>
              </div>
              <i class="ph ph-caret-right text-slate-500 shrink-0"></i>
            </div>
            `;
        });
        agendaBody.innerHTML = html;
    } catch (e) {
        console.error("Erro ao carregar agenda", e);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    renderCalendar();
    loadAgenda();

    try {
        const pacientes = await window.api.getPacientes(0, 1);
        const statPacientes = document.getElementById('stat-pacientes');
        if(statPacientes) statPacientes.innerText = pacientes.total || 0;
        
        const medicos = await window.api.getMedicos(0, 1);
        const statMedicos = document.getElementById('stat-medicos');
        if(statMedicos) statMedicos.innerText = medicos.total || 0;
        
        const today = new Date().toISOString().split('T')[0];
        const consultas = await window.api.getConsultas(0, 1, { data: today });
        const statConsultas = document.getElementById('stat-consultas');
        if(statConsultas) statConsultas.innerText = consultas.total || 0;
        
        const allConsultas = await window.api.getConsultas(0, 1000);
        const statTaxa = document.getElementById('stat-taxa');
        if(statTaxa && allConsultas.items && allConsultas.items.length > 0) {
            const realizadas = allConsultas.items.filter(c => c.status && c.status.toLowerCase() === 'realizada').length;
            const taxa = Math.round((realizadas / allConsultas.items.length) * 100);
            statTaxa.innerText = taxa + '%';
        } else if (statTaxa) {
            statTaxa.innerText = '0%';
        }
    } catch (e) {
        console.error('Erro ao carregar métricas:', e);
    }
});
</script>
</body>"""

# Substitute
content = re.sub(pattern, new_script, content, flags=re.DOTALL)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Calendar and Agenda integration added.")
