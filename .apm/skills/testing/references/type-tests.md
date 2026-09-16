# 값과 타입 검증

공개 제네릭·유니온·타입 유틸리티처럼 추론 결과가 계약인 경우에 사용합니다. 단순한 타입 선언마다 테스트를 만들지는 않습니다.

일반 `.test.ts` 파일에서 값 검증과 함께 작성합니다. 값 단언은 Vitest가 실행하고, `expectTypeOf` 단언은 테스트 파일을 포함한 프로젝트의 `typecheck` 스크립트로 확인합니다.

## 첫 원소의 값과 추론 결과

일반 호출과 빈 목록에서 반환값·추론 타입을 함께 검증합니다.

```ts
// first-item.ts

/**
 * 목록을 변경하지 않고 첫 원소를 반환합니다.
 *
 * @typeParam T - 목록 원소의 타입
 * @returns 첫 원소. 빈 목록이면 undefined
 */
export function firstItem<T>(items: readonly T[]): T | undefined {
  return items[0];
}
```

```ts
// first-item.test.ts
import { expect, expectTypeOf, it } from "vitest";

import { firstItem } from "./first-item.ts";

it("읽기 전용 목록의 첫 상태를 반환합니다", () => {
  const statuses = ["pending", "paid"] as const;

  const status = firstItem(statuses);

  expect(status).toBe("pending");
  expectTypeOf(status).toEqualTypeOf<"pending" | "paid" | undefined>();
});

it("빈 목록이면 undefined를 반환합니다", () => {
  const values: number[] = [];

  const value = firstItem(values);

  expect(value).toBeUndefined();
  expectTypeOf(value).toEqualTypeOf<number | undefined>();
});
```

기대 타입은 호출자의 계약을 직접 명시합니다. `ReturnType<typeof firstItem>`에서 가져오면 잘못된 반환 타입 변경도 그대로 따라갑니다.

위 예제는 반환 타입을 `unknown`으로 넓히면 `typecheck`에서 실패합니다.

참고: [Vitest 타입 테스트](https://vitest.dev/guide/testing-types)·[expectTypeOf](https://vitest.dev/api/expect-typeof).
