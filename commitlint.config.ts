// Conventional Commits 형식을 공식 규칙으로 검사합니다.
//
// 참고: https://commitlint.js.org/reference/configuration.html
import type { UserConfig } from "@commitlint/types";

export default {
  extends: ["@commitlint/config-conventional"],

  // 한글 요약 안의 영문 고유명사·식별자 표기를 허용합니다.
  // 참고: https://commitlint.js.org/reference/rules.html#subject-case
  rules: {
    "subject-case": [0],
  },
} satisfies UserConfig;
