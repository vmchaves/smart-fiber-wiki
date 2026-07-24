---
id: "BE-API-201"
type: "api"
title: "Compilação Exaustiva da Tabela de Endpoints da API"
description: "Mapeamento completo de todos os endpoints HTTP, Server-Sent Events (SSE) e WebSockets expostos pelo backend NestJS."
domain: "smart_fiber"
status: "active"
tech_stack:
  - typescript
  - nestjs
  - REST
  - SSE
  - websocket
tags:
  - backend
  - api
  - endpoints
  - swagger
related_files:
  - "../OTDR_FINAL_BACKEND/src/auth/auth.controller.ts"
  - "../OTDR_FINAL_BACKEND/src/invites/invites.controller.ts"
  - "../OTDR_FINAL_BACKEND/src/entities/entities.controller.ts"
  - "../OTDR_FINAL_BACKEND/src/otdr/otdr.controller.ts"
  - "../OTDR_FINAL_BACKEND/src/measurement/measurement.controller.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# BE-API-201: Compilação Exaustiva de Endpoints da API

> **Resumo Executivo:** Mapeamento exaustivo de todos os contratos de API RESTful, streaming Server-Sent Events (SSE) e gateways WebSockets expostos pelo ecossistema Smart Fiber.

---

## 🎯 Tabela de Endpoints da API

| Categoria | Método | Rota | Autenticação Exigida | Parâmetros (Path/Query) | Body DTO | Resposta de Sucesso (200/201) | Erros Possíveis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Auth** | `GET` | `/auth/me` | JWT Bearer | N/A | N/A | Objeto do usuário e organizações | `401 Unauthorized` |
| **Auth** | `POST` | `/auth/refresh` | Public | N/A | `{ refreshToken: string }` | Novo JWT Access Token | `400 Bad Request`, `401` |
| **Auth** | `POST` | `/auth/me/ui-flags` | JWT Bearer | N/A | `{ product: string, flag: string, value: any }` | State atualizado de flags | `400 Bad Request` |
| **Invites** | `POST` | `/invites` | JWT Bearer (Admin) | N/A | `{ email: string, role: string }` | `{ success: true, message: string }` | `400`, `409 Conflict` |
| **Invites** | `GET` | `/invites/details/:token` | Public | Path: `token` | N/A | `{ tenantName, invitedByName, role, email }` | `404 Not Found`, `400 Expired` |
| **Invites** | `POST` | `/invites/accept` | JWT Bearer | N/A | `{ token: string }` | `{ success: true, tenantId: string }` | `400`, `403 Forbidden`, `500` |
| **Onboarding**| `POST` | `/onboarding/setup` | JWT Bearer | N/A | `SetupAccountDto` | `{ tenantId: string, status: string }` | `400`, `409 Conflict` |
| **License** | `GET` | `/license/active` | JWT Bearer | Query: `product` | N/A | Dados da licença e limites | `404 Not Found` |
| **Entities** | `GET` | `/entities/viewport` | JWT Bearer | Query: `bounds` (`ViewportDto`) | N/A | GeoJSON FeatureCollection de elementos | `400 Bad Request` |
| **Entities** | `POST` | `/entities` | JWT Bearer | N/A | `CreateEntityDto` | Objeto da entidade criada com `_id` | `400 Validation Error` |
| **Entities** | `POST` | `/entities/:id/upload-sor`| JWT Bearer | Path: `id` | FormData (`file`, `otdrId`, `port`) | Objeto do traço analisado | `400 Invalid SOR Format` |
| **Entities** | `PATCH`| `/entities/move` | JWT Bearer | N/A | `UpdateOrderItemDto[]` | Status de reordenação | `400 Bad Request` |
| **Pins** | `POST` | `/pins` | JWT Bearer | N/A | `CreatePinDto` | Pin geoespacial criado | `400 Validation Error` |
| **OTDR** | `POST` | `/otdr/test-connection` | JWT Bearer | N/A | `TestConnectionDto` | `{ connected: boolean, latencyMs: number }` | `504 Gateway Timeout` |
| **OTDR** | `PATCH`| `/otdr/limits` | JWT Bearer | N/A | `CreateLimitDto` | Configuração de limiares salva | `400 Bad Request` |
| **OTDR** | `POST` | `/otdr/measure/:otdrId/:port` | JWT Bearer | Path: `otdrId`, `port` | Options de medição | ID da medição em fila | `500 Hardware Error` |
| **Measurements**| `GET`| `/measurements/:id/download`| JWT Bearer | Path: `id` | N/A | Stream `application/octet-stream` (.sor) | `404 Not Found` |
| **Monitoring** | `POST` | `/monitoring/:otdrId/:port/sync-agent` | JWT Bearer | Path: `otdrId`, `port` | N/A | Status do agente ativo | `409 Agent Conflict` |

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Backend:** [BE-OVERVIEW-200: Visão Geral](./overview.md)
* **Core Services:** [BE-SERV-202: Serviços Backend](../services/core-services.md)
* **DTOs e Schemas:** [BE-MODEL-203: DTOs e Schemas](../models/dtos-and-entities.md)
