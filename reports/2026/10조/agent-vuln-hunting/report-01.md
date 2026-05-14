---
project_name: "Agent 취약점 분석 및 버그헌팅"
quad_name: "10조"
members: ["20221594_류석준", "20231816_정태영", "20245023_곽동윤", "20241919_김현민"]
report_number: 1
date: "2026-04-26"
status: "진행 중"
cl_level: "CL2"
contributions:
  - name: "20221594_류석준"
    role: "팀장 / 위협 모델링"
    tasks: "분석 대상 오픈소스 Agent 프레임워크(OpenClaw) 선정 및 아키텍처·신뢰 경계 도식화, OpenClaw에 공개된 GitHub 보안 권고(GHSA) 469건 전수 분류, 상용 Agent 서비스 버그바운티 프로그램 스코프 비교, 다음 회차 분석 우선순위 선정, 공통 로컬 환경 가이드 작성, 팀 작업 규칙 정비"
    percentage: 28
  - name: "20231816_정태영"
    role: "정적 분석"
    tasks: "오픈소스 정적 분석 도구(Semgrep)로 OpenClaw 소스 스캔, 자동 분석 한계 보완을 위한 수동 코드 리뷰에서 권한 우회를 허용하는 위험 플래그 패턴(`dangerouslyAllow*`) 신규 식별, OpenClaw가 사용하는 외부 라이브러리의 미패치 보안 결함 5건 정리, AI Agent 보안 기초 개념·취약점 공개 절차·도구 호출 데이터 흐름 문서화"
    percentage: 24
  - name: "20245023_곽동윤"
    role: "환경 / 도구"
    tasks: "Windows 11 + Docker Desktop 환경에서 OpenClaw 구동 절차 검증 및 가이드 작성, 환경변수 차단 목록 우회를 자동 탐지할 자체 퍼저(env-denylist fuzzer) 프로토타입 설계 (구현은 다음 회차)"
    percentage: 24
  - name: "20241919_김현민"
    role: "선행 연구"
    tasks: "OWASP LLM Top 10, Indirect Prompt Injection 핵심 논문, Agent 보안 전문가 블로그 등 선행 문헌 서베이 및 1주차 위협 카탈로그 초안 작성"
    percentage: 24
---

# [제 1차 프로젝트 진행 보고서] Agent 취약점 분석 및 버그헌팅

- **팀원:** (팀장) 20221594_류석준, (팀원) 20231816_정태영, 20245023_곽동윤, 20241919_김현민
- **활동 기간:** 2026. 04. 13. ~ 2026. 04. 26. (2주)

## 회차 개요

본 프로젝트는 ChatGPT, Claude 등 LLM 기반 AI Agent에서 새롭게 부각되는 보안 위협(프롬프트 주입, 도구 남용, 권한 상승 등)을 체계적으로 분석하고, 발견한 취약점을 책임 있는 공개 또는 버그바운티 프로그램으로 제출하는 것을 목표로 한다. 전체 일정은 8회차(약 18주) **4단계(Phase)** 로 구성되며, 이번 1차 회차는 **Phase 1 — 기반 연구 및 환경 구축**의 1주차에 해당한다. 본 단계에서는 본격적인 취약점 사냥에 앞서 (1) 분석 대상 시스템을 확정하고, (2) 그 시스템의 구조와 위협 모델을 파악하며, (3) 모든 팀원이 동일한 환경에서 분석할 수 있도록 로컬 테스트 환경을 정비하는 것이 핵심이다.

## 팀 전체 진행 현황

- **이번 회차 목표:** ① OWASP LLM Top 10(LLM 애플리케이션의 대표 보안 위협 10가지)을 Agent 환경에 매핑하여 어떤 위협을 우선 다룰지 정한다. ② 1차 분석 대상이 될 오픈소스 Agent 프레임워크를 선정하고, 그 코드베이스의 아키텍처와 신뢰 경계를 정리한다. ③ 팀 전원이 동일한 코드 스냅샷을 기준으로 분석할 수 있도록 도커 기반 로컬 테스트 환경을 구축한다.
- **현재 진행률:** 약 12.5% (전체 8회차 중 1차 완료)
- **주요 달성 사항:**
  - **분석 대상 확정 — OpenClaw**: 1차 분석 대상으로 오픈소스 LLM Agent 프레임워크 **OpenClaw** (Node.js 24, MIT 라이선스)를 선정했다. OpenClaw는 외부 도구 실행·파일 시스템 접근·MCP(Model Context Protocol) 플러그인 연동을 지원하는 자율 Agent 프레임워크로, 보안 권고가 풍부하게 축적되어 있어 분석/학습 대상으로 적합하다. 분석 결과의 재현성을 위해 모든 분석은 동일한 기준 커밋(`81535d39`)을 기준으로 수행하기로 합의했다.
  - **아키텍처 및 위협 모델 매핑**: OpenClaw를 18개 핵심 컴포넌트로 분해하여 데이터 흐름도를 작성하고, 사용자 요청이 도구 실행으로 이어지기까지의 4단 신뢰 경계(`operator.read < pairing < write < admin`)를 도식화했다. 이 과정에서 도구 호출 디스패처, MCP 호환 플러그인 SDK, 도커 기반 샌드박스 등 향후 공격 표면이 될 핵심 경로를 식별했다.
  - **GitHub 보안 권고(GHSA) 469건 전수 분석**: GitHub Security Advisory Database에 공개된 OpenClaw 관련 보안 권고 **469건**(Critical 13 / High 151 / Medium 254 / Low 51)을 수집하고, 각 권고를 CWE(Common Weakness Enumeration: 보안 약점 분류 체계)와 OWASP LLM Top 10에 매핑했다. 그 결과 권한 부여 오류(CWE-863) 87건, OS 명령 주입(CWE-78) 33건, 경로 조작(CWE-22) 32건이 핵심 약점으로 드러났고, OWASP 분류로는 LLM06(Excessive Agency, Agent의 과도한 권한) 42.6%, LLM01(Prompt Injection) 25.6%로 집계되어 어떤 위협 카테고리에 분석 역량을 집중해야 할지 근거를 확보했다.
  - **상용 서비스 버그바운티 스코프 비교**: 이후 Phase 3에서 상용 Agent 서비스를 대상으로 버그헌팅을 수행할 것에 대비하여, Anthropic(HackerOne 운영)과 OpenAI(Bugcrowd 운영)의 버그바운티 프로그램에 대해 보고 가능한 범위(In-scope), 제외 항목(Out-of-scope), 보상 구간, 신고 절차를 비교 정리했다.
  - **로컬 테스트 환경 구축**: 분석 결과의 재현성을 보장하기 위해 도커 기반 OpenClaw 구동 절차를 6가지 경로로 정리한 공통 가이드와, Windows 11 + Docker Desktop 환경 별도 가이드를 함께 정비했다. 이로써 팀원의 호스트 OS와 무관하게 동일한 컨테이너 안에서 동일한 코드 스냅샷을 분석할 수 있다.
  - **정적 분석 착수와 신규 위험 패턴 발견**: 오픈소스 정적 분석 도구 **Semgrep**의 공개 룰셋 209개(자바스크립트·Node.js·시크릿·보안 감사·타입스크립트·명령 주입 카테고리)를 OpenClaw에 적용했다. 자동 분석 결과 5건의 경고는 모두 실제 위험이 아닌 false positive로 판정되었으나, 그 한계를 보완하기 위해 진행한 수동 코드 리뷰에서 **`dangerouslyAllow*` 접두어를 가진 위험 플래그가 코드베이스 전반에 광범위하게 사용되고 있는 패턴**을 신규로 식별했다. 이 플래그들은 권한 검사를 우회하는 경로를 단일 옵션 한 번으로 열어주는 구조여서, 다음 회차의 핵심 분석 시드로 확보했다.
  - **외부 라이브러리(의존성) 보안 결함 확인**: OpenClaw가 사용하는 HTTP 클라이언트 라이브러리 `undici@8.1.0`에서 미패치 상태의 보안 결함 5건(HTTP 요청 밀반입, 웹소켓 자원 고갈, CRLF 헤더 주입, 메모리·CPU DoS)이 남아 있음을 확인했다. 의존성 단위에서 이미 알려진 결함이 갱신되지 않은 상태이므로, 향후 공격 표면 평가의 기초 데이터로 활용한다.
  - **선행 연구 정리**: OWASP LLM Top 10, Greshake 등의 Indirect Prompt Injection 논문(2023), Johann Rehberger의 Agent 보안 블로그 시리즈를 서베이하여 1주차 위협 카탈로그 초안을 작성했다. 이를 통해 학술·업계의 최신 위협 분류와 본 프로젝트의 분석 방향을 정렬했다.
  - **다음 회차 분석 우선순위 선정**: 위 분석 결과를 종합해 OpenClaw 코드베이스 내부의 정밀 분석 후보 6개 모듈을 우선순위와 함께 선정하여 다음 회차 작업 계획을 구체화했다.

## 개인별 기여 내역

> 본 프로젝트의 작업 저장소(Agent-Zero)는 책임 있는 공개 정책상 **private GitHub 레포지토리**로 운영되므로, 산출물 칸에는 외부 URL 대신 레포 내부의 파일 경로와 PR 번호만 표기한다.

| 팀원 | 역할 | 수행 작업 | 산출물 | 기여도 |
|------|------|----------|--------|--------|
| 20221594_류석준 | 팀장 / 위협 모델링 | 분석 대상(OpenClaw) 선정 및 아키텍처·신뢰 경계 도식화, GHSA 469건 전수 분류와 CWE/OWASP LLM 매핑, Anthropic·OpenAI 버그바운티 스코프 비교, 다음 회차 우선 분석 모듈 6건 선정, 공통 로컬 환경 가이드 작성, 레포 운영 정책 정비 | `learning/week1/architecture/openclaw-architecture.md`, `learning/week1/ghsa-audit/openclaw-ghsa-audit.md` (+ 원천 데이터 `openclaw-ghsa.json`), `learning/week1/bug-bounty/bugbounty-scope-compare.md`, `learning/week1/targets/week2-target-candidates.md`, `learning/week1/setup-openclaw.md`, `CONTRIBUTING.md` / `SECURITY.md` / `docs/team.md` 정비 | 28% |
| 20231816_정태영 | 정적 분석 | Semgrep 공개 룰셋 209개로 OpenClaw 자동 스캔, 자동 분석 한계 보완을 위한 수동 코드 리뷰에서 위험 플래그 패턴(`dangerouslyAllow*`) 신규 식별, 외부 라이브러리 `undici@8.1.0`의 미패치 결함 5건 정리, AI Agent 보안 기초 개념·취약점 공개 절차·도구 호출 데이터 흐름 문서화 | `learning/week1/analysis/openclaw-static-analysis.md`, `learning/week1/dependency-cve/dependency-cve.md`, `learning/week1/basic/ai-agent-security.md`, `learning/week1/basic/ghsa.md`, `learning/week1/ghsa/ghsa-cve-process.md`, `learning/week1/tool-mcp/tool-mcp-dataflow.md` (PR #1) | 24% |
| 20245023_곽동윤 | 환경 / 도구 | Windows 11 + Docker Desktop 환경에서 OpenClaw 빌드·구동 절차 검증과 가이드 정리, 환경변수 차단 목록(denylist) 우회를 자동 탐지할 자체 퍼저 프로토타입 설계 (실제 구현은 다음 회차) | `learning/week1/setup-openclaw-windows-dongyoon47.md`, `learning/week1/tools/env-denylist-fuzzer-prototype.md` | 24% |
| 20241919_김현민 | 선행 연구 | OWASP LLM Top 10, GitHub Security Advisory 운영 절차, Greshake et al.(2023)의 Indirect Prompt Injection 논문, Johann Rehberger Agent 보안 블로그 시리즈 등 선행 문헌 서베이 및 1주차 위협 카탈로그 초안 작성 | `learning/week1/research/agent-security-literature-survey.md` | 24% |

## 이슈 및 해결 방안

**문제 1 — 범용 정적 분석 도구만으로는 Agent 특유의 위험을 잡아낼 수 없음.** OpenClaw 코드베이스에 Semgrep 공개 룰셋 209개를 적용한 결과 5건의 경고가 발생하였으나 검토 결과 모두 실제 위험이 아닌 false positive로 판정되었다. 즉 이미 알려진 일반적 취약 패턴을 찾는 룰만으로는 Agent 환경 특유의 위험(권한 우회, 도구 남용, 신뢰 경계 위반 등)을 포착할 수 없다는 한계가 드러났다. 이에 자동 분석에만 의존하지 않고 수동 코드 리뷰를 병행하기로 방향을 전환하였으며, 그 과정에서 권한 검사 경로를 한 줄로 우회시키는 `dangerouslyAllow*` 계열 플래그가 코드 전반에 광범위하게 사용되고 있는 신규 위험 패턴을 식별하여 다음 회차의 핵심 분석 시드로 확보하였다. 다음 회차에는 OWASP LLM Top 10에서 우선순위가 가장 높은 LLM06(Excessive Agency)·LLM07(Insecure Plugin Design)에 맞춘 자체 Semgrep 룰을 작성해, 자동 분석과 수동 분석을 함께 운영할 계획이다.

**문제 2 — GHSA 469건의 대규모 데이터를 어떻게 의미 있게 분류할 것인가.** OpenClaw에 공개된 GitHub 보안 권고가 469건에 이르러 단순히 목록만 나열해서는 반복 취약 모듈, 패치가 부족했던 부분, 동일 결함의 재공개 사례 같은 의미 있는 패턴이 보이지 않는 문제가 있었다. 이를 해결하기 위해 자료 구조를 사람이 쉽게 수정하기 어려운 단일 원천 데이터(JSON 파일) 와 사람이 읽기 위한 분석 노트(Markdown) 로 분리하고, 각 권고를 CWE(보안 약점 분류) 와 OWASP LLM Top 10이라는 두 축으로 동시에 매핑하는 표를 도입하였다. 그 결과 권한 부여 오류(CWE-863) 87건, OS 명령 주입(CWE-78) 33건과 같은 상위 약점 분포를 한눈에 파악할 수 있게 되었으며, 같은 패치가 같은 모듈에 반복적으로 들어간 "패치 핫스팟"을 자동으로 추출하는 스크립트 작성은 다음 회차로 이월하였다.

**문제 3 — 팀원 간 OS 환경 차이로 인한 분석 결과 재현성 저하.** 팀원들의 개인 개발 환경이 Linux와 Windows로 혼재되어 있어 OpenClaw 빌드·구동 절차와 의존성 해석 결과가 미세하게 달라지고, 이로 인해 한 사람이 발견한 동작을 다른 사람이 그대로 재현하기 어려운 문제가 발생하였다. 이를 해결하기 위해 Linux 사용자를 위한 공통 가이드(`setup-openclaw.md`)와 Windows 11 + Docker Desktop 사용자를 위한 별도 가이드(`setup-openclaw-windows-dongyoon47.md`)를 동시에 유지·관리하기로 합의하였고, 본격적인 분석은 모두 동일한 도커 컨테이너 안에서 동일한 기준 커밋(`81535d39`)을 대상으로 수행하도록 강제하여 호스트 OS에서 비롯되는 변수를 최소화하였다.

## 다음 회차 목표

- **GHSA 패치 패턴 카탈로그화 자동화**: 동일 결함의 재공개·인접 함수의 누락된 패치·차단 목록(denylist) 우회 사례 등을 분류한 카탈로그를 정리하고, 같은 모듈에 반복 패치가 집중된 "핫스팟"을 자동 추출하는 스크립트를 완성한다.
- **자체 퍼저(env-denylist fuzzer) 구현**: Phase 1에서 설계만 마친 환경변수 차단 목록 우회 탐지 퍼저를 Python으로 실제 구현하고, 시드 입력 50개를 기반으로 OpenClaw가 차단하지 못하는 변종이 있는지 검증한다.
- **정밀 분석 노트 5건 이상 작성**: `analysis/openclaw/` 디렉터리를 셋업하고, 1차 회차에서 패치가 가장 집중되었던 핵심 파일(`message-handler.ts`, `audit.ts`, `device-pairing.ts` 등)을 정독한 분석 노트를 5건 이상 산출한다.
- **`dangerouslyAllow*` 플래그 영향 분석**: 1차 회차에서 식별한 `dangerouslyAllow*` 패턴의 실제 사용처를 코드베이스 전수로 열거(enumerate)하고, 각 사용처가 신뢰 경계를 어떻게 침해하는지 분석한다.
- **Phase 2 동적 분석 진입 준비**: Indirect Prompt Injection(외부 데이터에 악성 지시문을 숨겨 Agent를 조작) 및 Tool-Use Abuse(도구 호출 매개변수 조작) 시나리오의 PoC 초안을 작성하여, 3차 회차부터 본격화될 동적 분석에 대비한다.

## 참고 자료

- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- GitHub Security Advisory Database (OpenClaw 관련 권고 469건)
- Anthropic Bug Bounty Program (HackerOne): https://hackerone.com/anthropic
- OpenAI Bug Bounty Program (Bugcrowd): https://bugcrowd.com/openai
- Model Context Protocol (MCP) Specification: https://modelcontextprotocol.io/
- Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023)
- Johann Rehberger, "Prompt Injection and AI Agents" 블로그 시리즈
