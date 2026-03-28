"""Saúde feature server — registers tools, resources, and prompts.

This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import analise_rede_saude
from .resources import codigos_uf_cnes
from .tools import (
    buscar_estabelecimento_por_cnes,
    buscar_estabelecimentos,
    buscar_por_coordenadas,
    buscar_por_tipo,
    buscar_profissionais,
    buscar_urgencias,
    comparar_municipios,
    consultar_leitos,
    listar_tipos_estabelecimento,
    resumo_rede_municipal,
)

mcp = FastMCP("mcp-brasil-saude")

# Tools (10)
mcp.tool(buscar_estabelecimentos, tags={"busca", "estabelecimentos", "cnes", "sus"})
mcp.tool(buscar_profissionais, tags={"busca", "profissionais", "cnes"})
mcp.tool(listar_tipos_estabelecimento, tags={"listagem", "estabelecimentos", "tipos"})
mcp.tool(consultar_leitos, tags={"consulta", "leitos", "hospitalares"})
mcp.tool(buscar_urgencias, tags={"busca", "urgencia", "upa", "pronto-socorro", "emergencia"})
mcp.tool(buscar_por_tipo, tags={"busca", "estabelecimentos", "tipo", "cnes"})
mcp.tool(buscar_estabelecimento_por_cnes, tags={"consulta", "estabelecimento", "detalhe", "cnes"})
mcp.tool(buscar_por_coordenadas, tags={"busca", "estabelecimentos", "coordenadas", "proximidade"})
mcp.tool(resumo_rede_municipal, tags={"analise", "rede", "municipal", "resumo"})
mcp.tool(comparar_municipios, tags={"analise", "comparacao", "municipios"})

# Resources (URIs without namespace prefix — mount adds "saude/" automatically)
mcp.resource("data://codigos-uf", mime_type="application/json")(codigos_uf_cnes)

# Prompts
mcp.prompt(analise_rede_saude)
