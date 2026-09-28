import os, glob

html_files = glob.glob('*.html')
admin_link = '      <a href="admin-users.html" class="sidebar-item admin-only"><i class="ph ph-shield text-xl shrink-0"></i> <span class="max-w-0 opacity-0 group-hover:max-w-[200px] group-hover:opacity-100 transition-all duration-300 overflow-hidden whitespace-nowrap group-hover:ml-3 flex-1">Admin</span></a>\n'

for f in html_files:
    if f in ['login.html', 'index.html', 'admin-users.html', 'pacientes.html']: continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'href="admin-users.html"' not in content:
        content = content.replace('</nav>', admin_link + '    </nav>')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated {f}')
