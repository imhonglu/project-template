# 값과 타입 검증

공개 제네릭·유니온·타입 유틸리티의 추론 결과가 계약이면 값의 테스트에 타입 단언을 함께 둡니다. 구현 가까이의 일반 `.test.ts`에 작성하고 JSX는 `.test.tsx`, 기존 `.spec`은 그대로 사용합니다. 타입 테스트 전용 접미사·디렉터리는 만들지 않습니다.
값은 Vitest 실행으로, `expectTypeOf`는 해당 파일을 포함한 실제 타입 진단으로 검증합니다. 일반 Vitest 실행은 TypeScript를 변환할 뿐 타입 오류를 검사하지 않습니다.

## 첫 원소의 값과 추론 결과

두 파일을 같은 디렉터리에 둡니다.

```ts
// first-item.ts

/**
 * 목록을 변경하지 않고 첫 원소를 반환합니다.
 *
 * @typeParam T - 목록 원소의 타입
 *
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

기대 타입은 공개 계약에 따라 직접 명시합니다. `ReturnType<typeof firstItem>`에서 가져오면 잘못된 반환 타입 변경도 따라가므로 회귀를 잡을 수 없습니다. 값의 단언과 타입의 단언은 같은 사례에 남겨 어떤 입력에서 어떤 추론을 보장하는지 드러냅니다.

## 파일 포함과 검사 명령

실제 `package.json`·Vitest 설정·tsconfig에서 **테스트 수집과 타입 검사 포함 여부를 각각 확인**합니다. 아래는 두 예제 파일을 `libs/example/src/`에 두고 루트 `test`가 Vitest를 실행하는 경우입니다. 경로·명령은 기존 구성에 맞춥니다.

```sh
package_path=libs/example
pnpm exec tsc --project "$package_path/tsconfig.json" --showConfig
pnpm exec tsc --project "$package_path/tsconfig.json" --listFilesOnly
```

출력에 `first-item.ts`와 `first-item.test.ts`가 모두 있어야 합니다. 첫 명령은 상속된 설정, 둘째는 import된 선언까지 확인하며 타입 진단은 실행하지 않습니다.
테스트가 빠지면 포함 범위를 고칩니다. Node.js·브라우저 전역 충돌로 설정을 나눴다면 테스트용 설정도 기존 검사 단계에 연결합니다.

```sh
package_path=libs/example
pnpm exec tsc --project "$package_path/tsconfig.json" --noEmit
pnpm test "$package_path/src/first-item.test.ts"
```

기존 검사 명령이 같은 타입 진단·런타임 실행을 포함하면 중복 실행하지 않습니다. 루트 성공·미수집 성공·`passWithNoTests`만으로 해당 파일의 통과를 보고하지 않습니다.
타입 단언 실패를 감추려고 런타임 수집에서 빼거나 특수 접미사로 바꾸지 않습니다.

Oxlint를 사용하면 `pnpm exec oxlint --debug files`로 진입 파일을 별도로 확인합니다. tsconfig의 `include`·`exclude`만으로 Oxlint 탐색 범위가 제한되지는 않으며, 어느 쪽 파일 목록도 타입 진단 결과를 대신하지 않습니다.
실행한 명령·설정·대상 파일·진단 결과와 미검증 범위를 보고합니다.

## 참고

- [Vitest 타입 테스트](https://vitest.dev/guide/testing-types)
- [expectTypeOf](https://vitest.dev/api/expect-typeof)
- [TypeScript CLI의 설정·파일 목록 옵션](https://www.typescriptlang.org/docs/handbook/compiler-options.html#cli-commands)
- [TypeScript include](https://www.typescriptlang.org/tsconfig/include.html)
- [TypeScript exclude와 import 포함](https://www.typescriptlang.org/tsconfig/exclude.html)
- [Oxlint CLI의 파일 탐색 진단](https://oxc.rs/docs/guide/usage/linter/cli.md)
