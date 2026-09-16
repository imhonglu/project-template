# 브라우저 테스트

## 실행 조건

Vitest 브라우저 모드와 provider가 구성된 패키지에서 실행합니다. 이 예제의 `page`·`expect.element` 타입을 사용하려면 provider 패키지도 설치되어 있어야 합니다.

브라우저 테스트가 Node 프로젝트에도 포함되지 않도록 `include`·`exclude`를 설정합니다. JSX를 사용하면 해당 프레임워크의 렌더러와 `.tsx` 확장자를 사용합니다.

## 버튼 클릭으로 수량 증가

프레임워크 없이 DOM으로 구현하므로 `.ts`를 사용합니다. 버튼 클릭 전후의 수량을 화면에서 확인합니다.

```ts
// cart-counter.ts

/**
 * 1에서 시작해 버튼을 누를 때마다 수량이 증가하는 UI를 만듭니다.
 *
 * @returns 문서에 연결되지 않은 요소. 호출자가 DOM에 추가하고 사용 후 제거합니다.
 */
export function createCartCounter(): HTMLElement {
  let quantity = 1;
  const root = document.createElement("div");

  const output = document.createElement("output");
  output.setAttribute("aria-label", "수량");
  output.textContent = String(quantity);

  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "수량 추가";

  button.addEventListener("click", () => {
    quantity += 1;
    output.textContent = String(quantity);
  });

  root.append(output, button);

  return root;
}
```

```ts
// cart-counter.browser.test.ts
import { expect, it } from "vitest";
import { page } from "vitest/browser";

import { createCartCounter } from "./cart-counter.ts";

it("수량 추가 버튼을 누르면 화면의 수량이 1 증가합니다", async ({ onTestFinished }) => {
  const counter = createCartCounter();
  onTestFinished(() => counter.remove());
  document.body.append(counter);

  const quantity = page.getByLabelText("수량");

  await expect.element(quantity).toHaveTextContent("1");

  await page.getByRole("button", { name: "수량 추가", exact: true }).click();

  await expect.element(quantity).toHaveTextContent("2");
});
```

## 탐색·조작·단언

| 목적        | 컨벤션                                                                     |
| ----------- | -------------------------------------------------------------------------- |
| 요소 찾기   | `getByRole`·`getByLabelText` 우선; 의미 있는 식별자가 없을 때 test ID      |
| 사용자 조작 | locator의 `click`·`fill` 또는 `vitest/browser`의 `userEvent`; 항상 `await` |
| 화면 결과   | `await expect.element(locator)`; 고정 시간 대기 생략                       |
| 정리        | 직접 만든 DOM은 제거; 프레임워크 렌더러의 cleanup 지원 여부 확인           |

`querySelector(...).click()`·수동 이벤트 호출로 브라우저의 조작 가능 상태 검사를 우회하지 않습니다. 전체 앱의 페이지 전환·인증 흐름을 검증할 때는 해당 앱의 E2E 실행 환경을 사용합니다.

참고: [Vitest 컴포넌트 테스트](https://vitest.dev/guide/browser/component-testing)·[Playwright 테스트 원칙](https://playwright.dev/docs/best-practices).
