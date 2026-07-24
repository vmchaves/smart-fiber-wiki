---
id: "TEST-OVERVIEW-400"
type: "concept"
title: "Visão Geral da Estratégia de Qualidade e Testes"
description: "Visão geral da estrutura de testes automatizados no backend e frontend, ferramentas utilizadas e métricas de cobertura."
domain: "smart_fiber"
status: "active"
tech_stack:
  - jest
  - supertest
  - biomejs
  - eslint
tags:
  - testing
  - quality-assurance
  - coverage
  - jest
related_files:
  - "../OTDR_FINAL_BACKEND/package.json"
  - "../OTDR_FINAL_BACKEND/test/app.e2e-spec.ts"
  - "../OTDR-v2/package.json"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# TEST-OVERVIEW-400: Visão Geral da Estratégia de Qualidade

> **Resumo Executivo:** Apresentação da arquitetura de testes do ecossistema Smart Fiber, avaliando as ferramentas configuradas e o estado real da automação de testes no backend NestJS e frontend MFE.

---

## 🎯 Estrutura de Testes por Camada

| Camada | Framework de Testes | Linter / Análise Estática | Estado da Automação |
| :--- | :--- | :--- | :--- |
| **Backend (`OTDR_FINAL_BACKEND`)** | Jest `^29.5.0` & Supertest `^7.0.0` | ESLint `^8.0.0` / Prettier `^3.0.0` | Suíte configurada via Nest CLI. Testes unitários dispersos em `src/**/*.spec.ts` e E2E em `test/`. |
| **Frontend (`OTDR-v2`)** | `@types/jest ~29.2.4` (Sem runner) | BiomeJS `1.9.4` & Git Hooks | **Ausência total de testes unitários ou E2E.** A garantia baseia-se unicamente nas checagens de sintaxe do BiomeJS. |

---

## 🔗 Conexões no Grafo (Dependências)
* **Nó Raiz:** [ROOT-INDEX-000: Grafo de Conhecimento](../index.md)
* **Visão Geral Global:** [SYS-OVERVIEW-001: Visão Geral Integrada](../overview.md)
* **Diagnóstico de Qualidade:** [TEST-CASE-401: Diagnóstico Crítico](./test-cases/diagnostico-qualidade.md)
