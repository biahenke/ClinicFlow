import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add ID to taxa
content = content.replace('<div class="text-3xl font-bold text-white">92%</div>', '<div class="text-3xl font-bold text-white" id="stat-taxa">92%</div>')

# Add the script to fetch and populate dashboard data
script = """
<script>
document.addEventListener('DOMContentLoaded', async () => {
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
</body>
"""

content = content.replace('</body>', script)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dynamic dashboard metrics script added.")
