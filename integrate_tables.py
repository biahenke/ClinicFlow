import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the tbodys with IDs
tbody_consultas_pattern = r'<tbody>\s*<tr>\s*<td class="font-bold text-white">08:00.*?</tbody>'
content = re.sub(tbody_consultas_pattern, '<tbody id="proximas-consultas-body"></tbody>', content, flags=re.DOTALL)

tbody_pacientes_pattern = r'<tbody>\s*<tr>\s*<td class="font-bold text-white">Ana Clara Souza.*?</tbody>'
content = re.sub(tbody_pacientes_pattern, '<tbody id="ultimos-pacientes-body"></tbody>', content, flags=re.DOTALL)

# Now, add the functions to JS
functions = """
async function loadProximasConsultas() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const res = await window.api.getConsultas(0, 10, { data: today });
        const tbody = document.getElementById('proximas-consultas-body');
        if(!tbody) return;
        
        if (!res.items || res.items.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-slate-400 py-4">Nenhuma consulta</td></tr>';
            return;
        }
        
        let html = '';
        // Sort by time just in case, then take 3
        const sorted = res.items.sort((a,b) => (a.horario || '').localeCompare(b.horario || ''));
        const items = sorted.slice(0, 3);
        
        items.forEach(c => {
            const time = c.horario ? c.horario.substring(0, 5) : '--:--';
            const pNome = c.paciente && c.paciente.user ? c.paciente.user.nome : 'N/D';
            const mNome = c.medico && c.medico.user ? c.medico.user.nome : 'N/D';
            const esp = c.medico ? c.medico.especialidade : 'N/D';
            const status = c.status || 'Agendada';
            
            let statusColor = 'bg-blue-500/20 text-blue-400';
            if(status === 'Confirmada') statusColor = 'bg-emerald-500/20 text-emerald-400';
            if(status === 'Realizada') statusColor = 'bg-teal-500/20 text-teal-400';
            if(status === 'Cancelada') statusColor = 'bg-amber-500/20 text-amber-400';
            
            html += `<tr>
                <td class="font-bold text-white">${time}</td>
                <td>${pNome}</td>
                <td>${mNome}</td>
                <td>${esp}</td>
                <td><span class="${statusColor} px-2 py-0.5 rounded text-[10px] font-bold">${status}</span></td>
            </tr>`;
        });
        tbody.innerHTML = html;
    } catch(e) {}
}

async function loadUltimosPacientes() {
    try {
        // Just fetch latest (usually API returns latest or first ones)
        const res = await window.api.getPacientes(0, 3);
        const tbody = document.getElementById('ultimos-pacientes-body');
        if(!tbody) return;
        
        if (!res.items || res.items.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center text-slate-400 py-4">Nenhum paciente</td></tr>';
            return;
        }
        
        let html = '';
        // We can reverse it if we want them to look recent, or just leave it
        const items = res.items.reverse().slice(0, 3);
        
        items.forEach(p => {
            const nome = p.user ? p.user.nome : 'N/D';
            let idade = '--';
            if(p.data_nascimento) {
                const bday = new Date(p.data_nascimento);
                const ageDifMs = Date.now() - bday.getTime();
                const ageDate = new Date(ageDifMs);
                idade = Math.abs(ageDate.getUTCFullYear() - 1970) + ' anos';
            }
            
            let dataCad = p.created_at ? new Date(p.created_at).toLocaleDateString('pt-BR') : new Date().toLocaleDateString('pt-BR');
            
            html += `<tr>
                <td class="font-bold text-white">${nome}</td>
                <td>${idade}</td>
                <td>${dataCad}</td>
                <td class="text-right"><i class="ph ph-dots-three-vertical text-slate-400 cursor-pointer shrink-0"></i></td>
            </tr>`;
        });
        tbody.innerHTML = html;
    } catch(e) {}
}
"""

content = content.replace('async function loadAgenda() {', functions + '\nasync function loadAgenda() {')

# Also call them in DOMContentLoaded
init_calls = """    loadProximasConsultas();
    loadUltimosPacientes();"""
content = content.replace('loadAgenda();', 'loadAgenda();\n' + init_calls)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Tables integrated with actual data.")
