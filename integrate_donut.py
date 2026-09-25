import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace HTML for status chart to include IDs
pattern_html = r'<div class="donut-chart">.*?</div>\s*</div>\s*</div>'
new_html = """<div class="donut-chart" id="status-donut-chart">
                <div class="donut-inner">
                  <span class="text-2xl font-bold text-white" id="status-total">124</span>
                  <span class="text-[10px] text-slate-400">Consultas</span>
                </div>
              </div>
              
              <div class="flex flex-col gap-3 w-1/2">
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-teal-400"></div> Realizadas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs" id="perc-realizadas">34%</span><span class="text-[9px] text-slate-500" id="num-realizadas">42</span></div>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-blue-500"></div> Agendadas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs" id="perc-agendadas">49%</span><span class="text-[9px] text-slate-500" id="num-agendadas">61</span></div>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div> Canceladas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs" id="perc-canceladas">8%</span><span class="text-[9px] text-slate-500" id="num-canceladas">10</span></div>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2 text-xs text-slate-300"><div class="w-2.5 h-2.5 rounded-full bg-slate-500"></div> Não realizadas</div>
                  <div class="flex flex-col items-end"><span class="text-white font-bold text-xs" id="perc-nao-realizadas">8%</span><span class="text-[9px] text-slate-500" id="num-nao-realizadas">11</span></div>
                </div>
              </div>
            </div>"""
content = re.sub(pattern_html, new_html, content, flags=re.DOTALL)


# Insert JS logic inside loadConsultasSemana()
pattern_js = r'const daysToShow = \[1, 2, 3, 4, 5, 6\];'
new_js_logic = """
        let stats = { realizadas: 0, agendadas: 0, canceladas: 0, naorealizadas: 0 };
        let totalSemana = 0;
        if(res.items) {
            res.items.forEach(c => {
                if(c.data >= startStr && c.data <= endStr) {
                    totalSemana++;
                    const s = (c.status || '').toLowerCase();
                    if(s === 'realizada') stats.realizadas++;
                    else if(s === 'cancelada') stats.canceladas++;
                    else if(s === 'não realizada' || s === 'nao realizada') stats.naorealizadas++;
                    else stats.agendadas++;
                }
            });
        }
        
        const stTotal = document.getElementById('status-total');
        if(stTotal) stTotal.innerText = totalSemana;
        
        let pRealizadas = totalSemana > 0 ? Math.round((stats.realizadas / totalSemana) * 100) : 0;
        let pAgendadas = totalSemana > 0 ? Math.round((stats.agendadas / totalSemana) * 100) : 0;
        let pCanceladas = totalSemana > 0 ? Math.round((stats.canceladas / totalSemana) * 100) : 0;
        let pNaoRealizadas = totalSemana > 0 ? Math.round((stats.naorealizadas / totalSemana) * 100) : 0;
        
        let diff = 100 - (pRealizadas + pAgendadas + pCanceladas + pNaoRealizadas);
        if(totalSemana > 0 && Math.abs(diff) > 0 && diff !== 100) {
            const maxP = Math.max(pRealizadas, pAgendadas, pCanceladas, pNaoRealizadas);
            if(maxP === pRealizadas) pRealizadas += diff;
            else if(maxP === pAgendadas) pAgendadas += diff;
            else if(maxP === pCanceladas) pCanceladas += diff;
            else pNaoRealizadas += diff;
        }

        const elPr = document.getElementById('perc-realizadas');
        if(elPr) elPr.innerText = pRealizadas + '%';
        const elPa = document.getElementById('perc-agendadas');
        if(elPa) elPa.innerText = pAgendadas + '%';
        const elPc = document.getElementById('perc-canceladas');
        if(elPc) elPc.innerText = pCanceladas + '%';
        const elPn = document.getElementById('perc-nao-realizadas');
        if(elPn) elPn.innerText = pNaoRealizadas + '%';
        
        const elNr = document.getElementById('num-realizadas');
        if(elNr) elNr.innerText = stats.realizadas;
        const elNa = document.getElementById('num-agendadas');
        if(elNa) elNa.innerText = stats.agendadas;
        const elNc = document.getElementById('num-canceladas');
        if(elNc) elNc.innerText = stats.canceladas;
        const elNn = document.getElementById('num-nao-realizadas');
        if(elNn) elNn.innerText = stats.naorealizadas;
        
        const donut = document.getElementById('status-donut-chart');
        if(donut && totalSemana > 0) {
            const c1 = pRealizadas;
            const c2 = c1 + pAgendadas;
            const c3 = c2 + pCanceladas;
            donut.style.background = `conic-gradient(#2dd4bf 0% ${c1}%, #3b82f6 ${c1}% ${c2}%, #f59e0b ${c2}% ${c3}%, #64748b ${c3}% 100%)`;
        } else if (donut) {
            donut.style.background = '#1e293b';
        }
        
        const daysToShow = [1, 2, 3, 4, 5, 6];"""

content = content.replace(pattern_js, new_js_logic)

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Status chart dynamic logic added.")
