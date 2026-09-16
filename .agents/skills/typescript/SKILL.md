---
name: typescript
description: TypeScript 코드를 타입·모듈·비동기·TSDoc 컨벤션과 예제에 맞춰 작성·수정합니다. TS/TSX 구현, 타입 오류 수정, 코드 검토·리팩터링, API 문서화 요청에 사용합니다. 패키지 골격·개발 도구 설정만 변경하는 작업은 제외합니다.
---

# TypeScript 작성

기존 공개 API와 실행 환경을 유지하며 아래 컨벤션을 적용합니다.

## 사용 시점

- 코드 구현: "외부 API 응답을 검증하는 함수를 작성해줘"
- 타입 오류 수정: "단언 없이 이 타입 오류를 해결해줘"
- 구조 개선: "이 모듈의 타입과 비동기 처리를 정리해줘"
- API 문서화: "공개 함수와 타입의 사용 조건을 TSDoc으로 설명해줘"

## 작업 절차

### 모듈 구성

- 소스는 `.ts`, JSX를 포함하면 `.tsx`를 사용합니다.
- 타입은 사용하는 코드 가까이에 두고, 여러 모듈이 공유할 때 분리합니다.
- 사용하는 심벌만 named export로 공개합니다. 도구가 요구하면 default export를 사용합니다.
- 타입 의존성은 `import type`·`export type`으로 표시합니다. import 경로·확장자는 모듈 해석·빌드 방식에 맞추고, 정렬·서식은 설정된 도구에 맡깁니다.
- 타입 제거만으로 실행할 수 있는 문법을 사용합니다. `enum` 대신 `as const` 목록·객체를, `namespace` 대신 모듈을 사용하고, 생성자 매개변수 속성은 명시적으로 선언합니다.

### 이름·간격

| 대상                            | 컨벤션                                        | 예                                         |
| ------------------------------- | --------------------------------------------- | ------------------------------------------ |
| 변수·함수                       | `camelCase`                                   | `userId`, `loadUser`                       |
| 모듈 수준의 고정 상수           | 정책 값·고정 목록·조회표는 `UPPER_SNAKE_CASE` | `FREE_SHIPPING_THRESHOLD`, `ACCESS_LEVELS` |
| 타입·인터페이스·클래스·컴포넌트 | `PascalCase`; `I`·`T` 접두사 생략             | `User`, `UserState`                        |
| 불리언                          | 상태·가능 여부를 드러내는 이름                | `isReady`, `hasPermission`, `canEdit`      |

지역 변수·호출 결과·객체 인스턴스는 `const`여도 `camelCase`를 사용합니다. [상수 명명 기준](https://google.github.io/styleguide/tsguide.html#constants)

- 준비·계산과 `if`·`switch`·`try` 분기, `return`·`throw` 종료, `console.log` 출력 사이에는 빈 줄 하나를 둡니다.
- 블록·`case`의 첫 문장 앞에는 빈 줄을 추가하지 않습니다. 같은 목적의 연속 선언·출력·단언은 묶어 둡니다.

### 타입 선택

| 상황                  | 컨벤션                                                                             |
| --------------------- | ---------------------------------------------------------------------------------- |
| 새 객체 계약          | `interface`; 이미 공개된 타입은 표기 통일만을 위해 바꾸지 않음                     |
| 유니온·튜플·타입 조합 | `type`; 상태별 필드는 판별 가능한 유니온으로 묶음                                  |
| 기존 타입의 부분·변형 | 같은 계약을 공유하면 `Pick`·`Omit` 등으로 파생; 독립적으로 바뀌는 계약은 별도 정의 |
| 함수 선언             | 매개변수 타입과 export 함수의 반환 타입을 명시; 지역 값·콜백은 추론 활용           |
| 읽기 전용 입력        | `readonly` 속성·배열로 표시; 정렬·변환은 새 값으로 반환                            |
| 외부 입력             | `unknown`으로 받고 기존 스키마나 조건 검사로 검증                                  |
| 값의 구조 검사        | `satisfies`; 리터럴 고정이 필요할 때 `as const` 병용                               |
| 선택 속성             | 생략과 `undefined`를 구분; 생략은 속성 자체를 만들지 않음                          |
| 인덱스 조회           | 배열·레코드 조회 결과의 `undefined`를 처리; 존재를 확인한 뒤 사용                  |
| 단언·오류 억제        | `as`·`!`·`any`로 검증을 우회하지 않음; 불가피한 단언은 근거와 적용 범위를 명시     |

`satisfies`·타입 선언은 실행 시 입력을 검증하지 않습니다. 제네릭은 값 사이의 타입 관계를 보존할 때 사용하고, 타입 매개변수와 제약은 필요한 만큼만 둡니다.

외부 타입 선언의 오류를 임시로 억제해야 하면 `@ts-expect-error`와 이유·제거 조건을 남깁니다. `@ts-ignore`와 달리 오류가 사라지면 억제 주석도 검사에 실패합니다. [타입 오류 억제](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html#ts-expect-error-comments)

### 비동기·오류·자원

- 앞 작업의 결과가 필요하면 `await`로 순차 실행합니다. 독립된 고정 개수의 작업은 `Promise.all`로 묶고, 큰 입력 목록은 동시 실행 수를 제한합니다.
- 호출부가 기다릴 Promise는 반환하거나 `await`합니다. 분리한 백그라운드 작업에는 실패 처리와 종료 시점을 둡니다.
- `catch`는 복구 또는 맥락 추가가 필요할 때 사용합니다. 맥락을 추가하면 `new Error(message, { cause })`로 원인을 보존합니다.
- 빈 배열·`null` 등으로 복구할 수 있는 실패를 명시합니다. HTTP 오류·파싱 실패를 정상 응답으로 바꾸지 않습니다.
- 실행 환경과 API가 지원하면 `using`·`await using`으로 자원을 정리합니다. 자원을 사용하는 비동기 작업은 스코프가 끝나기 전에 기다립니다. 스코프 밖에서 공유하는 자원은 실제 사용 수명에 맞춰 정리합니다.

### TSDoc 문서화

- 공개 함수·타입·클래스 등 모듈 API와 공유 도우미는 선언 바로 위에 `/** ... */`로 문서화합니다. 내부 선언도 이름·타입만으로 사용 조건을 알기 어려우면 작성합니다.
- 첫 문장은 목적을 요약합니다. 속성에는 단위·허용 범위·생략 의미를, 함수에는 호출자가 알아야 할 동작을 설명합니다. 구현 선택의 이유는 해당 코드 옆 `//` 주석에 둡니다.
- 필요한 태그만 사용합니다. `@param value - 설명` 형식을 따르며 `{string}` 같은 타입 표기는 반복하지 않습니다. [매개변수 태그](https://tsdoc.org/pages/tags/param/)

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

- 사용 예는 import·입력 준비·호출을 포함합니다. `console.log` 옆 주석에 기대 출력을 적고 타입 추론 설명과 구분합니다. [사용 예 태그](https://tsdoc.org/pages/tags/example/)
- 비동기 호출은 `await`하고, 외부 서비스·파일 등 실행 전제를 명시합니다.
- 반환 타입과 생성 함수처럼 함께 알아야 할 선언을 연결합니다. 링크는 문맥에 필요한 곳에 두고, 같은 대상을 본문과 `@see`에 반복하지 않습니다. [인라인 링크](https://tsdoc.org/pages/tags/link/)·[관련 항목](https://tsdoc.org/pages/tags/see/)

### 예제 선택

구현은 표시된 파일명으로 저장합니다. `@example`은 구현과 같은 디렉터리의 임시 `.ts` 파일에 옮겨 TypeScript를 직접 실행할 수 있는 Node.js에서 실행합니다.

| 필요한 패턴                                           | 참고 파일                                   |
| ----------------------------------------------------- | ------------------------------------------- |
| 입력 검증·상태 유니온·읽기 전용·선택 속성·`satisfies` | [타입 예제](references/type-patterns.md)    |
| 타입 파생·키에 따른 반환 타입·제네릭 선택             | [타입 재사용](references/type-reuse.md)     |
| HTTP 응답 검증·오류 전달·독립 작업 병렬 처리          | [비동기 예제](references/async-patterns.md) |

## 결과 확인

- 프로젝트의 `typecheck`·`test` 스크립트로 관련 검사를 실행하고, 최종 검증은 `check`를 사용합니다. 전체 검사에 포함된 단계는 중복 실행하지 않습니다.
- 변경한 `@example`은 임시 파일도 타입 검사 대상에 포함해 검증한 뒤 제거합니다. 계속 검증할 사용 예는 테스트로 남깁니다.
- 공개 API 변경이 호출부·TSDoc·사용 예에도 반영됐는지 확인하고, 검증 결과와 미실행 범위를 보고합니다.

컨벤션 참고: [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)·[LobeHub TypeScript 가이드](https://github.com/lobehub/lobehub/blob/canary/.agents/skills/typescript/SKILL.md)·[TypeScript Advanced Types](https://github.com/wshobson/agents/blob/main/plugins/javascript-typescript/skills/typescript-advanced-types/SKILL.md).
