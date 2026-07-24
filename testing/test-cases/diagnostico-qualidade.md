---
id: "TEST-CASE-401"
type: "test_case"
title: "Diagnóstico Crítico de Qualidade e Cobertura de Testes"
description: "Análise profunda das lacunas de cobertura, falta de testes no frontend MFE e falhas na suíte E2E sem mocks de infraestrutura."
domain: "smart_fiber"
status: "active"
tech_stack:
  - jest
  - supertest
tags:
  - testing
  - quality-assurance
  - technical-debt
  - code-coverage
related_files:
  - "../OTDR_FINAL_BACKEND/test/app.e2e-spec.ts"
  - "../OTDR_FINAL_BACKEND/src/pins/pins.service.spec.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# TEST-CASE-401: Diagnóstico Crítico de Qualidade

> **Resumo Executivo:** Avaliação de efetividade e relatório de débitos técnicos identificados nas suítes de testes automatizados do ecossistema Smart Fiber.

---

## 🚨 Diagnóstico de Cobertura e Riscos de Regressão

> [!IMPORTANT]
> **Lacuna Crítica de Testes e Débito Técnico Operacional:**
>
> 1. **Falsa Cobertura Unitária no Backend (Boilerplate de CLI):**
>    - Todos os 10 arquivos `.spec.ts` encontrados na pasta `src/` do backend (como `pins.service.spec.ts`, `alarms.service.spec.ts` e `monitoring.service.spec.ts`) contêm apenas o código de exemplo gerado pelo NestJS CLI:
>      ```typescript
>      it('should be defined', () => {
>        expect(service).toBeDefined();
>      });
>      ```
>    - **Nenhuma regra de negócio real** (como o cálculo de catenária/atenuação em `links.service.ts`, o algoritmo binário em `sorParser.ts`, a validação de permissões no `TenantGuard` ou a fila BullMQ) possui testes unitários ou de integração.
>
> 2. **Falha na Suíte E2E do Backend:**
>    - O único teste End-to-End existente (`test/app.e2e-spec.ts`) é a checagem boilerplate `expect('Hello World!')`.
>    - A execução de `npm run test:e2e` falha imediatamente porque o teste tenta compilar o `AppModule` completo sem fornecer mocks para o MongoDB, Redis ou broker NATS.
>
> 3. **Ausência Total de Testes no Frontend:**
>    - O repositório `OTDR-v2` não possui **nenhum arquivo de teste unitário (`.spec.tsx` ou `.test.ts`)** para os seis micro-frontends. A integridade visual e funcional dos módulos de mapas e gráficos depende exclusivamente de validações manuais.

---

## 📐 Plano de Ação Recomendado para Qualidade

1. **Backend Unit Tests:** Implementar suíte de testes unitários com mocks do MongoDB/Redis cobrindo os métodos de cálculo de atenuação óptica em `links.service.ts` e validação de convites em `invites.controller.ts`.
2. **Backend Integration/E2E Tests:** Configurar `mongodb-memory-server` e mocks Redis no `test/app.e2e-spec.ts` para validar os contratos de API REST sem depender de banco físico.
3. **Frontend Component Tests:** Configurar **Vitest** ou **Jest** com **React Testing Library** no repositório `OTDR-v2` para validar a renderização dos componentes principais dos micro-frontends.

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral de Testes:** [TEST-OVERVIEW-400: Visão Geral](./overview.md)
* **Visão Geral do Backend:** [BE-OVERVIEW-200: Backend NestJS](../../backend/overview.md)
* **Regras de Negócio:** [DOM-RULES-011: Regras e RBAC](../../domain/regras-de-negocio.md)
