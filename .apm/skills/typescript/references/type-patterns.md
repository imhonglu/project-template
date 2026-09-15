# 타입 예제

## 외부 입력 → 검증된 객체

객체 계약은 `interface`, 검증 전 값은 `unknown`을 사용합니다. 이미 스키마 검증기를 사용하는 코드에서는 해당 스키마를 재사용합니다.

````ts
// user.ts

/**
 * 사용자를 식별하고 화면에 표시하는 기본 정보입니다.
 *
 * @see {@link parseUser} - 외부 입력 검증과 정규화
 */
export interface User {
  readonly id: string;
  name: string;
}

/**
 * 외부 입력을 검증하고 {@link User}로 정규화합니다.
 *
 * @param value - id와 name을 검사할 외부 입력
 * @returns id와 name의 양끝 공백을 제거한 새 객체. 나머지 속성은 포함하지 않습니다.
 * @throws TypeError - 입력이 객체가 아니거나, id·name이 문자열이 아니거나 공백 제거 후 비어 있는 경우
 *
 * @example
 * ```ts
 * import { parseUser } from "./user.ts";
 *
 * const user = parseUser({ id: " u1 ", name: " 민수 " });
 *
 * console.log(user); // { id: "u1", name: "민수" }
 * ```
 */
export function parseUser(value: unknown): User {
  if (typeof value !== "object" || value === null) {
    throw new TypeError("사용자 객체가 필요합니다.");
  }

  if (!("id" in value) || typeof value.id !== "string" || value.id.trim() === "") {
    throw new TypeError("id는 비어 있지 않은 문자열이어야 합니다.");
  }

  if (!("name" in value) || typeof value.name !== "string" || value.name.trim() === "") {
    throw new TypeError("name은 비어 있지 않은 문자열이어야 합니다.");
  }

  return { id: value.id.trim(), name: value.name.trim() };
}
````

`JSON.parse()`·`response.json()` 결과도 `unknown` 변수에 받은 뒤 검증합니다. `as User`는 위 검증의 대체물이 아닙니다. [타입 좁히기](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

## 상태 → 판별 가능한 유니온

`user?`·`error?`를 한 객체에 나열하면 둘 다 있거나 둘 다 없는 상태를 허용합니다. 상태별 필수 데이터를 묶고, 분기 마지막의 `never`로 새 상태 누락을 검사합니다.

```ts
// user-state.ts
import type { User } from "./user.ts";

/**
 * 사용자 조회 단계와 각 단계에서 사용할 데이터를 묶습니다.
 *
 * @see {@link getUserLabel} - 상태에 따른 화면 문구
 */
export type UserState =
  | { status: "loading" }
  | {
      status: "ready";
      user: User;
    }
  | {
      status: "failed";
      error: Error;
    };

/** {@link UserState}에 따라 대기 문구, 사용자 이름 또는 오류 메시지를 반환합니다. */
export function getUserLabel(state: UserState): string {
  switch (state.status) {
    case "loading":
      return "불러오는 중";
    case "ready":
      return state.user.name;
    case "failed":
      return state.error.message;
    default: {
      const unexpected: never = state;

      throw new Error("알 수 없는 상태", { cause: unexpected });
    }
  }
}
```

## 고정 목록·설정 → `as const`·`satisfies`

`as const`는 목록의 리터럴 타입을 유지하고, `satisfies`는 추론 결과를 유지하면서 필요한 키와 값 타입을 검사합니다.

```ts
// access-level.ts

/**
 * 지원하는 권한 목록입니다.
 *
 * @see {@link AccessLevel} - 목록에서 파생한 권한 타입
 */
export const ACCESS_LEVELS = ["reader", "editor"] as const;

/** {@link ACCESS_LEVELS}에 포함된 권한입니다. */
export type AccessLevel = (typeof ACCESS_LEVELS)[number];

/** {@link AccessLevel}별 화면 표시 문구입니다. */
export const ACCESS_LABELS = {
  reader: "읽기",
  editor: "편집",
} as const satisfies Record<AccessLevel, string>;
```

리터럴 고정이 필요 없는 일반 객체에는 `as const`를 붙이지 않습니다. [satisfies 연산자](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator)

## 읽기 전용 입력 → 새 배열로 변환

`readonly`는 해당 참조를 통한 변경을 타입 검사로 제한합니다. 입력 배열의 순서를 유지하며 정렬할 때는 `sort()` 대신 새 배열을 반환하는 `toSorted()`를 사용합니다.

````ts
// sorted-prices.ts

/**
 * 원본 가격 목록을 유지하며 낮은 가격부터 정렬합니다.
 *
 * @param prices - 정렬할 가격 목록
 * @returns 오름차순으로 정렬한 새 배열
 *
 * @example
 * ```ts
 * import { getSortedPrices } from "./sorted-prices.ts";
 *
 * const prices = [3000, 1200, 2400];
 * const sortedPrices = getSortedPrices(prices);
 *
 * console.log(sortedPrices); // [1200, 2400, 3000]
 * console.log(prices); // [3000, 1200, 2400]
 * ```
 */
export function getSortedPrices(prices: readonly number[]): number[] {
  return prices.toSorted((left, right) => left - right);
}
````

`readonly`·`Readonly<T>`는 런타임 동결이나 깊은 불변성을 보장하지 않습니다. 객체 배열을 복사해도 원소 객체는 공유하므로, 중첩 값을 바꿀 때는 해당 객체도 새로 만듭니다. [읽기 전용 속성](https://www.typescriptlang.org/docs/handbook/2/objects.html#readonly-properties)

## 선택 속성 → 생략과 빈 값 구분

아래 계약에서 속성 생략은 변경 없음, 빈 문자열은 값 비우기입니다. `nickname?: string`에 `undefined`를 대입하는 대신 속성을 생략합니다.

````ts
// profile-patch.ts

/**
 * 프로필에서 변경할 값만 전달합니다.
 *
 * @see {@link createProfilePatch} - 닉네임 입력을 변경 요청으로 변환
 */
export interface ProfilePatch {
  /** 생략하면 유지하고, 빈 문자열이면 기존 닉네임을 비웁니다. */
  nickname?: string;
}

/**
 * 닉네임 입력을 프로필 변경 요청으로 변환합니다.
 *
 * @param nickname - 새 닉네임. undefined이면 변경 요청에서 생략합니다.
 * @returns {@link ProfilePatch}의 생략·빈 값 규칙을 따르는 요청 객체
 *
 * @example
 * ```ts
 * import { createProfilePatch } from "./profile-patch.ts";
 *
 * console.log(createProfilePatch(undefined)); // {}
 * console.log(createProfilePatch("")); // { nickname: "" }
 * console.log(createProfilePatch("민수")); // { nickname: "민수" }
 * ```
 */
export function createProfilePatch(nickname: string | undefined): ProfilePatch {
  return nickname === undefined ? {} : { nickname };
}
````

`0`·`false`·빈 문자열이 유효한 값이면 `||`로 기본값을 채우지 않습니다. `null`·`undefined`만 대체할 때 `??`를 사용합니다. [exactOptionalPropertyTypes](https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html)
