---
name: typescript
description: TypeScript 코드를 타입·모듈·비동기·TSDoc 컨벤션과 예제에 맞춰 작성·수정합니다. TS/TSX 구현, 타입 오류 수정, 코드 검토·리팩터링, API 문서화 요청에 사용합니다. 패키지 골격·개발 도구 설정만 변경하는 작업은 제외합니다.
---

# TypeScript 작성

기존 공개 API와 실행 환경을 확인하고 요청 범위에 아래 컨벤션을 적용합니다.

## 사용 시점

- 코드 구현: "외부 API 응답을 검증하는 함수를 작성해줘"
- 타입 오류 수정: "단언 없이 이 타입 오류를 해결해줘"
- 구조 개선: "이 모듈의 타입과 비동기 처리를 정리해줘"
- API 문서화: "공개 함수와 타입의 사용 조건을 TSDoc으로 설명해줘"

## 작업 절차

### 모듈 구성

소스는 `.ts`, JSX를 포함하면 `.tsx`를 사용합니다.

#### 관심사별 파일 배치

디렉터리로 관심사를 묶은 경우, **공개 API 중심으로 파일을 구성합니다.** 파일명은 대표 API 이름을 `kebab-case`로 표현합니다.

| 관심사      | 파일과 대표 API                              | 같은 파일에 둘 구성요소                  |
| ----------- | -------------------------------------------- | ---------------------------------------- |
| 설정 해석   | `config/parse-config.ts` → `parseConfig`     | 결과 타입 `Config`, 전용 값 검증 함수    |
| 저장소 생성 | `storage/create-store.ts` → `createStore`    | `StoreOptions`·`Store`, 전용 초기화 함수 |
| 검증 실행   | `verify/verify-project.ts` → `verifyProject` | 검증 입력·결과 타입, 실행 의존성 구성    |

- 전용 보조 함수·입력·결과 타입은 API와 같은 파일에 둡니다. 독립적인 책임이나 재사용 필요가 생기면 분리합니다.
- 작은 모듈은 파일 하나로 유지할 수 있습니다. 함수·타입마다 파일을 나눌 필요는 없습니다.

API와 명령을 함께 제공한다면 구현·테스트를 다음처럼 묶습니다.

```text
src/
├── index.ts                              # 소비자용 API 재수출, main.ts 제외
└── verify/
    ├── verify-project.ts                 # verifyProject와 전용 타입·보조 함수
    ├── verify-project.integration.test.ts # API 테스트
    ├── main.ts                           # 인자·신호·출력 연결, verifyProject 호출
    └── main.integration.test.ts           # 명령 테스트
```

#### 내보내기·실행 문법

- 사용하는 심벌만 named export로 공개합니다. 도구가 요구하면 default export를 사용합니다.
- 패키지 공개 배럴에는 소비자용 API만 모읍니다. 관심사마다 `index.ts`를 추가할 필요는 없습니다.
- 타입 의존성은 `import type`·`export type`으로 표시합니다.
- import 경로·확장자는 모듈 해석·빌드 방식에 맞춥니다. 정렬·서식은 설정된 도구에 맡깁니다.

타입 제거만으로 실행할 수 있도록 다음 문법을 사용합니다.

| 용도         | 작성 방식                                        |
| ------------ | ------------------------------------------------ |
| 고정 값 목록 | `enum` 대신 `as const` 목록·객체                 |
| 코드 묶음    | `namespace` 대신 모듈                            |
| 클래스 속성  | 생성자 매개변수 속성 대신 속성을 명시적으로 선언 |

### 이름·간격

| 대상                              | 컨벤션                            | 예                                         |
| --------------------------------- | --------------------------------- | ------------------------------------------ |
| 변수·함수                         | `camelCase`                       | `userId`, `loadUser`                       |
| 모듈의 정책 상수·고정 목록·조회표 | `UPPER_SNAKE_CASE`                | `FREE_SHIPPING_THRESHOLD`, `ACCESS_LEVELS` |
| 타입·인터페이스·클래스·컴포넌트   | `PascalCase`; `I`·`T` 접두사 생략 | `User`, `UserState`                        |
| 불리언                            | 상태·가능 여부를 드러내는 이름    | `isReady`, `hasPermission`, `canEdit`      |

지역 변수·호출 결과·객체 인스턴스는 `const`여도 `camelCase`를 사용합니다. [상수 명명 기준](https://google.github.io/styleguide/tsguide.html#constants)

- 준비·계산, 분기(`if`·`switch`·`try`), 종료(`return`·`throw`), 출력(`console.log`) 사이에는 빈 줄 하나를 둡니다.
- 같은 목적의 연속 선언·출력·단언은 묶습니다. 블록·`case`의 첫 문장 앞에는 빈 줄을 넣지 않습니다.

### 타입 선택

기존 공개 타입은 표기 통일만을 위해 바꾸지 않습니다.

| 상황                  | 컨벤션                                                                   |
| --------------------- | ------------------------------------------------------------------------ |
| 새 객체 계약          | `interface`                                                              |
| 유니온·튜플·타입 조합 | `type`; 상태별 필드는 판별 가능한 유니온으로 묶음                        |
| 기존 타입의 부분·변형 | 함께 바뀌는 계약은 `Pick`·`Omit` 등으로 파생; 독립된 계약은 별도 정의    |
| 값 사이의 타입 관계   | 제네릭 사용; 타입 매개변수·제약은 필요한 만큼 선언                       |
| 함수 선언             | 매개변수 타입과 export 함수의 반환 타입을 명시; 지역 값·콜백은 추론 활용 |
| 읽기 전용 입력        | `readonly` 속성·배열로 표시; 정렬·변환은 새 값으로 반환                  |
| 외부 입력             | `unknown`으로 받고 기존 스키마나 조건 검사로 검증                        |
| 값의 구조 검사        | `satisfies`; 리터럴 고정이 필요할 때 `as const` 병용                     |
| 선택 속성             | 생략은 속성 자체를 만들지 않음; `{ key: undefined }`와 구분              |
| 인덱스 조회           | 배열·레코드 조회 결과의 `undefined`를 처리; 존재를 확인한 뒤 사용        |
| 타입 단언·검사 우회   | `as`·`!`·`any`로 검증을 우회하지 않음; 불가피한 단언은 근거·범위 명시    |

고정 목록에서 타입을 파생하고, 표시 문구의 키·값을 검사하는 예입니다.

```ts
// access-level.ts

/** {@link AccessLevel}의 원본이 되는 권한 목록입니다. */
export const ACCESS_LEVELS = ["reader", "editor"] as const;

/** {@link ACCESS_LEVELS}에 포함된 권한입니다. */
export type AccessLevel = (typeof ACCESS_LEVELS)[number];

/** {@link AccessLevel}별 화면 표시 문구입니다. */
export const ACCESS_LABELS = {
  reader: "읽기",
  editor: "편집",
} as const satisfies Record<AccessLevel, string>;
```

리터럴 고정이 필요 없으면 `as const`를 생략합니다. `satisfies`·타입 선언은 실행 시 입력을 검증하지 않습니다. [satisfies 연산자](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator)

외부 타입 선언의 오류를 임시로 억제할 때는 `@ts-expect-error`에 이유·제거 조건을 적습니다. 오류가 사라져도 주석이 남으면 검사에 실패합니다. [타입 오류 억제](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html#ts-expect-error-comments)

구현할 동작에 맞는 예제를 읽습니다.

- 입력 검증·상태·읽기 전용·선택 속성: [타입 예제](references/type-patterns.md)
- 타입 파생·제네릭: [타입 재사용 예제](references/type-reuse.md)

### 비동기·오류·자원

호출부가 완료를 기다려야 하는 Promise는 반환하거나 `await`합니다.

| 작업 관계               | 실행 방식                 |
| ----------------------- | ------------------------- |
| 앞 작업의 결과에 의존   | `await`로 순차 실행       |
| 독립된 고정 개수의 작업 | `Promise.all`로 병렬 실행 |
| 큰 입력 목록            | 동시 실행 수 제한         |
| 분리한 백그라운드 작업  | 실패 처리·종료 시점 명시  |

- **오류:** 복구하거나 맥락을 추가할 때 `catch`합니다. 맥락을 추가하면 `new Error(message, { cause })`로 원인을 보존합니다.
- **복구:** 빈 배열·`null`로 대체할 수 있는 실패를 명시합니다. HTTP 오류·파싱 실패를 정상 응답으로 바꾸지 않습니다.
- **자원:** 지원하는 환경에서는 `using`·`await using`으로 정리하고, 자원을 쓰는 비동기 작업은 스코프 종료 전에 기다립니다.
- **공유 자원:** 스코프 밖에서 공유하면 실제 사용 수명에 맞춰 정리합니다.

HTTP 응답 처리·병렬 I/O에는 [비동기 예제](references/async-patterns.md)를 사용합니다. 필요한 선행 파일·실행 환경은 각 예제에 적혀 있습니다.

### TSDoc 문서화

함수 계약은 [타입 예제의 `parseUser`](references/type-patterns.md), 제네릭 계약은 [타입 재사용 예제의 `getProperty`](references/type-reuse.md)를 참고합니다.

모듈의 공개 API와 공유 도우미는 선언 바로 위에 `/** ... */`를 작성합니다. 내부 선언도 이름·타입만으로 사용 조건을 알기 어려우면 문서화합니다.

- 첫 문장: 목적 요약.
- 속성 설명: 단위·허용 범위·생략 의미.
- 구현 선택의 이유: 해당 코드 옆 `//` 주석.

필요한 태그만 사용하고 `{string}` 같은 타입 표기는 반복하지 않습니다. 매개변수는 `@param value - 설명` 형식을 따릅니다. [매개변수 태그](https://tsdoc.org/pages/tags/param/)

| 태그                     | 작성할 내용                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| `@param`·`@typeParam`    | 입력 제약·기본 동작, 타입 매개변수의 역할·관계                     |
| `@returns`               | 반환값의 의미·빈 값 조건; 비동기는 Promise가 이행되는 값·완료 시점 |
| `@throws`                | 호출자가 처리할 오류와 발생 조건; 비동기는 Promise 거부 조건 명시  |
| `@remarks`               | 부수 효과·상태 변경·처리 순서 등 요약보다 긴 사용 조건             |
| `@example`               | 실제 호출과 출력으로 입력·결과를 보여주는 실행 가능한 예제         |
| `{@link User}`           | 문장에서 언급한 타입·함수의 실제 선언 연결                         |
| `@see {@link parseUser}` | 생성·변환·소비 등 관련 API를 별도 목록으로 연결                    |
| `@deprecated`            | 사용 중단 이유와 대체 API·이전 방법                                |

사용 예는 **import → 입력 준비 → 호출 → 기대 출력** 순서로 작성합니다.

- `console.log` 옆에 기대 출력을 적고, 타입 추론 설명은 별도로 표시합니다. [사용 예 태그](https://tsdoc.org/pages/tags/example/)
- 비동기 호출은 `await`합니다. 외부 서비스·파일 등 실행 전제를 적습니다.
- 함께 알아야 할 선언은 `{@link}` 또는 `@see`로 연결하며 같은 대상을 중복 연결하지 않습니다. [인라인 링크](https://tsdoc.org/pages/tags/link/)·[관련 항목](https://tsdoc.org/pages/tags/see/)

## 결과 확인

- 최종 검증은 프로젝트의 `check`로 실행합니다. 개별 확인에는 `typecheck`·`test`를 사용하며, 전체 검사에 포함된 단계는 중복 실행하지 않습니다.
- 변경한 예제는 표시된 파일명으로 저장합니다. `@example`은 같은 프로젝트의 임시 파일로 옮겨 타입 검사·실행 후 제거합니다.
- 예제는 Node.js·브라우저 등 대상 환경에서 실행합니다. 계속 검증할 사용 예는 테스트로 남깁니다.
- 공개 API 변경이 호출부·TSDoc·사용 예에도 반영됐는지 확인하고, 검증 결과와 미실행 범위를 보고합니다.

컨벤션 참고: [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)·[LobeHub TypeScript 가이드](https://github.com/lobehub/lobehub/blob/canary/.agents/skills/typescript/SKILL.md)·[TypeScript Advanced Types](https://github.com/wshobson/agents/blob/main/plugins/javascript-typescript/skills/typescript-advanced-types/SKILL.md).
