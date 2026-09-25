import os
import glob
import re

html_files = glob.glob('*.html')

sidebar_template = """      <nav class="flex flex-col gap-2 mt-4">
        <a href="dashboard.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_dashboard}">
          <i class="ph ph-house text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Início</span>
        </a>
        <a href="pacientes.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_pacientes}">
          <i class="ph ph-user text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Pacientes</span>
        </a>
        <a href="medicos.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_medicos} admin-only">
          <i class="ph ph-stethoscope text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Médicos</span>
        </a>
        <a href="consultas.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_consultas}">
          <i class="ph ph-calendar-blank text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Consultas</span>
        </a>
        <a href="relatorios.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_relatorios} admin-only">
          <i class="ph ph-chart-bar text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Relatórios</span>
        </a>
        <a href="admin-users.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_admin} admin-only">
          <i class="ph ph-shield text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Admin</span>
        </a>
        <a href="perfil.html" class="py-3 rounded-lg flex items-center gap-4 font-medium transition-all duration-300 mx-3 px-3 {nav_perfil}">
          <i class="ph ph-user-circle text-xl shrink-0"></i> 
          <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Perfil</span>
        </a>
      </nav>"""

active_class = "bg-[#4f46e5] text-white"
inactive_class = "text-slate-400 hover:text-white"

for f in html_files:
    if f in ['index.html', 'login.html']:
        continue
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Generate sidebar for this file
    fmt = {
        'nav_dashboard': active_class if f == 'dashboard.html' else inactive_class,
        'nav_pacientes': active_class if f == 'pacientes.html' else inactive_class,
        'nav_medicos': active_class if f == 'medicos.html' else inactive_class,
        'nav_consultas': active_class if f == 'consultas.html' else inactive_class,
        'nav_relatorios': active_class if f == 'relatorios.html' else inactive_class,
        'nav_admin': active_class if f == 'admin-users.html' else inactive_class,
        'nav_perfil': active_class if f == 'perfil.html' else inactive_class,
    }
    new_sidebar = sidebar_template.format(**fmt)
    
    # Replace the existing nav block
    # It starts with <nav ...> and ends with </nav>
    content = re.sub(r'<nav.*?</nav>', new_sidebar, content, flags=re.DOTALL)
    
    if f in ['relatorios.html', 'perfil.html']:
        # Fix styling to match current design
        content = re.sub(r'bg-\[#00111f\]', 'bg-[#0b1221]', content) # Maybe body background
        content = re.sub(r'bg-\[#001c30\]', 'sidebar-bg', content)
        content = re.sub(r'w-\[80px\] hover:w-\[260px\]', 'w-[80px] hover:w-[240px]', content)
        
        # Replace the aside declaration to match
        old_aside = r'<aside class="group w-\[80px\] hover:w-\[240px\] transition-all duration-300 sidebar-bg border-r border-\[#1e293b\] flex flex-col shrink-0 z-50 h-full overflow-hidden">'
        new_aside = r'<aside class="group w-[80px] hover:w-[240px] sidebar-bg flex flex-col justify-between shrink-0 z-50 h-full overflow-hidden transition-all duration-300 absolute md:relative">'
        content = re.sub(r'<aside.*?>', new_aside, content)
        
        # Also fix the top of the sidebar (C logo)
        top_sidebar = """<div class="flex flex-col w-[240px]">
      <div class="h-24 flex items-center px-6 mt-2">
        <div class="w-10 h-10 shrink-0 rounded-full bg-[#4f46e5] flex items-center justify-center font-bold text-white text-xl">
          C
        </div>
      </div>"""
        content = re.sub(r'<div class="h-24 flex items-center px-6 overflow-hidden">.*?</div>\s*</div>', top_sidebar, content, flags=re.DOTALL)
        
        # Sair button
        bottom_sidebar = """</div>
    <div class="p-4 mb-4 w-[240px]">
      <button class="w-[calc(100%-1.5rem)] px-3 py-3 rounded-lg text-slate-400 hover:text-white flex items-center gap-4 font-medium transition mx-3" onclick="logout()">
        <i class="ph ph-sign-out text-xl shrink-0"></i> 
        <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Sair</span>
      </button>
    </div>"""
        content = re.sub(r'<div class="p-6">.*?</div>', bottom_sidebar, content, flags=re.DOTALL)
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Done fixing sidebars and styles.")
