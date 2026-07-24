---
id: "DOM-FLOWS-012"
type: "concept"
title: "Fluxogramas e Máquinas de Estado do Sistema"
description: "Coleção de diagramas Mermaid em alta definição representando o fluxo de autenticação/telemetria e as máquinas de estado de convites, medições e agentes."
domain: "smart_fiber"
status: "active"
tech_stack:
  - mermaid
tags:
  - diagrams
  - sequence-diagram
  - state-diagram
  - workflows
related_files:
  - "../OTDR_FINAL_BACKEND/src/measurement/measurement.controller.ts"
  - "../OTDR_FINAL_BACKEND/src/invites/invites.controller.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# DOM-FLOWS-012: Fluxogramas e Máquinas de Estado

> **Resumo Executivo:** Especificação visual dos fluxos críticos de comunicação sequencial e transição de estados das entidades centrais da plataforma.

---

## 🎯 1. Diagrama de Sequência: Autenticação & Telemetria OTDR

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as Navegador (MFE Shell / OTDR)
    participant MFE as Micro-Frontend (SmartSite/OTDR)
    participant API as Backend NestJS (API Gateway)
    participant Auth as Zitadel OIDC Provider
    participant Redis as Redis Cache / Session
    participant Worker as Engine Async (BullMQ / Python)
    participant DB as Mongo Database

    Cliente->>MFE: Acessa rota de Telemetria / Mapa
    MFE->>API: GET /auth/me (x-tenant-id, Bearer JWT)
    API->>Auth: Valida Token & Claims Zitadel
    Auth-->>API: Token Válido (Roles: ORG_OWNER)
    API->>Redis: Consulta Sessão Ativa
    Redis-->>API: OK (padtec_session)
    API-->>MFE: Retorna Usuário, Permissões e UI Flags

    Cliente->>MFE: Executa Upload de Medição (.sor)
    MFE->>API: POST /entities/:id/upload-sor (FormData + sorRaw)
    API->>DB: Salva Registro da Medição (status: PROCESSING)
    API->>Worker: Envia Buffer ao Worker (sorParser.ts)
    Worker->>Worker: Executa child_process (sor_converter.py)
    Worker-->>API: Retorna JSON de Atenuação / Eventos
    API->>DB: Atualiza Medição (status: COMPLETED) + Checa Limites
    API-->>MFE: Evento SSE / WS (otdr_data / measurement_event)
    MFE-->>Cliente: Renderiza Gráfico da Curva Óptica
```

---

## 🎯 2. Diagrama de Estados: Ciclos de Vida das Entidades

```mermaid
stateDiagram-v2
    direction TB

    state "Ciclo de Vida do Convite (Invites)" as Convites {
        [*] --> PENDING: Criado pelo Admin (7 dias expiração)
        PENDING --> ACCEPTED: Usuário aceita e sincroniza com Zitadel
        PENDING --> EXPIRED: Data atual > expiresAt
        PENDING --> REVOKED: Cancelado pelo Administrador
        ACCEPTED --> [*]
        EXPIRED --> [*]
        REVOKED --> [*]
    }

    state "Ciclo de Vida da Medição OTDR (Measurements)" as Medicoes {
        [*] --> QUEUED: Disparo da Medição (BullMQ/NATS)
        QUEUED --> PROCESSING: Worker inicia leitura e parse binario (.sor)
        PROCESSING --> COMPLETED: Sucesso no parse e calculo de atenuação
        PROCESSING --> FAILED: Erro no script Python ou timeout de hardware
        COMPLETED --> ALARMED: Limiar de atenuação superado (LimitDto)
        COMPLETED --> NORMAL: Dentro dos padrões de engenharia
        ALARMED --> [*]
        NORMAL --> [*]
        FAILED --> [*]
    }

    state "Ciclo de Vida do Monitoramento Ativo (Active Agent)" as Monitoramento {
        [*] --> IDLE: Porta OTDR vinculada ao Link
        IDLE --> RUNNING: Agente de disparo periódico sincronizado
        RUNNING --> STOPPED: Interrupção manual ou falha de comunicação
        STOPPED --> RUNNING: Reinicialização do Agente
    }
```

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Domínio:** [DOM-OVERVIEW-010: Visão Geral](./overview.md)
* **Regras de Negócio:** [DOM-RULES-011: Regras e RBAC](./regras-de-negocio.md)
