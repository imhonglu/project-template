# 비동기 예제

## HTTP 응답

- 선행 파일: [외부 입력 예제](type-patterns.md#외부-입력)의 `user.ts`를 같은 디렉터리에 배치
- 실행: 독립된 Node.js 프로세스; `fetch` 고정 응답으로 외부 요청 없이 확인
- 적용: `api.example.com`을 실제 API 주소로 교체

````ts
// user-client.ts
import { parseUser } from "./user.ts";
import type { User } from "./user.ts";

/**
 * API에서 사용자를 조회하고 {@link parseUser}로 응답을 검증합니다.
 *
 * @param id - URL 경로에 인코딩해 넣을 사용자 식별자
 * @returns 검증·정규화된 {@link User}로 이행되는 Promise
 *
 * @throws Error
 * 네트워크·HTTP·응답 파싱·검증 실패 시 Promise를 거부합니다.
 * 원래 오류는 cause에 보존합니다.
 *
 * @example 외부 요청 없이 사용자 응답 처리
 * ```ts
 * import { loadUser } from "./user-client.ts";
 *
 * const originalFetch = globalThis.fetch;
 *
 * try {
 *   globalThis.fetch = () => Promise.resolve(Response.json({ id: " u1 ", name: " 민수 " }));
 *
 *   const user = await loadUser("u1");
 *
 *   console.log(user); // { id: "u1", name: "민수" }
 * } finally {
 *   globalThis.fetch = originalFetch;
 * }
 * ```
 */
export async function loadUser(id: string): Promise<User> {
  try {
    const url = `https://api.example.com/users/${encodeURIComponent(id)}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const value: unknown = await response.json();

    return parseUser(value);
  } catch (cause) {
    throw new Error(`사용자 ${id} 조회 실패`, { cause });
  }
}
````

- HTTP·파싱 실패를 빈 값으로 바꾸지 않습니다.
- 미존재가 정상 결과인 API는 해당 상태만 별도 처리합니다.

근거: [Error.cause](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause).

## 파일 I/O

독립된 파일 읽기 → 두 결과가 준비된 뒤 쓰기 순서입니다.

- 실행: `mkdtempDisposable`·`await using` 지원 Node.js
- 정리: 사용 예의 스코프 종료 시 임시 디렉터리 삭제 ([API](https://nodejs.org/api/fs.html#fspromisesmkdtempdisposableprefix-options))

````ts
// combine-files.ts
import { readFile, writeFile } from "node:fs/promises";

/**
 * 두 UTF-8 파일을 줄바꿈 하나로 이어 출력 파일에 씁니다.
 *
 * @remarks
 * - 두 파일을 모두 읽은 뒤 쓰기를 시작합니다.
 * - 기존 출력 파일은 덮어씁니다.
 * - 쓰기 실패 시 출력 파일이 일부만 기록될 수 있습니다.
 *
 * @param headerPath - 앞에 넣을 파일 경로
 * @param bodyPath - 뒤에 넣을 파일 경로
 * @param outputPath - 결과를 저장할 파일 경로
 * @returns 출력 파일 쓰기가 완료되면 이행되는 Promise
 *
 * @throws 파일 읽기·쓰기 실패 시 해당 오류로 Promise를 거부합니다.
 *
 * @example 임시 파일 결합 후 내용 확인
 * ```ts
 * import { mkdtempDisposable, readFile, writeFile } from "node:fs/promises";
 * import { tmpdir } from "node:os";
 * import { join } from "node:path";
 *
 * import { combineFiles } from "./combine-files.ts";
 *
 * await using directory = await mkdtempDisposable(join(tmpdir(), "combine-files-"));
 * const headerPath = join(directory.path, "header.txt");
 * const bodyPath = join(directory.path, "body.txt");
 * const outputPath = join(directory.path, "output.txt");
 *
 * await writeFile(headerPath, "제목", "utf8");
 * await writeFile(bodyPath, "본문", "utf8");
 *
 * await combineFiles(headerPath, bodyPath, outputPath);
 *
 * const content = await readFile(outputPath, "utf8");
 *
 * console.log(content); // "제목\n본문"
 * ```
 */
export async function combineFiles(
  headerPath: string,
  bodyPath: string,
  outputPath: string,
): Promise<void> {
  const [header, body] = await Promise.all([
    readFile(headerPath, "utf8"),
    readFile(bodyPath, "utf8"),
  ]);

  await writeFile(outputPath, `${header}\n${body}`, "utf8");
}
````

- `Promise.all` 실패는 이미 시작한 다른 작업을 취소하지 않습니다.
- 대량 요청·재시도에는 동시 실행 수·종료 조건을 정합니다.

근거: [Promise.all](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all).
