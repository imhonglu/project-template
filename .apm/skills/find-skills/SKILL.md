---
name: find-skills
description: 사용자가 "X는 어떻게 하나요", "X를 위한 스킬을 찾아줘", "이런 일을 할 수 있는 스킬이 있나요"라고 묻거나 기능 확장에 관심을 보일 때 에이전트 스킬을 찾고 설치하도록 돕습니다. 설치 가능한 스킬로 제공될 수 있는 기능을 찾을 때 사용합니다.
---

# 스킬 찾기

이 스킬은 개방형 에이전트 스킬 생태계에서 스킬을 찾고 설치하도록 돕습니다.

## 이 스킬을 사용하는 상황

사용자가 다음과 같이 요청할 때 사용합니다.

- 기존 스킬이 있을 법한 일반적인 작업에 대해 "X는 어떻게 하나요"라고 묻습니다.
- "X를 위한 스킬을 찾아줘" 또는 "X를 위한 스킬이 있나요"라고 말합니다.
- 전문적인 기능이 필요한 작업에 대해 "X를 할 수 있나요"라고 묻습니다.
- 에이전트 기능 확장에 관심을 보입니다.
- 도구, 템플릿 또는 워크플로를 찾고 싶어 합니다.
- 디자인, 테스트, 배포 등 특정 분야에서 도움을 받고 싶다고 말합니다.

## Skills CLI란?

Skills CLI (`npx skills`)는 개방형 에이전트 스킬 생태계의 패키지 관리자입니다. 스킬은 전문 지식, 워크플로, 도구로 에이전트의 기능을 확장하는 모듈형 패키지입니다.

검색에는 Skills CLI를, 프로젝트 설치·갱신에는 APM을 사용합니다.

**주요 명령:**

- `npx skills find [query] [--owner <owner>]` - 대화형 또는 키워드로 스킬을 검색합니다. 필요하면 GitHub 소유자로 범위를 제한합니다.
- `mise exec -- apm install <package>` - GitHub 또는 다른 소스에서 스킬을 설치합니다.
- `mise exec -- apm update` - 프로젝트 APM 의존성을 선언된 ref 범위 안에서 갱신합니다.

**스킬 둘러보기:** https://skills.sh/

## 사용자의 스킬 검색을 돕는 방법

### 1단계: 필요한 것 파악하기

사용자가 도움을 요청하면 다음을 파악합니다.

1. 분야: React, 테스트, 디자인, 배포 등
2. 구체적인 작업: 테스트 작성, 애니메이션 제작, PR 검토 등
3. 기존 스킬이 있을 만큼 일반적인 작업인지 여부

### 2단계: 인기 목록부터 확인하기

CLI 검색 전에 [skills.sh 인기 목록](https://skills.sh/)에서 해당 분야의 알려진 스킬이 있는지 확인합니다. 이 목록은 총 설치 수를 기준으로 순위를 매겨 인기가 높고 실사용으로 검증된 스킬을 보여줍니다.

예를 들어 웹 개발 분야의 인기 스킬은 다음과 같습니다.

- `vercel-labs/agent-skills` — React, Next.js, 웹 디자인: 각각 설치 10만 회 이상
- `anthropics/skills` — 프런트엔드 디자인, 문서 처리: 설치 10만 회 이상

### 3단계: 스킬 검색하기

인기 목록에서 사용자 요구에 맞는 스킬을 찾지 못하면 검색 명령을 실행합니다.

```bash
npx skills find [query] [--owner <owner>]
```

예시:

- "React 앱을 더 빠르게 만들려면 어떻게 하나요?" → `npx skills find react performance`
- "PR 검토를 도와줄 수 있나요?" → `npx skills find pr review`
- "변경 이력을 작성해야 해요" → `npx skills find changelog`

### 4단계: 추천 전에 품질 확인하기

**검색 결과만으로 스킬을 추천하지 않습니다.** 다음을 반드시 확인합니다.

1. **설치 수** — 설치 1,000회 이상인 스킬을 우선합니다. 100회 미만이면 주의합니다.
2. **출처의 평판** — 공식 출처(`vercel-labs`, `anthropics`, `microsoft`)는 알려지지 않은 작성자보다 신뢰할 수 있습니다.
3. **GitHub 별 수** — 원본 저장소를 확인합니다. 별이 100개 미만인 저장소의 스킬은 비판적으로 검토합니다.

### 5단계: 사용자에게 후보 제시하기

관련 스킬을 찾으면 다음 정보를 제시합니다.

1. 스킬 이름과 기능
2. 설치 수와 출처
3. 사용자가 실행할 수 있는 설치 명령
4. 자세히 알아볼 수 있는 skills.sh 링크

응답 예시:

```
도움이 될 만한 스킬을 찾았습니다! "react-best-practices"는
Vercel Engineering의 React·Next.js 성능 최적화 지침을 제공합니다.
(설치 18만 5천 회)

설치 명령:
mise exec -- apm install vercel-labs/agent-skills --skill react-best-practices

자세히 보기: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 6단계: 설치 제안하기

사용자가 진행하기를 원하면 스킬을 대신 설치할 수 있습니다.

```bash
mise exec -- apm install <owner/repo> --skill <skill>
```

스킬은 현재 프로젝트에 설치합니다.

## 자주 쓰이는 스킬 분야

검색할 때 다음 분야를 참고합니다.

| 분야      | 검색어 예시                              |
| --------- | ---------------------------------------- |
| 웹 개발   | react, nextjs, typescript, css, tailwind |
| 테스트    | testing, jest, playwright, e2e           |
| DevOps    | deploy, docker, kubernetes, ci-cd        |
| 문서화    | docs, readme, changelog, api-docs        |
| 코드 품질 | review, lint, refactor, best-practices   |
| 디자인    | ui, ux, design-system, accessibility     |
| 생산성    | workflow, automation, git                |

## 효과적인 검색 방법

1. **구체적인 키워드 사용**: "testing"보다 "react testing"이 낫습니다.
2. **대체 용어 사용**: "deploy"로 찾지 못하면 "deployment"나 "ci-cd"를 시도합니다.
3. **인기 출처 확인**: 많은 스킬이 `vercel-labs/agent-skills`나 `ComposioHQ/awesome-claude-skills`에서 제공됩니다.

## 스킬을 찾지 못했을 때

관련 스킬이 없으면 다음과 같이 대응합니다.

1. 기존 스킬을 찾지 못했다고 알립니다.
2. 일반적인 기능으로 해당 작업을 직접 돕겠다고 제안합니다.
3. `.apm/skills`에서 `npx skills init <name>`으로 로컬 스킬을 만들 수 있다고 안내합니다. 인자에는 경로가 아닌 스킬 이름만 전달합니다.

예시:

```
"xyz" 관련 스킬을 검색했지만 일치하는 항목을 찾지 못했습니다.
대신 이 작업을 직접 도와드릴 수 있습니다. 진행할까요?

자주 하는 작업이라면 직접 스킬을 만들 수도 있습니다.
(cd .apm/skills && npx skills init my-xyz-skill)
```

생성된 `.apm/skills/my-xyz-skill/SKILL.md`를 작성한 뒤 저장소 루트에서 `pnpm fix` → `mise run setup` → `pnpm check` 순서로 정리·배포·검사합니다.
