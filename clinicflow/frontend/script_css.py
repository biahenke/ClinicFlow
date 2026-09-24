import os

f = 'css/style.css'
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

content = content.replace('--bg-main: #1e1e2d;', '--bg-main: #11131e;')
content = content.replace('--bg-surface: #27293d;', '--bg-surface: #1e1f35;')
content = content.replace('--primary: #6366f1;', '--primary: #4f46e5;')
content = content.replace('--primary-hover: #4f46e5;', '--primary-hover: #4338ca;')

# table header styling
content = content.replace('border-bottom: 1px solid var(--border);', 'border-bottom: 1px solid rgba(255,255,255,0.1);')

# panel background
content = content.replace('--panel-bg: #27293d;', '--panel-bg: #1e1f35;')

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
