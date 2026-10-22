# 비동기 초기화와 소유권

비동기 준비를 마친 인스턴스를 반환하고, 직접 획득한 자원을 실패·종료 시 정리하는 예제입니다.

## 준비가 끝난 인스턴스 반환

Node.js의 `FileHandle`·`await using`을 지원하는 환경의 예제입니다.

````ts
// text-log.ts
import { open } from "node:fs/promises";
import type { FileHandle } from "node:fs/promises";

export interface TextLogOptions {
  /** 추가 모드로 연 일반 파일입니다. 생략하면 path를 열며, 제공하면 path는 사용하지 않습니다. */
  file?: FileHandle;
}

/**
 * UTF-8 문구를 파일 끝에 기록하고 직접 연 파일의 수명을 관리합니다.
 *
 * @remarks 호출자가 각 쓰기를 순서대로 기다린 뒤 종료해야 합니다.
 * 동시 쓰기·종료를 조정하는 큐는 제공하지 않습니다.
 *
 * @example 임시 파일에 기록한 뒤 닫기
 * ```ts
 * import { mkdtempDisposable, readFile } from "node:fs/promises";
 * import { tmpdir } from "node:os";
 * import { join } from "node:path";
 *
 * import { TextLog } from "./text-log.ts";
 *
 * await using directory = await mkdtempDisposable(join(tmpdir(), "text-log-"));
 * const path = join(directory.path, "events.log");
 *
 * {
 *   await using log = await TextLog.open(path);
 *
 *   await log.append("ready\n");
 * }
 *
 * const content = await readFile(path, "utf8");
 *
 * console.log(content); // "ready\n"
 * ```
 */
export class TextLog implements AsyncDisposable {
  readonly #file: FileHandle;
  readonly #ownsFile: boolean;
  #closed = false;

  private constructor(file: FileHandle, ownsFile: boolean) {
    this.#file = file;
    this.#ownsFile = ownsFile;
  }

  /**
   * 파일을 준비하고 일반 파일인지 확인한 뒤 반환합니다.
   *
   * @remarks 초기화 실패 시에도 직접 연 파일만 닫습니다. 실패 전에 새로 만든 파일은 제거하지 않습니다.
   *
   * @param path - 파일을 주입하지 않았을 때 추가 모드로 열 경로. 파일이 없으면 생성합니다.
   * @param options - 파일 주입은 {@link TextLogOptions}를 따릅니다.
   *
   * @returns 준비가 끝나 쓰기를 시작할 수 있는 로그 인스턴스
   * @throws 파일 열기·확인 실패 시 거부합니다. 일반 파일이 아니면 TypeError로 거부합니다.
   * 정리까지 실패하면 원래 오류와 정리 오류를 AggregateError에 보존합니다.
   */
  static async open(path: string, { file }: TextLogOptions = {}): Promise<TextLog> {
    const ownsFile = file === undefined;
    const handle = file ?? (await open(path, "a"));

    try {
      const stats = await handle.stat();

      if (!stats.isFile()) {
        throw new TypeError("일반 파일이 필요합니다.");
      }

      return new TextLog(handle, ownsFile);
    } catch (error) {
      if (ownsFile) {
        try {
          await handle.close();
        } catch (closeError) {
          throw new AggregateError([error, closeError], "파일 준비와 정리에 실패했습니다.");
        }
      }

      throw error;
    }
  }

  /**
   * 파일 끝에 문구를 기록합니다. 줄바꿈은 호출자가 제공합니다.
   *
   * @returns 파일 쓰기가 완료되면 이행됩니다.
   * @throws 종료 후 호출 또는 파일 쓰기 실패 시 거부합니다.
   */
  async append(text: string): Promise<void> {
    if (this.#closed) {
      throw new Error("이미 종료한 로그입니다.");
    }

    await this.#file.writeFile(text, "utf8");
  }

  /** 추가 쓰기를 막고 직접 연 파일을 닫습니다. 주입받은 파일의 종료 책임은 호출자에게 남습니다. */
  async [Symbol.asyncDispose](): Promise<void> {
    if (this.#closed) {
      return;
    }

    this.#closed = true;

    if (this.#ownsFile) {
      await this.#file.close();
    }
  }
}
````

## 확인할 경계

- 성공: 준비가 끝난 뒤 사용하고, 쓰기 완료 뒤 직접 연 파일을 닫는지 확인합니다.
- 초기화 실패: 자원을 얻기 전·후의 실패를 구분하고 얻은 자원의 정리와 원래 오류 보존을 확인합니다.
- 주입: 성공·실패·종료 뒤에도 빌린 자원의 소유자가 계속 사용할 수 있는지 확인합니다.
