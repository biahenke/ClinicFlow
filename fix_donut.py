import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the red color to amber
content = content.replace('conic-gradient(#2dd4bf 0% 34%, #3b82f6 34% 83%, #ef4444 83% 91%, #64748b 91% 100%)', 
                          'conic-gradient(#2dd4bf 0% 34%, #3b82f6 34% 83%, #f59e0b 83% 91%, #64748b 91% 100%)')

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Donut chart color fixed.")
