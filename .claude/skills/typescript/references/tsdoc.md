# TSDoc 문법

요약만 있으면 한 줄로 쓰고, 상세 설명·블록 태그·예제가 있으면 여러 줄로 나눕니다.

| 위치                                                                                                  | 담을 정보                                 | 예제                                                                |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------- |
| 요약·[`@remarks`](https://tsdoc.org/pages/tags/remarks/)                                              | 목적, 상세 동작·부수 효과                 | [입력 검증](type-patterns.md#외부-입력)                             |
| 옵션 속성·[`@defaultValue`](https://tsdoc.org/pages/tags/defaultvalue/)                               | 허용 범위·생략 의미·기본값                | [옵션 속성](#옵션과-호출-예제)                                      |
| `@typeParam`·[`@param`](https://tsdoc.org/pages/tags/param/)                                          | 타입 관계·입력 제약; 함수 인자의 기본값   | [재시도 입력](implementation-design.md#호출부에서-구분해야-할-의미) |
| [`@returns`](https://tsdoc.org/pages/tags/returns/)·[`@throws`](https://tsdoc.org/pages/tags/throws/) | 반환값·실패 값·완료 시점 / 예외·거부 조건 | [비동기 예제](async-patterns.md)                                    |
| [`@example`](https://tsdoc.org/pages/tags/example/)                                                   | 준비·호출·결과                            | [호출 예제](#옵션과-호출-예제)                                      |
| [`{@link}`](https://tsdoc.org/pages/tags/link/)·[`@see`](https://tsdoc.org/pages/tags/see/)           | 관련 선언·외부 자료                       | 옵션·결과 타입, 공식 API 문서                                       |

표 순서로 계약 설명에 필요한 그룹만 사용합니다. 타입·이름만 되풀이하는 `@param`·`@returns`는 생략합니다. 그룹 사이와 각 `@example` 앞에 빈 주석 줄을 두고, 블록 태그는 새 줄에서 시작합니다.
클래스의 전체 사용 흐름은 [클래스 주석](implementation-design.md#인스턴스가-상태를-소유하는-예제)에, 개별 계약은 생성자·메서드에 둡니다.

사용 중단은 `@deprecated`에 대체 API·이전 방법을, 구현 선택의 이유는 코드 옆 `//`에 적습니다.

## 참조 문법

TSDoc에서는 선언·외부 URL을 `{@link 대상 | 표시 이름}`으로 연결하고, 별도 참고 항목은 `@see`에 둡니다.

```ts
/**
 * 목록 순서대로 문구를 이어 붙입니다. 구분자는 {@link JoinLabelsOptions | 옵션}으로 지정합니다.
 *
 * @see {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join | Array.join의 구분자 처리}
 */
```

## 옵션과 호출 예제

````ts
// join-labels.ts

/** {@link joinLabels}의 구분자와 빈 목록 표시를 정합니다. */
export interface JoinLabelsOptions {
  /**
   * 문구 사이의 구분자입니다.
   *
   * @defaultValue `", "`
   */
  separator?: string;

  /**
   * 빈 목록에 표시할 문구입니다.
   *
   * @defaultValue `"없음"`
   */
  fallback?: string;
}

/**
 * 목록 순서대로 문구를 이어 붙입니다.
 *
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
