import re
import glob

files = glob.glob('*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    pattern1 = r'<button class="bg-\[#1e293b\] border border-\[#334155\] rounded-lg px-3 py-1\.5 text-xs text-slate-300 flex items-center gap-2">\s*Esta semana <i class="ph ph-caret-down shrink-0"></i>\s*</button>'
    pattern2 = r'<button class="bg-\[#1e293b\] border border-\[#334155\] rounded-lg px-3 py-1\.5 text-xs text-slate-300 flex items-center gap-2">\s*Últimos 5 dias <i class="ph ph-caret-down shrink-0"></i>\s*</button>'
    
    content = re.sub(pattern1, '', content, flags=re.DOTALL)
    content = re.sub(pattern2, '', content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Removed Esta Semana buttons.")
