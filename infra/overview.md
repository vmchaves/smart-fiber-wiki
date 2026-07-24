---
id: "INFRA-OVERVIEW-300"
type: "concept"
title: "Visão Geral da Infraestrutura de Deploy e Orquestração"
description: "Visão geral da infraestrutura baseada em Docker, Nginx Proxy, Harbor Registry e esteiras GitHub Actions Self-Hosted."
domain: "smart_fiber"
status: "active"
tech_stack:
  - docker
  - nginx
  - github-actions
  - harbor
tags:
  - infra
  - docker
  - ci-cd
  - deployment
related_files:
  - "../OTDR-v2/docker-compose.yml"
  - "../OTDR_FINAL_BACKEND/docker-compose.yml"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# INFRA-OVERVIEW-300: Visão Geral da Infraestrutura

> **Resumo Executivo:** O ecossistema Smart Fiber adota uma estratégia de implantação inteiramente baseada em contêineres Docker, orquestrada por **Docker Compose** e automatizada via **GitHub Actions** em runners corporativos self-hosted.

---

## 🎯 Topologia da Infraestrutura

```mermaid
graph TD
    User["Acesso Externo HTTP/WS"] --> ProxyContainer["mfe-proxy (Nginx Proxy Portas 8081/8082)"]
    
    subgraph DockerNetwork ["Rede Interna Docker (mfe-network)"]
        ProxyContainer --> ShellApp["mfe-shell (Contêiner Nginx)"]
        ProxyContainer --> LoginApp["mfe-login (Contêiner Nginx)"]
        ProxyContainer --> OtdrApp["mfe-otdr (Contêiner Nginx)"]
        ProxyContainer --> MapApp["mfe-map (Contêiner Nginx)"]
        ProxyContainer --> BackendApp["backend-api (Contêiner Node 20 / Porta 4000)"]
    end

    subgraph RegistryCorporate ["Harbor Container Registry"]
        Harbor["Harbor Registry (nmsdocker.padtec.com.br)"]
        Harbor --> ShellApp
        Harbor --> BackendApp
    end
```

---

## 📐 Estrutura de Comunicação e Portas

- **Proxy Central (`mfe-proxy`):** Escuta nas portas de host `8081` e `8082`, efetuando o repasse de chamadas para o shell de micro-frontends e para a API backend.
- **Backend API (`backend-api`):** Escuta na porta interna `4000`, processando requisições REST/SSE/WS.

---

## 🔗 Conexões no Grafo (Dependências)
* **Nó Raiz:** [ROOT-INDEX-000: Grafo de Conhecimento](../index.md)
* **Visão Geral Global:** [SYS-OVERVIEW-001: Visão Geral Integrada](../overview.md)
* **Docker & Divergências:** [INFRA-DOCKER-301: Docker & Alertas](./docker/containers.md)
* **Pipelines CI/CD:** [INFRA-CICD-302: GitHub Actions](./CI/pipelines.md)
