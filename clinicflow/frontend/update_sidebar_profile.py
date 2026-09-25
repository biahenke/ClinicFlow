import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if Configurações exists
    if "Configurações" in content:
        # Instead of DOTALL, replace only lines matching exactly or use a specific non-greedy pattern that excludes other links
        # A safer pattern: <a [^>]*class="sidebar-item[^>]*>(?:(?!<a).)*?Configurações.*?</a>
        content = re.sub(
            r'<a [^>]*class="sidebar-item[^>]*>(?:(?!<a).)*?Configurações(?:(?!<a).)*?</a>',
            r'<a href="perfil.html" class="sidebar-item"><i class="ph ph-user text-xl shrink-0"></i> <span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">Perfil</span></a>',
            content,
            flags=re.DOTALL
        )
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
