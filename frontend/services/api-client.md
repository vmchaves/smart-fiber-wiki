---
id: "FE-SERV-102"
type: "service"
title: "Clientes HTTP, Gerenciamento de Sessão e WebSockets"
description: "Documentação dos serviços de comunicação HTTP via Axios, fluxo de interceptors para JWT/Tenant e gateways WebSocket com Socket.io."
domain: "smart_fiber"
status: "active"
tech_stack:
  - typescript
  - axios
  - socket.io-client
tags:
  - frontend
  - http-client
  - sockets
  - session
related_files:
  - "../OTDR-v2/packages/shared_services/src/api.ts"
  - "../OTDR-v2/apps/smartsite-mfe/src/hooks/useSmartSiteLive.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# FE-SERV-102: Clientes HTTP, Sessão e WebSockets

> **Resumo Executivo:** Especificação das rotinas de comunicação de rede no frontend, incluindo a injeção declarativa de headers de tenant, gerenciamento de tokens JWT e canais Socket.io em tempo real.

---

## 🎯 Clientes HTTP (Axios Interceptors)

Toda comunicação REST entre o frontend e a API NestJS utiliza uma instância centralizada do **Axios** em `packages/shared_services`.

### 1. Injeção Automática de Cabeçalhos
- **`Authorization`:** Envia o Bearer Token obtido via OIDC / Zitadel.
- **`x-tenant-id`:** Lê a chave `active_tenant` armazenada no `localStorage` e injeta em cada requisição para garantir a contextualização multi-tenant no backend.

### 2. Tratamento do Refresh Token (HTTP 401)
- Quando a API responde com erro `401 Unauthorized`, o interceptor do Axios pausa as requisições na fila, aciona o endpoint `POST /auth/refresh` e reenvia as chamadas originais com a nova chave JWT.

---

## 📐 Comunicação em Tempo Real (WebSockets & Socket.io)

O frontend mantém duas conexões ativas com o servidor Socket.io:

1. **Namespace `/telemetry`:** Subscreve os eventos `otdr_data` e `measurement_event` para atualizar o gráfico de atenuação live durante medições de hardware.
2. **Namespace `/pins`:** Subscreve o canal de movimentação e criação de pins/sites no SmartSite MFE.

> [!WARNING]
> **Alerta de Hardcode em Produção:** No arquivo `apps/smartsite-mfe/src/hooks/useSmartSiteLive.ts`, a URL do Socket encontra-se definida estaticamente como `http://localhost:4000/pins`. Em ambiente conteinerizado corporativo, esta variável deve ser substituída por `process.env.PUBLIC_SOCKET_URL`.

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Frontend:** [FE-OVERVIEW-100: Visão Geral](./overview.md)
* **MFE Components:** [FE-COMP-101: Micro-Frontends](./components/micro-frontends.md)
* **Endpoints Backend:** [BE-API-201: Endpoints API](../backend/api/endpoints.md)
