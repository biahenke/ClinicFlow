import os
import re

files = ['admin-users.html', 'consultas.html', 'medicos.html', 'pacientes.html']

for fname in files:
    path = os.path.join(r'c:\Users\Public\ClinicFlow\clinicflow\frontend', fname)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract title, desc, button
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    desc_match = re.search(r'<p class="text-sm text-slate-400[^>]*>(.*?)</p>', content)
    
    title = title_match.group(1).replace('👋', '').strip() if title_match else 'Página'
    desc = desc_match.group(1).strip() if desc_match else ''
    
    # Try to find a button in the header
    btn_match = re.search(r'<header.*?(<button.*?id="openModalBtn".*?</button>).*?</header>', content, flags=re.DOTALL)
    btn_html = ''
    if btn_match:
        btn_html = btn_match.group(1)
        # Update button classes to new design
        btn_html = re.sub(r'class=".*?"', 'class="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2.5 px-5 rounded-xl flex items-center gap-2 shadow-[0_4px_14px_0_rgba(59,130,246,0.39)] transition-all text-sm"', btn_html)
        
    # Extract inner content
    # The old structure is usually `<div class="content-panel...` to the end of main
    inner_match = re.search(r'<div class="content-panel[^>]*>(.*?)</div>\s*</main>', content, flags=re.DOTALL)
    inner_content = inner_match.group(1) if inner_match else ''
    
    # Extract scripts
    script_match = re.search(r'<script>(.*?)</script>\s*</body>', content, flags=re.DOTALL)
    custom_script = script_match.group(1) if script_match else ''
    custom_script = custom_script.replace('lucide.createIcons();', '')
    custom_script = custom_script.replace('data-lucide="edit"', 'class="ph ph-pencil-simple"')
    custom_script = custom_script.replace('data-lucide="trash-2"', 'class="ph ph-trash"')
    custom_script = custom_script.replace('data-lucide=', 'class="ph ph-') # generic fallback
    
    # Determine active page for sidebar
    active = fname.split('.')[0]
    if active == 'admin-users': active = 'admin'
    
    def get_class(page):
        base = "sidebar-item"
        if page == active: return base + " active"
        return base
        
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Clínica Vida</title>
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
    
    .dark-card {{ background: #131c31; border-radius: 1rem; border: 1px solid #1e293b; padding: 1.5rem; }}
    
    .table {{ width: 100%; border-collapse: collapse; }}
    .table th {{ color: #94a3b8; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; padding: 1rem; text-align: left; border-bottom: 1px solid #1e293b; }}
    .table td {{ padding: 1.25rem 1rem; font-size: 0.85rem; color: #cbd5e1; border-bottom: 1px solid #1e293b; }}
    .table tr:hover td {{ background: rgba(255,255,255,0.02); }}
    
    .badge-success {{ background: rgba(16,185,129,0.15); color: #34d399; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 99px; font-weight: 600; }}
    .badge-error {{ background: rgba(244,63,94,0.15); color: #fb7185; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 99px; font-weight: 600; }}
    
    .form-control {{ background: #0b1221; border: 1px solid #1e293b; color: white; padding: 0.75rem 1rem; border-radius: 0.75rem; font-size: 0.85rem; width: 100%; transition: 0.2s; }}
    .form-control:focus {{ border-color: #3b82f6; outline: none; box-shadow: 0 0 0 2px rgba(59,130,246,0.2); }}
    
    .modal-container {{ background: #131c31; color: #e2e8f0; border: 1px solid #1e293b; border-radius: 1rem; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }}
    .modal-header {{ border-bottom: 1px solid #1e293b; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; }}
    .modal-footer {{ border-top: 1px solid #1e293b; padding: 1.5rem; display: flex; justify-content: flex-end; gap: 1rem; }}
    
    .btn-secondary {{ background: transparent; color: #94a3b8; border: 1px solid #334155; padding: 0.5rem 1rem; border-radius: 0.75rem; font-weight: 600; font-size: 0.85rem; transition: 0.2s; }}
    .btn-secondary:hover {{ background: #1e293b; color: white; }}
    .btn-primary {{ background: #3b82f6; color: white; border: none; padding: 0.5rem 1.25rem; border-radius: 0.75rem; font-weight: 600; font-size: 0.85rem; transition: 0.2s; }}
    .btn-primary:hover {{ background: #2563eb; }}
    
    label.form-label {{ display: block; font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.5rem; font-weight: 500; }}
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
      <a href="dashboard.html" class="{get_class('dashboard')}"><i class="ph ph-house text-xl"></i> Início</a>
      <a href="pacientes.html" class="{get_class('pacientes')}"><i class="ph ph-users text-xl"></i> Pacientes</a>
      <a href="#" class="{get_class('agendamentos')}"><i class="ph ph-calendar-plus text-xl"></i> Agendamentos</a>
      <a href="consultas.html" class="{get_class('consultas')}"><i class="ph ph-stethoscope text-xl"></i> Consultas</a>
      <a href="medicos.html" class="{get_class('medicos')} admin-only"><i class="ph ph-user-md text-xl"></i> Médicos</a>
      <a href="#" class="{get_class('equipe')} admin-only"><i class="ph ph-users-three text-xl"></i> Equipe</a>
      <a href="#" class="{get_class('relatorios')} admin-only"><i class="ph ph-chart-bar text-xl"></i> Relatórios</a>
      <a href="admin-users.html" class="{get_class('admin')} admin-only"><i class="ph ph-shield text-xl"></i> Admin</a>
    </nav>
    
    <div class="p-6">
      <button onclick="logout()" class="sidebar-item !mx-0 !px-0 flex items-center gap-3 w-full text-left">
        <i class="ph ph-sign-out text-2xl text-slate-400"></i>
        <div class="flex flex-col">
          <span class="text-white font-medium text-sm">Sair</span>
          <span class="text-xs text-slate-500">Encerrar sessão</span>
        </div>
      </button>
    </div>
  </aside>

  <!-- MAIN AREA -->
  <div class="flex-1 flex flex-col overflow-hidden bg-[#0b1221]">
    
    <!-- TOP HEADER -->
    <header class="h-20 px-8 flex items-center justify-between shrink-0">
      <div class="relative">
        <i class="ph ph-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
        <input type="text" placeholder="Buscar..." class="w-[300px] bg-[#131c31] border border-[#1e293b] rounded-full py-2 pl-12 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500">
      </div>
      
      <div class="flex items-center gap-6">
        <button class="relative text-slate-400 hover:text-white transition">
          <i class="ph ph-bell text-2xl"></i>
        </button>
        <div class="flex items-center gap-3 border-l border-[#1e293b] pl-6 cursor-pointer">
          <div class="w-10 h-10 rounded-full bg-cyan-400 text-slate-900 flex items-center justify-center font-bold text-lg" id="avatar-initial">U</div>
        </div>
      </div>
    </header>

    <!-- CONTENT -->
    <main class="flex-1 overflow-y-auto p-8 pt-2 flex flex-col gap-6 relative">
      <div class="flex justify-between items-center shrink-0">
        <div>
          <h1 class="text-3xl font-bold text-white tracking-tight">{title}</h1>
          <p class="text-sm text-slate-400 mt-1">{desc}</p>
        </div>
        <div>
          {btn_html}
        </div>
      </div>
      
      <div class="dark-card flex-1 flex flex-col overflow-hidden">
        <div class="overflow-y-auto flex-1">
          {inner_content}
        </div>
      </div>
    </main>
  </div>
  
  <script src="js/api.js"></script>
  <script src="js/auth.js"></script>
  <script>
    {custom_script}
  </script>
</body>
</html>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Updated all other pages.")
