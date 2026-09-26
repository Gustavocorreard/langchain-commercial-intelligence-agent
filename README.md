# LangChain Commercial Intelligence Agent

Commercial intelligence agent built with LangChain to answer business questions using structured SQL data.

> Work in progress — project currently under development.

## Goal

Build an AI agent capable of answering commercial questions in natural language by querying structured business data.

## Architecture

User → LangChain Agent → SQL Tool → SQLite → Agent → Structured Output

## Current progress

- [x] Project environment with uv
- [x] Synthetic commercial dataset
- [x] SQLite relational database
- [x] Data validation
- [ ] LangChain SQL integration
- [ ] SQL tools
- [ ] Agent
- [ ] Structured output
- [ ] LangSmith tracing
- [ ] Automated tests

## Stack

- Python 3.13
- LangChain
- OpenAI
- LangSmith
- SQLite
- SQLAlchemy
- uv
- pytest