import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

aside_replacement = '''  <!-- 3. PAINEL DIREITO -->
  <aside class="w-[320px] sidebar-bg shrink-0 z-40 h-full p-6 flex flex-col gap-6 overflow-y-auto hidden xl:flex">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 rounded-full bg-[#4f46e5] text-white flex items-center justify-center text-xl font-bold border border-indigo-500/30" id="avatar-initial">U</div>
      <div>
        <h4 class="text-white font-bold" id="profile-name">Carregando...</h4>
        <p class="text-xs text-slate-400" id="user-role">Usuário</p>
      </div>
    </div>
    
    <div class="panel-bg rounded-[1.25rem] p-5 border border-slate-800/50">
      <div class="flex justify-between items-center mb-4 text-white font-bold text-sm" id="calendar-header"></div>
      <div class="grid grid-cols-7 gap-1 text-center text-xs" id="calendar-grid"></div>
    </div>
    
    <div class="flex-1 flex flex-col">
      <h4 id="agenda-title" class="text-white font-bold mb-4 text-sm">Agenda do Dia</h4>
      <div class="flex flex-col gap-3 overflow-y-auto" id="agenda-list-body">
        <div class="text-center text-slate-400 text-sm">Carregando...</div>
      </div>
    </div>
  </aside>

  <style>
    .calendar-day { font-size: 0.85rem; display: flex; align-items: center; justify-content: center; height: 28px; width: 28px; cursor: pointer; transition: 0.2s; border-radius: 8px; color: #94a3b8; margin: 0 auto; }
    .calendar-day:hover { background: rgba(255,255,255,0.05); color: white; }
    .calendar-day.active { background: #4f46e5 !important; color: white !important; font-weight: 700; }
    .agenda-item { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px; display: flex; gap: 12px; align-items: center; transition: background 0.2s; }
    .agenda-item:hover { background: rgba(255,255,255,0.05); }
    .agenda-time { font-weight: 700; color: #a78bfa; font-size: 0.85rem; min-width: 45px; }
    .agenda-details h5 { color: white; font-size: 0.85rem; font-weight: 600; margin-bottom: 2px; }
    .agenda-details p { color: #94a3b8; font-size: 0.75rem; margin: 0; }
  </style>'''

content = re.sub(r'<!-- 3\. PAINEL DIREITO -->.*?</aside>', aside_replacement, content, flags=re.DOTALL)

with open(r'c:\Users\Public\ClinicFlow\temp.txt', 'r', encoding='utf-8') as f:
    old_content = f.read()

js_match = re.search(r'<script src="js/api\.js"></script>.*?</script>', old_content, flags=re.DOTALL)
if js_match:
    js_content = js_match.group(0)
    js_content = js_content.replace('data-lucide="chevron-left"', 'class="ph ph-caret-left"')
    js_content = js_content.replace('data-lucide="chevron-right"', 'class="ph ph-caret-right"')
    js_content = js_content.replace('lucide.createIcons();', '')
    js_content = js_content.replace('carregarGraficoSemanaEStatus();', '// carregarGraficoSemanaEStatus();')
    
    content = content.replace('<script src="js/auth.js"></script>', '')
    content = content.replace('</body>', js_content + '\\n</body>')

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
