import os
import glob

frontend_dir = r"c:\Users\Public\ClinicFlow\clinicflow\frontend"

html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

for filepath in html_files:
    if "login.html" in filepath or "index.html" in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '<nav class="flex flex-col gap-2 mt-4 flex-1">' in content:
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            new_lines.append(line)
            if 'href="pacientes.html"' in line:
                # Add Medicos
                m_class = 'sidebar-item active' if 'medicos.html' in filepath else 'sidebar-item'
                m_link = f'      <a href="medicos.html" class="{m_class}"><i class="ph ph-user-circle-plus text-xl shrink-0"></i> <span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">Médicos</span></a>'
                
                # Add Consultas
                c_class = 'sidebar-item active' if 'consultas.html' in filepath else 'sidebar-item'
                c_link = f'      <a href="consultas.html" class="{c_class}"><i class="ph ph-calendar-plus text-xl shrink-0"></i> <span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">Consultas</span></a>'
                
                if 'href="medicos.html"' not in content:
                    new_lines.append(m_link)
                if 'href="consultas.html"' not in content:
                    new_lines.append(c_link)
                    
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
            print(f"Updated {os.path.basename(filepath)}")
