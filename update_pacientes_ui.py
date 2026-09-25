import re

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\pacientes.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Novo Paciente button
btn_html = """<div>
          <button class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-2 transition-colors" onclick="openModalPaciente()">
            <i class="ph ph-plus text-lg"></i> Novo Paciente
          </button>
        </div>"""
content = content.replace("""<div>
          
        </div>""", btn_html)

# 2. Add Modal HTML before </main>
modal_html = """
      <!-- Modal Paciente -->
      <div id="modal-paciente" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center">
        <div class="bg-[#131c31] border border-[#1e293b] rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl">
          <div class="px-6 py-4 border-b border-[#1e293b] flex justify-between items-center">
            <h2 class="text-xl font-bold text-white" id="modal-paciente-title">Novo Paciente</h2>
            <button onclick="closeModalPaciente()" class="text-slate-400 hover:text-white transition-colors"><i class="ph ph-x text-xl"></i></button>
          </div>
          <div class="p-6">
            <form id="form-paciente" class="grid grid-cols-2 gap-4">
              <input type="hidden" id="paciente-id">
              <div class="col-span-2">
                <label class="block text-xs font-semibold text-slate-400 mb-1">Nome Completo</label>
                <input type="text" id="paciente-nome" required class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-semibold text-slate-400 mb-1">E-mail</label>
                <input type="email" id="paciente-email" required class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
              <div class="col-span-1" id="div-senha">
                <label class="block text-xs font-semibold text-slate-400 mb-1">Senha de Acesso</label>
                <input type="password" id="paciente-senha" class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-semibold text-slate-400 mb-1">CPF</label>
                <input type="text" id="paciente-cpf" required class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-semibold text-slate-400 mb-1">Telefone</label>
                <input type="text" id="paciente-telefone" class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-semibold text-slate-400 mb-1">Data de Nascimento</label>
                <input type="date" id="paciente-nascimento" class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-semibold text-slate-400 mb-1">Gênero</label>
                <select id="paciente-genero" class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
                  <option value="">Selecione</option>
                  <option value="M">Masculino</option>
                  <option value="F">Feminino</option>
                  <option value="O">Outro</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-xs font-semibold text-slate-400 mb-1">Endereço</label>
                <input type="text" id="paciente-endereco" class="w-full bg-[#0b1221] border border-[#1e293b] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500">
              </div>
            </form>
          </div>
          <div class="px-6 py-4 bg-[#0b1221] border-t border-[#1e293b] flex justify-end gap-3">
            <button onclick="closeModalPaciente()" class="px-4 py-2 rounded-lg font-bold text-sm text-slate-300 hover:text-white transition-colors">Cancelar</button>
            <button onclick="salvarPaciente()" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-bold text-sm transition-colors">Salvar Paciente</button>
          </div>
        </div>
      </div>
"""
content = content.replace('</main>', modal_html + '\n    </main>')

# 3. Add Ações column to table
content = content.replace('<th>Telefone</th>', '<th>Telefone</th>\n                                <th>Ações</th>')

# 4. Modify carregarPacientes to render "Editar" button
js_table_logic = """
                    const initial = p.user.nome ? p.user.nome.charAt(0).toUpperCase() : '?';
                    let rawData = JSON.stringify(p).replace(/'/g, "&#39;").replace(/"/g, '&quot;');
                    
                    html += `
                        <tr>
                            <td>
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-full bg-[#1e293b] flex items-center justify-center font-bold text-white text-xs shrink-0">${initial}</div>
                                    <span class="font-bold text-white">${p.user.nome}</span>
                                </div>
                            </td>
                            <td>${p.cpf}</td>
                            <td>${dataNasc}</td>
                            <td>${telefone}</td>
                            <td>
                                <button onclick="openModalPaciente(true, '${rawData}')" class="text-blue-400 hover:text-blue-300 text-sm font-bold transition-colors">Editar</button>
                            </td>
                        </tr>
                    `;
"""
# Replace the original inner table body loop in JS
old_loop_logic = r"""const initial = p\.user\.nome \? p\.user\.nome\.charAt\(0\)\.toUpperCase\(\) : '\?';.*?</tr>\s*`;"""
content = re.sub(old_loop_logic, js_table_logic, content, flags=re.DOTALL)


# 5. Add JS functions for Modal
js_modal_functions = """
        function openModalPaciente(isEdit = false, rawData = null) {
            const modal = document.getElementById('modal-paciente');
            const title = document.getElementById('modal-paciente-title');
            const divSenha = document.getElementById('div-senha');
            const inputSenha = document.getElementById('paciente-senha');
            
            document.getElementById('form-paciente').reset();
            document.getElementById('paciente-id').value = '';
            
            if(isEdit && rawData) {
                const p = JSON.parse(rawData);
                title.innerText = 'Editar Paciente';
                divSenha.classList.add('hidden'); // Hide password on edit for now
                inputSenha.removeAttribute('required');
                
                document.getElementById('paciente-id').value = p.id;
                document.getElementById('paciente-nome').value = p.user.nome || '';
                document.getElementById('paciente-email').value = p.user.email || '';
                document.getElementById('paciente-cpf').value = p.cpf || '';
                document.getElementById('paciente-telefone').value = p.telefone || '';
                document.getElementById('paciente-nascimento').value = p.data_nascimento || '';
                document.getElementById('paciente-genero').value = p.genero || '';
                document.getElementById('paciente-endereco').value = p.endereco || '';
            } else {
                title.innerText = 'Novo Paciente';
                divSenha.classList.remove('hidden');
                inputSenha.setAttribute('required', 'required');
            }
            
            modal.classList.remove('hidden');
        }

        function closeModalPaciente() {
            document.getElementById('modal-paciente').classList.add('hidden');
        }

        async function salvarPaciente() {
            const form = document.getElementById('form-paciente');
            if(!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            
            const id = document.getElementById('paciente-id').value;
            const isEdit = !!id;
            
            const payload = {
                nome: document.getElementById('paciente-nome').value,
                email: document.getElementById('paciente-email').value,
                cpf: document.getElementById('paciente-cpf').value,
                telefone: document.getElementById('paciente-telefone').value,
                data_nascimento: document.getElementById('paciente-nascimento').value || null,
                genero: document.getElementById('paciente-genero').value || null,
                endereco: document.getElementById('paciente-endereco').value || null
            };
            
            try {
                if(isEdit) {
                    await window.api.updatePaciente(id, payload);
                    window.showToast('Paciente atualizado com sucesso!');
                } else {
                    payload.password = document.getElementById('paciente-senha').value;
                    await window.api.createPaciente(payload);
                    window.showToast('Paciente cadastrado com sucesso!');
                }
                closeModalPaciente();
                carregarPacientes(currentPage);
            } catch(e) {
                alert('Erro: ' + e.message);
            }
        }
"""
content = content.replace('async function carregarPacientes', js_modal_functions + '\n        async function carregarPacientes')

with open(r'c:\Users\Public\ClinicFlow\clinicflow\frontend\pacientes.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("UI applied.")
