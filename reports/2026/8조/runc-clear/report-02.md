---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 2          # 격주 보고 회차 (1~8)
date: "2026-05-19"
status: "진행 중"          # 시작 전 / 진행 중 / 보류 / 완료
cl_level: "CL2"           # 쿼드 팀 CL 등급 (CL1 / CL2 / CL3 / CL4)
contributions:            # 팀원별 기여도 (합계 100%)
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "runc 실행 환경 구성 실습, Filesystem & Jail 매니저 분석"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "runc 실행 환경 구성 실습 및 격리성 검증, Communication & Sync 매니저 분석"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "runc 내부 코드 분석, Communication & Sync 매니저 분석"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "OCI 스펙/syscall 추적, Filesystem & Jail 매니저 분석, 보고서 작성"
    percentage: 25
---

# [제 2차 프로젝트 진행 보고서] runc-clear

- **팀원:** (팀장) 20231726_박민영, (팀원) 20251788_김동후, 20245024_김진호, 20231754_한지선
- **활동 기간:** 2026. 05. 01. ~ 2026. 05. 14. (2주)

## 팀 전체 진행 현황

- **이번 회차 목표:** runc 실행 & 실행 흐름 분석 + runc 주요 코드 분석
- **현재 진행률:** 30%
- **주요 달성 사항:** 
  - Docker export 및 OCI Bundle(config.json, rootfs) 생성 실습 완료
  - `runc run` / `runc create` / `runc start` 직접 실행 및 동작 차이 확인
  - `strace`를 활용한 시스템 콜(clone, unshare, pivot_root) 흐름 및 Namespace 격리 검증
  - runc 내부 로직 분석 완료:
    - Filesystem & Jail 매니저 (`rootfs_linux.go`, `mount_linux.go`, `init_linux.go`) 분석
    - Communication & Sync 매니저 (`sync.go`, `process_linux.go`) 분석
    - C nsexec 3단계 stage, 부모-자식 동기화, rootfs 구성, 상태 관리 로직 파악
    - Resource & Interface 매니저 (`capabilities.go`, `fs2/fs2.go`, `fs2/create.go`, `cgroups/file.go`) 분석

## 개인별 기여 내역

> 각 팀원이 이번 회차에 구체적으로 무엇을 했는지 작성합니다.
> 산출물 링크(GitHub 커밋 로그, PR 링크, 분석한 코드 주소 등)를 반드시 포함합니다.

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20231726_박민영 | 팀장 | OCI Bundle 생성 및 runc 실행 실습, `rootfs_linux.go` · `mount_linux.go` · `init_linux.go` 핵심 함수 분석 | runc 실행 흐름 분석: https://www.notion.so/runc-35944fff78a7808fa7e6d2413d0ac57d?source=copy_link, Filesystem & Jail 매니저 분석: https://www.notion.so/runc-35f44fff78a780689a65e8a6e6220ddc?source=copy_link | 25% | 
| 20251788_김동후 | 팀원 | runc 실행 환경 구성 및 격리성 검증 실습 (PID/파일시스템 격리, Capabilities 권한 실습), `capabilities.go` · cgroup v2 (`fs2.go`, `create.go`, `file.go`) 분석 | runc 실행 흐름 및 내부 구조 분석: https://www.notion.so/runc-36444fff78a78012a99dff834a63db50?source=copy_link, Communication & Sync 매니저 분석: https://www.notion.so/rucn-36244fff78a780f0ad9fe93c4c6c671c?source=copy_link | 25% |
| 20245024_김진호 | 팀원 | runc CLI 진입점~`newParentProcess` 전체 실행 흐름 분석, nsexec C 코드 및 부모-자식 동기화 프로토콜 분석 | runc 실행 흐름 및 내부 구조 분석: https://www.notion.so/runc-35244fff78a780f0ba05e64cad5a198d?source=copy_link, Communication & Sync 매니저 분석: https://www.notion.so/runc-36444fff78a7804bb7ebc76bba0e3540?source=copy_link | 25% |
| 20231754_한지선 | 팀원 | strace로 syscall 흐름 추적 및 namespace 격리 확인, `rootfs_linux.go` · `mount_linux.go` 보안 관련 함수 분석 | runc 실행 흐름 분석: https://www.notion.so/runc-35944fff78a780b488cad9476ab3d1bf?, Filesystem & Jail 매니저 분석: https://www.notion.so/rucn-36044fff78a780a9a5ecf264d8b8cb60?source=copy_linksource=copy_link | 25% | 

## 이슈 및 해결 방안

- **문제 상황:** `runc create` 실행 시 PTY(Pseudo Terminal) 관련 오류가 발생하여 컨테이너가 생성되지 않았다.
- **해결 현황:** `config.json`의 `"terminal"` 값을 `false`로 변경하여 해결하였다. `runc create`는 detach 상태로 동작하기 때문에 PTY master를 관리할 프로세스가 없어 발생하는 문제로, 원래는 `--console-socket` 옵션을 통해 PTY master fd를 별도 프로세스에 전달해야 한다.


## 다음 회차 목표

- runc 관련 CVE 조사 및 선정, 분석 지점 식별

## 참고 자료

- https://velog.io/@zzerym/runc%EB%A1%9C-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88-%EB%A7%8C%EB%93%A4%EC%96%B4%EB%B3%B4%EA%B8%B0 // runc로 컨테이너 만들어보기
- https://wikidocs.net/336825 // Just Read. 쿠버네티스
- https://github.com/opencontainers/runc/tree/main // runc 공식 github repository
- https://github.com/madhuakula/kubernetes-goat // Kubernetes Goat - 보안 실습 환경