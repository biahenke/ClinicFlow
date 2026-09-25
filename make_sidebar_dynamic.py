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

    # 1. Remove Médicos and Equipe
    content = re.sub(r'<a href="medicos\.html"[^>]*>.*?Médicos\s*</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a href="#"[^>]*>.*?Equipe\s*</a>', '', content, flags=re.DOTALL)
    
    # 2. Make sidebar dynamic
    # Find the aside block
    aside_pattern = r'<aside class="w-\[260px\] bg-\[#0e1628\] border-r border-\[#1e293b\] flex flex-col shrink-0 z-50 h-full">'
    new_aside = r'<aside class="group w-[80px] hover:w-[260px] transition-all duration-300 bg-[#0e1628] border-r border-[#1e293b] flex flex-col shrink-0 z-50 h-full absolute md:relative overflow-hidden">'
    content = content.replace(aside_pattern, new_aside)

    # 3. Update the logo section
    logo_pattern = r'<span class="text-white font-bold text-xl leading-tight">Clínica Vida</span>\s*<span class="text-\[0\.65rem\] text-slate-400 font-semibold tracking-widest">GESTÃO DE SAÚDE</span>'
    new_logo = r'<span class="text-white font-bold text-xl leading-tight opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Clínica Vida</span><span class="text-[0.65rem] text-slate-400 font-semibold tracking-widest opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">GESTÃO DE SAÚDE</span>'
    content = re.sub(logo_pattern, new_logo, content)

    # 4. Update the menu items text to be hidden when collapsed
    # This involves wrapping the text part of the links in a span with opacity classes
    # Old: <a ...><i class="..."></i> Text</a>
    # We want: <a ...><i class="..."></i> <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Text</span></a>
    
    # Let's fix the links inside nav
    def replacer(match):
        icon = match.group(1)
        text = match.group(2).strip()
        return f'{icon} <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">{text}</span>'

    # Nav items
    content = re.sub(r'(<i class="ph[^>]+></i>)\s*([A-Za-zÀ-ÿ]+(?:\s[A-Za-zÀ-ÿ]+)*)(?=\s*</a>)', replacer, content)

    # Sair button
    content = re.sub(r'<span class="text-white font-medium text-sm">Sair</span>', r'<span class="text-white font-medium text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Sair</span>', content)
    content = re.sub(r'<span class="text-xs text-slate-500">Encerrar sessão</span>', r'<span class="text-xs text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Encerrar sessão</span>', content)

    # Suporte button if it exists
    content = re.sub(r'<span class="text-white font-medium text-sm">Suporte</span>', r'<span class="text-white font-medium text-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Suporte</span>', content)
    content = re.sub(r'<span class="text-xs text-slate-500">Precisa de ajuda\?</span>', r'<span class="text-xs text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Precisa de ajuda?</span>', content)

    # 5. Fix the sidebar-item class to ensure icon doesn't shrink
    # Add shrink-0 to the icons in sidebar
    content = re.sub(r'<i class="ph ([^"]+)"', r'<i class="ph \1 shrink-0"', content)
    content = re.sub(r'<i class="ph-fill ([^"]+)"', r'<i class="ph-fill \1 shrink-0"', content)

    # 6. Adjust padding/margins inside sidebar to prevent breaking when collapsed
    content = content.replace('h-24 flex items-center px-6', 'h-24 flex items-center px-6 overflow-hidden')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Dynamic sidebar applied.")
