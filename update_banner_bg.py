import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<div id="welcome-panel" class="relative w-full rounded-\[1\.5rem\] overflow-hidden flex items-center justify-between px-10 shadow-xl mb-6".*?>\s*<!-- Holographic effect shapes -->'

new_banner = """<div id="welcome-panel" class="relative w-full rounded-[1.5rem] overflow-hidden flex items-center justify-between px-10 shadow-xl mb-6 bg-cover bg-center" style="height: 176px; min-height: 176px; background-image: url('img/banner-bg.jpg');">
          <div class="absolute inset-0 bg-[#0e1628]/70"></div>
          <div class="absolute inset-0 bg-gradient-to-r from-[#0e1628] via-[#0e1628]/40 to-transparent"></div>
          <!-- Holographic effect shapes -->"""

content = re.sub(pattern, new_banner, content)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Banner background updated.")
