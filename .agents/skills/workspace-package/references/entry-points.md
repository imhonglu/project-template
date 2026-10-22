# 공개 API와 실행 진입점

TypeScript 소스를 직접 처리하는 소비자용 구성 예제입니다.
이름·경로는 실제 패키지·모듈로 바꾸고 JSON은 `package.json`에 병합합니다.
빌드해 배포하면 산출물·타입 선언 경로를 지정합니다.

Node.js의 내장 타입 제거는 `node_modules` 아래의 TypeScript 파일에 적용되지 않습니다.
배포 패키지는 지원 로더 또는 JavaScript 산출물로 실행하며, 워크스페이스 실행과 별도로 검증합니다.

참고: [Node.js 의존성의 타입 제거 제한](https://nodejs.org/api/typescript.html#type-stripping-in-dependencies)

## 단일 배럴

공유 패키지 `@example/library`가 제공할 API를 `src/index.ts`에서 모읍니다.

```json
{
  "exports": "./src/index.ts"
}
```

```ts
// src/index.ts
export * from "./parse-input.ts";
export * from "./input-error.ts";
export type * from "./transport.ts";
```

내부 도우미·테스트 준비·실행부는 재수출하지 않습니다.
기존 공개 이름·경로와 전용 타입이 유지되는지 확인합니다.
CLI만 제공하면 배럴과 `exports`를 생략합니다.

## 제품·검증 배럴

소비 목적과 실행 환경이 다른 API를 하위 경로로 구분하는 예제입니다.

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./node": "./src/node.ts",
    "./testing": "./src/testing/index.ts"
  }
}
```

| import 경로                | 용도                    | 실행 환경            |
| -------------------------- | ----------------------- | -------------------- |
| `@example/library`         | 타입·스키마·계산        | 공통 JavaScript      |
| `@example/library/node`    | 파일·프로세스·서버 실행 | Node.js              |
| `@example/library/testing` | 소비자용 검증 도구      | 도구가 요구하는 환경 |

```ts
// src/node.ts
export * from "./documents/read-document.ts";
```

```ts
// src/testing/index.ts
export * from "../documents/testing/create-document.ts";
export * from "./verify-document.ts";
```

제품 코드는 검증 도구에 의존하지 않고 기본 배럴도 검증 배럴을 재수출하지 않습니다.

브라우저용 경로의 전이 실행 의존성에는 Node.js 전용 구현을 포함하지 않습니다.
서버 계약의 type-only 참조는 실행 코드를 만들지 않지만 참조된 타입도 소비 환경에서 해석할 수 있어야 합니다.
지원하는 소비자 타입 환경과 브라우저 빌드로 각각 확인합니다.

하위 경로를 나눠도 설치 의존성은 그대로입니다.

## 환경별 구현 선택

| 바꿀 대상                        | 설정                        |
| -------------------------------- | --------------------------- |
| 같은 공개 API의 환경별 구현      | conditional exports         |
| 패키지 내부 의존성의 환경별 구현 | `imports`의 `#` 이름과 조건 |

조건은 객체의 키 순서대로 선택되므로 구체적인 조건을 먼저, 범용 대체 구현인 `default`를 마지막에 둡니다.
사용자 조건의 지원·활성화 여부를 런타임·번들러·타입 검사기에서 확인합니다.
소비 환경별로 선택된 구현과 공개 API·초기화 동작을 검증합니다.

### 참고

- [하위 경로](https://nodejs.org/api/packages.html#subpath-exports)
- [조건부 진입점](https://nodejs.org/api/packages.html#conditional-exports)
- [내부 imports](https://nodejs.org/api/packages.html#subpath-imports)

## 부수 효과를 보존하는 경로

`sideEffects` 배열에 없는 파일은 제거 가능한 것으로 취급됩니다. 초기화를 별도 경로로 제공하면 소비자가 그 경로를 import하도록 안내합니다.

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./register": "./src/register.ts"
  },
  "sideEffects": ["**/*.css", "./src/register.ts"]
}
```

`import "@example/library/register"`로 초기화합니다.
루트 import로도 초기화하려면 `src/index.ts`에서 등록 파일을 import하고 루트 파일도 `sideEffects`에 포함합니다.
빌드 배포 시 두 필드의 경로를 산출물 기준으로 맞추고 프로덕션 번들에서 초기화·스타일을 확인합니다.

참고: [webpack의 부수 효과 경로 처리](https://webpack.js.org/guides/tree-shaking/#mark-the-file-as-side-effect-free)

## 실행 명령

TypeScript 직접 실행을 지원하는 Node.js 환경의 CLI 예제입니다.

```json
{
  "scripts": {
    "start": "node src/main.ts"
  }
}
```

```text
packages/cli/src/
├── main.ts             # 인수·신호·출력·종료 코드 연결
└── run-cli.ts          # 명령 처리

packages/library/src/testing/
├── index.ts            # 검증 API 배럴
├── verify-document.ts  # 검증 구현
└── verify/main.ts      # 독립 실행 프로그램
```

배럴은 `main.ts`를 가져오거나 재수출하지 않습니다.
테스트용 자식 프로그램은 가까운 `fixtures/<프로그램>/main.ts`에 두고 진입점 검색 규칙에 포함합니다.

부수 효과가 없는 도움말 명령부터 확인합니다.

```sh
pnpm --filter @example/cli run start --help
```

`pnpm --filter`의 스크립트는 패키지 디렉터리에서 실행되므로 파일 인수도 해당 cwd를 기준으로 해석합니다.
