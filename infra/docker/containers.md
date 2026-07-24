---
id: "INFRA-DOCKER-301"
type: "infra"
title: "Análise de Containers Docker e Alertas de Divergência"
description: "Detalhamento técnico dos Dockerfiles multi-stage, docker-compose.yml e callout WARNING apontando bugs críticos de infraestrutura."
domain: "smart_fiber"
status: "active"
tech_stack:
  - docker
  - docker-compose
  - nginx
  - nodejs
tags:
  - infra
  - docker
  - nginx
  - warnings
related_files:
  - "../OTDR_FINAL_BACKEND/Dockerfile"
  - "../OTDR_FINAL_BACKEND/docker-compose.yml"
  - "../OTDR-v2/Dockerfile"
  - "../OTDR-v2/docker-compose.yml"
  - "../OTDR-v2/nginx-proxy.conf"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# INFRA-DOCKER-301: Containers e Divergências Críticas

> **Resumo Executivo:** Análise detalhada da configuração de contêineres Docker, Dockerfiles multi-stage e diagnóstico crítico de inconsistências de portas, variáveis de ambiente e dependências ausentes no runtime de produção.

---

## 🎯 Configuração de Dockerfiles

### 1. Backend API (`OTDR_FINAL_BACKEND/Dockerfile`)
- **Estágio Builder (`node:20-alpine`):** Instala todas as dependências (`npm install --legacy-peer-deps`) e gera o JavaScript compilado em `/dist`.
- **Estágio Production (`node:20-alpine`):** Copia apenas dependências de produção (`--only=production`) e o diretório `/dist`. Expõe a porta `4000`.

### 2. Frontend Micro-Frontends (`OTDR-v2/Dockerfile`)
- Imagem ultra-leve baseada em `nginx:alpine`, substituindo a configuração padrão pelo `nginx-docker.conf` e servindo os arquivos estáticos da pasta `/dist`.

---

## 🚨 Alertas Críticos de Divergência de Infraestrutura

> [!WARNING]
> **Inconsistências Gravíssimas de Portas, Redis e Dependências de Runtime:**
>
> 1. **Falta da Engine Python no Contêiner de Produção (Erro no Parser .SOR):**
>    - A classe `sorParser.ts` executa o script `sor_converter.py` via `child_process.spawn("python", ...)`.
>    - A imagem Docker de produção (`FROM node:20-alpine`) **NÃO instala o binário `python3`**. Qualquer tentativa de upload ou análise de arquivo `.sor` em contêineres de produção resultará em erro fatal de execução (`ENOENT`).
>    - **Ação Corretiva:** Adicionar `RUN apk add --no-python3` no `Dockerfile` de produção do backend.
>
> 2. **Inconsistência da Porta do Backend (3000 vs 4000):**
>    - O arquivo `OTDR_FINAL_BACKEND/docker-compose.yml` declara `expose: - "3000"`.
>    - No entanto, a esteira de deploy (`deploy-backend.yml`) injeta a variável `PORT=4000` no arquivo `.env`. Se o proxy Nginx rotear para a porta `3000`, a aplicação retornará **502 Bad Gateway**.
>
> 3. **Hardcode da Conexão Redis no Bootstrap (`src/main.ts`):**
>    - No arquivo `src/main.ts` (linhas 35-36), a conexão do gerenciador de sessões `connect-redis` possui hardcode apontando para `localhost:6380`.
>    - Enquanto o `app.module.ts` lê a variável `REDIS_PORT` (default `6379`). Em contêineres isolados, o bootstrap da sessão falhará por tentar conectar na porta incorreta.

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral da Infra:** [INFRA-OVERVIEW-300: Visão Geral](../overview.md)
* **Core Services (Parser):** [BE-SERV-202: Serviços Backend](../../backend/services/core-services.md)
* **Pipelines CI/CD:** [INFRA-CICD-302: GitHub Actions](../CI/pipelines.md)
