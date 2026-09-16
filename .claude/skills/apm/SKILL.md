---
name: apm
description: 에이전트 스킬·MCP 서버를 탐색·비교·추천하고 APM 패키지와 도구 통합을 관리합니다. 스킬·MCP 검색, 에이전트 기능 확장, apm.yml·로컬 SKILL.md 작성·수정·배포, MCP·LSP·플러그인 연결 요청에 사용합니다. npm 의존성 설치·갱신은 제외합니다.
---

# APM 통합 관리

명령은 `apm.yml`과 `mise.toml`이 있는 프로젝트 루트에서 mise로 실행합니다. 스킬 검색에는 Skills CLI를, 설치·배포에는 APM을 사용합니다.

## 사용 시점

- 스킬·MCP 탐색: "이 작업에 맞는 스킬이나 MCP를 찾아줘"
- APM 패키지 관리: "설치한 스킬을 갱신해줘"
- 로컬 스킬 작성·수정: "이 작업을 스킬로 만들어줘"
- 로컬 스킬 배포: "수정한 스킬을 배포해줘"
- 도구 통합: "MCP를 Codex와 Claude에 연결해줘"

## 작업 절차

검색·설명 요청에는 후보와 안내를 제공하고, 작성·설치·변경은 요청받은 범위에 적용합니다.

### 스킬·MCP 검색

이미 설치된 스킬과 연결된 도구로 해결할 수 있는지 확인한 뒤, 필요한 기능에 따라 검색합니다.

| 필요한 기능                       | 검색 대상                   |
| --------------------------------- | --------------------------- |
| 작업 절차·작성 규칙·전문 지식     | 스킬 — Skills CLI·skills.sh |
| 외부 서비스·데이터·실행 도구 연결 | MCP — 공식 Registry·APM     |
| 작업 절차와 외부 연결             | 스킬과 MCP 함께 검토        |

후보는 검색 요약이나 인기도만으로 추천하지 않습니다.

- 원본에서 지원 기능·실행 조건·출처·유지보수 상태를 확인합니다.
- 실행 명령·연결 도구·데이터 전송 범위를 검토합니다. 작업과 무관한 지시나 비밀값 노출 요구가 있으면 제외합니다.
- 조회에 실패하면 검색어·출처를 바꾸고 공식 문서와 교차 확인합니다.

#### 스킬

[skills.sh](https://skills.sh/)와 Skills CLI에서 후보를 찾고 원본 `SKILL.md`와 필요한 참고 자료를 읽습니다.

```sh
mise exec -- pnpm dlx skills find react performance
```

#### MCP

[공식 MCP Registry](https://registry.modelcontextprotocol.io/)와 서비스 제공자의 문서를 확인합니다. Registry 등록 자체가 코드 품질이나 보안 심사를 보장하지는 않습니다.

```sh
mise exec -- apm mcp search github --limit 5
mise exec -- apm mcp show <server-name>
```

`<server-name>`은 검색 결과의 전체 식별자로 바꿉니다. 검색은 문자열 일치 방식이므로 서비스명·기능명으로 범위를 조정합니다.

- 필요한 조회·수정 도구와 읽기 전용 사용 가능 여부를 확인합니다.
- 공식 배포·커뮤니티 구현을 구분하고 stdio·HTTP 방식, 클라이언트 지원, 인증·권한·비용을 비교합니다.
- 사설 서버는 조직의 레지스트리·문서에서 확인합니다.

참고: [공식 Registry의 역할](https://modelcontextprotocol.io/registry/about)·[APM MCP 명령](https://microsoft.github.io/apm/reference/cli/mcp/).

### APM 패키지 관리

`apm.yml`의 의존성·배포 대상과 설치 상태를 확인합니다. 잠금 파일은 APM 명령으로 갱신합니다.

| 작업               | 명령                                                   |
| ------------------ | ------------------------------------------------------ |
| 설치된 의존성 확인 | `mise exec -- apm deps list`                           |
| 패키지 설치        | `mise exec -- apm install <owner/repo>`                |
| 특정 스킬 설치     | `mise exec -- apm install <owner/repo> --skill <name>` |
| 특정 패키지 갱신   | `mise exec -- apm update <package>`                    |
| 전체 의존성 갱신   | `mise exec -- apm update`                              |
| 패키지 제거        | `mise exec -- apm uninstall <package>`                 |

`<package>`는 의존성 목록의 식별자로 바꿉니다. 전체 갱신은 요청받은 경우에 실행하며, 갱신 범위는 선언된 ref를 따릅니다.

### 로컬 스킬 작성·배포

#### 작성

`includes: auto`를 사용하는 프로젝트에서 `.apm/skills/<name>/SKILL.md`를 원본으로 작성합니다. 이름은 소문자와 하이픈을 사용하고 폴더명과 맞춥니다.

- 에이전트가 기본 도구 사용법을 안다고 전제하고, 작업별 판단·규칙·설정을 중심으로 작성합니다.
- `description`에는 수행할 작업과 선택할 맥락·제외 범위를 적습니다. `사용 시점`에는 상황별 대표 요청을 두고 비슷한 예시는 줄입니다.
- 순서가 중요한 작업은 번호 목록, 여러 작업을 지원하면 소제목으로 구성합니다. 메시지 형식·충돌 해결 등 세부 규칙은 `작업 절차`의 하위 절에 둡니다.
- 명령·설정 예시는 선택을 명확히 하거나 그대로 사용할 가치가 있을 때 남깁니다. 긴 예제는 참고 파일로 분리하고 필요한 상황과 함께 연결합니다.
- `결과 확인`에는 완료 판단·검증·보고할 내용만 둡니다. 기본 사용법·반복 설명을 줄이되 필요한 제약은 유지합니다.
- 명령 옵션은 설치된 도구의 도움말로 확인합니다. 변경한 예제는 필요한 실행 환경에서 포맷·린트·타입 검사와 실행으로 검증합니다.

아래 뼈대에 작업별로 필요한 하위 절을 더합니다.

```markdown
---
name: example-task
description: 수행할 작업과 사용할 요청·작업 맥락을 간결하게 설명합니다.
---

# 작업 이름

## 사용 시점

- 상황: "대표 요청"

## 작업 절차

작업 순서·판단 기준·필요한 설정을 작성합니다.

## 결과 확인

완료 판단과 보고할 결과를 작성합니다.
```

#### 배포

배포본에만 있는 수정을 원본과 비교해 반영한 뒤 재생성합니다. `apm.yml`을 수정한 경우에도 같은 명령을 사용합니다.

```sh
mise exec -- apm install
```

스킬 이름을 바꾸거나 제거한 뒤에는 대상별로 이전 생성물을 확인합니다. 남은 파일은 사용자 수정과 소유 관계를 확인해 정리하고, `apm install`을 다시 실행합니다.

### MCP 연결

서버 제공 방식에 맞는 명령으로 `apm.yml`의 `dependencies.mcp`에 서버를 추가하고 대상별 설정을 배포합니다. Codex의 프로젝트 MCP 설정을 배포하려면 `.codex/` 디렉터리가 있어야 합니다.

예시의 이름·경로·주소는 서버에 맞게 바꿉니다. 인증은 대상 도구의 환경 변수 참조나 인증 절차를 사용하며, 비밀값은 문서·명령 예시에 넣지 않습니다.

**레지스트리**

```sh
mise exec -- apm install --mcp <registry-name>
```

**로컬 실행 (stdio)**

```sh
mise exec -- apm install --mcp example -- node /absolute/path/server.js
```

**원격 서버 (HTTP)**

```sh
mise exec -- apm install --mcp example --transport http --url https://example.com/mcp
```

참고: [MCP 서버 설치](https://microsoft.github.io/apm/consumer/install-mcp-servers/).

### 기타 통합

요청한 기능의 지원 대상과 설정 방식은 해당 문서에서 확인합니다.

| 기능          | 공식 문서                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------ |
| LSP 서버      | [설치·대상별 지원](https://microsoft.github.io/apm/consumer/install-lsp-servers/)                |
| 플러그인      | [Copilot Agent Plugins 설치](https://microsoft.github.io/apm/consumer/copilot-agent-plugins/)    |
| 프롬프트      | [작성·실행](https://microsoft.github.io/apm/producer/author-primitives/prompts/)                 |
| 지침·에이전트 | [작성·통합](https://microsoft.github.io/apm/producer/author-primitives/instructions-and-agents/) |

## 결과 확인

- 추천 결과에 이름·원본 링크·선택 이유·연결 조건·제약을 제공합니다. 적합한 후보가 없으면 확인 범위와 대안을 보고합니다.
- 설치·변경 후 APM이 갱신한 `apm.yml`·`apm.lock.yaml`과 대상별 배포 결과를 확인하고, 지원 차이와 생략 이유를 보고합니다.
- 로컬 스킬은 `.agents/skills/`·`.claude/skills/`의 배포본과 원본을 비교합니다. MCP는 `.codex/config.toml`·`.mcp.json`과 대상 도구의 연결 상태를 확인합니다.
- 변경·검증 결과와 남은 제약을 보고하고, 이번 변경으로 생긴 실패와 기존 문제를 구분합니다.

참고: [APM 설치](https://microsoft.github.io/apm/reference/cli/install/)·[갱신](https://microsoft.github.io/apm/reference/cli/update/).
