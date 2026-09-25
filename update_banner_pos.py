import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace bg-center with bg-bottom in the banner div
pattern = r'<div id="welcome-panel" class="relative w-full rounded-\[1\.5rem\] overflow-hidden flex items-center justify-between px-10 shadow-xl mb-6 bg-cover bg-center"'
new_banner = r'<div id="welcome-panel" class="relative w-full rounded-[1.5rem] overflow-hidden flex items-center justify-between px-10 shadow-xl mb-6 bg-cover bg-[center_70%]"'

content = re.sub(pattern, new_banner, content)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Banner background position updated.")
