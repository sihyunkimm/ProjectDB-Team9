---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 6          # 격주 보고 회차 (1~8)
date: "2026-08-02"
status: "진행 중"            # 시작 전 / 진행 중 / 보류 / 완료
cl_level: "CL2"           # 쿼드 팀 CL 등급 (CL1 / CL2 / CL3 / CL4)
contributions:            # 팀원별 기여도 (합계 100%)
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "기존 분석 CVE Root Cause 정리, CVE 조사, CVE-2026-42306 분석"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "기존 CVE 취약 버전 및 패치 코드 비교 정리, CVE 조사, CVE-2026-42306 분석"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "기존 PoC 양식 통일 및 검증, CVE 조사, CVE-2026-42306 분석"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "기존 분석 CVE Root Cause 정리, CVE 조사, CVE-2026-42306 분석"
    percentage: 25
---

# [제 6차 프로젝트 진행 보고서] runc-clear

- **팀원:** (팀장) 20231726_박민영, (팀원) 20251788_김동후, 20245024_김진호, 20231754_한지선
- **활동 기간:** 2026. 07. 16. ~ 2026. 07. 29.

## 팀 전체 진행 현황

- **이번 회차 목표:** 지금까지 분석한 CVE 정리 및 보완, 다음으로 분석할 CVE 조사 및 선정, CVE-2026-42306 분석
- **현재 진행률:** 90%
- **주요 달성 사항:** 지금까지 분석한 CVE(CVE-2024-45310, CVE-2024-25621, CVE-2026-41567)에 대한 Root Cause를 정리하고, 취약한 버전의 코드가 어떻게 패치되었는지 통일된 양식으로 정리하였으며, PoC 양식을 통일하였음. 또한 CVE-2026-42306에 대한 분석과 PoC를 진행 중이며, 일부 성공 케이스를 확인함.

## 개인별 기여 내역

> 각 팀원이 이번 회차에 구체적으로 무엇을 했는지 작성합니다.
> 산출물 링크(GitHub 커밋 로그, PR 링크, 분석한 코드 주소 등)를 반드시 포함합니다.

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20231726_박민영 | Root Cause 정리 | 기존 분석 CVE의 Root Cause를 정리하고, CVE 분석 문서의 구조와 내용을 보완함. CVE-2026-42306 분석을 진행함. | https://app.notion.com/p/Root-Cause-3a544fff78a78054b69fc9600e4c7635?source=copy_link, https://app.notion.com/p/CVE-3a844fff78a78084b6d9d8c11f67f466?source=copy_link, https://app.notion.com/p/CVE-2026-42306-3ac44fff78a7802cb162cb6be21061ec?source=copy_link | 25% |
| 20251788_김동후 | 취약 버전 및 패치 코드 비교 정리 | 기존 CVE의 취약한 버전의 코드와 패치 이후 코드를 비교하여 정리함. CVE-2026-42306 분석을 진행함. | https://app.notion.com/p/CVE-39e44fff78a7809d9420fd721948885f?source=copy_link, https://app.notion.com/p/CVE-3a844fff78a7801092acd0df38ce73d1?source=copy_link, https://app.notion.com/p/CVE-2026-42306-3ab44fff78a7803390bccafe351480b8?source=copy_link | 25% |
| 20245024_김진호 | PoC 양식 통일, 검증 | 기존 CVE PoC 양식을 통일하고 검증하여 내용을 정리함. CVE-2026-42306 PoC를 진행하여 일부 성공 케이스를 확인함. | https://app.notion.com/p/PoC-3a344fff78a780cf976bd3b58ef1ecb6?source=copy_link, https://app.notion.com/p/CVE-3a844fff78a78040acf7db28add95e98?source=copy_link, https://app.notion.com/p/CVE-2026-42306-3ac44fff78a780e9b15ef3f2f7b4197e?source=copy_link | 25% |
| 20231754_한지선 | Root Cause 정리 | 기존 분석 CVE의 Root Cause를 정리함. CVE-2026-42306 분석을 진행함. | https://app.notion.com/p/Root-Cause-3a544fff78a78054b69fc9600e4c7635?source=copy_link, https://app.notion.com/p/CVE-3a844fff78a780c7a95ed22f086e1d10?source=copy_link, https://app.notion.com/p/CVE-2026-42306-3ac44fff78a7803fb993cd4efda0d45c?source=copy_link | 25% |

## 이슈 및 해결 방안

- **문제 상황:** CVE별 분석 문서의 작성 형식이 서로 달라 Root Cause 분석과 패치 코드 비교 내용을 일관된 형식으로 통합하고 정리할 필요가 있었음. 또한 PoC 코드에 따라 재현 결과가 달라지는 문제가 있어 검증 절차를 표준화하고 재현 가능한 형태로 정리해야 했음.
- **해결 현황:** 기존 CVE 분석 문서와 PoC의 양식을 통일하여 정리하였으며,PoC 실행 절차를 스크립트화하여 누구나 동일한 방식으로 검증 및 재현할 수 있도록 개선하였음. 부족한 내용은 피드백을 반영해 보완함으로써 일관성을 확보하였음.

## 다음 회차 목표

- CVE-2026-42306 심화 활동
- 활동 내용 정리, 보완 및 발표 준비

## 참고 자료

- https://nvd.nist.gov/vuln/detail/CVE-2026-42306
- https://github.com/moby/moby/security/advisories/GHSA-rg2x-37c3-w2rh
- https://www.sentinelone.com/vulnerability-database/cve-2026-42306/
- https://github.com/moby/moby/commit/43fa458a9c40873867e75221454de10709b04236
- https://github.com/advisories/GHSA-rg2x-37c3-w2rh
