import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace banner to have a proper gradient if Unsplash fails, and make it look holographic
banner_pattern = r'<!-- BANNER -->.*?<!-- METRICS -->'
new_banner = '''<!-- BANNER -->
        <div class="relative w-full h-44 rounded-[1.5rem] overflow-hidden flex items-center justify-between px-10 shadow-xl mb-6 bg-gradient-to-r from-[#0f172a] via-[#1e3a8a] to-[#0f172a]">
          <!-- Holographic effect shapes -->
          <div class="absolute top-[-50%] left-[-10%] w-[60%] h-[200%] bg-blue-500/20 blur-[80px] rounded-full pointer-events-none"></div>
          <div class="absolute bottom-[-50%] right-[-10%] w-[50%] h-[200%] bg-cyan-400/20 blur-[80px] rounded-full pointer-events-none"></div>
          
          <div class="relative z-10 flex flex-col gap-1">
            <h1 class="text-4xl font-bold text-white tracking-tight">Olá, <span class="text-cyan-400 drop-shadow-md">Administrador!</span></h1>
            <p class="text-slate-300">Aqui está o resumo da clínica para hoje.</p>
          </div>
          
          <div class="relative z-10 flex items-center gap-4 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 shadow-[0_8px_32px_0_rgba(31,38,135,0.37)]">
            <i class="ph-fill ph-calendar-blank text-3xl text-blue-400"></i>
            <div class="flex flex-col">
              <span class="text-sm text-white font-medium" id="banner-date">Quinta-feira, 24 de setembro de 2026</span>
              <div class="flex items-center gap-2 mt-1">
                <i class="ph-fill ph-sun text-xl text-yellow-400"></i>
                <span class="text-white font-bold">28°C</span>
                <span class="text-xs text-slate-300">Dia ensolarado</span>
              </div>
            </div>
          </div>
        </div>

        <!-- METRICS -->'''

content = re.sub(banner_pattern, new_banner, content, flags=re.DOTALL)

# Add gradients to sparklines in metrics
content = content.replace('<svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 25C10 25 15 5 25 15C35 25 45 10 55 5L60 0" stroke="#3b82f6" stroke-width="2"/></svg>', 
'''<svg width="80" height="40" viewBox="0 0 80 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path d="M0 35C10 35 20 10 35 20C50 30 65 15 80 5 L80 40 L0 40 Z" fill="url(#gradBlue)"/>
  <path d="M0 35C10 35 20 10 35 20C50 30 65 15 80 5" stroke="#3b82f6" stroke-width="2" stroke-linecap="round"/>
</svg>''')

content = content.replace('<svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 25C10 25 15 15 25 20C35 25 45 10 55 5L60 0" stroke="#10b981" stroke-width="2"/></svg>', 
'''<svg width="80" height="40" viewBox="0 0 80 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path d="M0 35C10 35 20 20 35 25C50 30 65 15 80 5 L80 40 L0 40 Z" fill="url(#gradGreen)"/>
  <path d="M0 35C10 35 20 20 35 25C50 30 65 15 80 5" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>
</svg>''')

content = content.replace('<svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 20C10 20 15 5 25 10C35 15 45 5 55 0" stroke="#a855f7" stroke-width="2"/></svg>',
'''<svg width="80" height="40" viewBox="0 0 80 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradPurple" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path d="M0 30C10 30 20 10 35 15C50 20 65 10 80 5 L80 40 L0 40 Z" fill="url(#gradPurple)"/>
  <path d="M0 30C10 30 20 10 35 15C50 20 65 10 80 5" stroke="#a855f7" stroke-width="2" stroke-linecap="round"/>
</svg>''')

content = content.replace('<svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 25C10 25 15 15 25 15C35 15 45 5 55 0" stroke="#f59e0b" stroke-width="2"/></svg>',
'''<svg width="80" height="40" viewBox="0 0 80 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradOrange" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <path d="M0 35C10 35 20 20 35 20C50 20 65 10 80 5 L80 40 L0 40 Z" fill="url(#gradOrange)"/>
  <path d="M0 35C10 35 20 20 35 20C50 20 65 10 80 5" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
</svg>''')

# Gradient for Consultas da Semana Bars
bars_pattern = r'class="w-12 h-\[([0-9.]+)%\] bg-blue-500 rounded-t-sm flex justify-center relative"'
content = re.sub(bars_pattern, r'class="w-12 h-[\1%] bg-gradient-to-t from-blue-600 to-cyan-400 rounded-t-sm flex justify-center relative shadow-[0_0_15px_rgba(34,211,238,0.3)]"', content)


# Fix Agenda Layout inside JS
# The agenda generation is inside the script tag
# We need to change the innerHTML template in the JS

js_agenda_replacement = """
                        const div = document.createElement('div');
                        div.className = 'bg-[#131c31] border border-[#1e293b] rounded-xl p-3 flex gap-3 items-center hover:bg-[#1e293b] transition cursor-pointer mb-3 shadow-md';
                        div.innerHTML = `
                            <div class="bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded-md">${c.horario.substring(0,5)}</div>
                            <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700 shrink-0">
                              <i class="ph ph-user text-slate-300"></i>
                            </div>
                            <div class="flex-1 overflow-hidden">
                                <h5 class="text-white text-xs font-bold truncate">${c.paciente.user.nome}</h5>
                                <p class="text-slate-400 text-[10px] truncate">${c.medico.user.nome} - ${c.medico.especialidade}</p>
                            </div>
                            <i class="ph ph-caret-right text-slate-500"></i>
                        `;
                        agendaBody.appendChild(div);
"""

# Finding the agenda appending block in the JS
# We can just replace the whole agenda-item generation
content = re.sub(
    r"div\.className = 'agenda-item';\s*div\.innerHTML = `.*?`;\s*agendaBody\.appendChild\(div\);", 
    js_agenda_replacement, 
    content, 
    flags=re.DOTALL
)

# Also update the hardcoded "Simulated list" in the HTML for Agenda do Dia
simulated_agenda = """
            <div class="bg-[#131c31] border border-[#1e293b] rounded-xl p-3 flex gap-3 items-center hover:bg-[#1e293b] transition cursor-pointer shadow-md">
              <div class="bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded-md">08:00</div>
              <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700 shrink-0">
                <i class="ph ph-user text-slate-300"></i>
              </div>
              <div class="flex-1 overflow-hidden">
                <h5 class="text-white text-xs font-bold truncate">Felipe Ribeiro Gomes</h5>
                <p class="text-slate-400 text-[10px] truncate">Dra. Paula Lima - Ortopedia</p>
              </div>
              <i class="ph ph-caret-right text-slate-500"></i>
            </div>
            
            <div class="bg-[#131c31] border border-[#1e293b] rounded-xl p-3 flex gap-3 items-center hover:bg-[#1e293b] transition cursor-pointer shadow-md">
              <div class="bg-teal-500 text-white text-xs font-bold px-2 py-1 rounded-md">09:00</div>
              <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700 shrink-0">
                <i class="ph ph-user text-slate-300"></i>
              </div>
              <div class="flex-1 overflow-hidden">
                <h5 class="text-white text-xs font-bold truncate">Maria Souza Rocha</h5>
                <p class="text-slate-400 text-[10px] truncate">Dr. Carlos Lima - Pediatria</p>
              </div>
              <i class="ph ph-caret-right text-slate-500"></i>
            </div>
"""
content = re.sub(r'<!-- Simulated list for the layout match.*?</div>\s*</div>', simulated_agenda + '          </div>', content, flags=re.DOTALL)


with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard updated with holographic elements.")
