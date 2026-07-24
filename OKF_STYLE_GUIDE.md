# 📖 Guia de Estilo OKF (Open Knowledge Format)

Este documento define a especificação e as regras obrigatórias para a criação, atualização e manutenção da documentação técnica nesta `/wiki`.

O formato OKF foi projetado para ser **100% legível por humanos** e **otimizado para Agentes de IA e LLMs** (navegação em grafo, busca vetorial e baixo consumo de tokens).

---

## 1. Princípios Fundamentais

1. **Atomicidade (Conceito Único):** Cada arquivo `.md` deve abordar **apenas um único conceito, endpoint, componente ou manifesto**. Nunca misture múltiplos tópicos complexos no mesmo arquivo.
2. **Metadata-First (YAML Frontmatter):** Todo arquivo DEVE iniciar com um cabeçalho YAML padronizado na **linha 1**. Os metadados permitem filtragem instantânea pela IA sem necessidade de parsing do texto completo.
3. **Grafo de Conhecimento Interligado:** Nenhum arquivo deve ser "órfão". Todo documento precisa se conectar a outros através de **links relativos nativos do Markdown** (`[Texto](../pasta/arquivo.md)`).
4. **Rastreabilidade de Código:** O Frontmatter deve mapear explicitamente os arquivos de código-fonte reais (`.js`, `.ts`, `.yaml`) associados ao documento.

---

## 2. Esquema Obrigatório do Frontmatter YAML

Todo documento criado dentro da pasta `/wiki` DEVE incluir a estrutura abaixo nas primeiras linhas:

```yaml
---
id: "DOC-TIPO-0000"              # OBRIGATÓRIO: Identificador único (ex: API-BE-001, COMP-FE-042, INFRA-K8S-003)
type: "concept"                 # OBRIGATÓRIO: domain | component | api | model | infra | test_case | process
title: "Título Conciso do Documento"
description: "Resumo de 1 a 2 frases explicando a finalidade deste item no ecossistema."
domain: "nome_do_dominio"       # Ex: checkout, pagamentos, autenticacao, infraestrutura
status: "active"                # draft | active | deprecated | archived
tech_stack:                     # Lista de tecnologias/frameworks relacionados
  - typescript
  - nestjs
  - react
  - mongodb
  - docker
tags:                           # Palavras-chave para busca semântica
  - frontend
  - api
  - deployment
  - database
  - backend
related_files:                  # Caminhos relativos apontando para o código-fonte real
  - "../backend/src/main/java/com/app/controller/OrderController.java"
  - "../frontend/src/components/CheckoutForm.tsx"
owner: "time_ou_responsavel"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
---

```

---

## 3. Estrutura de Pastas e Nomenclatura

### Nomenclatura de Arquivos

* Use estritamente **`kebab-case`** e caracteres minúsculos (ex: `processamento-pedidos-api.md`).
* Evite nomes genéricos como `index.md` dentro de subpastas profundas; prefira nomes descritivos.

### Árvore Padrão do Diretório `/wiki`

```text
wiki/
├── OKF_STYLE_GUIDE.md             <-- Este guia de estilo
├── log.md                         <-- Log de alterações no formato OKF
├── index.md                       <-- Nó raiz e mapa do Grafo de Conhecimento
├── overview.md                    <-- Visão geral global e integrada do ecossistema
│
├── domain/                        <-- Regras de Negócio, Conceitos Globais e Fluxogramas Mermaid
│   ├── overview.md                <-- Visão geral do domínio
│   ├── regras-de-negocio.md       <-- Regras de Negócio aplicadas no projeto
│   └── fluxogramas.md             <-- Fluxogramas Mermaid
│
├── frontend/                      <-- Aplicação React
│   ├── overview.md                <-- Visão geral do frontend
│   ├── components/                <-- Componentes de UI
│   └── services/                  <-- Clientes de API / HTTP
│
├── backend/                       <-- Aplicação Java (Spring Boot / Quarkus)
│   ├── overview.md                <-- Visão geral do backend
│   ├── api/                       <-- Controllers e Endpoints (necessário arquivo .md compilando todos os endpoints)
│   ├── services/                  <-- Serviços
│   └── models/                    <-- Entities e DTOs
│
├── infra/                         <-- Docker, CI 
│   ├── overview.md                <-- Visão geral da infraestrutura
│   ├── docker/                    <-- Deployments, Services
│   └── CI/                        <-- Env Vars, ConfigMaps
│
└── testing/                       <-- Qualidade e Testes
    ├── overview.md                <-- Visão geral dos testes
    └── test-cases/                <-- Casos de teste

```

### Diretrizes para Arquivos de Visão Geral (`overview.md`)

* **Análise Arquitetural Profunda:** O `overview.md` global (raiz) e os de cada subpasta (`frontend/`, `backend/`, `infra/`, `testing/`) devem conter uma análise arquitetural profunda baseada na leitura do código-fonte real contido nos repositórios, explicando os padrões arquiteturais, fluxos e contratos de comunicação de forma detalhada.
* **Alinhamento com Melhores Práticas:** Relacione os padrões encontrados com as melhores práticas recomendadas pela indústria para cenários semelhantes (ex: segurança de cookies, CORS, micro-frontends, testes automatizados, conteinerização multi-stage), baseando-se em pesquisas em canais de grande relevância técnica.
* **Citações Obrigatórias:** Sempre que conceitos ou melhores práticas forem baseados em referências externas (como RFCs, documentações oficiais ou guias técnicos da indústria), as fontes devem ser citadas na seção `# Citations` ao final do arquivo.

### Diretrizes para Arquivo de Log (`log.md`)

A log.md file at root level of `/wiki` records the history of changes to that scope. The format is a flat list of date-grouped entries, newest first:

```
# Directory Update Log

## 2026-05-22
* **Update**: Added new BigQuery table reference for [Customer Metrics](/tables/customer-metrics.md).
* **Creation**: Established the [Dataplex Playbook](/playbooks/dataplex.md).

## 2026-05-15
* **Initialization**: Created foundational directory structure.
* **Update**: Added progressive-disclosure guidelines to the root [index](/index.md).
```

Date headings MUST use ISO 8601 YYYY-MM-DD form. Log entries are prose; the leading bold word (**Update**, **Creation**, **Deprecation**, etc.) is a convention, not a requirement.

---

## 4. Estrutura Padrão do Corpo do Documento

Abaixo do bloco YAML, siga a seguinte ordem de seções:

```markdown
# [ID]: [Título Limpo do Documento]

> **Resumo Executivo:** [Descrição de uma linha do objetivo do documento].

## 🎯 Visão Geral
Explicação direta sobre a finalidade deste item, o problema que resolve e seu papel na arquitetura.

## 📐 Detalhes Técnicos e Contratos
*(Para APIs: métodos, rotas, payloads de exemplo e respostas HTTP)*
*(Para Infra: variáveis de ambiente, portas, limites de recursos no K8s)*
*(Para Frontend: props, gerenciamento de estado e rotas)*
*(Para Arquitetura: arquitetura e padrões de projeto)*
*(Para Domain: regras de negócio e fluxos)*
*(Para Testing: testes automatizados e procedimentos de verificação)*
*(Para Database: banco de dados, modelos de dados e consultas)*

## 🧪 Estratégia de Teste e Validação
* Referência de testes automatizados ou procedimentos de verificação.
* Instruções ou rotinas de Replay/Debug.

## 📚 Citations
*(Opcional)* Se o corpo do documento fizer alegações baseadas em fontes externas, essas referências DEVEM ser listadas sob um cabeçalho `# Citations` ao final do arquivo, de forma numerada:

[1] [BigQuery public dataset announcement](https://cloud.google.com/blog/products/data-analytics/...)
[2] [Internal data quality runbook](https://wiki.acme.internal/data/quality)

## 🔗 Conexões no Grafo (Dependências)
* **Consumidor (Frontend):** [Checkout Form Component](../../frontend/components/checkout-form.md)
* **Provedor (Backend):** [Order Controller (Java)](../../backend/api/order-controller.md)
* **Deploy (Infra):** [Manifesto K8s Backend](../../infra/k8s/backend-deployment.md)
* **Ambiente (Rancher):** [Variáveis de Ambiente](../../infra/rancher/env-vars.md)

```

Os links de citação PODEM ser URLs absolutas, caminhos relativos ao pacote ou caminhos para o subdiretório `references/` que espelha materiais externos como conceitos OKF de primeira classe.

---

## 5. Matriz de Boas Práticas (Do's & Don'ts)

| Prática Recomendada (Do) | ❌ Prática Proibida (Don't) |
| --- | --- |
| Criar arquivos pequenos e desacoplados focados em um único conceito. | ❌ Criar um único documento monolítico que mistura Java, Node.js e K8s. |
| Usar caminhos relativos nativos: `[Texto](../pasta/arquivo.md)`. | ❌ Usar caminhos absolutos de SO (`C:\...`) ou URLs estáticas de localhost. |
| Mapear todos os arquivos reais alterados na chave `related_files`. | ❌ Deixar o Frontmatter YAML vazio ou sem as chaves `id` e `type`. |
| Manter trechos de código curtos e com a linguagem especificada no bloco (````nestjs`). | ❌ Colocar blocos de código gigantes sem especificação de sintaxe. |
