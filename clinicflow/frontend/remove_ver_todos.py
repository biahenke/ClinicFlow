import re
import glob

files = glob.glob('*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to remove Ver todas and Ver todos
    content = re.sub(r'<a href="#" class="text-xs text-blue-400 hover:text-blue-300">Ver tod[oa]s</a>', '', content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Removed Ver todos/todas links.")
