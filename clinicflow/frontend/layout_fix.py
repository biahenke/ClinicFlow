import os
import re

files = ['admin-users.html', 'consultas.html', 'dashboard.html', 'medicos.html', 'pacientes.html']

style_block = '''  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    body { font-family: 'Inter', sans-serif; background-color: #171728; color: #94a3b8; }
    .sidebar-bg { background-color: #1a1a2e; border-right: 1px solid rgba(255,255,255,0.03); }
    .panel-bg { background-color: #1e1e32; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
    
    .table th { color: #94a3b8 !important; border-bottom: 1px solid rgba(255,255,255,0.05) !important; padding: 1.25rem 1rem !important; text-transform: uppercase; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-align: left;}
    .table td { color: white !important; border-bottom: 1px solid rgba(255,255,255,0.03) !important; padding: 1.25rem 1rem !important; font-size: 0.85rem; font-weight: 500;}
    .table tbody tr:hover { background-color: rgba(255,255,255,0.02) !important; }
    
    .form-control { background: #171728 !important; border: 1px solid rgba(255,255,255,0.05) !important; color: white !important; padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.85rem;}
    .form-control:focus { border-color: #4f46e5 !important; outline: none; }
    
    .btn-primary { background: #4f46e5 !important; color: white !important; border: none !important; padding: 0.6rem 1.2rem; border-radius: 99px; font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem;}
    .btn-primary:hover { background: #4338ca !important; }
    .btn-secondary { background: #171728 !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; padding: 0.6rem 1.2rem; border-radius: 99px; font-weight: 600; font-size: 0.85rem;}
    .btn-secondary:hover { background: rgba(255,255,255,0.05) !important; }
    
    .modal-container { background: #1e1e32 !important; color: #e2e8f0 !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 16px;}
    .modal-header { border-bottom: 1px solid rgba(255,255,255,0.05) !important; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center;}
    .modal-footer { border-top: 1px solid rgba(255,255,255,0.05) !important; background: transparent !important; padding: 1.5rem; display: flex; justify-content: flex-end; gap: 1rem;}
    
    .content-panel { background: #1e1e32 !important; border-radius: 1rem !important; padding: 1rem !important; }
    
    .badge-success { background: #d1fae5; color: #065f46; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 99px; font-weight: 600;}
    .badge-error { background: #fee2e2; color: #991b1b; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 99px; font-weight: 600;}
  </style>'''

def get_sidebar(active):
    def get_class(page):
        if page == active:
            return "px-4 py-3 rounded-lg bg-[#4f46e5] text-white flex items-center gap-3 font-medium transition mx-4"
        return "px-4 py-3 rounded-lg text-slate-400 hover:text-white flex items-center gap-3 font-medium transition mx-4"
    
    return f'''  <aside class="w-[240px] sidebar-bg flex flex-col justify-between shrink-0 z-10 h-full">
    <div>
      <div class="h-24 flex items-center px-8 mt-2">
        <div class="w-10 h-10 rounded-full bg-[#4f46e5] flex items-center justify-center font-bold text-white text-xl">
          C
        </div>
      </div>
      <nav class="flex flex-col gap-1 px-2 mt-4">
        <a href="dashboard.html" class="{get_class('dashboard')}">
          <i class="ph ph-house text-xl"></i> Início
        </a>
        <a href="pacientes.html" class="{get_class('pacientes')}">
          <i class="ph ph-user text-xl"></i> Pacientes
        </a>
        <a href="medicos.html" class="{get_class('medicos')} admin-only">
          <i class="ph ph-stethoscope text-xl"></i> Médicos
        </a>
        <a href="consultas.html" class="{get_class('consultas')}">
          <i class="ph ph-calendar-blank text-xl"></i> Consultas
        </a>
        <a href="admin-users.html" class="{get_class('admin')} admin-only">
          <i class="ph ph-shield text-xl"></i> Admin
        </a>
      </nav>
    </div>
    <div class="p-4 mb-4">
      <button class="w-full px-4 py-3 text-slate-400 hover:text-white flex items-center gap-3 font-medium transition mx-4" onclick="logout()">
        <i class="ph ph-sign-out text-xl"></i> Sair
      </button>
    </div>
  </aside>'''

def get_header(title, desc, btn_inner):
    btn_html = ''
    if btn_inner:
        if 'Novo M' in btn_inner: btn_inner = '<i class="ph ph-plus font-bold text-sm"></i> Novo Médico'
        elif 'Agendar' in btn_inner: btn_inner = '<i class="ph ph-plus font-bold text-sm"></i> Agendar Consulta'
        elif 'Novo Pac' in btn_inner: btn_inner = '<i class="ph ph-plus font-bold text-sm"></i> Novo Paciente'
        elif 'Novo Usu' in btn_inner: btn_inner = '<i class="ph ph-plus font-bold text-sm"></i> Novo Usuário'
        btn_html = f'<button class="btn-primary" id="openModalBtn">{btn_inner}</button>'
        
    return f'''    <header class="flex justify-between items-center mb-8 px-2 mt-4">
      <div>
        <h1 class="text-3xl font-bold text-white tracking-tight">{title}</h1>
        <p class="text-sm text-slate-400 mt-2">{desc}</p>
      </div>
      <div class="flex items-center gap-4">
        {btn_html}
        <button class="w-10 h-10 rounded-full bg-[#1e1e32] border border-slate-700 flex items-center justify-center text-slate-300 hover:text-white transition">
          <i class="ph ph-bell text-lg"></i>
        </button>
      </div>
    </header>'''

for fname in files:
    if not os.path.exists(fname): continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update <style>
    if '<style>' in content:
        content = re.sub(r'<style>.*?</style>', style_block, content, flags=re.DOTALL)
    else:
        content = content.replace('</head>', style_block + '\\n</head>')
    
    # 2. Update body/main
    content = re.sub(r'<body class=".*?">', '<body class="h-screen overflow-hidden flex">', content)
    content = re.sub(r'<main class=".*?">', '<main class="flex-1 flex flex-col p-8 overflow-y-auto gap-4 relative">', content)
    
    # 3. Replace aside
    active = fname.split('.')[0]
    if active == 'admin-users': active = 'admin'
    if '<aside' in content:
        content = re.sub(r'<aside.*?</aside>', get_sidebar(active), content, flags=re.DOTALL)
        
    # 4. Modify header
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    desc_match = re.search(r'<p[^>]*>(.*?)</p>', content)
    btn_match = re.search(r'<button class="bg-[#4f46e5][^>]*id="openModalBtn"[^>]*>(.*?)</button>', content, flags=re.DOTALL)
    if not btn_match:
        btn_match = re.search(r'<button class="bg-indigo-600[^>]*id="openModalBtn"[^>]*>(.*?)</button>', content, flags=re.DOTALL)
    if not btn_match:
        btn_match = re.search(r'<button class="btn btn-primary[^>]*id="openModalBtn"[^>]*>(.*?)</button>', content, flags=re.DOTALL)
    
    if title_match and desc_match:
        title = title_match.group(1).replace('👋', '').strip()
        desc = desc_match.group(1).strip()
        btn_inner = btn_match.group(1).strip() if btn_match else ''
        content = re.sub(r'<header.*?</header>', get_header(title, desc, btn_inner), content, flags=re.DOTALL)
        
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
