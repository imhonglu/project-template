---
name: typescript
description: TypeScript 구현·타입·모듈·비동기 처리와 TSDoc을 간결한 API와 예제 중심으로 작성·정리합니다. TS/TSX 구현, 타입 오류 수정, 리팩터링, TSDoc 정비 요청에 사용합니다.
---

# TypeScript 작성

기존 공개 API·실행 환경을 확인하고 요청 범위에 적용합니다.

## 기본 예제

API와 전용 옵션을 함께 두고, 빈 값 처리 → 정상 결과 순서로 작성합니다.

````ts
// join-labels.ts

/** {@link joinLabels}의 구분자와 빈 목록 표시를 정합니다. */
export interface JoinLabelsOptions {
  /** 생략하면 쉼표와 공백으로 구분합니다. */
  separator?: string;

  /** 빈 목록에 표시할 문구. 생략하면 "없음"입니다. */
  fallback?: string;
}

/**
 * 목록 순서대로 문구를 이어 붙입니다.
 *
 * @param source - 순서를 유지하며 읽을 문구 목록
 * @returns 합친 문구. 빈 목록이면 설정한 fallback을 반환합니다.
 *
 * @example
 * ```ts
 * import { joinLabels } from "./join-labels.ts";
 *
 * console.log(joinLabels(["읽기", "쓰기"], { separator: " · " })); // "읽기 · 쓰기"
 * console.log(joinLabels([])); // "없음"
 * ```
 *
 * @see {@link JoinLabelsOptions} - 구분자와 빈 목록 표시
 */
export function joinLabels(
  source: readonly string[],
  { separator = ", ", fallback = "없음" }: JoinLabelsOptions = {},
): string {
  if (source.length === 0) {
    return fallback;
  }

  return source.join(separator);
}
````

- 공개 함수는 함수 선언, 짧은 콜백은 화살표 함수를 사용합니다.
- 준비·분기·반환·출력 사이에는 빈 줄을 둡니다. 같은 목적의 선언·단언은 묶고, 블록 첫머리는 띄우지 않습니다.
- 긴 조건은 의미 있는 값·함수로 분리합니다.

| 이름                | 예                                             |
| ------------------- | ---------------------------------------------- |
| 변수·함수·인스턴스  | `source`, `joinLabels`, `isReady`              |
| 타입·클래스         | `JoinLabelsOptions`, `User`                    |
| 정책 상수·고정 목록 | `ACCESS_LEVELS`; 일반 `const` 변수는 camelCase |

## 작업별 기준

### 모듈

대표 API의 이름을 파일명으로 옮기고, 전용 타입·도우미·테스트를 가까이 둡니다.

```text
src/
├── index.ts                   # 소비자용 API 재수출
└── labels/
    ├── join-labels.ts         # joinLabels와 JoinLabelsOptions
    └── join-labels.test.ts
```

| 경계        | 기준                                                                        |
| ----------- | --------------------------------------------------------------------------- |
| 파일 분리   | 독립적인 책임·재사용이 생길 때; 작은 관련 함수는 함께 배치                  |
| 공개 API    | named export; 도구가 요구할 때 default export                               |
| 공개 배럴   | `export *`로 소비자용 API만 재수출; 내부 도우미·테스트 파일·CLI 실행부 제외 |
| 타입 의존성 | `import type`·`export type`; 경로·정렬은 프로젝트 설정 준수                 |
| CLI         | 인자·신호·출력 연결과 실제 작업 함수 분리                                   |

### 타입

구현할 동작에 맞는 참고 예제를 읽습니다.

| 작업                     | 참고 예제                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| 외부 입력 검증·상태 표현 | [입력 검증](references/type-patterns.md#외부-입력)·[상태별 데이터](references/type-patterns.md#상태별-데이터) |
| 원본 보존·부분 갱신      | [읽기 전용](references/type-patterns.md#읽기-전용-입력)·[선택 속성](references/type-patterns.md#선택-속성)    |
| 값·타입의 관계 유지      | [고정 값](references/type-patterns.md#고정-값)·[제네릭](references/type-reuse.md#제네릭)                      |
| 기존 계약 재사용         | [계약 파생](references/type-reuse.md#계약-파생)                                                               |
| 타입 오류 억제·실패 사례 | [타입 오류 검증](references/type-reuse.md#타입-오류-검증)                                                     |

- 객체 계약은 `interface`, 유니온·튜플·조합은 `type`을 사용합니다. 표기 통일만으로 기존 공개 타입을 바꾸지 않습니다.
- 매개변수 타입은 명시합니다. 반환 타입은 계약 고정·복잡한 추론에 명시하고, 단순한 구현·지역 값·콜백은 추론합니다.
- 외부 입력은 `unknown`에서 검증합니다. 불가피한 단언은 근거가 확인되는 좁은 경계에 둡니다.
- 인덱스 조회의 `undefined`를 처리합니다. 리터럴 추론이 필요하면 `const` 타입 매개변수를 사용합니다.
- 타입 제거로 실행할 때는 `enum`·런타임 `namespace`·생성자 매개변수 속성을 피합니다.

### 비동기·오류

응답 검증은 [HTTP 예제](references/async-patterns.md#http-응답), 병렬 읽기와 순차 쓰기는 [파일 I/O 예제](references/async-patterns.md#파일-io)를 읽습니다.

| 상황                         | 처리                                                             |
| ---------------------------- | ---------------------------------------------------------------- |
| 완료를 기다릴 작업           | Promise 반환 또는 `await`                                        |
| 독립된 작업 / 앞 결과에 의존 | `Promise.all` / 순차 `await`                                     |
| 대량 입력                    | 동시 실행 수 제한                                                |
| 복구·오류 맥락 추가          | `catch`; 감싼 원인은 `{ cause }`로 보존                          |
| 실패를 값으로 반환하는 API   | 성공·실패를 판별 가능한 유니온으로 표현                          |
| 자원 정리                    | 지원 환경에서 `using`·`await using`; 사용 중인 작업 완료 후 정리 |
| 공유 자원·백그라운드 작업    | 실제 수명에 맞춰 실패 처리·종료 시점 정의                        |

### TSDoc

공개 API·공유 도우미는 선언 바로 위에 문서화합니다. **대표 호출·결과를 먼저 정하고**, 설명은 아래 순서로 배치합니다.

| 순서                    | 내용                             | 참고 예제                                             |
| ----------------------- | -------------------------------- | ----------------------------------------------------- |
| 요약 → `@remarks`       | 목적 → 상세 동작·부수 효과       | [parseUser](references/type-patterns.md#외부-입력)    |
| `@typeParam` → `@param` | 타입 관계·입력 역할·제약         | [getProperty](references/type-reuse.md#제네릭)        |
| `@returns` → `@throws`  | 결과·완료 시점 → 오류·거부 조건  | [loadUser·combineFiles](references/async-patterns.md) |
| `@example` → `@see`     | import·입력·호출·출력 → 관련 API | 위 예제의 TSDoc                                       |

- 기본값·허용 범위·생략 의미는 옵션 속성에 둡니다. 함수에서는 관련 타입을 `{@link}`로 연결합니다.
- 상세 계약은 보존하고, 긴 조건은 문단·목록으로 나눕니다. 같은 사실·타입 표기를 반복하지 않습니다.
- 단순한 도우미는 요약만 작성할 수 있습니다. 내부 선언의 사용 조건도 필요하면 문서화합니다.
- 예제는 실제 출력과 타입 추론을 구분합니다. 비동기는 `await`하고, 외부 서비스·파일 등 실행 전제를 밝힙니다.
- 관련 선언은 `{@link}` 또는 `@see`로 한 번 연결합니다. 사용 중단은 `@deprecated`에 대체 API·이전 방법을 적습니다.
- 구현 선택의 이유는 코드 옆 `//`에 둡니다.

공식 문법: [요약·상세 분리](https://tsdoc.org/pages/tags/remarks/)·[매개변수](https://tsdoc.org/pages/tags/param/)·[오류](https://tsdoc.org/pages/tags/throws/).

## 결과 확인

1. 공개 API·호출부·TSDoc의 일치를 확인합니다. 제네릭은 결과·추론·잘못된 입력을 함께 검사합니다.
2. 표시된 파일명·대상 환경에서 예제를 타입 검사합니다. 실행 예제는 동작도 확인하고, 검증 후 임시 파일을 제거합니다.
3. 프로젝트의 `check`를 실행하고 결과·미실행 범위를 보고합니다. 포함된 단계는 중복 실행하지 않습니다.

스타일 근거: new-wheels의 [API와 옵션 배치](https://github.com/imhonglu/new-wheels/blob/967f54961853ddf9ca04014c54f30758994540d8/libs/toolkit/src/function/memoize.ts)·[타입 관계와 사용 예](https://github.com/imhonglu/new-wheels/blob/967f54961853ddf9ca04014c54f30758994540d8/libs/type-object/src/functions/entries.ts)·[입력 검증과 오류 원인](https://github.com/imhonglu/new-wheels/blob/967f54961853ddf9ca04014c54f30758994540d8/tools/json-schema-conformance/src/parse-test-groups.ts).
