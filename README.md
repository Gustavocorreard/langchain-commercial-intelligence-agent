# LangChain Commercial Intelligence Agent

Agente de inteligência comercial construído com LangChain para responder perguntas de negócio utilizando dados estruturados em SQL.

> Projeto em desenvolvimento.

## Objetivo

Construir um agente de IA capaz de responder perguntas comerciais em linguagem natural consultando dados estruturados de negócio.

## Arquitetura

User → LangChain Agent → SQL Tool → SQLite → Agent → Structured Output

## Progresso atual

- [x] Configuração do projeto com uv
- [x] Dataset comercial sintético
- [x] Banco relacional em SQLite
- [x] Validação dos dados
- [ ] Integração SQL com LangChain
- [ ] SQL Tools
- [ ] Agent
- [ ] Structured Output
- [ ] Observabilidade com LangSmith
- [ ] Testes automatizados

## Stack

- Python 3.13
- LangChain
- OpenAI
- LangSmith
- SQLite
- SQLAlchemy
- uv
- pytest

## Próximos passos

- Integrar o LangChain ao banco SQLite
- Criar as ferramentas SQL
- Construir o agente
- Implementar saída estruturada
- Adicionar tracing com LangSmith
- Criar testes automatizados

## Evolução futura

Em uma segunda versão, o agente também poderá consultar documentos utilizando RAG, combinando dados estruturados em SQL com informações não estruturadas.