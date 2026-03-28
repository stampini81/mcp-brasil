"""Static reference data for the Diário Oficial feature."""

from __future__ import annotations

import json

from .constants import (
    CAPITAIS_COBERTAS,
    DOU_SECTIONS_INFO,
    DOU_TIPOS_PUBLICACAO,
    UFS_COBERTAS,
)


def capitais_cobertas() -> str:
    """Capitais brasileiras com cobertura confirmada no Querido Diário."""
    data = [
        {"codigo_ibge": k, "cidade": v}
        for k, v in sorted(CAPITAIS_COBERTAS.items(), key=lambda x: x[1])
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)


def ufs_com_cobertura() -> str:
    """UFs brasileiras com municípios cobertos no Querido Diário."""
    return json.dumps(UFS_COBERTAS, ensure_ascii=False, indent=2)


def dicas_busca_diario() -> str:
    """Dicas para otimizar buscas em diários oficiais municipais e federais."""
    return json.dumps(
        {
            "busca_exata": 'Use aspas para termos exatos: "pregão eletrônico"',
            "cnpj": "Busque por CNPJ sem pontuação: 12345678000190",
            "operadores": "Use AND/OR: licitação AND pregão",
            "datas": "Formato YYYY-MM-DD para filtros de data",
            "multiplos_municipios": "Use territory_ids com lista de códigos IBGE",
            "ordenacao": "sort_by=descending_date para resultados mais recentes",
        },
        ensure_ascii=False,
        indent=2,
    )


def secoes_dou() -> str:
    """Seções do DOU e seus conteúdos típicos."""
    return json.dumps(DOU_SECTIONS_INFO, ensure_ascii=False, indent=2)


def tipos_publicacao_dou() -> str:
    """Tipos de publicação do DOU (decreto, portaria, lei, etc.)."""
    return json.dumps(DOU_TIPOS_PUBLICACAO, ensure_ascii=False, indent=2)
