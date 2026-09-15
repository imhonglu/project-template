# 모킹

## 타입이 있는 외부 의존성

조회 함수가 반환한 주문을 화면 문구로 바꾸는 예제입니다. 실제 DB 검증은 통합 테스트에서 수행하고, 여기서는 조회 결과별 분기를 검증합니다.

```ts
// order-label.ts

/**
 * 조회한 주문의 식별자와 합계입니다.
 *
 * @see {@link OrderLoader} - 주문 조회 계약
 */
export interface Order {
  id: string;

  /** 주문 합계(원). */
  total: number;
}

/**
 * {@link Order} 또는 undefined로 이행하고, 조회 실패 시 거부하는 함수입니다.
 *
 * @see {@link getOrderLabel} - 조회 결과를 화면 문구로 변환
 */
export type OrderLoader = (id: string) => Promise<Order | undefined>;

/**
 * {@link OrderLoader}로 조회한 주문을 식별자와 합계가 담긴 화면 문구로 바꿉니다.
 *
 * @param id - 조회할 주문 식별자
 * @param loadOrder - 주문 조회 함수
 * @returns 주문이 있으면 표시 문구, 없으면 "주문 없음"으로 이행되는 Promise
 * @throws 조회 실패 시 원본 오류로 Promise를 거부합니다.
 */
export async function getOrderLabel(id: string, loadOrder: OrderLoader): Promise<string> {
  const order = await loadOrder(id);

  return order ? `${order.id}: ${order.total}원` : "주문 없음";
}
```

```ts
// order-label.unit.test.ts
import { describe, expect, it, vi } from "vitest";

import { getOrderLabel } from "./order-label.ts";
import type { OrderLoader } from "./order-label.ts";

describe("getOrderLabel", () => {
  it("주문이 있으면 해당 주문의 합계를 표시합니다", async () => {
    const loadOrder = vi.fn<OrderLoader>().mockResolvedValue({ id: "order-1", total: 3600 });

    const label = await getOrderLabel("order-1", loadOrder);

    expect(label).toBe("order-1: 3600원");
    expect(loadOrder).toHaveBeenCalledWith("order-1");
  });

  it("주문이 없으면 미존재 문구를 표시합니다", async () => {
    const loadOrder = vi.fn<OrderLoader>().mockResolvedValue(undefined);

    await expect(getOrderLabel("missing", loadOrder)).resolves.toBe("주문 없음");
  });

  it("조회 실패는 호출부에 전달합니다", async () => {
    const failure = new Error("저장소 연결 실패");
    const loadOrder = vi.fn<OrderLoader>().mockRejectedValue(failure);

    await expect(getOrderLabel("order-1", loadOrder)).rejects.toBe(failure);
  });
});
```

테스트마다 `vi.fn<OrderLoader>()`를 새로 만들어 호출 이력과 구현을 공유하지 않습니다. 호출 인수 단언은 **조회할 주문 ID가 외부 의존성으로 전달되는 계약**을 확인합니다. 내부 함수의 호출 순서는 검증하지 않습니다.

## import한 외부 모듈 대체

Node.js의 파일 읽기를 모킹해 문구 정리와 오류 전달을 검증합니다. 실제 파일 저장·조회 검증에는 이 모킹을 적용하지 않습니다.

```ts
// welcome-message.ts
import { readFile } from "node:fs/promises";

/**
 * UTF-8 파일에서 읽은 환영 문구의 앞뒤 공백을 제거합니다.
 *
 * @returns 공백을 정리한 문구로 이행되는 Promise
 * @throws 파일 읽기 실패 시 원본 오류로 Promise를 거부합니다.
 */
export async function loadWelcomeMessage(filePath: string): Promise<string> {
  const content = await readFile(filePath, "utf8");

  return content.trim();
}
```

```ts
// welcome-message.unit.test.ts
import { readFile } from "node:fs/promises";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { loadWelcomeMessage } from "./welcome-message.ts";

vi.mock(import("node:fs/promises"));

const readFileMock = vi.mocked(readFile);

beforeEach(() => {
  readFileMock.mockReset();
});

describe("loadWelcomeMessage", () => {
  it("파일 내용의 앞뒤 공백을 제거합니다", async () => {
    readFileMock.mockResolvedValue("  환영합니다  \n");

    const message = await loadWelcomeMessage("welcome.txt");

    expect(message).toBe("환영합니다");
    expect(readFileMock).toHaveBeenCalledWith("welcome.txt", "utf8");
  });

  it("파일 읽기 실패는 호출부에 전달합니다", async () => {
    const failure = new Error("파일 읽기 실패");
    readFileMock.mockRejectedValue(failure);

    await expect(loadWelcomeMessage("missing.txt")).rejects.toBe(failure);
  });
});
```

- `vi.mock(import(...))`는 모듈의 함수를 자동으로 모킹합니다. `vi.mocked`는 모킹 타입을 제공하는 도우미이며, 자체적으로 모킹을 생성하지 않습니다.
- 공유한 모킹은 `mockReset()` 후 테스트별 반환값을 지정합니다.
- `vi.mock` 호출은 import보다 먼저 처리됩니다. 직접 팩터리를 작성하고 외부 변수를 공유해야 할 때는 `vi.hoisted`를 사용합니다.
- 같은 파일 안에서 직접 참조하는 함수 호출은 외부의 `vi.spyOn`·모듈 모킹으로 바뀌지 않습니다. 공개 동작을 검증하고, 의존성 대체가 필요하면 실제 모듈 경계나 주입 지점을 사용합니다.
- 브라우저의 네이티브 ESM export를 추적할 때는 직접 `spyOn`하는 대신 `vi.mock(import(...), { spy: true })`를 사용합니다.

## 시간 경계와 복구

현재 시각을 고정해 만료 직전·도달 시점을 검증하고, 테스트가 끝나면 실제 시계로 복구합니다.

```ts
// expiry.ts

/**
 * 현재 시각이 만료 시각에 도달했는지 확인합니다.
 *
 * @param expiresAt - Unix epoch 기준 밀리초 단위의 만료 시각
 * @returns 만료 시각과 같거나 지났으면 true
 */
export function isExpired(expiresAt: number): boolean {
  return Date.now() >= expiresAt;
}
```

```ts
// expiry.unit.test.ts
import { afterEach, expect, it, vi } from "vitest";

import { isExpired } from "./expiry.ts";

afterEach(() => {
  vi.useRealTimers();
});

it("만료 시각부터 만료로 판단합니다", () => {
  vi.useFakeTimers();
  const expiresAt = Date.UTC(2030, 0, 1);

  vi.setSystemTime(expiresAt - 1);
  expect(isExpired(expiresAt)).toBe(false);

  vi.setSystemTime(expiresAt);
  expect(isExpired(expiresAt)).toBe(true);
});
```

`vi.setSystemTime`은 시각만 바꾸고 타이머 콜백을 실행하지 않습니다. 지연·재시도 로직은 가짜 시계에서 `await vi.advanceTimersByTimeAsync(ms)`로 진행한 뒤 결과를 단언합니다. [타이머 진행](https://vitest.dev/api/vi.html#vi-advancetimersbytimeasync)

## 변경한 항목에 맞는 정리

| 변경 항목                    | 정리 방법                                       |
| ---------------------------- | ----------------------------------------------- |
| 호출 이력만 초기화           | `mockClear()`·`vi.clearAllMocks()`; 구현은 유지 |
| 호출 이력·구현 초기화        | `mockReset()`·`vi.resetAllMocks()`              |
| `vi.spyOn`으로 교체한 메서드 | `mockRestore()`·`vi.restoreAllMocks()`          |
| 가짜 시계                    | `vi.useRealTimers()`                            |
| `vi.stubGlobal`·`vi.stubEnv` | `vi.unstubAllGlobals()`·`vi.unstubAllEnvs()`    |

`vi.restoreAllMocks()`는 모든 모킹·호출 이력을 초기화하는 명령이 아닙니다.

참고: [Vitest 모듈 모킹](https://vitest.dev/guide/mocking/modules)·[vi 유틸리티](https://vitest.dev/api/vi).
