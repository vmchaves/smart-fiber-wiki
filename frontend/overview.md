---
id: "FE-OVERVIEW-100"
type: "concept"
title: "Visão Geral do Frontend - Arquitetura de Micro-Frontends"
description: "Visão geral da arquitetura de apresentação em Micro-Frontends baseada em Modern.js, Module Federation e React 18 (OTDR-v2)."
domain: "smart_fiber"
status: "active"
tech_stack:
  - react
  - typescript
  - modernjs
  - module-federation
  - pnpm
  - biomejs
  - recharts
  - echarts
  - turf
tags:
  - frontend
  - micro-frontends
  - react
  - architecture
related_files:
  - "../OTDR-v2/package.json"
  - "../OTDR-v2/docker-compose.yml"
  - "../OTDR-v2/nginx-proxy.conf"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# FE-OVERVIEW-100: Visão Geral do Frontend

> **Resumo Executivo:** A camada de interface do usuário do ecossistema Smart Fiber é construída sobre uma arquitetura de **Micro-Frontends (MFEs)** orquestrada pelo framework **Modern.js** e **Module Federation**, permitindo builds e deploys independentes para cada módulo da plataforma.

---

## 🎯 Visão Geral da Arquitetura MFE

A aplicação `OTDR-v2` utiliza a abordagem de micro-frontends para separar as responsabilidades visuais da plataforma em seis aplicações autônomas e três pacotes de código compartilhado.

```mermaid
graph TD
    Shell["mfe-shell (Orquestrador / Container Host)"] --> LoginMFE["mfe-login"]
    Shell --> MapMFE["mfe-map"]
    Shell --> OtdrMFE["mfe-otdr"]
    Shell --> SmartSiteMFE["mfe-smartsite"]
    Shell --> SidebarMFE["mfe-sidebar"]

    subgraph SharedPackages ["Packages Compartilhados"]
        Design["shared_design (Design System)"]
        ReactPkg["shared_react (Hooks & Contexts)"]
        ServicesPkg["shared_services (Clients HTTP & Sockets)"]
    end

    Shell --> SharedPackages
    OtdrMFE --> SharedPackages
    MapMFE --> SharedPackages
```

---

## 📐 Tecnologias e Otimizações de Build

1. **Meta-Framework Modern.js (`2.68.20`):** Prover estrutura React enterprise com suporte a bundling ultra-otimizado e gerenciamento nativo de exposições de Module Federation.
2. **Monorepo com PNPM Workspaces (`v11`):** Gerenciamento eficiente de dependências compartilhadas via links simbólicos sem duplicação de pacotes em disco.
3. **Análise Estática com BiomeJS (`1.9.4`):** Formatação de código e verificação de lint executada instantaneamente nos hooks de pre-commit.
4. **Visualização de Gráficos e GIS:** Integração com **Recharts** e **Echarts** para curvas de atenuação OTDR e **Turf.js** para cálculos espaciais de polígonos e distâncias no mapa.

---

## 🔗 Conexões no Grafo (Dependências)
* **Nó Raiz:** [ROOT-INDEX-000: Grafo de Conhecimento](../index.md)
* **Visão Geral Global:** [SYS-OVERVIEW-001: Visão Geral Integrada](../overview.md)
* **Componentes MFE:** [FE-COMP-101: Micro-Frontends](./components/micro-frontends.md)
* **API Client & WebSockets:** [FE-SERV-102: Client Services](./services/api-client.md)
