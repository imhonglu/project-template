# 패키지 README

## 공유 라이브러리

`libs/example/README.md`의 예제입니다. `createStore` API, `typecheck` 스크립트, 패키지 이름과 같은 Vitest 프로젝트가 있는 구성을 가정합니다.

````markdown
# @project-template/example

앱에서 사용하는 메모리 저장소를 제공합니다. Node.js와 브라우저에서 사용할 수 있으며 데이터를 외부에 저장하지 않습니다.

## 사용법

TypeScript 소스를 직접 처리하는 실행 환경·번들러에서 사용합니다.

[저장소 설치](../../README.md#시작)를 마친 뒤 소비 패키지의 `package.json`에 의존성을 추가하고 루트에서 `pnpm install`을 실행합니다.

```json
{
  "dependencies": {
    "@project-template/example": "workspace:*"
  }
}
```

```ts
import { createStore } from "@project-template/example";

const store = createStore("ready");

console.log(store.value); // "ready"
```

## 개발

저장소 루트에서 실행합니다.

```sh
pnpm --filter @project-template/example run typecheck
pnpm test --project @project-template/example
```
````

명령의 패키지 이름과 테스트 프로젝트 이름은 실제 설정으로 바꿉니다. 루트에서 테스트를 모아 실행한다면 하위 패키지에 없는 `test` 스크립트를 안내하지 않습니다. [pnpm 필터](https://pnpm.io/filtering)·[Vitest 프로젝트 선택](https://vitest.dev/guide/projects.html#running-tests)

## 패키지 유형에 맞추기

소개·사용법·개발 구조를 유지하고, 사용법의 예시를 바꿉니다.

| 유형      | 사용법에 담을 예시                                            |
| --------- | ------------------------------------------------------------- |
| 앱        | 환경 변수·외부 서비스 준비 → 실행 명령 → 접속 주소·확인 방법  |
| 개발 도구 | 명령·필수 인자·입력 → 출력 위치·형식과 파일 변경 등 실행 효과 |

비동기 호출은 `await`하고, 파일·서비스·빌드가 필요하면 준비 방법을 예시 앞에 둡니다.

## 필요한 설명 더하기

기본 예제로 설명되지 않는 내용이 있을 때만 절을 추가합니다. 실행 전 필요한 설정은 사용법에서 연결합니다.

| 절             | 내용 예시                                                                               |
| -------------- | --------------------------------------------------------------------------------------- |
| 공개 진입점    | `/browser`는 DOM 환경, `/testing`은 테스트 도우미; 초기화·CSS import 조건               |
| 설정           | 환경 변수·옵션 이름, 필수 여부·생략 시 동작, 설정 위치·`.env.example` 링크; 비밀값 제외 |
| 설계·설정 근거 | 저장 방식을 선택한 이유, `package.json`의 `sideEffects` 지정 근거와 해당 파일 링크      |
| 빌드·배포      | 빌드 산출물·실행 환경·실제 배포 절차; 짧은 빌드 안내는 개발 절에 작성                   |
| 제약·문제 해결 | 지원 범위, 자주 겪는 증상·원인·해결 방법                                                |

참고: [GitHub README 안내](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)·[npm 패키지 README 안내](https://docs.npmjs.com/about-package-readme-files/).

실제 사례: [Fluent UI의 라이브러리 사용 예](https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-components/README.md)·[create-vite의 도구 실행 예](https://github.com/vitejs/vite/blob/main/packages/create-vite/README.md).
