import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the status parsing logic in loadProximasConsultas
pattern = r"const status = c\.status \|\| 'Agendada';\s*let statusColor = 'bg-blue-500/20 text-blue-400';\s*if\(status === 'Confirmada'\) statusColor = 'bg-emerald-500/20 text-emerald-400';\s*if\(status === 'Realizada'\) statusColor = 'bg-teal-500/20 text-teal-400';\s*if\(status === 'Cancelada'\) statusColor = 'bg-amber-500/20 text-amber-400';"

new_logic = """const rawStatus = c.status || 'Agendada';
            const status = rawStatus.charAt(0).toUpperCase() + rawStatus.slice(1);
            
            let statusColor = 'bg-blue-500/20 text-blue-400';
            if(status.toLowerCase() === 'confirmada') statusColor = 'bg-emerald-500/20 text-emerald-400';
            if(status.toLowerCase() === 'realizada') statusColor = 'bg-teal-500/20 text-teal-400';
            if(status.toLowerCase() === 'cancelada') statusColor = 'bg-amber-500/20 text-amber-400';"""

content = re.sub(pattern, new_logic, content)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Capitalization fix applied.")
