import os
import glob

for fpath in glob.glob('*.html'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<a href="#" class="sidebar-item admin-only"><i class="ph ph-chart-bar', '<a href="relatorios.html" class="sidebar-item admin-only"><i class="ph ph-chart-bar')
        
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
