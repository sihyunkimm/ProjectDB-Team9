---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 4          # 격주 보고 회차 (1~8)
date: "2026-07-03"
status: "진행 중"          # 시작 전 / 진행 중 / 보류 / 완료
cl_level: "CL2"           # 쿼드 팀 CL 등급 (CL1 / CL2 / CL3 / CL4)
contributions:            # 팀원별 기여도 (합계 100%)
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "CVE-2024-25621 개요·영향 버전·공개 시점·운영상 위험도·대응 방안 정리, PoC 실습"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "취약/패치 containerd 환경 구성, 버전 비교 검증, 비권한 사용자 접근 테스트 자동화"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "PoC 1·2 실습, SUID 바이너리 실행 시도, 익스플로잇 실패 원인 및 제약 분석"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "업스트림 패치 커밋 분석, 권한 비트 변화 확인, ctr 기반 실험 제약 및 우회 절차 정리"
    percentage: 25
---

# [제 4차 프로젝트 진행 보고서] runc-clear

- **팀원:** (팀장) 20231726_박민영, (팀원) 20251788_김동후, 20245024_김진호, 20231754_한지선
- **활동 기간:** 2026. 06. 18. ~ 2026. 07. 03.

## 팀 전체 진행 현황

- **이번 회차 목표:** CVE-2024-25621 취약점 원리 분석, 취약/패치 버전 비교 실험, 비권한 접근 재현, 권한 상승 가능성 검토
- **현재 진행률:** 70%
- **주요 달성 사항:**
  - `containerd`의 디렉터리 권한 오설정 취약점인 **CVE-2024-25621**을 분석 대상으로 선정하고, 영향 버전·수정 버전·공개 advisory 시점을 정리
  - 취약 버전 `1.7.28`과 수정 버전 `1.7.29`를 비교하여 `/var/lib/containerd` 권한이 각각 `0711`, `0700`으로 생성됨을 확인
  - 비권한 사용자가 취약 버전의 `meta.db` 경로에 접근 가능하고, 수정 버전에서는 동일 경로 접근이 차단됨을 검증
  - `passwd`, `mount` 등 SUID 바이너리를 활용한 권한 상승 시도를 수행하고, 실행 가능 여부와 실제 상승 실패 원인을 정리
  - 업스트림 패치 커밋을 분석하여 `chmod 0700` 보강, CRI 디렉터리 권한 강화, 일부 state 경로 예외 처리 로직을 확인
  - 중첩 Docker 환경에서 `ctr run`, `ctr snapshot prepare`가 실패하는 원인을 파악하고 `ctr image mount` 기반 우회 절차를 정리

## 개인별 기여 내역

| 팀원 | 역할 | 수행 작업 | 산출물 링크/근거 자료 | 기여도 |
|------|------|----------|----------------------|--------|
| 20231726_박민영 | 팀장 | CVE-2024-25621의 개요, 취약점 메커니즘을 정리하였다. Docker 기반 Ubuntu 실험 환경에서 비권한 사용자로 디렉터리에 접근하는 PoC를 실습하였다. | https://app.notion.com/p/CVE-2024-25621-38744fff78a78093a13bc565f68b8e8d?source=copy_link | 25% |
| 20251788_김동후 | 팀원 | 공식 `containerd` 릴리스 `1.7.28`과 `1.7.29`를 동일 게스트에서 분리된 `--root`, `--state`, `--address` 값으로 실행하는 비교 실험을 구성하였다. 각 버전에서 생성된 디렉터리 권한을 측정하고, 비권한 사용자로 `meta.db`를 읽을 수 있는지 확인하는 검증 절차와 스크립트를 정리하였다. | https://app.notion.com/p/CVE-2024-25621-38344fff78a7809295dbda7320ffac88?source=copy_link | 25% |
| 20245024_김진호 | 팀원 | Docker 기반 Ubuntu 실험 환경에서 `containerd`를 기동하여 `/var/lib/containerd`의 traverse 비트를 재확인하였다. 이후 비권한 사용자로 `stat` 기반 접근을 검증하고, `passwd`, `mount` SUID 바이너리를 해당 경로 아래에 배치하여 실제 익스플로잇을 시도한 뒤 내부 권한 검사로 인해 권한 상승이 차단되는 과정을 분석하였다. | https://app.notion.com/p/CVE-2024-25621-38944fff78a780659864f5b93229ba19?source=copy_link | 25% |
| 20231754_한지선 | 팀원 | 업스트림 패치에서 `config.Root`, `config.TempDir`, CRI 및 sandbox controller 경로 권한이 `0700`으로 보강되는 지점을 분석하였다. 또한 중첩 컨테이너 환경에서 `ctr run`과 `ctr snapshot prepare`가 실패한 이유를 정리하고, 이미지 전개를 위해 `ctr image mount`를 사용하는 우회 절차를 문서화하였다. | https://app.notion.com/p/CVE-2024-25621-38844fff78a780aeb609cecaf7392806?source=copy_link | 25% |

## 이슈 및 해결 방안

- **이슈 1: CVE-2024-25621의 실제 취약 지점이 runc가 아니라 containerd 디렉터리 권한 로직이라는 점을 먼저 분리해야 했다.**
  - **문제 상황:** 초기에는 기존 runc 분석 흐름의 연장선에서 컨테이너 실행 자체가 핵심일 수 있다고 보았으나, 실제 취약점은 `containerd` 데몬이 관리 디렉터리를 생성할 때 권한 비트를 잘못 부여하는 문제였다.
  - **해결 방안:** GitHub advisory, NVD, 업스트림 패치 커밋을 대조하여 취약 트리거를 `containerd`의 디렉터리 생성 로직으로 한정하고, 실험 범위를 취약/패치 버전 비교와 비권한 접근 검증 중심으로 재구성하였다.

- **이슈 2: 중첩 Docker 환경에서 일반적인 `ctr run` 방식이 그대로 동작하지 않았다.**
  - **문제 상황:** Docker 컨테이너 내부에서 다시 `ctr run`을 수행하면 overlay 마운트가 충돌했고, `ctr snapshot prepare`는 이미지 이름을 직접 인자로 받지 않아 실험 흐름이 끊겼다.
  - **해결 방안:** 컨테이너 실행까지 포함한 경로를 포기하고, `ctr image mount`로 rootfs를 직접 전개한 뒤 필요한 SUID 바이너리만 추출하는 방식으로 실험 절차를 단순화하였다.

- **이슈 3: 취약 조건 재현과 실제 권한 상승 성공을 동일하게 볼 수 없었다.**
  - **문제 상황:** `/var/lib/containerd`의 `0711` 권한과 비권한 사용자 접근은 확인되었지만, 이것만으로 곧바로 root 획득이 보장되지는 않았다.
  - **해결 방안:** 취약 조건 검증과 익스플로잇 가능성 검토를 분리하였다. 전자는 `meta.db` 접근 성공/실패 비교로 증명하고, 후자는 SUID 바이너리 실행 시도 결과와 내부 권한 검사로 인해 차단된 이유를 별도로 정리하였다.

- **이슈 4: 패치 후에도 일부 state 경로는 의도적으로 넓은 권한을 유지할 수 있어 오탐 가능성이 있었다.**
  - **문제 상황:** 단순히 `0711`만 기준으로 보면 모든 state 디렉터리를 취약점으로 오해할 수 있었다.
  - **해결 방안:** 업스트림 패치 주석과 advisory 설명을 함께 검토하여, 실제 핵심 지표는 `root` 및 CRI 관련 민감 경로 권한이 `0700`으로 강화되는지 여부라는 점을 기준으로 삼았다.

## 다음 회차 목표

- 이번 회차 실험 로그와 패치 분석 결과를 기반으로 최종 발표 자료 및 보고서 문안 보강
- CVE-2026-41567

## 참고 자료

- https://github.com/containerd/containerd/security/advisories/GHSA-pwhc-rpq9-4c8w // containerd 공식 advisory
- https://nvd.nist.gov/vuln/detail/CVE-2024-25621 // CVE-2024-25621 NVD 상세 정보
- https://osv.dev/vulnerability/CVE-2024-25621 // OSV 취약점 레코드
- https://github.com/containerd/containerd/commit/7c59e8e9e970d38061a77b586b23655c352bfec5 // 업스트림 수정 커밋
- https://github.com/containerd/containerd/releases // containerd 릴리스 및 영향/수정 버전 확인
- https://ubuntu.com/security/notices/USN-7983-1 // Ubuntu 보안 공지
