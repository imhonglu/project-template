# 유닛 테스트

계산·분기의 정상·경계·실패 사례를 검증하는 예제입니다. 무료 배송 기준 전후의 금액과 유효하지 않은 입력을 사용합니다.

```ts
// shipping-fee.ts

/** 무료 배송을 적용할 최소 주문 금액(원). */
const FREE_SHIPPING_THRESHOLD = 30_000;

/** 무료 배송 기준 미만일 때의 배송비(원). */
const STANDARD_SHIPPING_FEE = 3_000;

/**
 * 주문 금액에 따른 배송비를 원 단위로 계산합니다.
 *
 * @param orderTotal - 0 이상의 유한한 주문 금액(원)
 * @returns 30,000원 이상이면 0원, 미만이면 3,000원
 * @throws RangeError - 주문 금액이 음수이거나 유한한 수가 아닌 경우
 */
export function getShippingFee(orderTotal: number): number {
  if (!Number.isFinite(orderTotal) || orderTotal < 0) {
    throw new RangeError("주문 금액은 0 이상의 유한한 수여야 합니다.");
  }

  return orderTotal >= FREE_SHIPPING_THRESHOLD ? 0 : STANDARD_SHIPPING_FEE;
}
```

```ts
// shipping-fee.test.ts
import { describe, expect, it } from "vitest";

import { getShippingFee } from "./shipping-fee.ts";

describe("getShippingFee", () => {
  it.each([
    { total: 0, expected: 3_000 },
    { total: 29_999, expected: 3_000 },
    { total: 30_000, expected: 0 },
    { total: 30_001, expected: 0 },
  ])("주문 금액 $total원이면 배송비는 $expected원입니다", ({ total, expected }) => {
    const fee = getShippingFee(total);

    expect(fee).toBe(expected);
  });

  it.each([-1, NaN, Infinity])("유효하지 않은 주문 금액 %s를 거부합니다", (total) => {
    expect(() => getShippingFee(total)).toThrow(RangeError);
  });
});
```

- 같은 흐름의 정상·경계 사례는 `it.each`로 묶고, 오류 검증은 분리합니다.
- 기대값은 계산식을 반복하지 않고 고정값으로 작성합니다. 실패 사례도 `number` 안에서 선택해 `as any` 없이 검증합니다.

참고: [it.each](https://vitest.dev/api/test#test-each)·[toThrow](https://vitest.dev/api/expect#tothrow).
