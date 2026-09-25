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

    # Replace the old aside tag (which might be w-[260px]) with the dynamic one
    # Use regex to match the aside tag properly
    aside_regex = r'<aside class="w-\[260px\].*?flex-col shrink-0 z-50 h-full">'
    new_aside = r'<aside class="group w-[80px] hover:w-[260px] transition-all duration-300 bg-[#0e1628] border-r border-[#1e293b] flex flex-col shrink-0 z-50 h-full overflow-hidden">'
    content = re.sub(aside_regex, new_aside, content)

    # We also need to fix the text to not take up space when collapsed
    # Replace the opacity span with hidden/block or w-0
    # Current: <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Text</span>
    # We will change it to:
    # <span class="max-w-0 opacity-0 group-hover:max-w-xs group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap ml-1">Text</span>
    
    bad_span_regex = r'<span class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">(.*?)</span>'
    good_span = r'<span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">\1</span>'
    content = re.sub(bad_span_regex, good_span, content)

    # In my previous script, I might have messed up the CSS for `.sidebar-item` padding/gap
    # Gap will push the hidden span even if it's max-w-0. Let's remove gap from .sidebar-item if it exists and add margin to the span.
    style_regex = r'\.sidebar-item \{ padding: 0\.75rem 1rem; border-radius: 0\.75rem; display: flex; align-items: center; gap: 1rem; font-weight: 500; transition: 0\.3s; color: #cbd5e1; margin: 0 1rem; \}'
    new_style = r'.sidebar-item { padding: 0.75rem 1rem; border-radius: 0.75rem; display: flex; align-items: center; font-weight: 500; transition: 0.3s; color: #cbd5e1; margin: 0 0.75rem; overflow: hidden; }'
    content = content.replace(style_regex, new_style)

    # Also fix the logo text span gap
    logo_regex = r'<div class="flex items-center gap-3">'
    new_logo = r'<div class="flex items-center">'
    content = content.replace(logo_regex, new_logo)

    # Update the logo texts
    content = content.replace(
        '<span class="text-white font-bold text-xl leading-tight opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Clínica Vida</span>',
        '<span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 text-white font-bold text-xl leading-tight">Clínica Vida</span>'
    )
    content = content.replace(
        '<span class="text-[0.65rem] text-slate-400 font-semibold tracking-widest opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">GESTÃO DE SAÚDE</span>',
        '<span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 text-[0.65rem] text-slate-400 font-semibold tracking-widest">GESTÃO DE SAÚDE</span>'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Sidebar fix applied.")
