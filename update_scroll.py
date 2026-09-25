import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change main
# <main class="flex-1 overflow-y-auto p-8 pt-2 flex gap-8">
content = content.replace('<main class="flex-1 overflow-y-auto p-8 pt-2 flex gap-8">', '<main class="flex-1 overflow-hidden p-8 pt-2 flex gap-8">')

# 2. Change left column
# <div class="flex-1 flex flex-col gap-6">
content = content.replace('<div class="flex-1 flex flex-col gap-6">', '<div class="flex-1 flex flex-col gap-6 overflow-y-auto pr-2 pb-10" id="main-left-column">')

# 3. Change right column
# <div class="w-[300px] shrink-0 flex flex-col gap-6">
content = content.replace('<div class="w-[300px] shrink-0 flex flex-col gap-6">', '<div class="w-[300px] shrink-0 flex flex-col gap-6 h-full overflow-hidden pb-4">')

# 4. Change Agenda container to have min-h-0
# <div class="flex-1 flex flex-col"> right after <!-- AGENDA DO DIA -->
agenda_pattern = r'<!-- AGENDA DO DIA -->\s*<div class="flex-1 flex flex-col">'
agenda_new = r'<!-- AGENDA DO DIA -->\n        <div class="flex-1 flex flex-col min-h-0">'
content = re.sub(agenda_pattern, agenda_new, content)

# Also add pr-2 to agenda list body for scrollbar spacing
content = content.replace('id="agenda-list-body"', 'id="agenda-list-body" style="padding-right: 0.25rem;"')

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Scroll behavior updated.")
