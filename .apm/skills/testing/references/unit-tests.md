# 유닛 테스트

배송비 계산의 정상·경계·실패 사례입니다. 구현과 테스트를 같은 디렉터리에 둡니다.

```ts
// get-shipping-fee.ts

const FREE_SHIPPING_THRESHOLD = 30_000;
const STANDARD_SHIPPING_FEE = 3_000;

/**
 * 주문 금액에 따른 배송비를 원 단위로 계산합니다.
 *
 * @param orderTotal - 0 이상의 유한한 주문 금액(원)
 *
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
// get-shipping-fee.test.ts
import { describe, expect, it } from "vitest";

import { getShippingFee } from "./get-shipping-fee.ts";

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

음수·`NaN`·`Infinity`도 `number` 입력이므로 타입을 우회하지 않고 오류 경로를 검증합니다.

## 참고

- [it.each](https://vitest.dev/api/test#test-each)
- [toThrow](https://vitest.dev/api/expect#tothrow)
