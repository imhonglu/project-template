---
name: apm
description: 작업에 맞는 에이전트 스킬과 MCP 서버를 탐색·비교·추천하고 APM으로 패키지와 MCP·LSP·플러그인 통합을 관리합니다. "이 작업을 도와주는 스킬이 있어?", "에이전트 기능을 확장하고 싶어", "스킬 설치·갱신", "MCP 검색·연결" 요청이나 apm.yml·로컬 SKILL.md의 작성·수정·배포에 사용합니다. 일반적인 구현 질문은 스킬·도구 탐색 의도가 있을 때 적용하며, npm 의존성 설치는 제외합니다.
---

# APM 통합 관리

스킬은 Skills CLI로, MCP 서버는 APM의 레지스트리 명령으로 검색합니다. 프로젝트 설치·배포는 APM으로 관리합니다. 아래 명령은 `apm.yml`과 `mise.toml`이 있는 프로젝트 루트에서 mise로 실행합니다.

## 사용 시점

- 스킬을 찾거나 비교할 때: "PR 검토에 쓸 스킬을 찾아줘", "이 두 스킬 중 어떤 게 맞아?"
- MCP 서버를 찾거나 비교할 때: "GitHub 이슈를 조회할 MCP가 있어?", "이 서비스의 공식 MCP 서버를 찾아줘"
- 검색 대상을 판단할 때: "이 작업에는 스킬과 MCP 중 무엇이 필요해?", "문서 작성을 도와주는 기능을 찾으려면 어디서 검색해?"
- 에이전트 기능을 확장할 때: "테스트 작업을 더 잘 지원하도록 구성하고 싶어", "반복 작업을 자동화할 스킬이 필요해"
- 외부 패키지를 관리할 때: "이 스킬을 설치해줘", "설치한 스킬을 갱신해줘", "사용하지 않는 패키지를 제거해줘"
- 로컬 절차를 스킬로 만들거나 수정할 때: "이 작업을 스킬로 분리해줘", "description과 사용 시점을 다듬어줘", "수정한 스킬을 배포해줘"
- 도구 통합을 구성할 때: "MCP를 Codex와 Claude에 연결해줘", "APM으로 LSP를 설정할 수 있어?", "배포 대상에 반영되지 않는 이유를 확인해줘"

일반적인 "이 기능을 구현해줘" 요청에서는 구현을 진행합니다. 사용자가 재사용할 기능·스킬을 찾거나 설치 환경을 구성하려는 맥락에서 적용합니다. 검색·설명 요청에는 후보와 안내를, 설치·변경 요청에는 실행 결과를 제공합니다.

## 검색 대상 선택

이미 설치된 스킬과 연결된 도구로 해결할 수 있는지 확인한 뒤, 필요한 기능에 따라 검색합니다.

| 필요한 기능                       | 검색 대상                   | 예시                                              |
| --------------------------------- | --------------------------- | ------------------------------------------------- |
| 작업 절차·작성 규칙·전문 지식     | 스킬 — Skills CLI·skills.sh | "PR 검토 기준을 적용할 스킬을 찾아줘"             |
| 외부 서비스·데이터·실행 도구 연결 | MCP — 공식 Registry·APM     | "GitHub PR을 읽고 댓글을 달 수 있는 MCP를 찾아줘" |
| 작업 절차와 외부 연결             | 스킬과 MCP 함께 검토        | "이슈를 조회하고 팀 규칙에 맞춰 분류하고 싶어"    |

스킬에 MCP 사용 절차가 포함될 수도 있으므로 필요한 연결 도구를 함께 확인합니다. 요청만으로 판단하기 어렵다면 작업 방식이 필요한지, 외부 데이터 접근이 필요한지 확인합니다.

## 작업별 안내

### 스킬 검색·추천

분야·구체적인 작업·사용 도구를 파악해 검색어로 바꿉니다. 이미 설치된 스킬로 해결할 수 있는지 확인하고, [skills.sh](https://skills.sh/)의 관련 후보와 Skills CLI 검색 결과를 살펴봅니다.

```sh
mise exec -- pnpx skills find react performance
mise exec -- pnpx skills find pull request review
mise exec -- pnpx skills find changelog
```

후보의 원본 `SKILL.md`와 필요한 참고 자료를 읽고 비교합니다.

- 요청한 작업을 실제로 지원하는지, 필요한 도구와 실행 환경이 맞는지 확인합니다.
- 출처와 유지보수 상태를 확인합니다. 설치 수와 별 수는 보조 정보로 사용합니다.
- 적용 범위가 겹치는 후보는 차이와 선택 이유를 설명합니다. 검색 결과의 요약만으로 추천하지 않습니다.
- 설치로 이어질 수 있도록 저장소·스킬 이름·원본 링크를 제공합니다.

```text
스킬: <name>
원본: <owner/repo> — <SKILL.md 링크>
적합한 이유: <요청과 연결되는 기능>
제약: <필요한 도구나 지원 범위>
```

적합한 후보가 없으면 구체적인 도구명·유사어·출처로 검색 범위를 조정합니다. 그래도 없으면 확인한 범위와 한계를 알리고 직접 작업하거나 반복할 절차를 로컬 스킬로 만드는 방안을 제시합니다.

### MCP 검색·추천

[공식 MCP Registry](https://registry.modelcontextprotocol.io/)와 서비스 제공자의 공식 MCP 문서를 먼저 확인합니다. Registry는 서버 메타데이터를 모으는 공식 목록이며, 등록 자체가 코드 품질이나 보안 심사를 보장하지는 않습니다.

```sh
mise exec -- apm mcp search github --limit 5
mise exec -- apm mcp show <server-name>
```

`<server-name>`은 검색 결과의 전체 식별자로 바꿉니다. 검색은 문자열 일치 방식이므로 서비스명·기능명으로 범위를 조정하고 상세 정보와 원본 문서를 확인합니다.

- 필요한 조회·수정 도구를 제공하는지, 읽기 전용 사용이 가능한지 확인합니다.
- 서비스 제공자의 공식 배포인지 커뮤니티 구현인지 구분하고 원본 저장소·서버 주소·유지보수 상태를 확인합니다.
- stdio·HTTP 방식, 실행 도구, 대상 클라이언트 지원, 인증·권한·비용 조건을 비교합니다.
- 등록 여부만으로 선택하지 않습니다. CLI 결과가 없거나 조회에 실패하면 공식 Registry와 제공자 문서로 교차 확인합니다. 사설 서버는 조직의 레지스트리·문서를 확인합니다.

```text
서버: <registry-name 또는 제공자·서버명>
원본: <공식 문서 또는 저장소 링크>
제공 기능: <요청에 필요한 도구>
연결 조건: <stdio·HTTP, 실행 환경, 인증·권한·비용>
```

적합한 후보가 없으면 확인한 범위와 한계를 설명합니다. 마켓플레이스는 추가 후보를 찾는 데 사용하고 실제 제공 기능·설치 방법은 원본에서 확인합니다.

참고: [공식 Registry의 역할](https://modelcontextprotocol.io/registry/about)·[APM MCP 명령](https://microsoft.github.io/apm/reference/cli/mcp/).

### 패키지 관리

`apm.yml`의 의존성·배포 대상과 `apm deps list` 결과를 확인해 요청한 범위에 적용합니다.

| 작업               | 명령                                                   |
| ------------------ | ------------------------------------------------------ |
| 설치된 의존성 확인 | `mise exec -- apm deps list`                           |
| 패키지 설치        | `mise exec -- apm install <owner/repo>`                |
| 특정 스킬 설치     | `mise exec -- apm install <owner/repo> --skill <name>` |
| 특정 패키지 갱신   | `mise exec -- apm update <package>`                    |
| 전체 의존성 갱신   | `mise exec -- apm update`                              |
| 패키지 제거        | `mise exec -- apm uninstall <package>`                 |

`<package>`는 의존성 목록의 식별자로 바꿉니다. 특정 패키지 요청에는 해당 대상만 적용하고, 전체 갱신 요청에는 전체 명령을 사용합니다. 갱신은 선언된 ref 범위를 따릅니다.

### 로컬 스킬 작성·배포

`includes: auto`를 사용하는 프로젝트에서 `.apm/skills/<name>/SKILL.md`를 원본으로 작성합니다. 이름은 소문자와 하이픈을 사용하고 폴더명과 맞춥니다.

```markdown
---
name: example-task
description: 수행할 작업을 설명하고, 사용할 요청 표현·작업 대상·관련 파일을 명시합니다.
---

# 작업 이름

## 작업 절차

필요한 절차와 명령 예시를 작성합니다.
```

`description`에는 스킬 선택에 필요한 단서를, 본문에는 적용 상황·작업 절차·예시를 둡니다. 관련 파일이 있다는 이유만으로 무관한 작업에 적용하지 않도록 범위를 정합니다.

배포본의 직접 수정 내용을 원본에 반영하고 관련 파일을 정리한 뒤 배포합니다. `apm.yml`을 직접 수정한 경우에도 같은 명령을 사용합니다.

```sh
mise exec -- apm install
```

### MCP 연결

서버 제공 방식에 맞는 명령 하나를 사용합니다. 각 명령은 `apm.yml`의 `dependencies.mcp`에 서버를 추가하고 대상별 설정을 배포합니다.

레지스트리

```sh
mise exec -- apm install --mcp <registry-name>
```

로컬 실행 (stdio)

```sh
mise exec -- apm install --mcp example -- node /absolute/path/server.js
```

원격 서버 (HTTP)

```sh
mise exec -- apm install --mcp example --transport http --url https://example.com/mcp
```

예시의 이름·경로·주소는 사용할 서버의 값으로 바꿉니다. 인증은 대상 도구가 지원하는 환경 변수 참조나 인증 절차로 구성하고, 비밀값을 문서·명령 예시에 넣지 않습니다.

Codex의 프로젝트 MCP 설정은 `.codex/`가 있어야 배포되므로 필요하면 디렉터리를 만듭니다. 설치 후 대상 도구에서 서버 연결 상태를 확인합니다.

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

- `apm.yml`의 선언과 `apm.lock.yaml`의 변경 범위를 확인합니다. 잠금 파일은 APM으로 갱신합니다.
- `targets`에 지정한 대상별 배포 결과와 생략된 이유를 확인합니다. 지원 기능과 설치 범위는 대상마다 다릅니다.
- 로컬 스킬은 `.agents/skills/`·`.claude/skills/`의 배포본과 원본을 비교합니다. Codex·Claude의 프로젝트 MCP 설정은 `.codex/config.toml`·`.mcp.json`에서 확인합니다.
- 이름 변경·제거 후 이전 생성물이 남았는지 확인합니다. 남은 파일은 사용자 수정 여부와 소유 관계를 확인한 뒤 정리합니다.

참고: [APM 설치](https://microsoft.github.io/apm/reference/cli/install/)·[갱신](https://microsoft.github.io/apm/reference/cli/update/).
