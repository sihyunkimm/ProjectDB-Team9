---
project_name: "Agent 취약점 분석 및 버그헌팅"
quad_name: "10조"
members: ["20221594_류석준", "20231816_정태영", "20245023_곽동윤", "20241919_김현민"]
report_number: 0
date: "2026-03-29"
status: "시작 전"
cl_level: "CL2"
field: "AI 보안"
contributions:
  - name: "20221594_류석준"
    role: "팀장"
    tasks: "Agent 취약점 분석 및 버그헌팅, 프로젝트 총괄 관리, 위협 모델링 설계"
    percentage: 30
  - name: "20231816_정태영"
    role: "팀원"
    tasks: "Agent 취약점 분석 및 버그헌팅, 오픈소스 Agent 정적 분석, 보안 패치 PR 작성"
    percentage: 25
  - name: "20245023_곽동윤"
    role: "팀원"
    tasks: "Agent 취약점 분석 및 버그헌팅, 테스트 환경 구축, 퍼저 개발 및 자동화"
    percentage: 25
  - name: "20241919_김현민"
    role: "팀원"
    tasks: "Agent 취약점 분석 및 버그헌팅, 선행 연구 조사, 보고서 문서화"
    percentage: 20
---

# 2026년 ASC 프로젝트 계획서

| 항목 | 내용 |
|------|------|
| **학교명** | 숭실대학교 |
| **동아리명** | ASC |
| **프로젝트명(주제)** | Agent 취약점 분석 및 버그헌팅 |
| **프로젝트 분야** | AI 보안 |

## 프로젝트 개요

> LLM(Large Language Model) 기반 AI Agent의 보안 취약점을 체계적으로 분석하고 실제 버그헌팅을 수행하는 프로젝트이다. 상용 서비스(ChatGPT, Claude 등)와 오픈소스 Agent 프레임워크(OpenClaw, ZeptoClaw 등)를 대상으로 Prompt Injection, Tool-Use Abuse, 권한 상승, 데이터 유출, MCP(Model Context Protocol) 악용 등 Agent 고유의 공격 표면을 분석한다. OWASP Top 10 for LLM Applications를 기반 분류 체계로 활용하며, 발견된 취약점은 PoC를 작성하여 책임 있는 공개(Responsible Disclosure) 또는 버그바운티 프로그램을 통해 제출하는 것을 최종 목표로 한다.

## 기대 효과

- LLM Agent 보안이라는 신규 분야에 대한 실전 취약점 분석 역량 확보
- 상용 서비스 버그바운티 제출 또는 오픈소스 프로젝트 CVE 발급을 통한 대외 실적 확보
- OWASP LLM Top 10 기반의 체계적 Agent 위협 모델링 방법론 내재화

---

# 프로젝트 세부 계획서

## 1. 프로젝트 목적 (추진배경, 취지 등)

- **AI Agent 보안 위협의 급증:** 2025년 이후 ChatGPT Plugins, Claude MCP, Microsoft Copilot 등 LLM 기반 Agent가 외부 도구(Tool)를 호출하고, 파일 시스템 접근, 코드 실행, API 호출 등을 자율적으로 수행하는 시대가 도래하였다. 이에 따라 전통적인 웹/시스템 취약점과는 본질적으로 다른 새로운 공격 표면이 대두되고 있다.
- **Agent 특유의 공격 표면:** 기존 LLM 보안 연구가 주로 Prompt Injection과 Jailbreak에 집중된 반면, Agent 환경에서는 (1) Tool Calling을 통한 임의 코드 실행, (2) Memory Poisoning을 통한 장기 지속 공격, (3) Multi-Agent 간 신뢰 체인 악용, (4) MCP 서버를 통한 공급망 공격, (5) Sandbox Escape를 통한 호스트 시스템 침투 등 복합적인 위협이 존재한다.
- **버그바운티 시장의 확대:** OpenAI, Anthropic, Google DeepMind 등 주요 AI 기업이 버그바운티 프로그램을 운영하고 있으며, AI 관련 취약점에 대한 보상 금액이 지속적으로 증가하고 있다. HackerOne, Bugcrowd 등 플랫폼에서도 AI/ML 카테고리가 신설되어 버그헌터에 대한 수요가 급증하고 있다.
- **오픈소스 Agent 프레임워크의 보안 미비:** OpenClaw, ZeptoClaw 등 GitHub 상의 오픈소스 Agent 프레임워크는 기능 개발에 집중되어 보안 검증이 부족한 상태이다. 임의의 MCP 서버 연결, 검증 없는 Tool 출력 신뢰, 부적절한 샌드박싱 등의 문제를 내포하고 있어 CVE 발급 가능성이 높다.
- **교육적 가치:** 본 프로젝트를 통해 팀원들은 LLM 내부 동작 원리, Agent 아키텍처 분석, 위협 모델링 방법론, PoC 작성 및 책임 있는 공개 절차, 버그바운티 리포트 작성법 등 AI 보안 실무 역량을 종합적으로 습득할 수 있다.

## 2. 프로젝트 세부내용

### Phase 1 — 기반 연구 및 환경 구축 (1~2회차, 4주)

- **OWASP Top 10 for LLM Applications 심층 분석**: 10개 항목 각각에 대해 Agent 환경에서의 적용 가능성과 공격 시나리오를 정리
- **Agent 아키텍처 분류 및 공격 표면 매핑**: 단일 Agent, Multi-Agent, ReAct 패턴, Plan-and-Execute 패턴 등 주요 아키텍처별 데이터 흐름도를 작성하고, 각 경로에서의 공격 가능 지점을 식별
- **타겟 조사**: GHSA나 버그바운티 프로그램을 운영하는 Agent 조사
- **로컬 테스트 환경 구축**: Docker 기반 격리 환경에서 오픈소스 Agent를 설치하고, 퍼징 및 수동 테스트를 위한 파이프라인을 구성

### Phase 2 — 오픈소스 Agent 취약점 분석 (3~5회차, 6주)

- **정적 분석(Static Analysis)**: 오픈소스 Agent 프레임워크의 소스 코드를 분석하여 위험 패턴 탐지
  - Tool 호출 시 입력값 검증 로직 부재 여부
  - Sandbox 구현의 우회 가능성 (subprocess 호출, 파일 시스템 접근)
  - 사용자 입력과 시스템 프롬프트 간 경계 처리 미흡
  - MCP 서버 응답에 대한 신뢰 검증 부재
- **동적 분석(Dynamic Analysis)**: 실제 Agent를 구동하며 악의적 입력을 통한 이상 동작 유발
  - Indirect Prompt Injection: 외부 데이터소스에 악성 지시문 삽입하여 Agent 동작 조작
  - Tool-Use Abuse: Agent가 호출 가능한 Tool의 파라미터를 조작하여 의도치 않은 동작 유도
  - Memory Poisoning: 대화 히스토리 또는 벡터 DB에 악성 컨텍스트 주입
  - Context Window Overflow: 대량의 토큰을 주입하여 시스템 프롬프트 밀어내기 공격
- **퍼징(Fuzzing)**: 자체 제작한 Agent 퍼저를 활용하여 비정상 입력에 대한 Agent 반응 자동화 테스트

### Phase 3 — 상용 서비스 버그헌팅 (5~7회차, 4주, Phase 2와 일부 병행)

- **ChatGPT (OpenAI) 대상 분석**: GPTs Action 호출 시 SSRF, 인증 토큰 유출 가능성 분석, Code Interpreter 샌드박스 우회 시도, Memory 기능을 활용한 Cross-Conversation 공격, 시스템 프롬프트 추출 기법 고도화
- **Claude (Anthropic) 대상 분석**: MCP Tool 연동 시 권한 경계 분석, Computer Use 기능 보안 경계 테스트, Artifacts 기능을 통한 XSS/데이터 유출 가능성 분석, Multi-modal 입력을 활용한 Indirect Prompt Injection
- **기타 Agent 서비스**: Microsoft Copilot, Google Gemini 등 접근 가능한 상용 Agent에 대해 동일 방법론 적용
- **버그바운티 리포트 작성**: 발견된 취약점에 대해 재현 단계, 영향도 분석, 수정 권고안을 포함한 전문적 리포트 작성

### Phase 4 — 종합 보고 및 성과 정리 (7~8회차, 2주)

- 발견된 모든 취약점에 대한 PoC 코드 정리 및 GitHub 레포지토리 공개 (안전한 범위 내)
- 취약점 분류 체계(Taxonomy)를 정리한 Agent Security Cheat Sheet 작성
- 버그바운티 제출 현황 및 결과 정리
- 오픈소스 프로젝트에 대한 보안 패치 PR 제출 현황 정리
- 최종 기술 보고서 작성 및 발표 준비

## 3. 프로젝트 기대효과

- **실전 취약점 발견 및 대외 실적 확보:** 오픈소스 프레임워크 대상 CVE 발급(목표 1건 이상) 또는 상용 서비스 버그바운티 보상 획득(목표 1건 이상)을 통해 팀원 개개인의 보안 실무 역량을 객관적으로 입증
- **AI Agent 위협 모델링 방법론 정립:** OWASP LLM Top 10을 Agent 환경에 맞게 확장한 자체 위협 모델링 프레임워크를 구축하여, 신규 Agent 서비스 출시 시 신속한 보안 평가 수행 기반 마련
- **보안 기여:** 취약점의 책임 있는 공개, 오픈소스 보안 패치 PR 제출, Agent Security Cheat Sheet 공개 등을 통해 AI 보안 생태계 전반에 기여
- **취업 및 진학 경쟁력 강화:** AI 보안은 글로벌 인재 수요가 공급을 크게 초과하는 분야로, 본 프로젝트 수행 경험은 보안 기업 취업, AI 보안 대학원 진학 등에 직접적으로 활용 가능
- **동아리 내 AI 보안 연구 기반 구축:** 분석 방법론, 테스트 환경, 문서화 결과물을 후배 기수에게 인수인계하여 ASC 동아리의 AI 보안 연구 역량을 지속적으로 축적

## 4. 프로젝트 수행시 문제점 (내외부 요인 기술)

- **상용 서비스 접근 제한:** ChatGPT, Claude 등 상용 서비스는 API 호출에 비용이 발생하며, Rate Limit 및 이용 약관에 의해 자동화된 대량 테스트가 제한될 수 있다. 버그바운티 프로그램의 범위(Scope)를 벗어난 테스트는 법적 문제를 야기할 수 있으므로 각 프로그램의 정책을 사전에 면밀히 검토해야 한다.
- **취약점의 재현 가능성:** LLM 기반 시스템은 본질적으로 비결정적(non-deterministic)이므로, 동일한 입력에 대해 매번 다른 출력이 나올 수 있다. 취약점 재현이 어려울 수 있으며, 버그바운티 리포트 작성 시 충분한 재현 빈도 데이터를 수집해야 한다.
- **빠른 기술 변화 속도:** LLM Agent 생태계는 주 단위로 새로운 프레임워크와 업데이트가 출시되고 있어, 분석 중인 대상의 코드가 급격히 변경될 수 있다. 특정 버전에 대한 분석 결과가 최신 버전에서는 유효하지 않을 가능성이 있다.
- **윤리적 경계 설정:** Agent를 통한 공격 시나리오 중 일부(예: 데이터 유출, 시스템 명령 실행)는 실제 사용자 데이터에 영향을 줄 수 있으므로, 반드시 로컬 환경 또는 허가된 테스트 환경에서만 수행해야 한다.
- **팀원 간 기술 수준 격차:** AI/ML 기초 지식과 보안 분석 경험이 팀원마다 다를 수 있으므로, 초기 2주간 집중 스터디를 통해 공통 기반 지식을 확보할 필요가 있다.

## 5. 프로젝트 수행시 요구사항 (프로젝트 구성원, 개발환경 등)

- **프로젝트 구성원:** 팀장 1명(프로젝트 총괄, 일정 조율, 버그바운티 제출 관리), 팀원 3명(각자 담당 Agent/프레임워크 취약점 분석 수행), 전원 CL2 수준의 보안 기초 역량 보유
- **개발 및 분석 환경:** Ubuntu 24.04 LTS (Docker 컨테이너 기반 격리 환경 병행), Python 3.11+, Docker & Docker Compose, Git & GitHub
- **API 접근:** OpenAI API 키 (GPT-4 계열 테스트용), Anthropic API 키 (Claude 계열 테스트용), 각 서비스의 버그바운티 프로그램 가입 및 정책 숙지
- **지식 요구사항:** LLM 기본 동작 원리, Agent 아키텍처 패턴 (ReAct, Plan-and-Execute, Multi-Agent), MCP 명세, OWASP Top 10 for LLM Applications, 버그바운티 리포트 작성 방법론
- **커뮤니케이션:** 주 1회 정기 미팅, GitHub Issues를 통한 취약점 후보 추적, Notion을 통한 분석 노트 공유

## 6. 프로젝트 수행시 활용되는 장비 및 물품

| 장비명/물품명 | 세부사양 |
|:---:|------|
| **H/W** | 개인 노트북 (최소 RAM 16GB, SSD 256GB 이상) x 4대 — 로컬 Agent 구동 및 분석 환경 |
| **S/W** | Python 3.11+, Docker Desktop, VS Code, Burp Suite Community Edition, mitmproxy, Wireshark, Git |
| **API 서비스** | OpenAI API (GPT-4o), Anthropic API (Claude Sonnet/Opus) |
| **기타(도서 등)** | OWASP LLM Top 10 공식 문서, Agent 보안 관련 논문 및 블로그, 오픈소스 Agent 프레임워크(OpenClaw, ZeptoClaw 등) |

## 팀원 역할 분담

| 팀원 | 역할 | 담당 업무 |
|------|------|----------|
| 20221594_류석준 | 팀장 | Agent 취약점 분석 및 버그헌팅, 프로젝트 총괄 관리, 버그바운티 제출 관리, 위협 모델링 설계 |
| 20231816_정태영 | 팀원 | Agent 취약점 분석 및 버그헌팅, 오픈소스 Agent 정적 분석, 보안 패치 PR 작성 |
| 20245023_곽동윤 | 팀원 | Agent 취약점 분석 및 버그헌팅, 테스트 환경 구축, 퍼저 개발 및 자동화 |
| 20241919_김현민 | 팀원 | Agent 취약점 분석 및 버그헌팅, 선행 연구 조사, 보고서 문서화 |

## 참고 자료

- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Anthropic Bug Bounty Program (HackerOne): https://hackerone.com/anthropic
- OpenAI Bug Bounty Program (Bugcrowd): https://bugcrowd.com/openai
- Model Context Protocol (MCP) Specification: https://modelcontextprotocol.io/
- Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023)
- Zhan et al., "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents" (2024)
- Johann Rehberger, "Prompt Injection and AI Agents" Blog Series
- NIST AI Risk Management Framework (AI RMF)
