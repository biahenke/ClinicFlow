import glob
import re

files = glob.glob('*.html')
for f in files:
    if f in ['login.html', 'index.html']: continue
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to remove the button containing ph-bell
    content = re.sub(r'<button[^>]*>\s*<i class="ph ph-bell[^>]*></i>.*?</button>', '', content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Bell removed from all pages.")
