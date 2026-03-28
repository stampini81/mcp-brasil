"""Constants for the Saúde feature."""

CNES_API_BASE = "https://apidadosabertos.saude.gov.br/cnes"

ESTABELECIMENTOS_URL = f"{CNES_API_BASE}/estabelecimentos"
PROFISSIONAIS_URL = f"{CNES_API_BASE}/profissionais"
TIPOS_URL = f"{CNES_API_BASE}/tipodeestabelecimento"
LEITOS_URL = f"{CNES_API_BASE}/leitos"

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

# Códigos de tipo de unidade para urgência/emergência (CNES)
TIPOS_URGENCIA: dict[str, str] = {
    "36": "Clínica/Centro de Especialidade",
    "39": "Unidade de Serviço de Apoio de Diagnose e Terapia",
    "40": "Unidade Móvel Terrestre",
    "42": "Unidade Móvel de Nível Pré-Hospitalar na Área de Urgência",
    "73": "Pronto Atendimento",
    "74": "Polo Academia da Saúde",
    "76": "Central de Regulação Médica das Urgências",
}
