import os
import re

files = ['admin-users.html', 'consultas.html', 'dashboard.html', 'medicos.html', 'pacientes.html']

for fname in files:
    if not os.path.exists(fname): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the aside tag and replace it
    # We will use regex to find the entire aside block and replace it
    
    # We can just rebuild the aside for each file since the structure is identical except for the active link
    active = fname.split('.')[0]
    if active == 'admin-users': active = 'admin'
    
    def get_class(page):
        # We add 'justify-center group-hover:justify-start' so icons center when collapsed
        base = "py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3"
        if page == active:
            return f"{base} bg-[#4f46e5] text-white"
        return f"{base} text-slate-400 hover:text-white"
        
    new_aside = f'''  <aside class="group w-[80px] hover:w-[240px] sidebar-bg flex flex-col justify-between shrink-0 z-50 h-full overflow-hidden transition-all duration-300 absolute md:relative">
    <div class="flex flex-col w-[240px]">
      <div class="h-24 flex items-center px-6 mt-2">
        <div class="w-10 h-10 shrink-0 rounded-full bg-[#4f46e5] flex items-center justify-center font-bold text-white text-xl">
          C
        </div>
      </div>
      <nav class="flex flex-col gap-2 mt-4">
        <a href="dashboard.html" class="{get_class('dashboard')}">
          <i class="ph ph-house text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Início</span>
        </a>
        <a href="pacientes.html" class="{get_class('pacientes')}">
          <i class="ph ph-user text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Pacientes</span>
        </a>
        <a href="medicos.html" class="{get_class('medicos')} admin-only">
          <i class="ph ph-stethoscope text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Médicos</span>
        </a>
        <a href="consultas.html" class="{get_class('consultas')}">
          <i class="ph ph-calendar-blank text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Consultas</span>
        </a>
        <a href="admin-users.html" class="{get_class('admin')} admin-only">
          <i class="ph ph-shield text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Admin</span>
        </a>
      </nav>
    </div>
    <div class="p-4 mb-4 w-[240px]">
      <button class="w-[calc(100%-1.5rem)] px-3 py-3 rounded-lg text-slate-400 hover:text-white flex items-center gap-4 font-medium transition mx-3" onclick="logout()">
        <i class="ph ph-sign-out text-xl shrink-0"></i> 
        <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Sair</span>
      </button>
    </div>
  </aside>'''

    content = re.sub(r'<aside.*?</aside>', new_aside, content, flags=re.DOTALL)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
