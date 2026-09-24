import os, re

files = ['admin-users.html', 'consultas.html', 'medicos.html', 'pacientes.html']

for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Also fix the Sair text
    content = content.replace('<i class="ph ph-sign-out text-2xl"></i></button>', '<i class="ph ph-sign-out text-xl"></i> Sair</button>')
    
    # Change buttons to primary color
    content = content.replace('bg-indigo-600', 'bg-[#4f46e5]')
    content = content.replace('hover:bg-indigo-700', 'hover:bg-[#4338ca]')
    
    # Change the header styling slightly to match
    content = content.replace('rounded-[2rem] p-6 px-8', 'mb-2')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
