---
name: workspace-package
description: pnpm 워크스페이스에 로컬 TypeScript 패키지의 기본 파일·실행 환경·공유 진입점·테스트 설정을 구성합니다. "워크스페이스 패키지 추가", "공유 라이브러리 생성", "Node.js 도구 골격 작성"처럼 apps/·libs/·tools/에 새 패키지를 만드는 요청에 사용합니다. npm 패키지 설치나 기존 의존성 갱신은 제외합니다.
---

# 저장소 내부 패키지 생성

앱·공유 라이브러리·개발 도구의 기본 파일과 타입·검사 설정을 구성합니다.

## 사용 시점

- 새 앱을 추가할 때: "apps에 브라우저 앱 골격을 만들어줘", "워크스페이스에 앱 패키지를 추가해줘"
- 공통 코드를 분리할 때: "libs에 공유 라이브러리를 만들어줘", "여러 앱에서 쓸 코드를 패키지로 나누고 싶어"
- 개발 도구를 추가할 때: "tools에 Node.js 도구 골격을 작성해줘", "스크립트를 독립 패키지로 구성해줘"
- 새 패키지의 설정을 정할 때: "Node.js 환경의 tsconfig를 어떻게 구성해?", "내부 라이브러리 진입점은 어떻게 공개해?"
- 파일 예시만 필요할 때: "패키지 기본 구조를 보여줘", "브라우저 환경 예시를 작성해줘"

설정·진입점 질문은 로컬 패키지를 새로 구성하는 맥락에서 적용합니다. "lodash를 설치해줘", "TypeScript 버전을 올려줘" 같은 기존 의존성의 설치·갱신은 대상이 아닙니다.

## 작업 절차

용도에 따라 `apps/`, `libs/`, `tools/`에 패키지를 만듭니다. 명령은 저장소 루트에서 실행하며, 예시만 요청받으면 템플릿을 제공합니다.

### 1. 기본 파일

비공개 ESM 패키지의 기본형입니다. `example`을 패키지 이름으로 바꿉니다.

```text
tools/example/
├── package.json
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

### 2. 실행 환경

`tsconfig.json`에 해당 환경의 옵션을 추가합니다. 프레임워크의 생성 설정이 있으면 이를 기준으로 공통 설정을 연결합니다.

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

### 3. 공유 진입점

TypeScript 소스를 직접 처리하는 내부 소비자에 라이브러리 진입점을 공개합니다.

`package.json`

```json
{
  "exports": "./src/index.ts"
}
```

### 4. 테스트

테스트가 있는 패키지에 `vitest.config.ts`를 추가합니다. 루트에서 패키지별 테스트를 모아 실행하므로 실행 환경 등 프로젝트 옵션은 여기서 지정합니다.

```ts
import { defineProject } from "vitest/config";

export default defineProject({});
```

### 5. 의존성 연결

- 내부 의존성은 `workspace:*`, 공유 버전은 catalog에 선언해 `catalog:`로 참조합니다.
- 패키지 사용법·설정 근거는 해당 README에 작성합니다.

```sh
pnpm install
```

## 결과 확인

패키지의 타입 검사와 루트 전체 검사를 실행합니다. 관련 파일을 먼저 정리하고, 검사 실패는 이번 변경과 기존 실패를 구분해 보고합니다.

```sh
pnpm --filter @project-template/example typecheck
pnpm check
```
