---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 3          # 격주 보고 회차 (1~8)
date: "2026-06-23"
status: "진행 중"          # 시작 전 / 진행 중 / 보류 / 완료
cl_level: "CL2"           # 쿼드 팀 CL 등급 (CL1 / CL2 / CL3 / CL4)
contributions:            # 팀원별 기여도 (합계 100%)
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "runc CVE 후보 조사, CVE-2024-45310 개요·공격 구조·방어 관점 정리, 재현 결과 및 한계 정리"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "PoC 미공개 CVE 조사, CVE-2024-45310 원리 분석, 취약 runc 환경 구성 및 PoC 시도·실패 원인 분석"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "PoC 미공개 CVE 후보 조사, CVE-2024-45310 재현 실험 및 취약/패치 환경 비교 로그 확보"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "PoC 미공개 CVE 조사, CVE-2024-45310 PoC 시나리오 작성, runc 패치 전후 코드 분석"
    percentage: 25
---

# [제 3차 프로젝트 진행 보고서] runc-clear

- **팀원:** (팀장) 20231726_박민영, (팀원) 20251788_김동후, 20245024_김진호, 20231754_한지선
- **활동 기간:** 2026. 05. 15. ~ 2026. 06. 17.

## 팀 전체 진행 현황

- **이번 회차 목표:** runc 관련 CVE 조사 및 분석 대상 선정, CVE-2024-45310 취약점 원리 분석, PoC 재현 시도 및 패치 전후 동작 비교
- **현재 진행률:** 50%
- **주요 달성 사항:**
  - runc 및 컨테이너 런타임 관련 CVE 후보를 조사하고, 공개 PoC 존재 여부와 분석 난이도를 기준으로 주요 분석 대상 검토
  - 최종적으로 runc의 `os.MkdirAll` 기반 TOCTOU Race Condition 취약점인 **CVE-2024-45310**을 분석 대상으로 선정
  - CVE-2024-45310의 기본 정보를 정리
  - CVE-2024-45310 PoC 시나리오 설계 및 실습
  - 취약/패치 환경 비교 재현 로그를 확보
  - runc 패치 전후 코드 차이를 분석
  - 방어 관점 정리

## 개인별 기여 내역

| 팀원 | 역할 | 수행 작업 | 산출물 링크/근거 자료 | 기여도 |
|------|------|----------|----------------------|--------|
| 20231726_박민영 | 팀장 | runc 관련 CVE 후보군을 정리하고 공개 PoC 유무, 재현 난이도, 분석 포인트를 기준으로 우선순위를 검토하였다. CVE-2024-45310에 대해 개요, 영향 버전, 공격 조건, SecureJoin 이후 `os.MkdirAll` race 구조, 방어 관점, PoC 실행 결과 및 한계를 정리하였다. | `PoC 없는 CVE 조사: https://app.notion.com/p/PoC-CVE-36744fff78a780b19acbed9a15596fb3?source=copy_link`, `CVE-2024-45310 PoC 결과: https://app.notion.com/p/CVE-2024-45310-36e44fff78a78069b5cff3bb01cf4729?source=copy_link`, CVE-2024-45310 회의록 | 25% |
| 20251788_김동후 | 팀원 | PoC 미공개 또는 분석 대상 후보 CVE를 조사하고, `CVE-2023-25809`, `CVE-2025-31133`, `CVE-2025-52881`의 취약점 메커니즘과 분석 포인트를 정리하였다. CVE-2024-45310에 대해서는 취약 버전 runc 교체, attacker script 작성, PoC 실행, 실패 원인 분석, 병렬 실행을 통한 race 성공률 개선 방향을 정리하였다. | `PoC 없는 CVE 조사: https://app.notion.com/p/PoC-CVE-36544fff78a780d989defa22622664da?source=copy_link`, `CVE-2024-45310 PoC 결과: https://app.notion.com/p/CVE-2024-45310-36b44fff78a780d1b677c5c9634d0f83?source=copy_link` | 25% |
| 20245024_김진호 | 팀원 | 공개 PoC가 없는 CVE 후보를 조사하고 CVSS, 취약점 내용, 공개 PoC 여부를 표로 정리하였다. 이후 CVE-2024-45310 재현 실험에서 취약 환경과 패치 환경을 비교하고, 유일하게 PoC에 성공하였다. 취약 환경에서 host target 파일 생성이 관찰된 로그와 패치 환경에서 동일 동작이 관찰되지 않은 로그를 확보하였다. | `PoC 없는 CVE 조사: https://app.notion.com/p/PoC-CVE-36744fff78a780ee9d4ec10716cb39df?source=copy_link`, `CVE-2024-45310 PoC 결과: https://app.notion.com/p/CVE-2024-45310-38244fff78a78009bbe4e4c02fe4c3c6?source=copy_link` | 25% |
| 20231754_한지선 | 팀원 | PoC 존재 여부 확인 절차를 정리하고, runc 관련 CVE 후보의 패치 버전·CVSS·분석 포인트를 조사하였다. CVE-2024-45310 PoC 시나리오를 작성하고, 실행하였다. `rootfs_linux.go`, `system/linux.go`, `utils_unix.go`를 중심으로 패치 전후 코드 차이를 분석하였다. 특히 `createMountpoint`, `MkdirAllInRootOpen`, `Openat`, `Mkdirat`, `O_NOFOLLOW` 기반 방어 로직을 정리하였다. | `PoC 없는 CVE 조사: https://app.notion.com/p/PoC-CVE-36644fff78a78072ad2ec339ebd0bbc3?source=copy_link`, `CVE-2024-45310 PoC 결과: https://app.notion.com/p/CVE-2024-45310-36c44fff78a780bfa487ed4b829363d0?source=copy_link` | 25% |

## 이슈 및 해결 방안

- **이슈 1: 분석 대상 CVE 선정 기준이 필요하였다.**
  - **문제 상황:** runc 및 컨테이너 런타임 관련 CVE가 많고, 일부는 이미 공개 PoC가 존재하여 CVE를 선정하기 어려웠다.
  - **해결 방안:** 각 팀원이 후보 CVE를 분담 조사하고, 공개 PoC 존재 여부, CVSS, 재현 난이도, runc 내부 코드와의 연결성을 기준으로 비교하였다. 그 결과 공개 PoC가 제한적이고 runc mountpoint 생성 로직과 직접 연결되는 CVE-2024-45310을 우선 분석 대상으로 선정하였다.

- **이슈 2: 취약 runc 버전 교체가 바로 반영되지 않았다.**
  - **문제 상황:** 취약 버전 runc `v1.1.13` 바이너리를 다운로드했지만, Docker가 실제로 사용하는 runc 경로와 사용자가 확인한 runc 경로가 달라 버전 변경 여부가 혼동되었다.
  - **해결 방안:** 기존 `/usr/bin/runc`, `/usr/sbin/runc`를 백업한 뒤 취약 버전 바이너리로 교체하고, Docker 서비스를 재시작하였다. 이후 `runc --version`, `/usr/bin/runc --version`, `docker info | grep -i runc`로 실제 적용 여부를 확인하였다.

- **이슈 3: Race Condition 특성상 PoC 재현이 안정적이지 않았다.**
  - **문제 상황:** 초기 WSL/VM 기반 실험에서는 attacker 컨테이너가 symlink를 교체하는 속도와 target 컨테이너가 mountpoint 생성을 수행하는 타이밍이 맞지 않아 `hacked_file` 또는 `pocfile` 생성이 관찰되지 않았다.
  - **해결 방안:** 컨테이너 내부에서 깨질 수 있는 호스트 절대경로 기반 symlink 대신 공유 볼륨 내부 경로를 사용하도록 attacker script를 수정하였다. 또한 반복 실행 횟수를 늘리고, 여러 target 컨테이너를 병렬로 실행하여 runc 호출량을 늘리는 방식으로 race 성공률을 높이는 방향을 검토하였다.

- **이슈 4: 패치 환경 로그에 mount 실패와 cgroup 관련 warning이 반복되었다.**
  - **문제 상황:** patched build log에서 `/race/point/pocfile` 접근 실패, mount destination 생성 실패, cgroup memory event 관련 warning이 반복되었다.
  - **해결 방안:** 해당 로그를 별도로 보존하고, 핵심 관찰 지표를 host target 파일 생성 여부로 정리하였다. cgroup warning은 컨테이너 종료/정리 과정에서 발생한 부수 로그로 분리하고, PoC 판정은 `target=/cve-2024-45310-host-target/pocfile`의 생성 여부와 취약/패치 환경 비교 결과를 기준으로 판단하였다.

## 다음 회차 목표

- CVE-2024-25621 PoC 

## 참고 자료

- https://nvd.nist.gov/vuln/detail/cve-2024-45310 // CVE-2024-45310 NVD 상세 정보
- https://www.cve.org/CVERecord?id=CVE-2024-45310 // CVE 공식 레코드
- https://github.com/opencontainers/runc/security/advisories/GHSA-jfvp-7x6p-h2pv // runc CVE-2024-45310 공식 advisory
- https://github.com/advisories/GHSA-jfvp-7x6p-h2pv // GitHub Advisory Database
- https://www.suse.com/security/cve/CVE-2024-45310.html // SUSE CVE 정보
- https://www.wiz.io/vulnerability-database/cve/cve-2024-45310 // Wiz CVE 요약
- https://github.com/opencontainers/runc/tree/main // runc 공식 GitHub repository
- https://github.com/opencontainers/runc/releases // runc release 및 취약/패치 버전 확인
- https://nvd.nist.gov/vuln/detail/CVE-2025-52881 // CVE-2025-52881 NVD 상세 정보
- https://github.com/opencontainers/runc/security/advisories/GHSA-cgrx-mc8f-2prm // runc arbitrary write gadgets and procfs write redirects advisory
- https://nvd.nist.gov/vuln/detail/CVE-2025-31133 // CVE-2025-31133 NVD 상세 정보
- https://github.com/skynet-f-nvidia/CVE-2025-31133 // CVE-2025-31133 PoC 참고
- https://nvd.nist.gov/vuln/detail/CVE-2025-52565 // CVE-2025-52565 NVD 상세 정보
- https://nvd.nist.gov/vuln/detail/cve-2024-21626 // CVE-2024-21626 NVD 상세 정보
- https://github.com/NitroCao/CVE-2024-21626 // CVE-2024-21626 PoC 참고
- https://nvd.nist.gov/vuln/detail/cve-2023-28642 // CVE-2023-28642 NVD 상세 정보
- https://github.com/opencontainers/runc/pull/3785 // CVE-2023-28642 관련 runc 패치 PR
- https://nvd.nist.gov/vuln/detail/cve-2023-27561 // CVE-2023-27561 NVD 상세 정보
- https://gist.github.com/LiveOverflow/c937820b688922eb127fb760ce06dab9 // CVE-2023-27561 PoC 참고
- https://nvd.nist.gov/vuln/detail/cve-2021-43784 // CVE-2021-43784 NVD 상세 정보
- https://project-zero.issues.chromium.org/issues/42451364 // CVE-2021-43784 관련 Project Zero 분석
- https://github.com/T1erno/CVE-2022-0492-Docker-Breakout-Checker-and-PoC // CVE-2022-0492 PoC 참고
- https://asec.ahnlab.com/ko/91155/ // runc 보안 업데이트 권고 참고
- https://github.com/madhuakula/kubernetes-goat // Kubernetes Goat - 보안 실습 환경