# Codex CLI 평가 기록 집계

[집계 스크립트](../scripts/summarize-evaluation.py)로 기존 CLI 실행의 JSON 이벤트와 결과 파일을 요약합니다. 집계 JSON을 표준 출력으로 냅니다. 모델 실행·네트워크 요청·파일 수정은 하지 않습니다.

manifest의 `runs[].path`는 manifest 위치 기준입니다. 각 실행 폴더에는 `events.jsonl`과 `result.json`이 있어야 합니다. `result.json`에는 `elapsed_seconds`·`exit_code`·`timeout`을 기록합니다. 식별자·비교 버전·과제는 manifest에 둡니다.

```json
{
  "rates_per_million": { "input": 10, "cached_input": 1, "output": 50 },
  "runs": [
    { "id": "before-case-1", "variant": "before", "case": "case-1", "path": "runs/before-case-1" },
    { "id": "after-case-1", "variant": "after", "case": "case-1", "path": "runs/after-case-1" }
  ]
}
```

예시 단가이며 현재 가격을 뜻하지 않습니다. 비용 비교에는 양쪽에 같은 명시적 단가를 적용합니다. 단가를 생략하거나 별도 캐시 쓰기 토큰의 단가가 없으면 비용은 `null`입니다.

스킬 디렉터리에서 실행합니다.

```sh
python3 scripts/summarize-evaluation.py /absolute/path/evaluation.json
```

`measurement_complete: true`이면 전체 사용량을 집계할 수 있습니다. 미완료 실행은 `observed_usage`와 종료 상태를 함께 보고합니다. 형식 오류는 종료 코드 1과 오류 메시지로 보고합니다. 선택·품질은 자동 채점하지 않습니다. 실행 환경이 같은지는 별도로 확인합니다.
