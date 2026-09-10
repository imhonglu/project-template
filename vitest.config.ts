// 패키지별 테스트 설정을 모아 실행합니다. 루트는 리포터·커버리지 등 전역 옵션을 관리합니다.
// 프로젝트 실행 옵션은 자동으로 상속되지 않으므로 패키지별로 구성합니다.
//
// 참고: https://vitest.dev/guide/projects
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    projects: ["apps/*", "libs/*", "tools/*"],

    // 테스트 파일이 없는 경우를 허용합니다. 테스트를 추가하면 제거합니다.
    // projects에 해당하는 패키지가 없는 경우의 시작 오류는 허용하지 않습니다.
    // 참고: https://vitest.dev/config/passWithNoTests
    passWithNoTests: true,
  },
});
