# 문서 구조·Markdown·출처

## 구조 선택

### 순서가 있으면 번호 목록

아래 명령이 정의된 프로젝트의 절차 예제입니다.

```markdown
저장소 루트에서 실행합니다. 설치·자동 수정은 파일을 바꿀 수 있습니다.

1. `pnpm install`로 의존성을 설치합니다.
2. `pnpm fix`로 린트·포맷을 자동 수정합니다.
3. `pnpm check`로 검사합니다.

검사가 종료 코드 0으로 끝나면 성공입니다. 첫 실패 이후의 검사는 실행되지 않습니다.
```

### 같은 기준으로 비교하면 표

```markdown
| 목적                     | 명령         |
| ------------------------ | ------------ |
| 린트·포맷 자동 수정      | `pnpm fix`   |
| 파일 수정 없이 전체 검사 | `pnpm check` |
```

선택지가 짧으면 한 문장으로 충분합니다. 실행 위치·필수 설정도 비교해야 하면 열을 추가하고, 항목별 설명·예제가 길어지면 소제목으로 나눕니다.

## 중복과 계약 구분

### 코드가 이미 표현하면 설명 삭제

**중복 설명**

> 공개 모듈은 `export *`로, 타입만 제공하는 모듈은 `export type *`로 재수출합니다.

**예제로 충분** — 구현을 생략한 재수출 예제

```ts
export * from "./parse-input.ts";
export type * from "./transport.ts";
```

### 행동을 바꾸는 조건은 유지

- **과도한 축약:** 파일을 닫습니다.
- **계약 유지:** 쓰기 완료를 기다린 뒤 직접 연 파일을 닫습니다. 주입받은 파일은 호출자가 닫습니다.

완료 시점·종료 책임이 확인된 경우의 예입니다. API 설명에 섞인 서비스 재시작·싱글턴의 테스트 격리 검토는 운영 지침으로 옮깁니다. 표현만 수정하는 요청에서는 이 의무를 이동·삭제하지 않습니다.

## 설계안

가정·선택 기준·결정 상태가 드러나는 제안 예제입니다.

```markdown
## 제안과 근거

파일 내보내기에 작업 ID를 반환하고 결과를 조회하는 방식을 제안합니다.
큰 파일의 처리 시간이 HTTP 요청 제한을 넘길 수 있다는 가정입니다.

## 대안과 확인

지원할 최대 파일 크기·동시 요청 수에서 동기 응답과 작업 ID 방식의 처리 시간을 비교합니다.
동기 응답이 응답 시간 목표를 충족하면 동기 응답을 선택합니다.
측정 전이므로 방식은 미결정입니다.
```

## PR 설명

대상 PR의 base와 head 사이 최종 변경으로 제목·본문을 맞춥니다. 변경 이유를 먼저 쓰고 영향받는 동작과 검증 근거를 잇습니다. 되돌린 시도는 최종 선택을 설명하는 데 필요할 때만 남깁니다.
기존 본문의 이미지·재현 자료·관련 이슈는 유지합니다. 저장소 템플릿의 필수 항목을 채우고, 추가 검증은 이번 변경의 동작을 확인한 근거로 설명합니다. 코드 위치는 저장소 상대 경로나 고정 리비전 링크로 연결합니다.

참고: [Codex의 PR 설명 작성 기준](https://github.com/openai/codex/blob/5e96aabd68dc6194f5ad928cb7f5d0bc71b72df9/.codex/skills/codex-pr-body/SKILL.md)

## Markdown 외부 링크

자료 하나는 설명 가까이에 두고, 링크 이름에 확인할 내용을 씁니다.

```markdown
참고: [pnpm 패키지 선택](https://pnpm.io/filtering)

대상 패키지는 [pnpm 필터](https://pnpm.io/filtering)로 선택합니다.
```

문맥에 맞는 방식 하나를 고릅니다. 여러 자료는 참고 목록으로, 다른 주제는 소제목으로 묶습니다. 항목마다 `참고:`를 반복하지 않습니다.

```markdown
## 참고

### 실행 명령

- [pnpm 패키지 선택](https://pnpm.io/filtering)
- [Vitest 프로젝트별 실행](https://vitest.dev/guide/projects.html#running-tests)

### 문서 구성

- [GitHub README 안내](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
```

Markdown 자체를 코드 블록으로 보여줄 때는 바깥 울타리를 안쪽보다 길게 씁니다. 안쪽 백틱이 3개면 바깥은 4개 이상이며, 내부 코드가 블록 밖으로 나오지 않는지 확인합니다.

## 출처와 적용 범위

예제는 자체 작성했습니다. 표준 검토를 요청받으면 아래 출처에서 적용 범위와 요청한 판본을 확인합니다. 공개 개요만으로 조항별 적합성·인증·독자의 성공을 주장하지 않습니다.

- 쉬운 언어: [ISO 24495-1 공개 개요](https://www.iso.org/standard/78907.html), [국제 쉬운 언어 연맹 공개 해설](https://www.iplfederation.org/wp-content/uploads/2024/06/Plain-language-certification-for-organizations_A-Consultation-Paper-1-1.pdf). 유료 전문은 확인하지 않았습니다.
- 제품 사용 정보: [KS C IEC/IEEE 82079-1 공개 목록](https://www.kssn.net/search/stddetail.do?itemNo=K001010145434). 목록·범위만 참고하며 모든 README의 규칙으로 확대하지 않습니다.
- 영어 통제 언어: [ASD-STE100 소개](https://www.asd-ste100.org/about_STE.html)·[Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf). 요청 판본의 전체 규칙·사전과 [사용 조건](https://www.asd-ste100.org/STE_downloads.html)을 확인합니다. 한국어에 단어 수·사전 제한을 적용하거나 원문을 복제하지 않습니다.
