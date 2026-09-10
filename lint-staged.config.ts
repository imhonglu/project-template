// 스테이징된 파일에 린트 자동 수정·포맷·철자 검사를 순서대로 적용합니다.
// 파일 검색과 생성물 제외는 각 도구의 설정을 따릅니다.
//
// 참고: https://github.com/lint-staged/lint-staged#configuration
import { defineConfig } from "lint-staged/config";

export default defineConfig({
  // 문서·잠금 파일 등 도구별 검사 대상이 없는 경우에도 커밋을 허용합니다.
  // 참고: https://oxc.rs/docs/guide/usage/linter/cli
  // 참고: https://oxc.rs/docs/guide/usage/formatter/cli
  "*": [
    "oxlint --fix --no-error-on-unmatched-pattern",
    "oxfmt --no-error-on-unmatched-pattern",

    // 파일 경로를 glob으로 해석하지 않고, 제외된 파일만 있는 경우도 허용합니다.
    // 참고: https://github.com/streetsidesoftware/cspell/tree/main/packages/cspell
    "cspell --no-progress --no-must-find-files --file",
  ],
});
