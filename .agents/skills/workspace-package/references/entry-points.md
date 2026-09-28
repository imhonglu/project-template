# 공유 진입점

아래 JSON은 `package.json`에 추가할 필드입니다. 소비자가 TypeScript 소스를 직접 처리하며, 공개할 모듈이 해당 경로에 구현되어 있다고 가정합니다.

## 단일 배럴

`src/index.ts`에서 공통 API를 공개합니다. import 시 필요한 부수 효과가 없을 때 `sideEffects: false`를 선언합니다.

```json
{
  "exports": "./src/index.ts",
  "sideEffects": false
}
```

## 환경별 하위 경로

공통 API에 전용 의존성이 섞이지 않도록 진입점을 나눕니다.

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./browser": "./src/browser/index.ts",
    "./testing": "./src/testing/index.ts"
  }
}
```

| 소비자의 import 경로                | 공개 대상                                 |
| ----------------------------------- | ----------------------------------------- |
| `@project-template/example`         | Node.js·브라우저 공통 API·타입            |
| `@project-template/example/browser` | DOM·브라우저 API 연동                     |
| `@project-template/example/testing` | 다른 패키지에서도 쓰는 테스트 팩터리·mock |

```ts
// src/browser/index.ts
export * from "./mount-store.ts";
```

```ts
// src/testing/index.ts
export * from "./create-store-fixture.ts";
```

루트 배럴은 공통 API만 내보냅니다. Node.js 전용 API는 `./node`, 브라우저 전용 테스트 도우미는 `./testing/browser`처럼 필요한 경계만 추가합니다. [Node.js 하위 경로](https://nodejs.org/api/packages.html#subpath-exports)·[조건부 진입점](https://nodejs.org/api/packages.html#conditional-exports)

## 부수 효과 파일

CSS와 import 시 실행되는 등록 코드가 있다면 `false` 대신 파일 목록을 선언합니다. 등록은 소비자가 별도 경로를 import하도록 공개할 수 있습니다.

```json
{
  "exports": {
    ".": "./src/index.ts",
    "./register": "./src/register.ts"
  },
  "sideEffects": ["**/*.css", "./src/register.ts"]
}
```

```ts
// 소비자의 초기화 코드
import "@project-template/example/register";
```

목록에 없는 파일은 부수 효과가 없는 것으로 취급합니다. 빌드 결과를 배포하면 `exports`와 목록의 경로를 산출물에 맞춥니다.

루트 배럴을 import할 때 반드시 초기화해야 하는 설계라면 배럴도 목록에 포함합니다. 예를 들어 `src/index.ts`가 `import "./register.ts"`를 수행하면 `"./src/index.ts"`와 `"./src/register.ts"`를 모두 남깁니다. [webpack 부수 효과와 트리 셰이킹](https://webpack.js.org/guides/tree-shaking/#mark-the-file-as-side-effect-free)
