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

    # The text is inside a span with class text-slate-400
    # <span class="text-slate-400 font-normal ml-1">em relação ao mês anterior</span>
    # <span class="text-slate-400 font-normal ml-1">em relação a ontem</span>
    
    pattern = r'<span class="text-slate-400 font-normal ml-1">.*?</span>'
    content = re.sub(pattern, '', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Small text removed from cards.")
