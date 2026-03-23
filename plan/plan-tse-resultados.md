# Plano: Acesso Completo a Dados de Votação TSE

## Problema

A feature TSE atual usa apenas a API DivulgaCandContas, que retorna votos totalizados por candidato **dentro de um município**, mas **não retorna votação por município para eleições federais** (presidente, senador, deputado federal). O LLM não consegue responder "quantos votos Lula teve em São Paulo?" ou "qual candidato venceu em cada estado?".

## Fontes de Dados Disponíveis

| Fonte | Tipo | Granularidade | Cobertura | Auth |
|-------|------|---------------|-----------|------|
| **resultados.tse.jus.br** (CDN) | JSON estático | País > UF > Município > Zona > Seção | Eleições recentes (2014+) | Nenhuma |
| **dadosabertos.tse.jus.br** (CKAN) | CSV (ZIP) | Município/Zona/Seção | 1933-2024 | Nenhuma |
| **DivulgaCandContas** (já implementado) | REST JSON | Município (1 por vez) | 2010-2024 | Nenhuma |
| **CEPESP Data (FGV)** | REST CSV | País > Seção | 1998-2018 | Nenhuma |

## Estratégia Escolhida: resultados.tse.jus.br (CDN JSON)

**Por quê?**
- JSON nativo (sem parsing CSV)
- Granularidade completa (país → UF → município)
- Dados oficiais do TSE
- Sem autenticação
- Resposta instantânea (arquivos estáticos pré-gerados)
- Rate limit generoso (100 req/s)

**Trade-offs:**
- URLs são estáticas (CDN), não uma REST API queryable
- Precisa navegar hierarquicamente via `ele-c.json` de configuração
- Dados podem ficar offline após certo tempo pós-eleição
- Códigos de município são TSE internos (não IBGE)

## Novas Tools (5)

### 1. `resultado_nacional`
Resultado de um cargo em nível nacional (todos os candidatos, votos totais).
```
resultado_nacional(ano=2022, cargo="presidente", turno=1)
→ Tabela com todos os candidatos rankeados + % votos + situação
```
**Endpoint:** `dados-simplificados/br/br-c0001-e{eleicao}-r.json`

### 2. `resultado_por_estado`
Resultado de um cargo em um estado específico.
```
resultado_por_estado(ano=2022, cargo="presidente", uf="SP", turno=1)
→ Votos de cada candidato em SP + % apurado
```
**Endpoint:** `dados-simplificados/{uf}/{uf}-c{cargo}-e{eleicao}-r.json`

### 3. `mapa_resultado_estados`
Comparação estado-a-estado: quem venceu em cada UF.
```
mapa_resultado_estados(ano=2022, cargo="presidente", turno=2)
→ Tabela: UF | Vencedor | Votos | % | Apuração
```
**Lógica:** Itera sobre as 27 UFs, faz 27 requests ao CDN, extrai o candidato com mais votos de cada estado.

### 4. `resultado_por_municipio`
Resultado de um cargo em um município específico.
```
resultado_por_municipio(ano=2022, cargo="presidente", uf="SP", municipio="São Paulo", turno=1)
→ Votos de cada candidato no município
```
**Endpoint:** `dados/{uf}/{uf}{cod_mun}-c{cargo}-e{eleicao}-u.json` (precisa resolver código TSE do município via config)

### 5. `apuracao_ao_vivo`
Status da apuração (% seções totalizadas, votos válidos, abstenções).
```
apuracao_ao_vivo(ano=2024, cargo="prefeito", uf="SP")
→ % apurada, total eleitores, comparecimento, abstenção
```
**Endpoint:** Mesmo `dados-simplificados`, extrai campos `s`, `pst`, `c`, `a`.

## Mudanças no Código

### `constants.py` — Novas constantes
```python
# API de Resultados (CDN estático)
RESULTADOS_CDN_BASE = "https://resultados.tse.jus.br/oficial"
RESULTADOS_CONFIG_URL = f"{RESULTADOS_CDN_BASE}/comum/config/ele-c.json"

# Mapeamento cargo → código CDN
CARGO_CODES_CDN = {
    "presidente": "0001",
    "governador": "0003",
    "senador": "0005",
    "deputado_federal": "0006",
    "deputado_estadual": "0007",
    "prefeito": "0011",
    "vereador": "0013",
}
```

### `schemas.py` — Novos modelos
```python
class ResultadoEstado(BaseModel):
    """Resultado de uma eleição em um estado/região."""
    uf: str
    total_secoes: int | None = None
    secoes_totalizadas: str | None = None
    pct_apurado: str | None = None
    total_eleitores: int | None = None
    total_comparecimento: int | None = None
    total_abstencoes: int | None = None
    candidatos: list[ResultadoCDN] = []

class ResultadoCDN(BaseModel):
    """Candidato com resultado do CDN de resultados."""
    sequencia: str | None = None
    nome: str | None = None
    numero: str | None = None
    nome_vice: str | None = None
    coligacao: str | None = None
    votos: int | None = None
    percentual: str | None = None
    eleito: bool = False
    situacao: str | None = None

class ConfigEleicao(BaseModel):
    """Configuração de uma eleição no CDN."""
    ciclo: str  # "ele2022"
    codigo_eleicao: str  # "544"
    codigo_pleito: str
    nome: str | None = None
```

### `client.py` — Novas funções

```python
async def buscar_config_eleicao(ano: int, turno: int = 1) -> ConfigEleicao | None:
    """Busca configuração da eleição no CDN (ciclo, código)."""

async def resultado_simplificado(
    ciclo: str, eleicao: str, uf: str, cargo_code: str
) -> ResultadoEstado | None:
    """Busca resultado simplificado de um cargo em uma UF."""

async def resultado_municipio(
    ciclo: str, eleicao: str, uf: str, cod_municipio: str, cargo_code: str
) -> ResultadoEstado | None:
    """Busca resultado de um cargo em um município."""

async def listar_municipios_eleicao(
    ciclo: str, eleicao: str, uf: str
) -> list[dict]:
    """Lista municípios com códigos TSE para uma eleição/UF."""
```

### `server.py` — Registrar 5 novas tools

### Testes — ~40 novos testes
- `test_client.py`: Mock do CDN com respx (config, dados-simplificados, dados municipais)
- `test_tools.py`: Mock client, testa formatação das 5 tools
- `test_integration.py`: E2E com fastmcp.Client

## Fluxo de Resolução de Eleição

O CDN não usa IDs simples. Precisa resolver:
1. `ano + turno` → `ciclo + codigo_eleicao` (via `ele-c.json`)
2. `cargo` string → `cargo_code` (via `CARGO_CODES_CDN`)
3. `municipio` nome → `cod_municipio` TSE (via config do CDN)

A função `buscar_config_eleicao()` faz o passo 1, cacheando o `ele-c.json` com `@ttl_cache`.

## Resource e Prompt

### Resource: `cargos-resultados`
Mapeamento de cargos para consulta de resultados (nome → código CDN).

### Prompt: `analise_resultado_eleicao`
```
analise_resultado_eleicao(ano, cargo, turno)
→ Orienta o LLM a:
  1. Buscar resultado nacional
  2. Buscar mapa por estados
  3. Comparar desempenho dos candidatos
  4. Calcular votação por região
```

## Ordem de Implementação

1. **constants.py** — CDN base URL + cargo codes
2. **schemas.py** — ResultadoCDN, ResultadoEstado, ConfigEleicao
3. **client.py** — buscar_config_eleicao, resultado_simplificado, resultado_municipio
4. **tools.py** — 5 novas tools
5. **resources.py** — cargos-resultados
6. **prompts.py** — analise_resultado_eleicao
7. **server.py** — registrar tudo
8. **Testes** — ~40 testes
9. **TECH_DEBT.md** — atualizar

## Riscos

- **CDN offline** — Dados antigos podem ser removidos. Mitigação: tratar 404 com mensagem clara
- **Formato pode mudar** — CDN é semi-oficial. Mitigação: parser defensivo com fallbacks
- **27 requests para mapa** — `mapa_resultado_estados` faz 27 GETs. Mitigação: `asyncio.gather` paralelo + rate limiter
- **Código município TSE ≠ IBGE** — Precisa lookup via config. Mitigação: cachear `ele-c.json`
