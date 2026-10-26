# 패키지 구성

## Node.js 패키지

`packages/example/`에 `@example/sample`을 추가하는 예제입니다.
루트의 `tsconfig.base.json`과 `packages/*`를 수집하는 pnpm·Vitest 설정, 개발 의존성이 필요합니다.

기존 패키지에는 필요한 필드만 반영합니다.

```text
packages/example/
├── package.json
├── README.md
├── tsconfig.json
├── vitest.config.ts
└── src/
    └── index.ts          # 공유 API를 제공할 때 추가
```

`package.json`

```json
{
  "name": "@example/sample",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "typecheck": "tsc"
  }
}
```

`tsconfig.json`

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "lib": ["es2025"],
    "module": "nodenext",
    "types": ["node"]
  }
}
```

공통 설정의 전제:

- `noEmit`·`.ts` 확장자 import 허용
- `files`·`include`·`exclude` 미지정

파일 탐색 범위를 상속받으면 실제 목록을 확인하고 패키지 범위로 재정의합니다.

```ts
// vitest.config.ts
import { defineProject } from "vitest/config";

// Knip이 기본 테스트 파일을 인식하도록 test 객체를 유지합니다.
// 참고: https://knip.dev/reference/plugins/vitest
export default defineProject({ test: {} });
```

프로젝트 이름은 루트 Vitest 설정과 맞춥니다. Node.js 외의 실행 환경은 해당 프로젝트에 지정합니다.

공유 API는 [단일 배럴](entry-points.md#단일-배럴)을, CLI는 [실행 명령](entry-points.md#실행-명령)을 적용합니다.

## 타입 검사 범위

소스·테스트·설정의 전역 타입·모듈 해석 규칙이 호환되면 함께 검사합니다.
선언 충돌이나 브라우저의 Node.js 전역 차단이 필요하면 설정을 나눕니다.

| 설정                | 적용 기준·제약                                                              |
| ------------------- | --------------------------------------------------------------------------- |
| `types`             | 모든 대상 파일에 전역 타입 제공; 실행 기능은 추가하지 않음                  |
| `include`·`exclude` | 기본 탐색으로 부족할 때 지정; 제외한 파일도 import되면 검사에 포함          |
| `paths`             | 런타임 경로는 그대로이므로 생성 도구·테스트·번들러도 별칭을 해석하는지 확인 |

변경 전후 `tsc --showConfig`의 시작 파일과 `tsc --listFilesOnly`의 전이 참조를 대조합니다.
분리한 설정을 검사 명령에 모두 연결하고 실제 실행·빌드도 검증합니다.

### 참고

- [실행 환경과 모듈 옵션](https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html)
- [전역 타입](https://www.typescriptlang.org/tsconfig/types.html)
- [파일 제외](https://www.typescriptlang.org/tsconfig/#exclude)
- [경로 별칭](https://www.typescriptlang.org/tsconfig/#paths)

## 빌드와 릴리스 소유권

독립 배포할 앱은 해당 패키지에서 산출물을 만들고, 공유 라이브러리는 소비 앱의 번들에 포함할 수 있습니다.

| 소유자                      | 책임                                                                   |
| --------------------------- | ---------------------------------------------------------------------- |
| 각 실행 패키지              | 빌드 명령·바이너리 이름·실행 진입점·전용 자산 생성                     |
| 공통 빌드 도구              | 명시한 구성의 번들·실행 파일 생성·메타데이터·실패 시 정리              |
| 특정 의존성을 사용하는 모듈 | 환경별 로더·네이티브 파일 선택 등 해당 의존성의 배포 계약              |
| 릴리스 조립 영역            | 각 패키지의 공개 빌드 명령 실행·결과 대조·전체 릴리스 취합과 설치 검증 |

공통 빌드 도구는 앱의 공개 설정·콜백을 받습니다.
이를 사용하는 앱의 개발 의존성으로 연결하고, 단순 명령 반복은 워크스페이스 실행 도구에 맡깁니다.
릴리스 조립에 독립된 의존성·진입점이 필요하면 별도 패키지로 구성할 수 있습니다.

아래 경로는 기존 저장소에 맞춥니다.

```text
packages/
├── app/                        # 실행 진입점·앱 전용 빌드 설정과 명령
├── library/src/codec/          # 선택한 의존성의 로더·자산 준비
└── build-tool/src/             # 앱과 무관한 구성·생성 계약
scripts/release/                # 공개 빌드 명령의 실행·취합·설치 검사
```

개발·배포 명령이 올바른 진입점을 사용하는지 확인합니다.
배포 파일과 선언한 실행 의존성만으로 실행해 네이티브 기능·정적 자산까지 검증합니다.

## 워크스페이스 연결

`packages/*` 또는 `apps/*`·`libs/*`·`tools/*` 등 기존 저장소의 구조를 따릅니다.
디렉터리를 옮겨도 패키지의 공개 이름·명령은 유지합니다.

| 연결할 항목    | 확인할 내용                                                                             |
| -------------- | --------------------------------------------------------------------------------------- |
| 패키지 검색    | pnpm·Vitest·미사용 코드 분석 도구의 검색 범위; 공통 glob이 포함하면 개별 경로 추가 생략 |
| 경로 참조      | import·실행 진입점·문서 링크·린트 경계·테스트 픽스처                                    |
| 의존성         | 내부 패키지는 `workspace:*`, 루트 catalog의 공유 버전은 `catalog:`                      |
| 공통 개발 도구 | Node.js 타입·TypeScript·Vitest는 루트 구성 사용                                         |
| 패키지 안내    | README의 사용법·개발 명령과 실제 구성 일치                                              |

루트에서 설치를 실행해 새 패키지를 잠금 파일에 반영한 뒤 전체 검사를 실행합니다.

```sh
pnpm install
pnpm check
```

루트 검사가 패키지의 타입 검사·테스트를 포함하는지 확인합니다. 테스트가 없는 골격은 동작 검증을 미실행으로 보고합니다.

브라우저·프레임워크 패키지에는 해당 환경의 타입·빌드·테스트 설정을 구성합니다.
