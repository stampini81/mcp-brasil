# Usando o mcp-brasil em projetos futuros

Este guia mostra como usar o mcp-brasil como um servidor MCP reutilizavel em outros projetos, incluindo projetos Salesforce.

## Quando usar

Use o mcp-brasil quando voce quiser que seu assistente de IA consulte APIs publicas brasileiras durante o desenvolvimento.

Exemplos:

- buscar CEP, CNPJ, bancos e cambio durante implementacao de integracoes
- consultar dados legislativos, compras publicas, transparencia e TCU para automacoes internas
- gerar payloads, validar parametros e explorar APIs brasileiras sem sair do editor
- enriquecer projetos Salesforce com contexto de APIs externas durante desenvolvimento de Apex, LWC, Flow e integracoes

## Modelo recomendado

Trate o mcp-brasil como um catalogo central de integracoes brasileiras.

- Em desenvolvimento: conecte o MCP ao VS Code, Cursor, Claude Desktop ou outro cliente compativel
- Em producao: sistemas como Salesforce normalmente consomem REST/HTTP, nao MCP diretamente
- Para reaproveitamento: mantenha este repositorio como base das features e conecte-o a qualquer novo workspace

## Opcao 1: usar o pacote publicado

Se voce quer apenas consumir o servidor MCP em outro projeto, use o pacote publicado:

```json
{
  "servers": {
    "mcp-brasil": {
      "command": "uvx",
      "args": ["--from", "mcp-brasil", "python", "-m", "mcp_brasil.server"],
      "env": {
        "TRANSPARENCIA_API_KEY": "sua-chave-aqui",
        "DATAJUD_API_KEY": "sua-chave-aqui",
        "META_ACCESS_TOKEN": "seu-token-aqui"
      }
    }
  }
}
```

Essa opcao e a melhor quando o projeto consumidor nao precisa editar o codigo do servidor.

## Opcao 2: usar um clone local deste repositorio

Se voce quer evoluir o catalogo, adicionar APIs como Correios ou ajustar tools, prefira apontar para um clone local do repositorio:

```json
{
  "servers": {
    "mcp-brasil-local": {
      "command": "uv",
      "args": ["run", "python", "-m", "mcp_brasil.server"],
      "cwd": "C:/caminho/para/mcp-brasil",
      "env": {
        "TRANSPARENCIA_API_KEY": "sua-chave-aqui",
        "DATAJUD_API_KEY": "sua-chave-aqui",
        "META_ACCESS_TOKEN": "seu-token-aqui"
      }
    }
  }
}
```

Use essa opcao quando voce quiser manter um MCP proprio para o trabalho e ir adicionando novas integracoes ao longo do tempo.

## Fluxo para projetos futuros

Para cada novo projeto:

1. mantenha este repositorio atualizado em uma pasta central da sua maquina
2. adicione um arquivo `.vscode/mcp.json` no novo workspace
3. aponte esse arquivo para o pacote publicado ou para seu clone local
4. abra o projeto com o agente configurado para usar MCP
5. use as tools do mcp-brasil para pesquisa, validacao de dados e integracoes

## Uso com Salesforce

O melhor uso com Salesforce e separar desenvolvimento de runtime.

### Desenvolvimento

Conecte o MCP ao workspace do projeto Salesforce para ajudar em tarefas como:

- preparar integracoes com APIs brasileiras
- montar exemplos de request/response
- validar dados de CEP, CNPJ ou catalogos publicos
- explorar regras de negocio antes de escrever Apex ou Flow
- gerar testes e massa de dados com base em fontes publicas

### Runtime em producao

Para producao, o padrao recomendado e:

- Salesforce consome APIs REST/HTTP via Named Credentials e callouts
- o MCP fica como ferramenta de apoio ao desenvolvimento, nao como dependencia de runtime

Em outras palavras: use MCP para acelerar o trabalho do time e entender as APIs; use HTTP para a integracao real do sistema em producao.

## Exemplo de perguntas uteis em projetos Salesforce

- "Qual tool do mcp-brasil devo usar para buscar CEP e preencher endereco em um fluxo de cadastro?"
- "Monte um exemplo de integracao Apex consumindo dados de CNPJ e tratando erro 429."
- "Quais APIs publicas brasileiras podem enriquecer um cadastro de fornecedor?"
- "Quero comparar contratos publicos por CNPJ antes de criar uma validacao interna."

## Quando criar uma nova feature

Crie uma nova feature neste repositorio quando a API for util em mais de um projeto.

Boas candidatas:

- Correios
- Receita/CNPJ complementar
- servicos estaduais ou municipais recorrentes
- APIs publicas usadas pelo seu time em mais de um cliente

Para adicionar uma nova API, siga [Adicionando Features](adding-features.md).

## Recomendacao pratica

Se seu objetivo e usar o mcp-brasil em varios projetos futuros, mantenha este repositorio como seu hub de integracoes brasileiras e conecte os workspaces a ele.

Assim voce evita duplicar codigo de integracao dentro de cada projeto e evolui um catalogo unico de tools reutilizaveis.