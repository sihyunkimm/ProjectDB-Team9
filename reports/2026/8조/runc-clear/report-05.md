---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 5          # 격주 보고 회차 (1~8)
date: "2026-07-17"
status: "진행 중"            # 시작 전 / 진행 중 / 보류 / 완료
cl_level: "CL2"           # 쿼드 팀 CL 등급 (CL1 / CL2 / CL3 / CL4)
contributions:            # 팀원별 기여도 (합계 100%)
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "CVE-2026-41567 관련 내용 조사 및 코드 분석(archive_unix.go), 취약 메커니즘 요약, PoC 검증 시나리오 기획 및 재현"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "취약점 개요 및 RCE/Escape 원리 분석, 보안상 의미 도출, C 기반 가짜 xz 바이너리를 활용한 기본 PoC 시나리오 및 랩 환경 구조 설계"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "Docker Engine/Moby 권한 경계 붕괴 취약점 상세 원인(RunInFS 전환) 분석, curl API 기반 익스플로잇 설계 및 DinD 격리 환경에서의 PoC 재현"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "공격 성립 조건 및 위험도 평가, WSL2 Ubuntu 환경 기반 취약/패치 버전 교차 테스트, hostname 및 namespace 조회 기반 가짜 xz 백도어 스크립트 작성"
    percentage: 25
---

# [제 5차 프로젝트 진행 보고서] runc-clear

- **팀원:** (팀장) 20231726_박민영, (팀원) 20251788_김동후, 20245024_김진호, 20231754_한지선
- **활동 기간:** 2026. 07. 04. ~ 2026. 07. 15.

## 팀 전체 진행 현황

- **이번 회차 목표:** CVE-2026-41567 취약점 원리 파악, root cause 및 소스코드 분석, PoC 환경 구축 및 패치 전후 동작 비교 검증
- **현재 진행률:** 80%
- **주요 달성 사항:**
  - Docker Engine 및 Moby 프레임워크의 권한 경계 붕괴 취약점(`CVE-2026-41567`, `CWE-427 Uncontrolled Search Path Element`)을 심층 분석함.
  - `daemon/archive_unix.go` 분석을 통해, 컨테이너 파일시스템으로 root 전환(`RunInFS`) 후 압축 해제 바이너리(`xz`, `unpigz`)를 탐색하여 호스트 루트 권한으로 실행하게 되는 root cause와 이를 `UntarUncompressed` 방식으로 조치한 패치 로직을 파악함.
  - PoC 재현 (박민영): WSL2 Ubuntu 24.04 환경에서 `Docker Engine 29.5.0`(취약) 버전과 `29.5.1`(패치) 버전을 설치하고, API(`PUT /containers/{id}/archive`)를 통한 압축 아카이브 업로드 테스트를 진행함. 실행 결과와 로그를 통해 취약 버전에서 dockerd가 컨테이너 내부 바이너리인 fake xz와 unpigz를 직접 실행하였음을 확인함.
  - PoC 재현 (김진호): Colima + containerd 위에서 `docker:28.5.2-dind`를 실행해 실제 호스트 데몬 훼손 없이 안전하게 취약 환경을 구성함. 이후 `curl`을 이용해 API(`PUT /containers/{id}/archive`)에 페이로드를 전달하여 가짜 `xz` 실행 및 호스트 root 권한 획득 여부를 성공적으로 확인.
  - PoC 재현 (한지선): WSL2 Ubuntu 전용 배포판에 Docker 공식 apt 저장소를 연결하여 `29.5.0`(취약) 버전과 `29.5.1`(패치) 버전을 교차 설치함. `docker cp -` 파이프라인을 통한 아카이브 주입 테스트 결과, 패치 버전에서는 악성 바이너리가 호출되지 않음을 로그 및 결과 파일을 통해 증명함.


## 개인별 기여 내역

| 팀원 | 역할 | 수행 작업 | 산출물 링크/근거 자료 | 기여도 |
|------|------|----------|----------------------|--------|
| 20231726_박민영 | 팀장 | CVE-2026-41567의 핵심 개요 정리. Docker/Moby daemon이 archive를 처리할 때 컨테이너 내부를 `RunInFS`로 진입하여 압축 해제를 시도하는 과정의 소스코드(`archive_unix.go`) 취약 흐름을 문서화. PoC 전 과정 스크립트 작성 및 결과 로그 분석. | https://app.notion.com/p/CVE-2026-41567-39744fff78a780a3948edb58d92927eb?source=copy_link, https://app.notion.com/p/CVE-2026-41567-PoC-39d44fff78a780b6a2c0f1e1a12f9803?source=copy_link | 25% |
| 20251788_김동후 | 팀원 | 취약점의 보안상 의미(Container-to-Host 격리 붕괴 및 완전한 호스트 탈취)와 영향 범위를 분석. 가짜 `xz` C 소스코드를 컴파일하여 `/tmp` 경로에 권한 확인 마커를 생성하는 구조의 랩 환경(디렉터리 트리) 및 기본 PoC 시나리오 수립. | https://app.notion.com/p/CVE-2026-41567-39744fff78a780048076c570c6651caa?source=copy_link, https://app.notion.com/p/CVE-2026-41567-PoC-39e44fff78a78063a08fc5aa10cd8a4b?source=copy_link | 25% |
| 20245024_김진호 | 팀원 | 압축 바이너리 탐색 취약점에 대한 Go 로직 단위 분석. 호스트 데몬 보호를 위해 `DinD(Docker-in-Docker)` 환경으로 격리. `curl`을 활용한 xz-compressed tar API 업로드 스크립트 작성 및 HTTP 200 응답과 함께 생성된 `wrapper_generated.txt` 로그 검증 수행. | https://app.notion.com/p/CVE-2026-41567-39744fff78a7807ca143cbb76b57a846?source=copy_link, https://app.notion.com/p/CVE-2026-41567-PoC-39e44fff78a780b8bc0cc6cfc457fb76?source=copy_link | 25% |
| 20231754_한지선 | 팀원 | 취약 버전 지정 설치를 위한 환경(Ubuntu, docker-ce apt 저장소) 스크립트(`setup.sh`) 개발. `fake-xz` 스크립트를 고도화하여 네임스페이스(`pid_ns`, `mnt_ns`)와 `hostname`을 로깅하도록 작성, 컨테이너 컨텍스트 밖에서 실행됨을 교차 검증함. | https://app.notion.com/p/CVE-2026-41567-39744fff78a7800baf80d989fdfd4a8b?source=copy_link, https://app.notion.com/p/CVE-2026-41567-PoC-39e44fff78a7804094aac5f70619ff3e?source=copy_link | 25% |

## 이슈 및 해결 방안

- **이슈 1: Ubuntu 기본 저장소 환경에서의 패키지 버전 지정 설치 불가**
  - **문제 상황:** 처음에 시도한 Ubuntu 기본 저장소 환경에서는 Docker Engine 최신 버전대의 특정 patch 패키지를 골라 설치하기 어려워 29.5.0(취약) 및 29.5.1(패치) 버전 간의 정밀한 비교 테스트 진행이 불가능했음.
  - **해결 방안:** 실습용 컨테이너와 호스트 OS를 분리하기 위해 전용 WSL2 배포판을 새로 생성하고, Docker 공식 저장소(`download.docker.com`)를 수동으로 등록하여 원하는 특정 버전(`5:29.5.0-1~ubuntu.*`)을 정확하게 지정 설치함.

- **이슈 2: 컨테이너 내부 root와 호스트 root의 권한 구별 모호성**
  - **문제 상황:** 가짜 압축 해제 바이너리(`fake-xz`) 실행 시 `id -u`를 로깅했을 때 단순 `uid=0`으로 출력되었으나, Docker의 특성상 컨테이너 내부 root도 `uid=0`이므로 해당 바이너리가 호스트 컨텍스트에서 실행되었다고 확증하기 어려웠음.
  - **해결 방안:** 백도어 스크립트를 보강하여 단순히 uid/gid만 남기지 않고 `hostname`과 `/proc/self/ns/*` 정보를 추가로 기록하도록 수정. `docker exec`로 들어간 정상 쉘의 hostname(컨테이너 ID)과 가짜 바이너리가 찍은 hostname(호스트 데스크톱 이름)이 완전히 다름을 대조해 격리 탈출을 입증함.

- **이슈 3: `curl`을 이용한 API 호출 시 페이로드 파싱 에러 발생**
  - **문제 상황:** 2차 PoC 도중 `curl`의 `--data-binary`로 악성 압축 파일(`archive.tar.xz`)을 전송했을 때, 데몬이 바이너리 데이터 내부의 세미콜론을 URL 쿼리 파라미터 구분자로 오인하여 `{"message":"invalid semicolon separator in query"}` 에러가 발생하며 업로드가 거부됨.
  - **해결 방안:** HTTP PUT 요청 헤더에 `-H "Content-Type: application/x-tar"` 옵션을 강제 주입하여, Docker API가 해당 body를 일반 Form 데이터가 아닌 원시 바이너리로 인식하고 파싱 오류 없이 정상 수신하도록 교정함.

- **이슈 4: Ubuntu 20.04에서 특정 Docker Engine 버전 설치 불가**
  - **문제상황:** : `Ubuntu 20.04`에서 PoC 환경을 구축하려고 하였으나, Docker 공식 APT 저장소 등록 후 설치 가능한 버전을 확인한 결과 `Docker Engine 29.x.x` 버전이 제공되지 않아 해당 버전을 설치할 수 없었음.
  - **해결 방안:** `Docker Engine 29.5.0` 및 `29.5.1`을 지원하는 `Ubuntu 24.04 LTS`환경에서 PoC를 진행함.

## 다음 회차 목표

- 기존에 분석한 취약점들의 root cause, 취약/패치 코드 비교, PoC 시나리오, 코드, 결과 정리 및 최종 요약
- 취약점 조사 내용 기반으로 최종 발표 자료 및 보고서 문안 보강
- 추후 분석할 CVE 조사 및 선정

## 참고 자료

- NVD: CVE-2026-41567 (https://nvd.nist.gov/vuln/detail/CVE-2026-41567)
- GitHub Security Advisory: GHSA-x86f-5xw2-fm2r
- Moby Patch Commit: 83946f17c3196c55434aa0b8a8773d3477cbd3dc
- Moby v29.5.1 release discussion