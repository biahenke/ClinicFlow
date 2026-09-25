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

    # The div looks like:
    # <div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1"><i class="ph ph-arrow-up shrink-0"></i> 12% </div>
    # <div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1"><i class="ph ph-arrow-up shrink-0"></i> 3% </div>
    
    # We can match the entire div that contains the arrow up
    pattern = r'<div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1">.*?</div>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Percentages removed from cards.")
