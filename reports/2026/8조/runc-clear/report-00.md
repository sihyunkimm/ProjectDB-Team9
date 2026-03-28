---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 0               # 0회차: 프로젝트 계획서
date: "2026-03-29"
status: "시작 전"
cl_level: "CL2"
field: "시스템 보안"           # 예: 웹 보안, 시스템 보안, 네트워크 보안, 암호학, 포렌식 등
contributions:
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "계획서 작성(세부내용, 문제점, 요구사항) 및 제출"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "계획서 작성(개요, 기대효과, 전체 취합)"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "계획서 작성(목적, 기대효과)"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "계획서 작성(세부내용, 문제점, 요구사항)"
    percentage: 25
---

# 2026년 ASC 프로젝트 계획서

| 항목 | 내용 |
|------|------|
| **학교명** | 숭실대학교 |
| **동아리명** | ASC |
| **프로젝트명(주제)** | runc-clear |
| **프로젝트 분야** | 시스템 보안 |

## 프로젝트 개요

> 컨테이너 런타임인 runc의 구조와 실행 흐름을 분석하고, 공개된 취약점을 기반으로 Container Escape 공격을 재현한다. 취약점의 동작 원리를 심층적으로 이해하고 exploit code를 작성하여, 공격 가능성을 검증한다.

## 기대 효과

- 컨테이너 및 클라우드 환경 보안 위협 이해도 향상
- runc 내부 동작 구조에 대한 분석 능력 향상
- 실제 취약점 기반 exploit 코드와 PoC 코드 작성 경험
- 공격과 방어 관점 모두 고려한 보안 역량 강화

---

# 프로젝트 세부 계획서

## 1. 프로젝트 목적 (추진배경, 취지 등)

- runc는 가장 기본적인 경량 런타임이자 Docker 및 Kubernetes의 기본 런타임
- 클라우드 환경에서 Container Escape 취약점의 위험성 증가 
- runc 취약점 분석 및 공격 재현을 통해 컨테이너 보안 이해 상승

## 2. 프로젝트 세부내용

- **1. 학습 단계**
  - Linux Namespace, cgroups 등 컨테이너 핵심 기술 학습
  - 컨테이너의 동작 원리 및 구조 이해

- **2. 분석 단계**
  - runc 실행 흐름 및 내부 구조 분석
  - 컨테이너 생성 및 실행 과정에서 발생 가능한 취약 지점 식별
  - runc 관련 공개 CVE 조사 및 분석
    - CVE-2019-5736
    - CVE-2024-21626
    - CVE-2025-31133
    - CVE-2025-52565
    - CVE-2025-52881
  - 취약점 발생 원인, 공격 조건 및 공격 벡터 분석
  - 패치 전후 코드 비교

- **3. 실습 단계**
  - 취약점 재현을 위한 환경 구성 (Docker 및 runc 취약 버전 설정)
  - 선정한 CVE에 대한 취약점 재현

- **4. 공격 수행 단계**
  - 분석한 취약점을 기반으로 exploit 코드(PoC) 작성
  - 컨테이너 내부에서 호스트 시스템으로 탈출(Container Escape) 공격 수행
  - 공격 과정 및 동작 흐름 분석

- **5. 추가 검토 사항**
  - 방어자 관점에서 대응 방안 연구
  - syscall 및 파일 접근 기반 탐지 가능성 검토
  - seccomp, AppArmor/SELinux 등 보안 설정 적용 효과 확인


## 3. 프로젝트 기대효과

- 컨테이너 환경 취약점 발생 구조 이해
- runc 기반 Container Escape 공격 방식 이해
- 컨테이너 보안 대응 방법 이해
- 최종 산출물 : runc 취약점 분석 보고서, Container Escape PoC 및 exploit 코드, 탐지 및 대응 가이드라인


## 4. 프로젝트 수행시 문제점 (내외부 요인 기술)

- **1. 취약 환경 구성의 어려움**
  - 특정 Docker 및 runc 버전에서만 취약점 재현 가능
  - 최신 환경에서는 취약점이 패치되어 있어 별도의 환경 구성이 필요함
  - → Dockerfile 등으로 구버전 환경을 구성하여 재현성 확보 

- **2.커널 및 저수준 시스템 이해 부족**
  - Namespace, 파일 시스템, 권한 구조 등에 대한 이해 필요
  - → 취약점과 관련된 system call 중심으로 집중 분석

- **3. runc 코드 분석의 어려움**
  - Go 기반 코드 구조가 복잡하고 규모가 큼
  - → 패치 전후 코드(diff) 중심으로 분석 예정


## 5. 프로젝트 수행시 요구사항 (프로젝트 구성원, 개발환경 등)

- **기술적 요구사항**
  - Linux 운영체제 및 시스템 프로그래밍에 대한 기본 이해
  - Docker 및 컨테이너 기술에 대한 기본 지식
  - C / Go 언어 코드 분석 능력
  - 시스템 콜 및 프로세스 구조에 대한 이해

- **개발환경 요구사항**
  - Docker 및 runc 실행이 가능한 Linux 환경
  - VM 환경(VMare, VirtualBox 등)
  - 취약 버전 재현을 위한 패키지 버전 설정

## 6. 프로젝트 수행시 활용되는 장비 및 물품

| 장비명/물품명 | 세부사양 |
|:---:|------|
| **H/W** | 개인 노트북 (듀얼 코어 이상, RAM 4GB 이상, 가상화 환경 실행 가능 사양) |
| **S/W** | Oracle VM VirtualBox 또는 VMare Workstation, Docker, containerd, runc |
| **기타(도서 등)** | 컨테이너 보안(리즈 라이스), Hacking and Securing Docker Containers v2.0 (Udemy 강의) |

## 팀원 역할 분담

| 팀원 | 역할 | 담당 업무 |
|------|------|----------|
| 20231726_박민영 | 팀장 | 익스코드 작성 |
| 20251788_김동후 | 팀원 | 환경 구성 |
| 20245024_김진호 | 팀원 | 취약점 분석 |
| 20231754_한지선 | 팀원 | 대응 방안 마련 |

## 참고 자료

- https://github.com/madhuakula/kubernetes-goat #Kubernetes 보안 실습 환경
- https://osckorea.tistory.com/189 #컨테이너 런타임 관련 개념 자료
- https://m.blog.naver.com/skinfosec2000/221492955019 #runc Container Escape 취약점 (CVE-2019-5736)
- https://www.moonding.co.kr/docker-container-escape-vulnerability-cve-2024-21626/ #Docker Container Escape 취약점 (CVE-2024-21626)
- https://rninche01.tistory.com/entry/Docker-Container-EscapeCVE-2019-5736-runC%EC%B7%A8%EC%95%BD%EC%A0%90 #Docker Container Escape 취약점 (CVE-2019-5736)
- https://karatus.tistory.com/170#google_vignette #리눅스 커널 관련 책, 사이트, 블로그 정리
- https://olc.kr/course/course_online_view.jsp?id=35&s_keyword=Kernel #Kernel of Linux 강의