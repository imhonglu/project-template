# MCP·LSP·플러그인 연결

MCP 서버 추가·연결 요청에 사용합니다. 아래는 mise를 사용하는 프로젝트 루트 기준입니다.
다음 명령은 `apm.yml`의 `dependencies.mcp`에 서버를 추가하고 대상별 설정을 배포합니다.
Codex의 프로젝트 설정에는 `.codex/` 디렉터리가 필요합니다.

예제의 이름·경로·주소는 서버에 맞춥니다. 인증은 환경 변수 참조나 도구의 인증 절차로 처리하고 비밀값은 기록하지 않습니다.

## 레지스트리

```sh
mise exec -- apm install --mcp "<registry-name>"
```

## 로컬 실행 (stdio)

```sh
mise exec -- apm install --mcp example -- node /absolute/path/server.js
```

## 원격 서버 (HTTP)

```sh
mise exec -- apm install --mcp example --transport http --url https://example.com/mcp
```

참고: [MCP 서버 설치](https://microsoft.github.io/apm/consumer/install-mcp-servers/)

## 기타 통합

요청한 기능의 지원 대상과 설정 방식은 해당 문서에서 확인합니다.

- [LSP 서버 설치·대상별 지원](https://microsoft.github.io/apm/consumer/install-lsp-servers/)
- [Copilot Agent Plugins 설치](https://microsoft.github.io/apm/consumer/copilot-agent-plugins/)
