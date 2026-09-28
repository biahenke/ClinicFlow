"""
ClinicFlow SOAP Service
Expõe operações de consulta via protocolo SOAP 1.1 com contrato WSDL.
"""
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Array
from spyne.protocol.soap import Soap11
from spyne.server import WsgiApplication
from spyne.model.complex import ComplexModel


# ─── Modelos de Dados SOAP ──────────────────────────────────────────────────

class ConsultaSOAP(ComplexModel):
    """Representação de uma consulta médica no contrato SOAP."""
    id = Integer
    paciente = Unicode
    medico = Unicode
    especialidade = Unicode
    data = Unicode
    horario = Unicode
    status = Unicode


class MedicoSOAP(ComplexModel):
    """Representação de um médico no contrato SOAP."""
    id = Integer
    nome = Unicode
    crm = Unicode
    especialidade = Unicode
    telefone = Unicode


class PacienteSOAP(ComplexModel):
    """Representação de um paciente no contrato SOAP."""
    id = Integer
    nome = Unicode
    cpf = Unicode
    telefone = Unicode


# ─── Serviço SOAP Principal ─────────────────────────────────────────────────

class ClinicFlowSOAPService(ServiceBase):
    """
    ClinicFlow SOAP WebService
    Permite consultar dados do sistema via protocolo SOAP 1.1.
    Contrato disponível em: GET /soap?wsdl
    """

    @rpc(Unicode, _returns=Unicode)
    def health_check(ctx, message):
        """
        Verifica o status do serviço SOAP.
        Parâmetro: message (ex: 'ping')
        Retorna: mensagem de confirmação do servidor
        """
        return f"ClinicFlow SOAP Service OK — recebido: {message}"

    @rpc(Integer, _returns=ConsultaSOAP)
    def get_consulta_by_id(ctx, consulta_id):
        """
        Retorna os dados de uma consulta pelo ID.
        Simula busca no banco de dados para demonstração do contrato SOAP.
        """
        # Dados simulados para demonstração do contrato WSDL
        consulta = ConsultaSOAP()
        consulta.id = consulta_id
        consulta.paciente = "Maria Silva"
        consulta.medico = "Dr. João Carvalho"
        consulta.especialidade = "Cardiologia"
        consulta.data = "2026-10-15"
        consulta.horario = "14:00"
        consulta.status = "agendada"
        return consulta

    @rpc(Unicode, _returns=Array(MedicoSOAP))
    def listar_medicos_por_especialidade(ctx, especialidade):
        """
        Lista médicos filtrados por especialidade.
        Parâmetro: especialidade (ex: 'Cardiologia')
        Retorna: lista de médicos da especialidade informada
        """
        medico1 = MedicoSOAP()
        medico1.id = 1
        medico1.nome = "Dr. João Carvalho"
        medico1.crm = "CRM/SP 12345"
        medico1.especialidade = especialidade
        medico1.telefone = "(11) 99999-1111"

        medico2 = MedicoSOAP()
        medico2.id = 2
        medico2.nome = "Dra. Ana Lima"
        medico2.crm = "CRM/SP 67890"
        medico2.especialidade = especialidade
        medico2.telefone = "(11) 99999-2222"

        return [medico1, medico2]

    @rpc(Unicode, _returns=PacienteSOAP)
    def buscar_paciente_por_cpf(ctx, cpf):
        """
        Busca dados de um paciente pelo CPF.
        Parâmetro: cpf (ex: '123.456.789-00')
        Retorna: dados do paciente
        """
        paciente = PacienteSOAP()
        paciente.id = 1
        paciente.nome = "Maria Silva"
        paciente.cpf = cpf
        paciente.telefone = "(11) 98765-4321"
        return paciente


# ─── Configuração da Aplicação WSGI ─────────────────────────────────────────

def create_soap_app():
    """Cria e retorna a aplicação WSGI do serviço SOAP."""
    soap_app = Application(
        services=[ClinicFlowSOAPService],
        tns="clinicflow.soap",
        name="ClinicFlowSOAP",
        in_protocol=Soap11(validator="lxml"),
        out_protocol=Soap11(),
    )
    return WsgiApplication(soap_app)
