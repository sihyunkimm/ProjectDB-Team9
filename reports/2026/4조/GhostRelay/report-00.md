---
project_name: "GhostRelay"
quad_name: "4조"
members:
  - "20233051_박도현"
  - "20253311_강수빈"
  - "20261717_이정훈"
  - "20241947_장수연"
report_number: 0
date: "2026-03-29"
status: "진행 중"
cl_level: "CL1"
contributions:
  - name: "20233051_박도현"
    role: "리버스 엔지니어링 / 팀장"
    tasks: "분석 환경 세팅, binwalk 펌웨어 추출 시도"
    percentage: 25
  - name: "20253311_강수빈"
    role: "Web & AI 보안 엔지니어링"
    tasks: "분석 환경 구축 및 LLM 기반 취약점 탐지 파이프라인 설계"
    percentage: 25
  - name: "20261717_이정훈"
    role: "리버스 엔지니어링"
    tasks: "공유기 해킹 입문을 위한 정보 탐색 및 팀 주제 선정, 분석 환경 세팅 Follow up"
    percentage: 25
  - name: "20241947_장수연"
    role: "리버스 엔지니어링"
    tasks: "다른 벤더 제품에서 UPnP Relay Command Injection 취약점 분석, 취약점 케이스 및 패치 분석"
    percentage: 25
---

# GhostRelay — 프로젝트 계획서

## 프로젝트명

ipTIME N2V 취약점 분석 및 LLM 기반 자동 탐지 에이전트 개발

## 프로젝트 개요

EoS(단종) 제품인 ipTIME N2V 공유기에서 발견된 CVE-2025-55423 (UPnP Relay Command Injection) 취약점을 직접 재현하고, 벤더의 공식 패치가 존재하지 않는 해당 모델에 대해 패치 가능성 탐색을 1차 목표로 한다. 여기에 LLM을 활용하여 바이너리 역공학 결과물(C 코드)에서 취약점 패턴을 자동으로 식별하는 지능형 보안 분석 에이전트를 직접 설계 및 구현한다. 이를 통해 수동 분석과 AI 자동 분석의 정확도를 비교 검증하며, AI를 활용한 보안 감사(Security Auditing) 프로세스의 효율성을 극대화한다.

## 이번 회차 진행 사항

### 완료한 작업

- 프로젝트 주제 선정 및 타깃 기기(ipTIME N2V, 펌웨어 12.16.8) 확정

### 진행 중인 작업

- 분석 환경 세팅 (Ubuntu VM 및 Python AI 개발 환경)
- binwalk 설치 및 펌웨어 추출 시도
- 패치 비교 대상 펌웨어(A604M 최신버전) 다운로드

### 이슈 및 블로커

- 특이사항 없음 (초기 세팅 단계)
- 데이터 컨텍스트 제한: 전체 소스 코드가 아닌 함수 단위로 AI가 분석할 수 있도록 코드를 파싱하고 전처리하는 로직 설계 필요

## 팀원별 기여 상세

| 팀원 | 역할 | 수행 작업 | 기여도 |
|------|------|-----------|--------|
| 20233051_박도현 | 리버스 엔지니어링 / 팀장 | 분석 환경 세팅, binwalk 추출 시도 | 25% |
| 20253311_강수빈 | Web & AI 보안 엔지니어링 | 분석 환경 구축 및 LLM 기반 취약점 탐지 파이프라인 설계 | 25% |
| 20261717_이정훈 | 리버스 엔지니어링 | 공유기 해킹 입문을 위한 정보 탐색 및 팀 주제 선정, 분석 환경 세팅 Follow up | 25% |
| 20241947_장수연 | 리버스 엔지니어링 | 다른 벤더 제품에서 UPnP Relay Command Injection 취약점 분석, 취약점 케이스 및 패치 분석 | 25% |

## 다음 회차 계획

- binwalk로 N2V 펌웨어 파일시스템 추출 완료 및 libcgi.so 위치 확인
- A604M 펌웨어에서 패치된 libcgi.so 추출 후 비교 준비
- [AI] 추출된 C 코드를 LLM에 전달하여 위험 함수(system, popen 등)와 사용자 입력값 사이의 흐름(Taint Analysis) 자동 추적 테스트

## 참고 자료

- [CVE-2025-55423 NVD 페이지](https://nvd.nist.gov/vuln/detail/CVE-2025-55423)
- [ipTIME N2V 공식 펌웨어 다운로드 페이지](https://iptime.com/iptime/?page_id=126)
- [binwalk GitHub](https://github.com/ReFirmLabs/binwalk)
