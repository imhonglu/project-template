# 패키지 구성

## Node.js 패키지

`packages/example/`에 `@example/sample`을 추가하는 예제입니다. 경로는 기존 저장소 구조에 맞추고, 기존 패키지에는 필요한 필드만 반영합니다.
저장소 루트의 `tsconfig.base.json`과 해당 경로를 수집하는 pnpm·Vitest 설정, 개발 의존성이 필요합니다.

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
  "type": "module"
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

공통 설정에 `files`·`include`·`exclude`가 있으면 아래 범위 진단 명령으로 상속 결과를 읽습니다. 다른 패키지의 파일까지 시작 파일로 수집하면 패키지의 실제 소스·테스트·설정 경로로 재정의합니다.

```ts
// vitest.config.ts
import { defineProject } from "vitest/config";

// Knip이 기본 테스트 파일을 인식하도록 test 객체를 유지합니다.
// 참고: https://knip.dev/reference/plugins/vitest
export default defineProject({ test: {} });
```

프로젝트 이름은 루트 Vitest 설정이 지정하는 이름과 맞춥니다. 브라우저·DOM 등 Node.js 이외의 전역·실행 기능이 필요하면 해당 프로젝트에 환경과 타입을 지정합니다.

공유 API는 [단일 배럴](entry-points.md#단일-배럴)을, CLI는 [실행 명령](entry-points.md#실행-명령)을 적용합니다.

## 타입 검사 범위

소스·테스트·설정이 같은 전역 선언과 모듈 해석 규칙을 사용하면 하나의 설정으로 검사합니다.
동명 전역 선언이 충돌하거나 브라우저 코드에서 Node.js 전역을 차단해야 하면 설정을 나누고 각 파일을 해당 환경의 검사에 포함합니다.

| 설정                | 선택·한계                                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `types`             | 대상 파일에 자동으로 포함할 전역 타입 패키지를 제한; 실행 기능을 추가하거나 명시적 import의 타입을 차단하지는 않음            |
| `include`·`exclude` | 기본 탐색이 대상 파일을 빠뜨리거나 다른 환경까지 수집할 때 지정; 제외한 파일도 import되면 포함될 수 있음                      |
| `paths`             | 타입 검사기의 경로 해석만 지정하고 import 문자열은 바꾸지 않음; 소비자의 실행·생성·테스트·번들 명령에도 같은 별칭 해석을 구성 |

저장소 루트에서 실제 설정 경로로 범위를 확인합니다.

```sh
pnpm exec tsc --project packages/example/tsconfig.json --showConfig
pnpm exec tsc --project packages/example/tsconfig.json --listFilesOnly
```

- `--showConfig`: 상속된 설정과 시작 파일. 의도한 소스·테스트·설정이 포함되는지 확인합니다.
- `--listFilesOnly`: import된 파일·선언까지 포함. 누락과 다른 환경의 전역 타입 유입을 구별합니다.

설정을 나누면 각 설정을 기존 타입 진단 단계에 연결합니다. 목록 출력은 타입 검사가 아니므로 실제 진단 명령도 실행합니다. 직접 검사하려면 다음 명령을 사용하며 같은 진단이 기존 검사에 있으면 반복하지 않습니다.

```sh
pnpm exec tsc --project packages/example/tsconfig.json --noEmit
```

Oxlint의 진입 파일은 별도로 확인합니다. tsconfig의 `include`·`exclude`만으로 Oxlint 탐색 범위가 제한되지는 않습니다.

```sh
pnpm exec oxlint --debug files
```

이 출력도 진단 결과나 전체 TypeScript 프로그램 목록은 아닙니다. 누락되면 실행 경로·지원 확장자·ignore 설정을 확인합니다. 검사 단계의 배치는 저장소 스크립트·훅 정책을 따릅니다.

### 참고

- [실행 환경과 모듈 옵션](https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html)
- [TypeScript CLI의 설정·파일 목록 옵션](https://www.typescriptlang.org/docs/handbook/compiler-options.html#cli-commands)
- [Oxlint CLI의 파일 탐색 진단](https://oxc.rs/docs/guide/usage/linter/cli.md)
- [전역 타입](https://www.typescriptlang.org/tsconfig/types.html)
- [파일 제외](https://www.typescriptlang.org/tsconfig/#exclude)
- [경로 별칭](https://www.typescriptlang.org/tsconfig/#paths)

## 빌드와 릴리스

배포 단위로 실행할 앱은 해당 패키지의 빌드 명령과 산출물을 정의합니다. 공유 라이브러리를 소비 앱이 직접 번들하면 라이브러리만의 빌드를 새로 만들지 않습니다.

| 소유자                      | 책임                                                             |
| --------------------------- | ---------------------------------------------------------------- |
| 각 실행 패키지              | 빌드 명령·바이너리 이름·실행 진입점·전용 자산 생성               |
| 공통 빌드 도구              | 명시한 구성의 번들·실행 파일 생성·메타데이터·실패 시 정리        |
| 특정 의존성을 사용하는 모듈 | 환경별 로더·네이티브 파일 선택 등 해당 의존성의 배포 계약        |
| 릴리스 조립 영역            | 각 패키지가 공개한 빌드 명령 실행·산출물 취합·설치 환경에서 실행 |

공통 빌드 도구를 쓰면 앱이 공개 설정·콜백을 전달하고 앱의 개발 의존성으로 연결합니다. 도구가 앱의 비공개 구현을 import해 빌드 설정을 추측하지 않게 합니다.
단순 명령 반복은 기존 워크스페이스 실행 도구에 맡깁니다.
릴리스 조립이 별도 실행 진입점·의존성 집합을 요구하면 그 구성도 명시합니다.

### 실행 검증

빌드·실행 명령은 각 패키지의 `package.json`과 README가 정한 것을 사용합니다. 모든 패키지에 같은 `build`·`start` 스크립트가 있다고 가정하지 않습니다.

| 대상              | 사용할 명령·성공 기준                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| 개발·배포 실행    | 해당 패키지의 개발 명령은 개발 진입점을, 배포 명령은 실제 산출물을 실행                            |
| 배포 파일         | 배포 디렉터리 또는 설치 패키지의 선언된 실행 의존성만으로 네이티브 로더·정적 자산을 읽고 기능 실행 |
| 소비자            | 소비 패키지의 타입 검사·빌드 명령이 지원하는 공개 경로를 해석하고, 실행 명령에서 그 API 호출 성공  |
| 라이브러리 import | import만으로 서비스·검사 프로세스가 시작되거나 종료 코드·종료 정책이 변경되지 않음                 |

`noEmit` 타입 검사는 JavaScript·선언 산출물을 만들지 않습니다. 배포할 파일·선언 경로는 실제 빌드 출력과 `exports`를 대조합니다.
프레임워크·번들러 설정을 작성·변경할 때는 설치 버전의 공식 문서를 따릅니다. 공식 `llms.txt`가 제공되면 해당 설정을 찾는 색인으로 사용합니다.

## 워크스페이스 연결

`packages/*` 또는 `apps/*`·`libs/*`·`tools/*` 등 기존 저장소의 구조를 따릅니다.
공통 검사는 저장소 루트에서, 환경별 빌드·실행·테스트 설정과 명령은 해당 패키지에서 관리합니다.

| 연결할 항목    | 확인할 내용                                                                             |
| -------------- | --------------------------------------------------------------------------------------- |
| 패키지 검색    | pnpm·Vitest·미사용 코드 분석 도구의 검색 범위; 공통 glob이 포함하면 개별 경로 추가 생략 |
| 경로 참조      | import·실행 진입점·문서 링크·린트 경계·테스트 픽스처                                    |
| 의존성         | 내부 패키지는 `workspace:*`, 루트 catalog의 공유 버전은 `catalog:`                      |
| 공통 개발 도구 | Node.js 타입·TypeScript·Vitest는 루트 구성 사용                                         |
| 패키지 안내    | README의 사용법·개발 명령과 실제 구성 일치                                              |

패키지·의존성 선언을 바꾸면 저장소 루트에서 설치와 기존 공통 검사를 실행합니다.

```sh
pnpm install
pnpm check
```

새 패키지와 소스·테스트·설정이 검색·검사 대상에 포함돼야 합니다. 중단된 후속 검사나 테스트가 없는 런타임 동작은 미검증으로 보고합니다.
빌드·검사 캐시는 전이 의존성의 변경도 반영해야 합니다. 루트 검사에 없는 빌드·설치 소비자의 실행은 패키지 명령으로 별도 확인합니다.

브라우저·프레임워크 패키지는 해당 환경의 전역 타입·모듈 해석·빌드·테스트 설정을 소유합니다. 타입 선언만 추가해 런타임 기능이 생긴 것으로 취급하지 않습니다.
