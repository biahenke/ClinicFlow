import re
import os

dashboard = r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html'
with open(dashboard, 'r', encoding='utf-8') as f:
    d_content = f.read()

# Extract the entire <aside> from dashboard.html
aside_match = re.search(r'<aside.*?</aside>', d_content, flags=re.DOTALL)
good_aside = aside_match.group(0)

# Extract the entire <style> from dashboard.html
style_match = re.search(r'<style>.*?</style>', d_content, flags=re.DOTALL)
good_style = style_match.group(0)

targets = ['relatorios.html', 'perfil.html']
base_dir = r'c:\Users\Public\ClinicFlow\clinicflow\frontend'

for t in targets:
    path = os.path.join(base_dir, t)
    with open(path, 'r', encoding='utf-8') as f:
        t_content = f.read()
        
    # Replace <style>
    t_content = re.sub(r'<style>.*?</style>', good_style, t_content, flags=re.DOTALL)
    
    # Replace <aside>
    t_content = re.sub(r'<aside.*?</aside>', good_aside, t_content, flags=re.DOTALL)
    
    # Update active class for sidebar item in the new aside
    # Remove 'active' from Início
    t_content = re.sub(r'<a href="dashboard\.html" class="sidebar-item active">', r'<a href="dashboard.html" class="sidebar-item">', t_content)
    
    # Add 'active' to the correct item
    if t == 'relatorios.html':
        t_content = re.sub(r'<a href="relatorios\.html" class="sidebar-item">', r'<a href="relatorios.html" class="sidebar-item active">', t_content)
    elif t == 'perfil.html':
        t_content = re.sub(r'<a href="perfil\.html" class="sidebar-item">', r'<a href="perfil.html" class="sidebar-item active">', t_content)

    # Fix background colors in the body of relatorios and perfil
    t_content = t_content.replace('bg-[#0b1221]', '')
    t_content = t_content.replace('bg-[#00111f]', '')
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t_content)

print("Applied aside and styles to relatorios and perfil.")
