# 타입 재사용

## 같은 계약의 부분·변형 → 내장 유틸리티

원본의 필드 변경을 함께 반영할 타입은 `Pick`·`Omit`으로 파생합니다. 별도로 진화해야 하는 API 계약까지 같은 타입에 묶지는 않습니다.

````ts
// product.ts

/**
 * 상품 목록과 생성 입력에서 공유하는 상품 정보입니다.
 *
 * @see {@link ProductSummary} - 목록용 상품 정보
 * @see {@link CreateProductInput} - 상품 생성 입력
 */
export interface Product {
  readonly id: string;
  name: string;
  price: number;
}

/**
 * {@link Product}에서 가격을 제외한 목록용 상품 정보입니다.
 *
 * @see {@link toProductSummary} - 실제 객체에서 공개할 필드 선택
 */
export type ProductSummary = Pick<Product, "id" | "name">;

/** {@link Product}의 식별자를 할당하기 전 생성 입력입니다. */
export type CreateProductInput = Omit<Product, "id">;

/**
 * 원본 {@link Product}를 변경하지 않고 {@link ProductSummary}를 만듭니다.
 *
 * @example
 * ```ts
 * import { toProductSummary } from "./product.ts";
 *
 * const product = { id: "p1", name: "머그컵", price: 1200 };
 *
 * console.log(toProductSummary(product)); // { id: "p1", name: "머그컵" }
 * console.log(product.price); // 1200
 * ```
 */
export function toProductSummary(product: Product): ProductSummary {
  return { id: product.id, name: product.name };
}
````

`Pick`·`Omit`은 실행 시 필드를 제거하지 않습니다. 반환할 필드를 제한하려면 위처럼 새 객체를 구성합니다. 내장 유틸리티로 표현할 수 있으면 같은 기능의 조건부·매핑 타입을 다시 만들지 않습니다. [유틸리티 타입](https://www.typescriptlang.org/docs/handbook/utility-types.html)

## 객체·키·반환값의 관계 → 제네릭

키가 객체에 존재하도록 제한하고, 선택한 속성의 타입을 그대로 반환합니다.

````ts
// get-property.ts

/**
 * 선택한 속성의 타입을 유지하며 값을 읽습니다.
 *
 * @typeParam T - 속성을 읽을 객체의 타입
 * @typeParam K - T에 존재하는 키. 반환 타입은 해당 속성의 타입으로 결정됩니다.
 *
 * @example
 * ```ts
 * import { getProperty } from "./get-property.ts";
 *
 * const product = { name: "머그컵", price: 1200 };
 * const price = getProperty(product, "price"); // number로 추론
 *
 * console.log(price.toFixed(2)); // "1200.00"
 * ```
 */
export function getProperty<T, K extends keyof T>(value: T, key: K): T[K] {
  return value[key];
}
````

존재하지 않는 키를 전달하면 타입 오류가 됩니다. `key: string`과 `unknown` 반환값으로 관계를 잃지 않습니다.

타입 관계를 보존할 필요가 없으면 `formatLabel(value: string): string`처럼 구체 타입을 사용합니다. 조건부·재귀 타입은 단순한 타입으로 필요한 관계를 표현할 수 없을 때 도입합니다. [제네릭 함수 작성 기준](https://www.typescriptlang.org/docs/handbook/2/functions.html#guidelines-for-writing-good-generic-functions)
