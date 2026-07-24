---
id: "DOM-RULES-011"
type: "concept"
title: "Regras de Negócio, Validações Físicas e Matriz RBAC"
description: "Detalhamento exaustivo das regras de negócio, limites de engenharia óptica, regras de isolamento multi-tenant e matriz de permissões RBAC."
domain: "smart_fiber"
status: "active"
tech_stack:
  - typescript
  - nestjs
  - class-validator
tags:
  - domain
  - business-rules
  - rbac
  - validation
related_files:
  - "../OTDR_FINAL_BACKEND/src/invites/invites.controller.ts"
  - "../OTDR_FINAL_BACKEND/src/otdr/dto/create-limit.dto.ts"
  - "../OTDR_FINAL_BACKEND/src/auth/guards/tenant.guard.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# DOM-RULES-011: Regras de Negócio, Validações Físicas e Matriz RBAC

> **Resumo Executivo:** Especificação detalhada das regras operacionais do negócio, incluindo a lógica matemática de engenharia óptica, controle de convites/licenciamento e autorização por papéis (RBAC).

---

## 🎯 Regras Globais de Negócio

### 1. Gestão de Convites e Onboarding Multi-Tenant
- **Criação de Convite:** Usuários administradores enviam convites (`POST /invites`) especificando e-mail e papel (`role`). O convite recebe um token hexadecimal seguro de 32 bytes com validade estrita de **7 dias** (`expiresAt`).
- **Unicidade de Membro:** Se o e-mail convidado já possuir uma licença ativa (`status: 'ACTIVE'`) no mesmo tenant, a criação do convite é rejeitada com `409 ConflictException`.
- **Aceitação e Hard-Sync:** Ao aceitar um convite (`POST /invites/accept`), o backend efetua uma chamada obrigatória à API do **Zitadel** (`grantUserOrgRole`). Caso o Zitadel retorne falha, a operação no banco de dados MongoDB é cancelada (`500 InternalServerErrorException`).

### 2. Cálculos Físicos de Engenharia Óptica (Catenária e Atenuação)
- **Fórmula de Distância Real do Cabo:** A distância óptica calculada para um enlace compensa o trajeto geodésico multiplicando pelo fator de catenária e adicionando as folgas técnicas reservadas:
  $$\text{Distância Total} = (\text{Distância GIS} \times \text{catenaryFactor}) + (N_{\text{caixas}} \times \text{slackPerBox}) + (N_{\text{postes}} \times \text{slackPerPole})$$
- **Disparo de Alarme:** Se o valor da atenuação medida pelo OTDR superar o campo `maxAttenuation` definido no `CreateLimitDto`, a medição assume o status `ALARMED` e gera alertas instantâneos no WebSocket (`/telemetry`).

---

## 📐 Matriz de Permissões e Papéis (RBAC)

A autorização no sistema é mapeada a partir dos papéis configurados na organização do Zitadel.

| Perfil (Role) | Papel Zitadel | Recursos Acessíveis | Operações Permitidas (CRUD) |
| :--- | :--- | :--- | :--- |
| **Admin (Org Owner)** | `ORG_OWNER` | Todo o workspace, Membros, Convites, Limites de Engenharia, Equipamentos OTDR e Configurações Globais | **CRUD Completo:** Gerenciar workspace, aceitar/revogar convites, alterar limiares de engenharia, deletar elementos no mapa. |
| **Member (User)** | `ORG_USER` | Topologia no Mapa, Disparo de Medições OTDR, Upload de Arquivos `.sor` e Visualização de Alertas | **CRU Parcial:** Criar elementos no mapa, disparar medições manuais, importar mídias `.sor`. Sem acesso a convites de admin ou limiares globais. |
| **Viewer** | `ORG_OWNER_VIEWER` | Visualização do Mapa, Leitura do Histórico de Medições e Acompanhamento do Monitoramento Live | **Leitura Apenas (Read-Only):** `GET` liberado em `/entities`, `/measurements` e `/otdr/limits`. Bloqueado para `POST`, `PATCH` ou `DELETE`. |

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Domínio:** [DOM-OVERVIEW-010: Visão Geral](./overview.md)
* **Fluxogramas:** [DOM-FLOWS-012: Diagramas Mermaid](./fluxogramas.md)
* **Backend Models:** [BE-MODEL-203: DTOs e Schemas](../backend/models/dtos-and-entities.md)
