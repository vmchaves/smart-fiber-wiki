---
id: "BE-MODEL-203"
type: "model"
title: "Mapeamento Exaustivo de DTOs e Schemas de Dados"
description: "Definição formal e em código TypeScript com comentários de negócio de todos os DTOs e validações class-validator."
domain: "smart_fiber"
status: "active"
tech_stack:
  - typescript
  - nestjs
  - class-validator
  - class-transformer
tags:
  - backend
  - dtos
  - schemas
  - validation
related_files:
  - "../OTDR_FINAL_BACKEND/src/otdr/dto/create-limit.dto.ts"
  - "../OTDR_FINAL_BACKEND/src/entities/dto/create-entity.dto.ts"
  - "../OTDR_FINAL_BACKEND/src/onboarding/dto/setup-account.dto.ts"
  - "../OTDR_FINAL_BACKEND/src/otdr/dto/test-connection.dto.ts"
  - "../OTDR_FINAL_BACKEND/src/pins/dto/create-pin.dto.ts"
owner: "padtec_engineering"
created_at: "2026-07-24"
updated_at: "2026-07-24"
---

# BE-MODEL-203: DTOs e Schemas de Dados

> **Resumo Executivo:** Mapeamento em código TypeScript dos Data Transfer Objects (DTOs) primários que sustentam a validação declarativa da API via `class-validator`.

---

## 🎯 Definições Formais de DTOs

### 1. DTO de Limites e Especificações de Engenharia (`CreateLimitDto`)

```typescript
import { IsNumber, IsOptional, IsString, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';

export class EngSpecsDto {
  @IsNumber()
  catenaryFactor: number; // Fator de sobredistância geodésica (ex: 1.05)

  @IsNumber()
  avgSpanBetweenBoxes: number; // Vão médio entre caixas de emenda em metros

  @IsNumber()
  avgSpanBetweenPoles: number; // Vão médio entre postes em metros

  @IsNumber()
  slackPerBox: number; // Metragem de folga técnica por caixa de emenda

  @IsNumber()
  slackPerPole: number; // Metragem de folga técnica por poste reservado
}

export class CreateLimitDto {
  @IsString()
  linkId: string; // ID do enlace de fibra no MongoDB

  @IsNumber()
  maxAttenuation: number; // Limiar máximo tolerado em dB

  @IsOptional()
  @ValidateNested()
  @Type(() => EngSpecsDto)
  engSpecs?: EngSpecsDto; // Especificações de cálculo físico
}
```

### 2. DTO Polimórfico de Entidades GIS (`CreateEntityDto`)

```typescript
import { IsString, IsNotEmpty, IsOptional, IsMongoId, IsEnum, ValidateNested, IsArray, ArrayMinSize, ArrayMaxSize, IsNumber, IsIn, ValidateIf } from 'class-validator';
import { Type } from 'class-transformer';

export enum EntityType {
  FOLDER = 'folder',
  SITE = 'site',
  LINK = 'link',
}

export class SiteGeometryDto {
  @IsIn(['Point'])
  type: 'Point'; // Formato GeoJSON Ponto

  @IsArray()
  @ArrayMinSize(2)
  @ArrayMaxSize(2)
  @IsNumber({}, { each: true })
  coordinates: number[]; // [Longitude, Latitude]
}

export class CreateEntityDto {
  @IsEnum(EntityType)
  readonly type: EntityType; // Tipo da estrutura física/lógica

  @IsString()
  @IsNotEmpty()
  readonly name: string; // Nome descritivo

  @IsOptional()
  @IsMongoId()
  readonly parentId?: string; // ID do grupo ou pasta pai

  @ValidateIf(o => o.type === EntityType.LINK)
  @IsNotEmpty()
  @IsMongoId()
  readonly startPinId?: string; // Origem do enlace

  @ValidateIf(o => o.type === EntityType.LINK)
  @IsNotEmpty()
  @IsMongoId()
  readonly endPinId?: string; // Destino do enlace
}
```

### 3. DTO de Setup da Conta (`SetupAccountDto`)

```typescript
import { IsString, IsNotEmpty, IsIn } from 'class-validator';

export class SetupAccountDto {
  @IsString()
  @IsNotEmpty()
  companyName: string; // Razão social do novo tenant

  @IsString()
  @IsNotEmpty()
  @IsIn(['starter', 'pro', 'enterprise'])
  plan: string; // Plano contratado
}
```

---

## 🔗 Conexões no Grafo (Dependências)
* **Visão Geral do Backend:** [BE-OVERVIEW-200: Visão Geral](./overview.md)
* **Regras de Negócio:** [DOM-RULES-011: Regras e RBAC](../../domain/regras-de-negocio.md)
* **Endpoints API:** [BE-API-201: Endpoints API](../api/endpoints.md)
