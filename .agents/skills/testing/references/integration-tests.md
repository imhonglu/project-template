# 통합 테스트

## 실제 파일에 저장한 메모 다시 읽기

`mkdtempDisposable`·`await using`을 지원하는 Node.js 환경의 예제입니다. 입력별 테스트를 동시에 실행하며 각각 새 임시 디렉터리에서 저장·조회합니다.

```ts
// note-store.ts
import { readFile, writeFile } from "node:fs/promises";

/**
 * 앞뒤 공백을 제거한 메모로 UTF-8 파일을 덮어씁니다.
 *
 * @returns 파일 쓰기가 완료되면 이행되는 Promise
 * @throws 파일 쓰기 실패 시 해당 오류로 Promise를 거부합니다.
 * @see {@link readNote} - 저장한 메모 다시 읽기
 */
export function saveNote(filePath: string, content: string): Promise<void> {
  return writeFile(filePath, content.trim(), "utf8");
}

/**
 * UTF-8 파일에 저장된 메모를 그대로 읽습니다.
 *
 * @returns 파일 내용으로 이행되는 Promise
 * @throws 파일 읽기 실패 시 해당 오류로 Promise를 거부합니다.
 * @see {@link saveNote} - 메모 정리와 저장
 */
export function readNote(filePath: string): Promise<string> {
  return readFile(filePath, "utf8");
}
```

```ts
// note-store.integration.test.ts
import { mkdtempDisposable } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { it } from "vitest";

import { readNote, saveNote } from "./note-store.ts";

it.concurrent.for([
  {
    name: "메모의 앞뒤 공백을 제거해 다시 읽습니다",
    input: "  다음 회의 안건  \n",
    expected: "다음 회의 안건",
  },
  {
    name: "공백뿐인 메모를 빈 문자열로 저장합니다",
    input: "  \n",
    expected: "",
  },
])("$name", async ({ input, expected }, { expect }) => {
  await using directory = await mkdtempDisposable(join(tmpdir(), "note-store-"));
  const filePath = join(directory.path, "note.txt");

  await saveNote(filePath, input);
  const content = await readNote(filePath);

  expect(content).toBe(expected);
});
```

`it.for`는 입력과 테스트 컨텍스트를 각각 전달합니다. 두 번째 인수의 `{ expect }`로 현재 테스트에 연결된 단언을 사용합니다. [매개변수화 테스트](https://main.vitest.dev/api/test#test-for)

`await using`은 테스트 콜백이 정상 종료되거나 예외로 끝나도 디렉터리와 내용을 삭제합니다. [Node.js 임시 디렉터리 정리](https://nodejs.org/api/fs.html#fspromisesmkdtempdisposableprefix-options)

이 예제에서 `readFile`·`writeFile`을 모킹하면 파일 저장·조회 경계를 검증할 수 없습니다.

## 다른 자원에 적용

| 자원      | 격리·검증 기준                                                      |
| --------- | ------------------------------------------------------------------- |
| 파일      | 테스트별 임시 경로; 저장 후 다시 읽어 내용 확인                     |
| DB        | 테스트 전용 DB·스키마·트랜잭션; 실제 마이그레이션·쿼리 실행 후 정리 |
| HTTP 서버 | 임의 포트로 시작하고 종료 훅 등록; 상태 코드·응답·저장 결과 확인    |

- 스코프 밖에서 공유하거나 자동 정리를 지원하지 않는 자원은 생성 직후 사용 수명에 맞는 정리 훅을 등록합니다.
- DB 엔진별 연산을 검증할 때는 해당 엔진을 사용합니다. 트랜잭션 롤백은 모든 작업이 그 트랜잭션에 참여할 때만 격리를 보장합니다.
- 테스트 간 공유 테이블을 무조건 비우는 정리 방식은 병렬 실행과 충돌할 수 있으므로 테스트별 격리 범위를 정합니다.

참고: [Vitest 테스트 컨텍스트](https://vitest.dev/guide/test-context)·[LobeHub DB 테스트 레퍼런스](https://github.com/lobehub/lobehub/blob/canary/.agents/skills/testing/references/db-model-test.md).
