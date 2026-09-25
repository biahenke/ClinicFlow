import os
import re

files = ['dashboard.html', 'admin-users.html', 'consultas.html', 'medicos.html', 'pacientes.html']
base_dir = r'c:\Users\Public\ClinicFlow\clinicflow\frontend'

for fname in files:
    path = os.path.join(base_dir, fname)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change .stat-card CSS
    old_stat = r'\.stat-card \{ background: #f8fafc; border-radius: 1rem; padding: 1\.25rem; display: flex; flex-direction: column; justify-content: space-between; \}'
    new_stat = r'.stat-card { background: #131c31; border: 1px solid #1e293b; border-radius: 1rem; padding: 1.25rem; display: flex; flex-direction: column; justify-content: space-between; }'
    content = re.sub(old_stat, new_stat, content)

    # Change text-slate-800 to text-white inside stat-card
    # We can just blindly replace text-slate-800 to text-white everywhere except if it breaks something.
    # Actually, in the dark theme, there shouldn't be ANY text-slate-800.
    content = content.replace('text-slate-800', 'text-white')

    # Change the icon background/text colors for dark theme
    content = content.replace('bg-blue-100', 'bg-blue-500/20')
    content = content.replace('text-blue-600', 'text-blue-400')

    content = content.replace('bg-emerald-100', 'bg-emerald-500/20')
    content = content.replace('text-emerald-600', 'text-emerald-400')

    content = content.replace('bg-purple-100', 'bg-purple-500/20')
    content = content.replace('text-purple-600', 'text-purple-400')

    content = content.replace('bg-amber-100', 'bg-amber-500/20')
    content = content.replace('text-amber-600', 'text-amber-400')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Cards are now dark.")
