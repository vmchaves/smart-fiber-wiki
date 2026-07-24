---
id: "DOM-OVERVIEW-010"
type: "concept"
title: "Visão Geral do Domínio de Engenharia Óptica e Telecomunicações"
description: "Visão geral das regras de domínio da plataforma Smart Fiber, focada em monitoramento OTDR, topologia de rede óptica física e operação multi-tenant."
domain: "smart_fiber"
status: "active"
tech_stack:
  - typescript
  - nestjs
  - python
tags:
  - domain
  - otdr
  - fiber-optics
  - GIS
related_files:
  - "../OTDR_FINAL_BACKEND/src/otdr/otdr.service.ts"
  - "../OTDR_FINAL_BACKEND/src/links/links.service.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# DOM-OVERVIEW-010: Visão Geral do Domínio de Engenharia Óptica

> **Resumo Executivo:** O domínio da aplicação Smart Fiber abrange a representação geoespacial de redes de fibra óptica (Sites e Links), telemetria em tempo real através de Reflectômetros Ópticos no Domínio do Tempo (OTDR) e governança multi-tenant baseada em licenças de uso.

---

## 🎯 Visão Geral do Domínio

A engenharia óptica de telecomunicações exige precisão milimétrica na localização de falhas (rompimentos ou atenuações excessivas em fusões e conectores). O Smart Fiber traduz medições de hardware industrial em representações visuais GIS.

### Principais Pilares do Domínio

1. **Infraestrutura Geoespacial (SmartSite):**
   - **Sites:** Pontos físicos de presença (POP, centrais, caixas de atendimento) mapeados como pontos GeoJSON (`Point`).
   - **Links:** Enlaces de fibra conectando dois Sites, mapeados como linhas GeoJSON (`LineString`).
2. **Telemetria e Medição OTDR:**
   - Disparo de pulsos ópticos para análise da curva de atenuação (dB/km) e detecção de eventos (conectores, fusões, curva de curvatura, rompimento).
3. **Isolamento de Workspaces (Multi-Tenant):**
   - Cada empresa opera em uma organização isolada, compartilhando equipamentos ou mantendo topologias exclusivas.

---

## 📐 Glossário do Domínio

| Termo | Definição Técnica |
| :--- | :--- |
| **OTDR** | Optical Time-Domain Reflectometer - Equipamento de teste que envia pulsos de luz pela fibra e mede a luz retroespalhada. |
| **Arquivo .SOR** | Formato binário padronizado Telcordia (GR-196 / SR-4731) contendo pontos da curva óptica e tabela de eventos. |
| **Fator de Catenária** | Multiplicador de sobredistância aplicado ao trajeto geodésico para compensar as curvas físicas do cabo de fibra. |
| **Limiar de Atenuação** | Valor máximo tolerado em dB para a perda de sinal ao longo de um enlace óptico (`CreateLimitDto`). |

---

## 🔗 Conexões no Grafo (Dependências)
* **Nó Raiz:** [ROOT-INDEX-000: Grafo de Conhecimento](../index.md)
* **Regras e RBAC:** [DOM-RULES-011: Regras de Negócio](../domain/regras-de-negocio.md)
* **Fluxogramas:** [DOM-FLOWS-012: Diagramas Mermaid](../domain/fluxogramas.md)
