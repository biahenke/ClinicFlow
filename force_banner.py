import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's forcefully add inline styles and a generic non-banner class
# to guarantee it renders no matter what Tailwind CDN or Adblock does.
pattern = r'<!-- HERO SECTION -->\s*<div class="relative w-full h-44[^>]+>'

new_div = '''<!-- HERO SECTION -->
        <div id="welcome-panel" class="relative w-full rounded-[1.5rem] overflow-hidden flex items-center justify-between px-10 shadow-xl mb-6" style="height: 176px; min-height: 176px; background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);">'''

content = re.sub(pattern, new_div, content, flags=re.DOTALL)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
