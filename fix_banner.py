import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change BANNER comment to HERO
content = content.replace('<!-- BANNER -->', '<!-- HERO SECTION -->')
content = content.replace('id="banner-date"', 'id="hero-date"')

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
