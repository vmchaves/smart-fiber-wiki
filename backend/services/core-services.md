---
id: "BE-SERV-202"
type: "service"
title: "Mapeamento dos Serviços Core e Engine Binária Python"
description: "Documentação técnica dos serviços de domínio backend e da integração binária de parsing de arquivos .sor via child_process Python."
domain: "smart_fiber"
status: "active"
tech_stack:
  - typescript
  - nestjs
  - python
  - child-process
  - mongodb
tags:
  - backend
  - services
  - python-integration
  - sor-parser
related_files:
  - "../OTDR_FINAL_BACKEND/sorParser.ts"
  - "../OTDR_FINAL_BACKEND/src/otdr/sor_converter.py"
  - "../OTDR_FINAL_BACKEND/src/otdr/otdr.service.ts"
  - "../OTDR_FINAL_BACKEND/src/zitadel/zitadel.service.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# BE-SERV-202: Serviços Core e Engine Binária Python

> **Resumo Executivo:** Mapeamento dos serviços principais da arquitetura NestJS e detalhamento da integração híbrida Node.js / Python para parsing binário de arquivos reflectométricos `.sor`.

---

## 🎯 Serviços Principais do Sistema

1. **`ZitadelService` (`src/zitadel/zitadel.service.ts`):**
   - Gerencia a comunicação via API OIDC com o server Zitadel. Executa a criação de organizações (`createOrganization`), adição de usuários (`grantUserOrgRole`) e atribuição de cargos (`ORG_OWNER`, `ORG_USER`, `ORG_OWNER_VIEWER`).
2. **`OtdrService` (`src/otdr/otdr.service.ts`):**
   - Controla o ciclo de vida dos equipamentos OTDR industriais, testes de conectividade de rede (`testConnection`) e persistência de limiares de engenharia (`saveLimit`).
3. **`EntitiesService` (`src/entities/entities.service.ts`):**
   - Provê consultas espaciais otimizadas por caixa de visualização (`findViewportData`), GridFS stream para upload/download de mídias e reordenação de elementos em árvore.
4. **`LinksService` (`src/links/links.service.ts`):**
   - Executa a computação matemática das curvas de atenuação em fibras e gerencia os enlaces conectados aos sites.

---

## 📐 Engine Binária Python (`sorParser.ts` & `sor_converter.py`)

A leitura de arquivos de reflectometria óptica (.sor) exige um parser de baixo nível para decodificar a estrutura binária Telcordia.

### Mecanismo de Execução

```typescript
// Trecho simplificado da integração em sorParser.ts
import { spawn } from "child_process";
import * as path from "path";

export const parseSorToJson = (sorBuffer: Buffer): Promise<any> => {
  return new Promise((resolve, reject) => {
    const scriptPath = path.resolve(process.cwd(), "src", "otdr", "sor_converter.py");
    const pythonProcess = spawn("python", [scriptPath, "--stdin"]);

    // Escreve o buffer binário do arquivo .sor no STDIN do script Python
    pythonProcess.stdin.write(sorBuffer);
    pythonProcess.stdin.end();

    // Captura o JSON resultante no STDOUT
    let stdoutData = "";
    pythonProcess.stdout.on("data", (chunk) => { stdoutData += chunk.toString(); });
    pythonProcess.on("exit", (code) => {
      if (code !== 0) return reject(new Error("Falha no script Python"));
      resolve(JSON.parse(stdoutData));
    });
  });
};
```

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Backend:** [BE-OVERVIEW-200: Visão Geral](./overview.md)
* **Endpoints API:** [BE-API-201: Endpoints API](../api/endpoints.md)
* **Containers Docker:** [INFRA-DOCKER-301: Docker Alertas](../../infra/docker/containers.md)
