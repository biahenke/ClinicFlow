import re

# Read old JS
with open(r'c:\Users\Public\ClinicFlow\temp.txt', 'r', encoding='utf-8') as f:
    old_content = f.read()

js_match = re.search(r'<script src="js/api\.js"></script>.*?</script>', old_content, flags=re.DOTALL)
js_code = js_match.group(0) if js_match else ''

# Replace lucide with phosphor just in case
js_code = js_code.replace('data-lucide="chevron-left"', 'class="ph ph-caret-left"')
js_code = js_code.replace('data-lucide="chevron-right"', 'class="ph ph-caret-right"')
js_code = js_code.replace('lucide.createIcons();', '')
js_code = js_code.replace('carregarGraficoSemanaEStatus();', '// carregarGraficoSemanaEStatus();')

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard - Clínica Vida</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    body {{ font-family: 'Inter', sans-serif; background-color: #0b1221; color: #94a3b8; }}
    
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}
    
    .sidebar-item {{ padding: 0.75rem 1rem; border-radius: 0.75rem; display: flex; align-items: center; gap: 1rem; font-weight: 500; transition: 0.3s; color: #cbd5e1; margin: 0 1rem; }}
    .sidebar-item:hover {{ background: rgba(255,255,255,0.05); color: white; }}
    .sidebar-item.active {{ background: linear-gradient(90deg, #3b82f6, #2563eb); color: white; font-weight: 600; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }}
    
    .stat-card {{ background: #f8fafc; border-radius: 1rem; padding: 1.25rem; display: flex; flex-direction: column; justify-content: space-between; }}
    .dark-card {{ background: #131c31; border-radius: 1rem; border: 1px solid #1e293b; padding: 1.5rem; }}
    
    .table-dark th {{ color: #94a3b8; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; padding-bottom: 1rem; text-align: left; border-bottom: 1px solid #1e293b; }}
    .table-dark td {{ padding: 1rem 0; font-size: 0.85rem; color: #cbd5e1; border-bottom: 1px solid #1e293b; }}
    .table-dark tr:last-child td {{ border-bottom: none; }}
    
    .calendar-day {{ font-size: 0.85rem; display: flex; align-items: center; justify-content: center; height: 28px; width: 28px; cursor: pointer; transition: 0.2s; border-radius: 50%; color: #94a3b8; margin: 0 auto; }}
    .calendar-day:hover {{ background: rgba(255,255,255,0.1); color: white; }}
    .calendar-day.active {{ background: #3b82f6 !important; color: white !important; font-weight: 700; box-shadow: 0 0 10px rgba(59,130,246,0.5); }}
    
    .donut-chart {{
      width: 160px; height: 160px; border-radius: 50%;
      background: conic-gradient(#2dd4bf 0% 34%, #3b82f6 34% 83%, #ef4444 83% 91%, #64748b 91% 100%);
      display: flex; align-items: center; justify-content: center;
    }}
    .donut-inner {{ width: 110px; height: 110px; border-radius: 50%; background: #131c31; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  </style>
</head>
<body class="h-screen overflow-hidden flex">

  <!-- LEFT SIDEBAR -->
  <aside class="w-[260px] bg-[#0e1628] border-r border-[#1e293b] flex flex-col shrink-0 z-50 h-full">
    <div class="h-24 flex items-center px-6">
      <div class="flex items-center gap-3">
        <i class="ph-fill ph-heartbeat text-4xl text-blue-500"></i>
        <div class="flex flex-col">
          <span class="text-white font-bold text-xl leading-tight">Clínica Vida</span>
          <span class="text-[0.65rem] text-slate-400 font-semibold tracking-widest">GESTÃO DE SAÚDE</span>
        </div>
      </div>
    </div>
    
    <nav class="flex flex-col gap-2 mt-4 flex-1">
      <a href="dashboard.html" class="sidebar-item active"><i class="ph ph-house text-xl"></i> Início</a>
      <a href="pacientes.html" class="sidebar-item"><i class="ph ph-users text-xl"></i> Pacientes</a>
      <a href="#" class="sidebar-item"><i class="ph ph-calendar-plus text-xl"></i> Agendamentos</a>
      <a href="consultas.html" class="sidebar-item"><i class="ph ph-stethoscope text-xl"></i> Consultas</a>
      <a href="medicos.html" class="sidebar-item"><i class="ph ph-user-md text-xl"></i> Médicos</a>
      <a href="#" class="sidebar-item"><i class="ph ph-users-three text-xl"></i> Equipe</a>
      <a href="#" class="sidebar-item"><i class="ph ph-chart-bar text-xl"></i> Relatórios</a>
      <a href="#" class="sidebar-item"><i class="ph ph-gear text-xl"></i> Configurações</a>
    </nav>
    
    <div class="p-6">
      <a href="#" class="sidebar-item !mx-0 !px-0 flex items-center gap-3">
        <i class="ph ph-headset text-2xl text-slate-400"></i>
        <div class="flex flex-col">
          <span class="text-white font-medium text-sm">Suporte</span>
          <span class="text-xs text-slate-500">Precisa de ajuda?</span>
        </div>
      </a>
    </div>
  </aside>

  <!-- MAIN AREA -->
  <div class="flex-1 flex flex-col overflow-hidden bg-[#0b1221]">
    
    <!-- TOP HEADER -->
    <header class="h-20 px-8 flex items-center justify-between shrink-0">
      <div class="relative">
        <i class="ph ph-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
        <input type="text" placeholder="Buscar paciente, consulta ou médico..." class="w-[450px] bg-[#131c31] border border-[#1e293b] rounded-full py-2.5 pl-12 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500">
        <span class="absolute right-4 top-1/2 -translate-y-1/2 text-[10px] bg-[#1e293b] px-2 py-1 rounded text-slate-400">Ctrl + K</span>
      </div>
      
      <div class="flex items-center gap-6">
        <button class="relative text-slate-400 hover:text-white transition">
          <i class="ph ph-bell text-2xl"></i>
          <span class="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[#0b1221]"></span>
        </button>
        
        <div class="flex items-center gap-3 border-l border-[#1e293b] pl-6 cursor-pointer">
          <div class="w-10 h-10 rounded-full bg-cyan-400 text-slate-900 flex items-center justify-center font-bold text-lg" id="avatar-initial">A</div>
          <div class="flex flex-col">
            <span class="text-white font-semibold text-sm" id="profile-name">Administrador</span>
            <span class="text-xs text-slate-400">admin</span>
          </div>
          <i class="ph ph-caret-down text-slate-400 ml-2"></i>
        </div>
      </div>
    </header>

    <!-- CONTENT -->
    <main class="flex-1 overflow-y-auto p-8 pt-2 flex gap-8">
      
      <div class="flex-1 flex flex-col gap-6">
        
        <!-- BANNER -->
        <div class="relative w-full h-44 rounded-[1.5rem] overflow-hidden flex items-center justify-between px-10 shadow-xl" style="background: url('https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;">
          <div class="absolute inset-0 bg-gradient-to-r from-[#0f172a] via-[#0f172a]/80 to-transparent"></div>
          
          <div class="relative z-10 flex flex-col gap-1">
            <h1 class="text-4xl font-bold text-white tracking-tight">Olá, <span class="text-cyan-400">Administrador!</span></h1>
            <p class="text-slate-300">Aqui está o resumo da clínica para hoje.</p>
          </div>
          
          <div class="relative z-10 flex items-center gap-4 bg-slate-900/40 backdrop-blur-md border border-white/10 rounded-2xl p-4">
            <i class="ph-fill ph-calendar-blank text-3xl text-blue-400"></i>
            <div class="flex flex-col">
              <span class="text-sm text-white font-medium">Quinta-feira, 24 de setembro de 2026</span>
              <div class="flex items-center gap-2 mt-1">
                <i class="ph-fill ph-sun text-xl text-yellow-400"></i>
                <span class="text-white font-bold">28°C</span>
                <span class="text-xs text-slate-300">Dia ensolarado</span>
              </div>
            </div>
          </div>
        </div>

        <!-- METRICS -->
        <div class="grid grid-cols-4 gap-4">
          <!-- Card 1 -->
          <div class="stat-card">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600"><i class="ph-fill ph-users text-lg"></i></div>
              <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Pacientes Cadastrados</span>
            </div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-3xl font-bold text-slate-800" id="stat-pacientes">305</div>
                <div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1"><i class="ph ph-arrow-up"></i> 12% <span class="text-slate-400 font-normal ml-1">em relação ao mês anterior</span></div>
              </div>
              <svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 25C10 25 15 5 25 15C35 25 45 10 55 5L60 0" stroke="#3b82f6" stroke-width="2"/></svg>
            </div>
          </div>
          <!-- Card 2 -->
          <div class="stat-card">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600"><i class="ph-fill ph-calendar-check text-lg"></i></div>
              <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Consultas Hoje</span>
            </div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-3xl font-bold text-slate-800" id="stat-consultas">17</div>
                <div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1"><i class="ph ph-arrow-up"></i> 3% <span class="text-slate-400 font-normal ml-1">em relação a ontem</span></div>
              </div>
              <svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 25C10 25 15 15 25 20C35 25 45 10 55 5L60 0" stroke="#10b981" stroke-width="2"/></svg>
            </div>
          </div>
          <!-- Card 3 -->
          <div class="stat-card">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600"><i class="ph-fill ph-stethoscope text-lg"></i></div>
              <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Médicos Ativos</span>
            </div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-3xl font-bold text-slate-800" id="stat-medicos">35</div>
                <div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1"><i class="ph ph-arrow-up"></i> 6% <span class="text-slate-400 font-normal ml-1">em relação ao mês anterior</span></div>
              </div>
              <svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 20C10 20 15 5 25 10C35 15 45 5 55 0" stroke="#a855f7" stroke-width="2"/></svg>
            </div>
          </div>
          <!-- Card 4 -->
          <div class="stat-card">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center text-amber-600"><i class="ph-fill ph-chart-pie-slice text-lg"></i></div>
              <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Taxa Comparecimento</span>
            </div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-3xl font-bold text-slate-800">92%</div>
                <div class="text-emerald-500 text-xs font-bold mt-1 flex items-center gap-1"><i class="ph ph-arrow-up"></i> 5% <span class="text-slate-400 font-normal ml-1">em relação ao mês anterior</span></div>
              </div>
              <svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 25C10 25 15 15 25 15C35 15 45 5 55 0" stroke="#f59e0b" stroke-width="2"/></svg>
            </div>
          </div>
        </div>

        <!-- CHARTS SECTION -->
        <div class="grid grid-cols-5 gap-4">
          
          <!-- Consultas da Semana -->
          <div class="col-span-3 dark-card flex flex-col">
            <div class="flex justify-between items-center mb-6">
              <div class="flex items-center gap-2">
                <i class="ph-fill ph-calendar-blank text-xl text-blue-400"></i>
                <h3 class="font-bold text-white text-sm">Consultas da Semana</h3>
              </div>
              <button class="bg-[#1e293b] border border-[#334155] rounded-lg px-3 py-1.5 text-xs text-slate-300 flex items-center gap-2">
                Esta semana <i class="ph ph-caret-down"></i>
              </button>
            </div>
            
            <div class="flex-1 relative flex mt-2 h-40">
              <!-- Y Axis -->
              <div class="flex flex-col justify-between text-[10px] text-slate-500 pr-4 h-full pb-6">
                <span>40</span><span>30</span><span>20</span><span>10</span><span>0</span>
              </div>
              
              <!-- Grid lines -->
              <div class="absolute inset-0 left-6 bottom-6 flex flex-col justify-between pointer-events-none">
                <div class="w-full border-t border-slate-700/50"></div>
                <div class="w-full border-t border-slate-700/50"></div>
                <div class="w-full border-t border-slate-700/50"></div>
                <div class="w-full border-t border-slate-700/50"></div>
                <div class="w-full border-t border-slate-700/50"></div>
              </div>
              
              <!-- Chart area -->
              <div class="flex-1 flex items-end justify-around relative z-10 pb-6 pl-4 h-full" id="grafico-semana">
                <div class="w-12 h-[65%] bg-blue-500 rounded-t-sm flex justify-center relative"><span class="absolute -top-5 text-[10px] text-white font-bold">26</span></div>
                <div class="w-12 h-[75%] bg-blue-500 rounded-t-sm flex justify-center relative"><span class="absolute -top-5 text-[10px] text-white font-bold">30</span></div>
                <div class="w-12 h-[42.5%] bg-blue-500 rounded-t-sm flex justify-center relative"><span class="absolute -top-5 text-[10px] text-white font-bold">17</span></div>
                <div class="w-12 h-[60%] bg-blue-500 rounded-t-sm flex justify-center relative"><span class="absolute -top-5 text-[10px] text-white font-bold">24</span></div>
                <div class="w-12 h-[80%] bg-blue-500 rounded-t-sm flex justify-center relative"><span class="absolute -top-5 text-[10px] text-white font-bold">32</span></div>
                <div class="w-12 h-[45%] bg-blue-500 rounded-t-sm flex justify-center relative"><span class="absolute -top-5 text-[10px] text-white font-bold">18</span></div>
              </div>
              
              <!-- X Axis Labels -->
              <div class="absolute bottom-0 left-6 right-0 flex justify-around text-[11px] text-slate-400 pl-4">
                <span class="w-12 text-center">Seg</span>
                <span class="w-12 text-center">Ter</span>
                <span class="w-12 text-center">Qua</span>
                <span class="w-12 text-center">Qui</span>
                <span class="w-12 text-center">Sex</span>
                <span class="w-12 text-center">Sáb</span>
              </div>
            </div>
          </div>

          <!-- Status da Semana -->
          <div class="col-span-2 dark-card flex flex-col">
            <div class="flex justify-between items-center mb-6">
              <div class="flex items-center gap-2">
                <i class="ph-fill ph-chart-pie-slice text-xl text-blue-400"></i>
                <h3 class="font-bold text-white text-sm">Status da Semana</h3>
              </div>
              <button class="bg-[#1e293b] border border-[#334155] rounded-lg px-3 py-1.5 text-xs text-slate-300 flex items-center gap-2">
                Esta semana <i class="ph ph-caret-down"></i>
              </button>
            </div>
            
            <div class="flex-1 flex items-center justify-between">
              <div class="donut-chart">
                <div class="donut-inner">
                  <span class="text-2xl font-bold text-white">124</span>
                  <span class="text-[10px] text-slate-400">Consultas</span>
                </div>
              </div>
              
              <div class="flex flex-col gap-3 w-1/2">
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-teal-400"></div> Realizadas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs">34%</span><span class="text-[9px] text-slate-500">42</span></div>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-blue-500"></div> Agendadas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs">49%</span><span class="text-[9px] text-slate-500">61</span></div>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div> Canceladas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs">8%</span><span class="text-[9px] text-slate-500">10</span></div>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-slate-500"></div> Não realizadas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs">8%</span><span class="text-[9px] text-slate-500">11</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TABLES SECTION -->
        <div class="grid grid-cols-2 gap-4">
          <!-- Próximas Consultas -->
          <div class="dark-card">
            <div class="flex justify-between items-center mb-4">
              <div class="flex items-center gap-2">
                <i class="ph-fill ph-calendar-check text-xl text-blue-400"></i>
                <h3 class="font-bold text-white text-sm">Próximas Consultas</h3>
              </div>
              <a href="#" class="text-xs text-blue-400 hover:text-blue-300">Ver todas</a>
            </div>
            <table class="w-full table-dark">
              <thead>
                <tr>
                  <th>Horário</th><th>Paciente</th><th>Médico</th><th>Especialidade</th><th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="font-bold text-white">08:00</td><td>Felipe Ribeiro Gomes</td><td>Dra. Paula Lima</td><td>Ortopedia</td>
                  <td><span class="bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded text-[10px] font-bold">Confirmada</span></td>
                </tr>
                <tr>
                  <td class="font-bold text-white">09:00</td><td>Maria Souza Rocha</td><td>Dr. Carlos Lima Costa</td><td>Pediatria</td>
                  <td><span class="bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded text-[10px] font-bold">Confirmada</span></td>
                </tr>
                <tr>
                  <td class="font-bold text-white">10:30</td><td>Roberto Pereira Mendes</td><td>Dr. Antônio Silva Oliveira</td><td>Ortopedia</td>
                  <td><span class="bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded text-[10px] font-bold">Confirmada</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Últimos Pacientes -->
          <div class="dark-card">
            <div class="flex justify-between items-center mb-4">
              <div class="flex items-center gap-2">
                <i class="ph-fill ph-user-plus text-xl text-blue-400"></i>
                <h3 class="font-bold text-white text-sm">Últimos Pacientes Cadastrados</h3>
              </div>
              <a href="#" class="text-xs text-blue-400 hover:text-blue-300">Ver todos</a>
            </div>
            <table class="w-full table-dark">
              <thead>
                <tr>
                  <th>Paciente</th><th>Idade</th><th>Data de Cadastro</th><th></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="font-bold text-white">Ana Clara Souza</td><td>28 anos</td><td>24/09/2026</td>
                  <td class="text-right"><i class="ph ph-dots-three-vertical text-slate-400 cursor-pointer"></i></td>
                </tr>
                <tr>
                  <td class="font-bold text-white">Bruno Henrique Alves</td><td>42 anos</td><td>24/09/2026</td>
                  <td class="text-right"><i class="ph ph-dots-three-vertical text-slate-400 cursor-pointer"></i></td>
                </tr>
                <tr>
                  <td class="font-bold text-white">Carla Beatriz Lima</td><td>36 anos</td><td>23/09/2026</td>
                  <td class="text-right"><i class="ph ph-dots-three-vertical text-slate-400 cursor-pointer"></i></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
      
      <!-- RIGHT SIDEBAR (CALENDAR & AGENDA) -->
      <div class="w-[300px] shrink-0 flex flex-col gap-6">
        
        <!-- CALENDAR CARD -->
        <div class="dark-card !p-4 flex flex-col gap-4">
          <div class="flex items-center gap-2 text-white font-bold text-sm">
            <i class="ph-fill ph-calendar-blank text-lg text-blue-400"></i>
            Calendário
          </div>
          
          <div class="flex justify-between items-center text-sm font-semibold text-white px-2 mt-2" id="calendar-header">
            <!-- Will be populated by JS -->
          </div>
          <div class="grid grid-cols-7 gap-y-2 gap-x-1 text-center text-xs mt-2" id="calendar-grid">
             <!-- Will be populated by JS -->
          </div>
        </div>

        <!-- AGENDA DO DIA -->
        <div class="flex-1 flex flex-col">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-white font-bold text-sm" id="agenda-title">Agenda do Dia</h4>
            <a href="#" class="text-xs text-blue-400 hover:text-blue-300">Ver todos</a>
          </div>
          
          <div class="flex flex-col gap-3 overflow-y-auto" id="agenda-list-body">
            <!-- Simulated list for the layout match, but JS will overwrite if running -->
            <div class="bg-[#131c31] border border-[#1e293b] rounded-xl p-3 flex gap-3 items-center hover:bg-[#1e293b] transition cursor-pointer">
              <div class="bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded-md">08:00</div>
              <div class="flex-1">
                <h5 class="text-white text-xs font-bold">Felipe Ribeiro Gomes</h5>
                <p class="text-slate-400 text-[10px]">Dra. Paula Lima - Ortopedia</p>
              </div>
              <i class="ph ph-caret-right text-slate-500"></i>
            </div>
            
            <div class="bg-[#131c31] border border-[#1e293b] rounded-xl p-3 flex gap-3 items-center hover:bg-[#1e293b] transition cursor-pointer">
              <div class="bg-teal-500 text-white text-xs font-bold px-2 py-1 rounded-md">09:00</div>
              <div class="flex-1">
                <h5 class="text-white text-xs font-bold">Maria Souza Rocha</h5>
                <p class="text-slate-400 text-[10px]">Dr. Carlos Lima - Pediatria</p>
              </div>
              <i class="ph ph-caret-right text-slate-500"></i>
            </div>
          </div>
        </div>

      </div>

    </main>
  </div>

  <script src="js/auth.js"></script>
{js_code}
</body>
</html>"""

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Done")
