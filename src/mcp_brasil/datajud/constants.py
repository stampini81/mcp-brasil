"""Constants for the DataJud (CNJ) feature."""

# API base
DATAJUD_API_BASE = "https://api-publica.datajud.cnj.jus.br/api_publica_"

# Default pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Tribunal endpoint mapping (sigla → sufixo da URL)
TRIBUNAIS: dict[str, str] = {
    # Tribunais Superiores
    "stf": "stf",
    "stj": "stj",
    "tst": "tst",
    "stm": "stm",
    "tse": "tse",
    # Tribunais Regionais Federais
    "trf1": "trf1",
    "trf2": "trf2",
    "trf3": "trf3",
    "trf4": "trf4",
    "trf5": "trf5",
    "trf6": "trf6",
    # Tribunais Regionais do Trabalho
    "trt1": "trt1",
    "trt2": "trt2",
    "trt3": "trt3",
    "trt4": "trt4",
    "trt5": "trt5",
    "trt6": "trt6",
    "trt7": "trt7",
    "trt8": "trt8",
    "trt9": "trt9",
    "trt10": "trt10",
    "trt11": "trt11",
    "trt12": "trt12",
    "trt13": "trt13",
    "trt14": "trt14",
    "trt15": "trt15",
    "trt16": "trt16",
    "trt17": "trt17",
    "trt18": "trt18",
    "trt19": "trt19",
    "trt20": "trt20",
    "trt21": "trt21",
    "trt22": "trt22",
    "trt23": "trt23",
    "trt24": "trt24",
    # Tribunais de Justiça Estaduais
    "tjac": "tjac",
    "tjal": "tjal",
    "tjam": "tjam",
    "tjap": "tjap",
    "tjba": "tjba",
    "tjce": "tjce",
    "tjdft": "tjdft",
    "tjes": "tjes",
    "tjgo": "tjgo",
    "tjma": "tjma",
    "tjmg": "tjmg",
    "tjms": "tjms",
    "tjmt": "tjmt",
    "tjpa": "tjpa",
    "tjpb": "tjpb",
    "tjpe": "tjpe",
    "tjpi": "tjpi",
    "tjpr": "tjpr",
    "tjrj": "tjrj",
    "tjrn": "tjrn",
    "tjro": "tjro",
    "tjrr": "tjrr",
    "tjrs": "tjrs",
    "tjsc": "tjsc",
    "tjse": "tjse",
    "tjsp": "tjsp",
    "tjto": "tjto",
}

# Nomes legíveis dos tribunais
TRIBUNAL_NOMES: dict[str, str] = {
    "stf": "Supremo Tribunal Federal",
    "stj": "Superior Tribunal de Justiça",
    "tst": "Tribunal Superior do Trabalho",
    "stm": "Superior Tribunal Militar",
    "tse": "Tribunal Superior Eleitoral",
    "trf1": "TRF 1ª Região (DF, GO, MT, TO, AC, AM, AP, BA, MA, MG, PA, PI, RO, RR)",
    "trf2": "TRF 2ª Região (RJ, ES)",
    "trf3": "TRF 3ª Região (SP, MS)",
    "trf4": "TRF 4ª Região (RS, PR, SC)",
    "trf5": "TRF 5ª Região (PE, CE, AL, SE, RN, PB)",
    "trf6": "TRF 6ª Região (MG)",
    "tjsp": "Tribunal de Justiça de São Paulo",
    "tjrj": "Tribunal de Justiça do Rio de Janeiro",
    "tjmg": "Tribunal de Justiça de Minas Gerais",
    "tjrs": "Tribunal de Justiça do Rio Grande do Sul",
    "tjpr": "Tribunal de Justiça do Paraná",
    "tjsc": "Tribunal de Justiça de Santa Catarina",
    "tjba": "Tribunal de Justiça da Bahia",
    "tjpe": "Tribunal de Justiça de Pernambuco",
    "tjce": "Tribunal de Justiça do Ceará",
    "tjgo": "Tribunal de Justiça de Goiás",
    "tjdft": "Tribunal de Justiça do Distrito Federal e Territórios",
}

# Classes processuais comuns
CLASSES_PROCESSUAIS: list[dict[str, str]] = [
    {"codigo": "1116", "nome": "Ação Civil Pública"},
    {"codigo": "7", "nome": "Ação Penal - Procedimento Ordinário"},
    {"codigo": "12078", "nome": "Execução Fiscal"},
    {"codigo": "1386", "nome": "Mandado de Segurança Cível"},
    {"codigo": "12158", "nome": "Procedimento Comum Cível"},
    {"codigo": "175", "nome": "Recurso Extraordinário"},
    {"codigo": "205", "nome": "Recurso Especial"},
    {"codigo": "1009", "nome": "Habeas Corpus"},
    {"codigo": "968", "nome": "Habeas Data"},
    {"codigo": "331", "nome": "Ação Direta de Inconstitucionalidade"},
]
