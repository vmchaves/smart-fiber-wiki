---
id: "INFRA-CICD-302"
type: "infra"
title: "Esteira CI/CD de Build e Implantação Automatizada"
description: "Fluxograma e explicação detalhada dos workflows do GitHub Actions Self-Hosted para Backend e Micro-Frontends."
domain: "smart_fiber"
status: "active"
tech_stack:
  - github-actions
  - harbor
  - docker
  - pnpm
tags:
  - infra
  - ci-cd
  - github-actions
  - harbor
related_files:
  - "../OTDR_FINAL_BACKEND/.github/workflows/deploy-backend.yml"
  - "../OTDR-v2/.github/workflows/deploy-apps.yml"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# INFRA-CICD-302: Esteira CI/CD GitHub Actions

> **Resumo Executivo:** Especificação dos fluxos de build, conteinerização e publicação automatizada de imagens no Harbor Registry via GitHub Actions Self-Hosted Runner.

---

## 🎯 Fluxograma das Esteiras de Implantação

```mermaid
graph TD
    Push["Push na Branch Main"] --> Trigger{"Análise dos Caminhos Alterados"}

    Trigger -->|Backend API| BuildBE["Workflow: deploy-backend.yml"]
    Trigger -->|Micro-Frontends| BuildFE["Workflow: deploy-apps.yml"]

    subgraph EsteiraBackend ["Esteira Backend (Runner Self-Hosted)"]
        BuildBE --> CalcVerBE["Gera Tag Dinâmica (1.0.0.BUILD_NUM)"]
        CalcVerBE --> LoginHarborBE["Autenticação Harbor Registry"]
        LoginHarborBE --> DockerBuildBE["docker build -t backend-api:TAG"]
        DockerBuildBE --> HarborPushBE["Push Imagem para Harbor"]
        HarborPushBE --> GenEnvBE["Gera Arquivo .env em Tempo de Execução"]
        GenEnvBE --> DeployBE["docker compose up -d --force-recreate backend"]
    end

    subgraph EsteiraFrontend ["Esteira Micro-Frontends (Matrix Strategy)"]
        BuildFE --> MatrixMFEs["Matriz: shell, sidebar, otdr, map, login, smartsite"]
        MatrixMFEs --> FilterFE["paths-filter: Filtra Modificações"]
        FilterFE -->|Alterado| PNPMSetup["Setup Node 24 + PNPM v11"]
        PNPMSetup --> DockerBuildFE["docker build com Base Nginx Alpine"]
        DockerBuildFE --> HarborPushFE["Push Imagens MFE para Harbor"]
        HarborPushFE --> DeployFE["docker compose up -d --force-recreate service"]
    end
```

---

## 📐 Detalhamento dos Workflows

### 1. Backend (`deploy-backend.yml`)
- Disparado em alterações na pasta `src/` ou arquivos Docker.
- Calcula a versão dinâmica concatenando a versão base com o número da execução (`1.0.0.${run_number}`).
- Efetua a compilação, envia a imagem para o Harbor Registry corporativo (`gitops/backend-api`) e injeta os segredos do repositório no arquivo `.env` local do servidor antes de recriar o contêiner via Docker Compose.

### 2. Frontend (`deploy-apps.yml`)
- Utiliza uma estratégia de matriz (`matrix strategy`) para construir e implantar individualmente cada um dos seis micro-frontends (`shell`, `sidebar-mfe`, `otdr-mfe`, `map-mfe`, `login-mfe`, `smartsite-mfe`).
- Utiliza a ação `dorny/paths-filter` para evitar builds desnecessários de MFEs que não sofreram alterações na branch main.

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral da Infra:** [INFRA-OVERVIEW-300: Visão Geral](../overview.md)
* **Docker & Divergências:** [INFRA-DOCKER-301: Docker Containers](../docker/containers.md)
