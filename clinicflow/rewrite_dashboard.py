import codecs

with codecs.open('c:/Users/Public/ClinicFlow/clinicflow/frontend/relatorios.html', 'r', 'utf-8') as f:
    original = f.read()

parts = original.split('<!-- MAIN AREA -->')
sidebar = parts[0]

main_area = """<!-- MAIN AREA -->
  <div class="flex-1 flex flex-col overflow-hidden bg-[#00111f]">
    
    <!-- TOP HEADER -->
    <header class="h-20 px-8 flex items-center justify-between shrink-0">
      <h2 class="text-xl font-bold text-white">Dashboard Analítico</h2>
      
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-3 border-l border-[#1e293b] pl-6 cursor-pointer">
          <div class="w-10 h-10 rounded-full bg-cyan-400 text-slate-900 flex items-center justify-center font-bold text-lg" id="avatar-initial">?</div>
          <div class="flex flex-col">
            <span class="text-white font-semibold text-sm" id="profile-name">Carregando...</span>
            <span class="text-xs text-slate-400" id="profile-role">-</span>
          </div>
        </div>
      </div>
    </header>

    <style>
        .filter-btn { background: #001c30; border: 1px solid #1e293b; color: #94a3b8; }
        .filter-btn:hover { background: #1e293b; color: white; }
        .filter-btn.active { background: linear-gradient(90deg, #0ea5e9, #0284c7); color: white; border-color: transparent; }

        .glass-card {
            background: rgba(0, 40, 69, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }
    </style>

    <!-- CONTENT -->
    <main class="flex-1 overflow-y-auto p-8 pt-4">
      
      <div id="error-message" class="hidden bg-red-500/20 text-red-400 p-4 rounded-xl border border-red-500/30 mb-6">
        <i class="ph-fill ph-warning-circle mr-2 text-lg"></i>
        Acesso negado. Você não tem permissão para visualizar estes relatórios.
      </div>

      <!-- FILTER BAR -->
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-8">
        <div class="flex gap-2" id="quick-filters">
          <button class="filter-btn active px-4 py-2 rounded-xl text-sm font-semibold transition" data-range="hoje">Hoje</button>
          <button class="filter-btn px-4 py-2 rounded-xl text-sm font-semibold transition" data-range="semana">Esta Semana</button>
          <button class="filter-btn px-4 py-2 rounded-xl text-sm font-semibold transition" data-range="mes">Este Mês</button>
        </div>
        <div class="flex items-center gap-3">
          <input type="date" id="filter-start" class="bg-[#00111f] border border-[#1e293b] rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-sky-500 [color-scheme:dark]">
          <span class="text-slate-500 text-sm">até</span>
          <input type="date" id="filter-end" class="bg-[#00111f] border border-[#1e293b] rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-sky-500 [color-scheme:dark]">
          <button id="btn-custom" class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-sm font-bold shadow-[0_0_15px_rgba(14,165,233,0.3)] transition">Personalizado</button>
        </div>
      </div>
      
      <div id="reports-content" class="flex flex-col gap-6 hidden">
        
        <!-- KPIs -->
        <div class="grid grid-cols-4 gap-6" id="kpi-cards">
            <div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
                <div class="absolute -right-6 -top-6 w-24 h-24 bg-sky-500/20 rounded-full blur-2xl group-hover:bg-sky-500/30 transition"></div>
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-10 h-10 rounded-full bg-sky-500/20 flex items-center justify-center text-sky-400">
                        <i class="ph-fill ph-calendar text-xl"></i>
                    </div>
                    <span class="text-slate-400 font-semibold text-sm">Total Consultas</span>
                </div>
                <div class="text-3xl font-bold text-white" id="kpi-total">0</div>
            </div>
            
            <div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
                <div class="absolute -right-6 -top-6 w-24 h-24 bg-emerald-500/20 rounded-full blur-2xl group-hover:bg-emerald-500/30 transition"></div>
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                        <i class="ph-fill ph-check-circle text-xl"></i>
                    </div>
                    <span class="text-slate-400 font-semibold text-sm">Realizadas</span>
                </div>
                <div class="text-3xl font-bold text-white" id="kpi-realizadas">0</div>
            </div>

            <div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
                <div class="absolute -right-6 -top-6 w-24 h-24 bg-sky-500/20 rounded-full blur-2xl group-hover:bg-sky-500/30 transition"></div>
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-10 h-10 rounded-full bg-sky-500/20 flex items-center justify-center text-sky-400">
                        <i class="ph-fill ph-clock text-xl"></i>
                    </div>
                    <span class="text-slate-400 font-semibold text-sm">Agendadas</span>
                </div>
                <div class="text-3xl font-bold text-white" id="kpi-agendadas">0</div>
            </div>

            <div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
                <div class="absolute -right-6 -top-6 w-24 h-24 bg-purple-500/20 rounded-full blur-2xl group-hover:bg-purple-500/30 transition"></div>
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400">
                        <i class="ph-fill ph-chart-line-up text-xl"></i>
                    </div>
                    <span class="text-slate-400 font-semibold text-sm">Taxa Conclusão</span>
                </div>
                <div class="text-3xl font-bold text-white" id="kpi-taxa">0%</div>
            </div>
        </div>

        <div class="grid grid-cols-12 gap-6">
            <!-- STATUS -->
            <div class="col-span-12 lg:col-span-5 dark-card p-6 rounded-2xl flex flex-col">
              <h3 class="text-white font-bold mb-6 flex items-center gap-2">
                <i class="ph-fill ph-chart-pie-slice text-xl text-sky-400"></i>
                Status das Consultas
              </h3>
              
              <div class="flex-1 flex items-center justify-between gap-6">
                <div class="w-36 h-36 shrink-0 relative">
                  <canvas id="statusChart"></canvas>
                </div>
                <div class="flex flex-col gap-3 w-full" id="status-legend">
                    <!-- JS Injected -->
                </div>
              </div>
            </div>

            <!-- VOLUME POR ESPECIALIDADE -->
            <div class="col-span-12 lg:col-span-7 dark-card p-6 rounded-2xl flex flex-col">
              <h3 class="text-white font-bold mb-6 flex items-center gap-2">
                <i class="ph-fill ph-users-three text-xl text-sky-400"></i>
                Top 5 Especialidades
              </h3>
              <div class="flex-1 flex flex-col gap-5 overflow-y-auto pr-2 py-1" id="list-especialidade">
                <!-- JS injected -->
              </div>
            </div>
        </div>

        <!-- VOLUME POR MÉDICO CHART -->
        <div class="dark-card p-6 rounded-2xl">
           <div class="flex justify-between items-center mb-6">
               <h3 class="text-white font-bold flex items-center gap-2">
                 <i class="ph-fill ph-chart-bar text-xl text-sky-400"></i>
                 Desempenho por Médico
               </h3>
               <div class="flex bg-[#00111f] rounded-lg p-1 border border-[#1e293b]" id="medico-toggle">
                   <button class="medico-btn active px-3 py-1 rounded-md text-xs font-semibold text-white bg-[#1e293b]" data-top="5">Top 5</button>
                   <button class="medico-btn px-3 py-1 rounded-md text-xs font-semibold text-slate-400 hover:text-white transition" data-top="10">Top 10</button>
                   <button class="medico-btn px-3 py-1 rounded-md text-xs font-semibold text-slate-400 hover:text-white transition" data-top="all">Ver Todos</button>
               </div>
           </div>
           
           <div class="w-full relative transition-all duration-300" style="height: 300px; min-height: 300px;" id="medico-chart-container">
               <canvas id="medicoChart"></canvas>
           </div>
        </div>

      </div>
    </main>
  </div>

  <script src="js/auth.js"></script>
  <script src="js/api.js"></script>
  
  <script>
    let statusChartInstance = null;
    let medicoChartInstance = null;
    let allMedicosData = [];
    let currentMedicoTop = 5;

    document.addEventListener('DOMContentLoaded', async () => {
      // User Profile
      try {
        const me = await window.api.getMe();
        if (me) {
          document.getElementById('profile-name').textContent = me.nome;
          document.getElementById('profile-role').textContent = me.role.charAt(0).toUpperCase() + me.role.slice(1);
          document.getElementById('avatar-initial').textContent = me.nome.charAt(0).toUpperCase();
        }
      } catch (e) {
         window.location.href = '/login.html';
      }

      setupFilters();
      // default: hoje
      document.querySelector('[data-range="hoje"]').click();
    });

    const formatLocal = (d) => {
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    function setupFilters() {
      const startInput = document.getElementById('filter-start');
      const endInput = document.getElementById('filter-end');

      document.getElementById('btn-custom').addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
        const filters = {};
        if (startInput.value) filters.start_date = startInput.value;
        if (endInput.value) filters.end_date = endInput.value;
        loadReports(filters);
      });

      document.getElementById('quick-filters').addEventListener('click', (e) => {
          if(e.target.tagName !== 'BUTTON') return;
          
          document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
          e.target.classList.add('active');
          
          const range = e.target.dataset.range;
          const today = new Date();
          let start = new Date(today);
          let end = new Date(today);

          if (range === 'semana') {
              start.setDate(today.getDate() - today.getDay());
              end.setDate(start.getDate() + 6);
          } else if (range === 'mes') {
              start.setDate(1);
              end.setMonth(start.getMonth() + 1, 0);
          }

          startInput.value = formatLocal(start);
          endInput.value = formatLocal(end);
          
          loadReports({ start_date: startInput.value, end_date: endInput.value });
      });

      document.getElementById('medico-toggle').addEventListener('click', (e) => {
          if(e.target.tagName !== 'BUTTON') return;
          
          document.querySelectorAll('.medico-btn').forEach(btn => {
              btn.classList.remove('active', 'text-white', 'bg-[#1e293b]');
              btn.classList.add('text-slate-400');
          });
          e.target.classList.remove('text-slate-400');
          e.target.classList.add('active', 'text-white', 'bg-[#1e293b]');
          
          currentMedicoTop = e.target.dataset.top === 'all' ? 'all' : parseInt(e.target.dataset.top);
          renderMedicoChart();
      });
    }

    async function loadReports(filters) {
      try {
        const metrics = await window.api.getRelatoriosSummary(filters);
        document.getElementById('reports-content').classList.remove('hidden');

        // Status & KPIs
        if(metrics.status) {
            const realizada = metrics.status.realizada || 0;
            const agendada = metrics.status.agendada || 0;
            const cancelada = metrics.status.cancelada || 0;
            const nao_realizada = metrics.status.nao_realizada || 0;
            
            const total = realizada + agendada + cancelada + nao_realizada;
            document.getElementById('kpi-total').innerText = total;
            document.getElementById('kpi-realizadas').innerText = realizada;
            document.getElementById('kpi-agendadas').innerText = agendada;
            const taxa = total === 0 ? 0 : Math.round((realizada / total) * 100);
            document.getElementById('kpi-taxa').innerText = taxa + '%';

            // Chart
            const ctxStatus = document.getElementById('statusChart').getContext('2d');
            if (statusChartInstance) statusChartInstance.destroy();
            statusChartInstance = new Chart(ctxStatus, {
                type: 'doughnut',
                data: {
                    labels: ['Realizada', 'Agendada', 'Cancelada', 'Não Realizada'],
                    datasets: [{
                        data: [realizada, agendada, cancelada, nao_realizada],
                        backgroundColor: ['#10b981', '#0ea5e9', '#ef4444', '#64748b'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            // Legend
            const statusConfig = [
                { label: 'Realizada', val: realizada, bg: 'bg-emerald-500' },
                { label: 'Agendada', val: agendada, bg: 'bg-sky-500' },
                { label: 'Cancelada', val: cancelada, bg: 'bg-red-500' },
                { label: 'Não Realizada', val: nao_realizada, bg: 'bg-slate-500' }
            ];
            
            document.getElementById('status-legend').innerHTML = statusConfig.map(s => `
                <div class="flex justify-between items-center p-2.5 bg-[#00111f] rounded-lg border border-[#1e293b]">
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 rounded-full ${s.bg}"></div> 
                        <span class="text-xs font-semibold text-slate-300">${s.label}</span>
                    </div>
                    <span class="text-sm font-bold text-white">${s.val}</span>
                </div>
            `).join('');
        }

        // Especialidade
        const espList = document.getElementById('list-especialidade');
        if(metrics.volume_especialidade) {
            const esps = Object.entries(metrics.volume_especialidade).sort((a,b)=>b[1]-a[1]);
            if(esps.length === 0) {
                espList.innerHTML = '<p class="text-slate-500 text-sm">Sem dados disponíveis no período.</p>';
            } else {
                const maxVal = esps[0][1];
                espList.innerHTML = esps.slice(0, 5).map(e => {
                    const perc = (e[1] / maxVal) * 100;
                    return `
                    <div class="flex flex-col gap-2">
                        <div class="flex justify-between text-xs font-semibold">
                            <span class="text-slate-300 uppercase tracking-wide">${e[0]}</span>
                            <span class="text-white">${e[1]}</span>
                        </div>
                        <div class="h-2 w-full bg-[#00111f] rounded-full overflow-hidden border border-[#1e293b]">
                            <div class="h-full bg-gradient-to-r from-sky-600 to-cyan-400 rounded-full shadow-[0_0_10px_rgba(34,211,238,0.5)]" style="width: ${perc}%"></div>
                        </div>
                    </div>
                    `;
                }).join('');
            }
        }

        // Medico
        if(metrics.volume_medico) {
            allMedicosData = Object.entries(metrics.volume_medico).sort((a,b)=>b[1]-a[1]);
            renderMedicoChart();
        }

      } catch (err) {
        document.getElementById('error-message').classList.remove('hidden');
      }
    }

    function renderMedicoChart() {
        let meds = allMedicosData;
        if (currentMedicoTop !== 'all') {
            meds = meds.slice(0, currentMedicoTop);
        }
        
        const container = document.getElementById('medico-chart-container');
        if (currentMedicoTop === 'all') {
            container.style.height = Math.max(300, meds.length * 40) + 'px';
        } else {
            container.style.height = '300px';
        }

        const labels = meds.map(m => m[0]);
        const data = meds.map(m => m[1]);

        const ctxMedico = document.getElementById('medicoChart').getContext('2d');
        if (medicoChartInstance) medicoChartInstance.destroy();
        medicoChartInstance = new Chart(ctxMedico, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Consultas',
                    data: data,
                    backgroundColor: '#0ea5e9',
                    borderRadius: 4,
                    maxBarThickness: 24
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, color: '#94a3b8', font: { family: 'Inter', size: 11 } },
                        grid: { color: '#1e293b' },
                        border: { display: false }
                    },
                    y: {
                        ticks: { color: '#cbd5e1', font: { family: 'Inter', size: 11 }, autoSkip: false },
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });
    }

  </script>
</body>
</html>
"""

with codecs.open('c:/Users/Public/ClinicFlow/clinicflow/frontend/relatorios.html', 'w', 'utf-8') as f:
    f.write(sidebar + main_area)
