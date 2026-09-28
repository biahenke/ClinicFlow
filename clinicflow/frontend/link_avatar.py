import glob

html_files = glob.glob('*.html')
for filepath in html_files:
    if filepath in ['login.html', 'index.html']: continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_div = '<div class="flex items-center gap-3 border-l border-[#1e293b] pl-6 cursor-pointer">'
    new_div = '<div class="flex items-center gap-3 border-l border-[#1e293b] pl-6 cursor-pointer" onclick="window.location.href=\'perfil.html\'">'
    
    if old_div in content:
        content = content.replace(old_div, new_div)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    elif new_div in content:
        print(f"Already updated {filepath}")
