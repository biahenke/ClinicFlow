import glob
import re

html_files = glob.glob('*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(
        r'<a href="#" class="sidebar-item([^"]*)"><i class="ph ph-chart-bar text-xl shrink-0"></i> <span class="max-w-0 opacity-0 group-hover:max-w-\[200px\] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">Relatórios</span></a>',
        r'<a href="relatorios.html" class="sidebar-item\1"><i class="ph ph-chart-bar text-xl shrink-0"></i> <span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">Relatórios</span></a>',
        content
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated Relatórios links.")
