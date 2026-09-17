---
name: workspace-package
description: pnpm 워크스페이스에 TypeScript 패키지의 기본 파일·실행 환경·공유 진입점·테스트 설정을 구성합니다. apps/·libs/·tools/의 패키지 생성, 진입점 분리·sideEffects 설정과 관련 구성·예시 요청에 사용합니다. 기존 패키지의 npm 의존성 설치·갱신은 제외합니다.
---

# 워크스페이스 패키지 구성

용도에 따라 `apps/`·`libs/`·`tools/`에 비공개 ESM 패키지를 구성합니다. 명령은 저장소 루트에서 실행합니다.

## 사용 시점

- 앱 추가: "apps에 브라우저 앱 골격을 만들어줘"
- 공유 라이브러리 생성: "libs에 공통 코드를 패키지로 분리해줘"
- 개발 도구 추가: "tools에 Node.js 도구 골격을 작성해줘"
- 진입점 정리: "공유 패키지의 브라우저·테스트 의존성을 별도 진입점으로 분리해줘"
- 설정·구조 검토: "새 Node.js 패키지의 기본 구성을 보여줘"

## 작업 절차

설명·예시 요청에는 구성안을 제공합니다. 생성·변경 요청에는 기존 패키지 이름과 공통 설정·소비자를 확인해 필요한 구성을 적용합니다.

### 1. 기본 파일 구성

`example`과 `@project-template`은 패키지 이름과 저장소의 이름 규칙에 맞춥니다.

```text
tools/example/
├── package.json
├── README.md
├── tsconfig.json
├── vitest.config.ts
└── src/
    └── index.ts
```

`package.json`에 비공개 ESM과 타입 검사 스크립트를 선언합니다.

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

`tsconfig.json`은 공통 설정을 상속합니다. `include`를 생략해 패키지의 소스·테스트·설정 파일을 함께 타입 검사합니다.

```json
{
  "extends": "../../tsconfig.base.json"
}
```

`vitest.config.ts`에 테스트 프로젝트를 선언하고, 실행 환경은 패키지별로 설정합니다.

```ts
import { defineProject } from "vitest/config";

// Knip이 기본 테스트 파일을 인식하도록 test 객체를 유지합니다.
// 참고: https://knip.dev/reference/plugins/vitest
export default defineProject({ test: {} });
```

실행 진입점에는 요청한 구현을 작성하고, 공유 API는 아래 진입점 기준을 따릅니다. 골격만 필요하면 `export {};`로 시작합니다.

### 2. 실행 환경 설정

기본 `tsconfig.json`에 해당 환경의 `compilerOptions`를 추가합니다. 프레임워크의 생성 설정이 있으면 이를 기준으로 공통 설정을 연결합니다.

#### Node.js

DOM 전역을 제외하고 Node.js의 모듈 해석과 전역 타입을 적용합니다.

```json
{
  "compilerOptions": {
    "lib": ["es2025"],
    "module": "nodenext",
    "types": ["node"]
  }
}
```

#### 브라우저

번들러를 사용하는 앱 기준입니다.

```json
{
  "compilerOptions": {
    "lib": ["es2025", "dom", "dom.iterable"],
    "module": "preserve"
  }
}
```

### 3. 공유 진입점 공개

#### 기본 배럴

공개할 모듈은 `src/index.ts`에서 `export *`로 모읍니다. 타입만 재내보낼 때는 `export type *`를 사용합니다.

```ts
export * from "./create-store.ts";
export type * from "./types.ts";
```

- 이름 충돌·공개 범위 제한·default export의 재내보내기가 필요할 때만 명시적으로 나열합니다. `export *`는 default export를 포함하지 않습니다.
- 구현 파일끼리는 해당 파일을 직접 참조해 자신의 공개 `index.ts`를 거치는 순환 참조를 피합니다.

TypeScript 소스를 직접 처리하는 내부 소비자에게는 `package.json`의 `exports`로 소스 진입점을 공개합니다. 빌드 결과를 소비하면 경로를 해당 산출물에 맞춥니다.

```json
{
  "exports": "./src/index.ts"
}
```

참고: [TypeScript 타입 재내보내기](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html#support-for-export-type-).

#### 환경·테스트 의존성 분리

단일 진입점을 기본으로 하고, 실행 환경·전용 의존성이 갈리거나 테스트 전용 API를 공개할 때 별도 `index.ts`와 공개 하위 경로를 둡니다. 파일 수나 내부 폴더 구조만으로 진입점을 늘리지 않습니다.

환경 중립 코드와 브라우저·테스트 전용 코드가 함께 있는 경우의 예시입니다. 필요한 경로만 추가합니다.

| 공개 경로   | 진입점                 | 공개 대상                                           |
| ----------- | ---------------------- | --------------------------------------------------- |
| `.`         | `src/index.ts`         | Node.js·브라우저에서 공통으로 쓰는 API·타입         |
| `./browser` | `src/browser/index.ts` | DOM·브라우저 API·브라우저 전용 라이브러리 연동      |
| `./testing` | `src/testing/index.ts` | 다른 패키지에서도 쓰는 테스트 팩터리·mock·도구 연동 |

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./browser": "./src/browser/index.ts",
    "./testing": "./src/testing/index.ts"
  }
}
```

- 각 진입점은 해당 경계의 공개 모듈을 `export *`로 모읍니다. 패키지 내부에서만 쓰는 테스트 도우미·테스트 파일·설정은 공개하지 않습니다.
- 공통 루트의 구현·공개 타입은 전용 코드에 의존하지 않으며, 전용 진입점도 다시 내보내지 않습니다. 전용 코드는 공통 구현을 직접 참조할 수 있습니다.
- 소비자는 `@project-template/example/browser`처럼 공개 경로를 사용합니다. Node.js 전용 코드는 `./node`, 브라우저 전용 테스트 도우미는 `./testing/browser`처럼 필요한 경계에만 추가합니다.

같은 API의 구현만 환경별로 바꿔야 할 때 conditional exports를 검토합니다. 하위 경로를 나눠도 의존성 설치 범위는 달라지지 않습니다.

참고: [Node.js 하위 경로 공개](https://nodejs.org/api/packages.html#subpath-exports)·[조건부 진입점](https://nodejs.org/api/packages.html#conditional-exports).

#### `sideEffects` 선언

`sideEffects`는 미사용 모듈을 제거해도 되는지 번들러에 알려주는 선언입니다. 공유 라이브러리의 import 시 동작을 기준으로 정하며, 내보낸 함수를 호출할 때의 I/O·상태 변경은 별개입니다.

| import 시 필요한 부수 효과                    | `package.json`의 `sideEffects` |
| --------------------------------------------- | ------------------------------ |
| 없음                                          | `false`                        |
| CSS 적용·폴리필·전역 등록 등 일부 파일에 있음 | 해당 파일·glob 배열            |
| 범위를 확인하지 못함                          | 생략                           |

배열에 나열하지 않은 파일은 부수 효과가 없는 것으로 취급합니다. 경로는 소비자가 읽는 소스 또는 빌드 결과에 맞춥니다.

```json
{
  "sideEffects": ["**/*.css", "./src/register.ts"]
}
```

- 초기화는 명시적으로 호출하는 함수나 import하는 별도 진입점으로 분리하는 것을 우선합니다. 배럴을 import할 때 초기화가 필요하면 배럴과 초기화 파일을 함께 목록에 포함합니다.
- `sideEffects`는 일반 ESM 실행에서 의존성 로드를 막지 않습니다. 환경·테스트 의존성은 진입점으로 분리합니다.

참고: [webpack 부수 효과와 트리 셰이킹](https://webpack.js.org/guides/tree-shaking/#mark-the-file-as-side-effect-free).

### 4. 의존성·문서 정리

- 내부 의존성은 `workspace:*`, 공유 버전은 catalog에 선언해 `catalog:`로 참조합니다.
- 패키지 사용법·설정 근거는 해당 README에 작성합니다.

패키지를 추가하거나 의존성 선언을 바꿨으면 설치를 실행해 잠금 파일에 반영합니다.

```sh
pnpm install
```

## 결과 확인

- 공개 경로를 통해 import하고 타입 검사해 `exports` 매핑과 실행 환경을 확인합니다. 환경 중립 루트는 DOM·테스트 전용 타입과 런타임 없이 사용할 수 있어야 합니다.
- 진입점을 분리했다면 공통 루트의 의존성 경로에 전용 코드가 없는지 확인합니다.
- `sideEffects`를 변경했다면 소비자의 프로덕션 빌드에서 미사용 모듈 제거와 필요한 CSS·초기화 보존을 확인합니다. 번들러가 없으면 빌드 검증을 미실행으로 보고합니다.

패키지를 생성·변경했다면 파일을 정리하고 루트 전체 검사를 실행합니다. 새 패키지의 타입 검사도 포함됐는지 확인합니다.

```sh
pnpm check
```

구성안 또는 생성·변경한 파일과 검증 결과를 보고합니다. 이번 변경으로 생긴 실패와 기존 문제·남은 제약을 구분합니다.
