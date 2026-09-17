# 패키지 구성

## Node.js 패키지

루트의 공통 TypeScript 설정과 Vitest 프로젝트 수집을 사용하는 예제입니다. 워크스페이스에서 `@types/node`와 Vitest를 사용할 수 있어야 합니다.

```text
tools/example/
├── package.json
├── README.md
├── tsconfig.json
├── vitest.config.ts
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
  "compilerOptions": {
    "lib": ["es2025"],
    "module": "nodenext",
    "types": ["node"]
  }
}
```

`include`를 생략해 소스·테스트·설정 파일을 함께 검사합니다.

```ts
// vitest.config.ts
import { defineProject } from "vitest/config";

// Knip이 기본 테스트 파일을 인식하도록 test 객체를 유지합니다.
// 참고: https://knip.dev/reference/plugins/vitest
export default defineProject({ test: {} });
```

## 브라우저 앱으로 변경

번들러를 사용하는 앱은 `apps/example/`에 두고 `tsconfig.json`을 다음처럼 구성합니다.

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "lib": ["es2025", "dom", "dom.iterable"],
    "module": "preserve"
  }
}
```

프레임워크가 생성한 설정이 있으면 그 구조에 공통 옵션을 연결합니다. DOM 타입 선언만으로 테스트가 브라우저에서 실행되지는 않으므로 Vitest 환경은 별도로 구성합니다.
