---
id: "FE-COMP-101"
type: "component"
title: "Mapeamento dos Micro-Frontends e Pacotes Compartilhados"
description: "Detalhamento funcional e de responsabilidade de cada micro-frontend (shell, login, otdr, map, sidebar, smartsite) e pacotes compartilhados."
domain: "smart_fiber"
status: "active"
tech_stack:
  - react
  - typescript
  - modernjs
  - module-federation
tags:
  - frontend
  - micro-frontends
  - components
related_files:
  - "../OTDR-v2/apps/shell/package.json"
  - "../OTDR-v2/apps/otdr-mfe/package.json"
  - "../OTDR-v2/apps/smartsite-mfe/package.json"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# FE-COMP-101: Mapeamento dos Micro-Frontends e Pacotes

> **Resumo Executivo:** Mapeamento exaustivo das 6 aplicações de Micro-Frontend e 3 pacotes compartilhados que compõem o repositório `OTDR-v2`.

---

## 🎯 Aplicações Micro-Frontend (`apps/`)

### 1. `shell` (Host Application)
- **Papel:** Aplicação container responsável por orquestrar a carga dinâmica dos MFEs remotos, gerenciar a rota principal, manter o contexto do usuário autenticado e renderizar o layout global (Header, Sidebar Container).

### 2. `login-mfe`
- **Papel:** Módulo de autenticação e gerenciamento de entrada. Interface para credenciais de acesso, fluxo de recuperação de senha e redirecionamento OIDC federado via Zitadel.

### 3. `otdr-mfe`
- **Papel:** Módulo especialista em Reflectometria Óptica. Responsável pelo gráfico interativo da curva de atenuação (dB x km), tabela de eventos ópticos, configuração de limiares de engenharia e disparos manuais de medição.

### 4. `smartsite-mfe`
- **Papel:** Módulo GIS de topologia física de rede. Exibe o mapa interativo com renderização de Sites e Links por coordenadas GeoJSON, suportando arrastar-e-soltar, zoom por `viewport` (bounding box) e pins em tempo real via WebSockets.

### 5. `map-mfe`
- **Papel:** Módulo auxiliar de mapas de calor, rotas de fibra e sobreposição de camadas cartográficas.

### 6. `sidebar-mfe`
- **Papel:** Menu de navegação lateral expansível, com controle de permissões por perfil (RBAC) e alternância de workspaces (`tenants`).

---

## 📐 Pacotes Compartilhados (`packages/`)

- **`shared_design`:** Biblioteca de componentes visuais base (botões, inputs, modais, temas dark/light, tokens CSS).
- **`shared_react`:** Providers de contexto React compartilhados (`AuthContext`, `TenantContext`, `ThemeContext`).
- **`shared_services`:** Clientes reutilizáveis de API HTTP (Axios) e gerenciadores de conexão Socket.io.

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Frontend:** [FE-OVERVIEW-100: Visão Geral](./overview.md)
* **API Client Services:** [FE-SERV-102: API Client](./services/api-client.md)
