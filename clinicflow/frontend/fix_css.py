import os
import re

dashboard = 'c:\\Users\\Public\\ClinicFlow\\clinicflow\\frontend\\dashboard.html'
with open(dashboard, 'r', encoding='utf-8') as f:
    d_content = f.read()

style_match = re.search(r'<style>.*?</style>', d_content, flags=re.DOTALL)
if style_match:
    good_style = style_match.group(0)
    
    for fname in ['perfil.html', 'relatorios.html']:
        path = os.path.join('c:\\Users\\Public\\ClinicFlow\\clinicflow\\frontend', fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = re.sub(r'<style>.*?</style>', good_style, content, flags=re.DOTALL)
        
        # Also need to fix the main background wrapper if it exists
        # dashboard.html has: body class="h-screen overflow-hidden flex"
        # And <main class="flex-1 flex flex-col p-8 overflow-y-auto gap-4 relative">
        # Let's fix background colors inside the body
        content = content.replace('bg-[#0b1221]', '')
        content = content.replace('bg-[#00111f]', '')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Styles applied to perfil and relatorios.")
