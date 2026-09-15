---
name: workspace-package
description: pnpm 워크스페이스에 TypeScript 패키지의 기본 파일·실행 환경·공유 진입점·테스트 설정을 구성합니다. apps/·libs/·tools/의 새 앱·공유 라이브러리·개발 도구 패키지 생성과 관련 설정·예시 요청에 사용합니다. 기존 패키지의 npm 의존성 설치·갱신은 제외합니다.
---

# 워크스페이스 패키지 생성

용도에 따라 `apps/`·`libs/`·`tools/`에 비공개 ESM 패키지를 구성합니다. 명령은 저장소 루트에서 실행합니다.

## 사용 시점

- 앱 추가: "apps에 브라우저 앱 골격을 만들어줘"
- 공유 라이브러리 생성: "libs에 공통 코드를 패키지로 분리해줘"
- 개발 도구 추가: "tools에 Node.js 도구 골격을 작성해줘"
- 설정·구조 검토: "새 Node.js 패키지의 기본 구성을 보여줘"

## 작업 절차

설명·예시 요청에는 구성안을 제공하고, 생성 요청에는 기존 이름·공통 설정을 확인해 아래 구성을 적용합니다.

### 1. 기본 파일 구성

`example`과 `@project-template`은 패키지 이름과 저장소의 이름 규칙에 맞춥니다.

```text
tools/example/
├── package.json
├── README.md
├── tsconfig.json
└── src/
    └── index.ts
```

`package.json`

```json
{
  "name": "@project-template/example",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "typecheck": "tsc"
  }
}
```

`tsconfig.json`

```json
{
  "extends": "../../tsconfig.base.json",
  "include": ["src"]
}
```

`src/index.ts`에 요청한 구현을 작성합니다. 골격만 필요하면 `export {};`로 시작합니다.

### 2. 실행 환경 설정

기본 `tsconfig.json`에 해당 환경의 `compilerOptions`를 추가합니다. 프레임워크의 생성 설정이 있으면 이를 기준으로 공통 설정을 연결합니다.

#### Node.js

DOM 전역을 제외하고 Node.js의 모듈 해석과 전역 타입을 적용합니다.

`tsconfig.json`

```json
{
  "compilerOptions": {
    "lib": ["es2025"],
    "module": "nodenext",
    "types": ["node"]
  }
}
```

```sh
pnpm --filter @project-template/example add -D @types/node
```

#### 브라우저

번들러를 사용하는 앱 기준입니다.

`tsconfig.json`

```json
{
  "compilerOptions": {
    "lib": ["es2025", "dom", "dom.iterable"],
    "module": "preserve"
  }
}
```

### 3. 공유 진입점 공개

TypeScript 소스를 직접 처리하는 내부 소비자에게 공유 라이브러리를 공개할 때 `package.json`에 진입점을 추가합니다.

`package.json`

```json
{
  "exports": "./src/index.ts"
}
```

### 4. 테스트 구성

테스트가 있는 패키지에 `vitest.config.ts`를 추가하고 실행 환경 등 프로젝트 옵션을 지정합니다. 첫 테스트를 추가하면 루트 `vitest.config.ts`의 `passWithNoTests`를 제거합니다.

```ts
import { defineProject } from "vitest/config";

export default defineProject({});
```

### 5. 의존성·문서 정리

- 내부 의존성은 `workspace:*`, 공유 버전은 catalog에 선언해 `catalog:`로 참조합니다.
- 패키지 사용법·설정 근거는 해당 README에 작성합니다.

```sh
pnpm install
```

## 결과 확인

패키지를 생성한 경우 파일을 정리하고 타입 검사와 루트 전체 검사를 실행합니다.

```sh
pnpm --filter @project-template/example typecheck
pnpm check
```

구성안 또는 생성·변경한 파일과 검증 결과를 보고합니다. 이번 변경으로 생긴 실패와 기존 문제·남은 제약을 구분합니다.
