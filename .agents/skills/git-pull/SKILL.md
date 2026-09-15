---
name: git-pull
description: 현재 로컬 브랜치에 origin/main의 최신 변경을 merge 방식으로 반영하고 충돌을 해결합니다. main 변경 반영, merge 방식의 브랜치 갱신, 갱신 중 발생한 병합 충돌 해결 요청에 사용합니다.
---

<!-- cspell:words rerere zdiff -->

# Git 브랜치 갱신

기본 병합 대상은 `origin/main`이며, 사용자가 다른 대상을 지정하면 해당 대상을 사용합니다. 갱신에 필요한 병합 커밋까지 생성하며, 푸시·이력 재작성은 별도 요청이 있을 때 수행합니다.

## 사용 시점

- main 변경 반영: "현재 브랜치에 최신 main을 반영해줘"
- merge 방식 갱신: "rebase 없이 브랜치를 최신 상태로 맞춰줘"
- 충돌 해결: "main 병합 중 발생한 충돌을 해결해줘"

## 작업 절차

1. 현재 브랜치·원격·병합 대상과 진행 중인 Git 작업을 확인합니다. 미커밋 변경은 임의로 커밋하지 않고 필요 시 stash에 보관하며, 기존 스테이징 상태를 보존합니다.
2. rerere와 자동 스테이징을 저장소 로컬 설정으로 켭니다.

   ```sh
   git config --local rerere.enabled true
   git config --local rerere.autoupdate true
   ```

3. `git fetch origin`이 성공하면 원격 작업 브랜치를 먼저 동기화합니다.
   - 존재·추적 관계를 확인하고, 다른 원격도 필요하면 fetch합니다.
   - 원격 작업 브랜치가 없거나 기준 브랜치와 같으면 생략합니다.
   - 가능한 경우 fast-forward하고, 분기한 이력은 확인 후 merge합니다.
4. 원격 작업 브랜치 동기화를 완료한 뒤 기준 브랜치를 병합합니다. 각 merge는 아래 방식으로 커밋 전에 검증합니다.

   ```sh
   git -c merge.conflictStyle=zdiff3 merge --ff --no-commit origin/main
   ```

5. 충돌을 해결하고 각 병합을 검증·완료합니다.
   - rerere가 자동 스테이징한 결과도 `git diff --cached`로 검토합니다.
   - 미해결 충돌을 확인하고 `git diff --cached --check`로 스테이징한 충돌 표시를 검사합니다.
   - 저장소 검사를 실행해 이번 병합으로 생긴 실패를 해결하고, 메시지 규칙과 훅을 적용해 진행 중인 병합을 커밋합니다. fast-forward이면 추가 커밋은 만들지 않습니다.
6. 보관한 사용자 변경은 스테이징 상태와 함께 복원합니다. 복원 확인 전에는 stash를 유지하고, 완료 후 이번 작업에서 만든 항목만 제거합니다.

### 충돌 해결

- 공통 조상과 양쪽 변경 의도를 확인해 기능·API 계약을 보존하는 최소 변경으로 해결합니다. 한쪽 전체가 최종 의도와 맞을 때만 ours·theirs를 선택합니다.
- 잠금 파일·생성물은 원본 충돌을 먼저 해결한 뒤 해당 도구로 재생성합니다.

코드·테스트·변경 이력으로 판단할 수 있으면 진행합니다. 병합 대상이나 제품 동작·외부 계약·데이터 보존에 관한 선택을 확정할 수 없을 때만 질문합니다.

## 결과 확인

- 병합 대상의 반영과 사용자 변경·스테이징 상태의 복원을 확인합니다.
- 병합 결과·주요 충돌의 해결 근거·검증 결과·남은 작업을 보고합니다. 검사 실패는 이번 변경과 기존 문제를 구분합니다.

참고: [Git merge](https://git-scm.com/docs/git-merge)·[Git stash](https://git-scm.com/docs/git-stash)·[Git diff](https://git-scm.com/docs/git-diff).
