---
project_name: "runc-clear"
quad_name: "8조"
members: ["20231726_박민영", "20251788_김동후", "20245024_김진호", "20231754_한지선"]
report_number: 1          # 격주 보고 회차 (1~8)
date: "2026-04-30"
status: "진행 중"          # 시작 전 / 진행 중 / 보류 / 완료
cl_level: "CL2"           # 쿼드 팀 CL 등급 (CL1 / CL2 / CL3 / CL4)
contributions:            # 팀원별 기여도 (합계 100%)
  - name: "20231726_박민영"
    role: "팀장"
    tasks: "자료조사 및 보고서 작성"
    percentage: 25
  - name: "20251788_김동후"
    role: "팀원"
    tasks: "자료조사"
    percentage: 25
  - name: "20245024_김진호"
    role: "팀원"
    tasks: "자료조사"
    percentage: 25
  - name: "20231754_한지선"
    role: "팀원"
    tasks: "자료조사"
    percentage: 25
---

# [제 1차 프로젝트 진행 보고서] runc-clear

- **팀원:** (팀장) 20231726_박민영, (팀원) 20251788_김동후, 20245024_김진호, 20231754_한지선
- **활동 기간:** 2026. 03. 29. ~ 2026. 04. 09. (2주)

## 팀 전체 진행 현황

- **이번 회차 목표:** 컨테이너 동작 원리, 핵심 기술 학습
- **현재 진행률:** 10% (전체 일정 대비)
- **주요 달성 사항:** 도커, 쿠버네티스, Linux Namespace, cgroups 관련 개념 이해

## 개인별 기여 내역

> 각 팀원이 이번 회차에 구체적으로 무엇을 했는지 작성합니다.
> 산출물 링크(GitHub 커밋 로그, PR 링크, 분석한 코드 주소 등)를 반드시 포함합니다.

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20231726_박민영 | 자료조사 및 공유 | 도커, 쿠버네티스, Linux Namespace, cgroups 관련 개념 정리 | https://www.notion.so/67044fff78a78218adee013844c19275?source=copy_link, https://www.notion.so/Linux-Namespace-cgroups-33d44fff78a780a4817eefd1f7fddc12?source=copy_link| 25% |
| 20251788_김동후 | 자료조사 및 공유 | 도커, 쿠버네티스, Linux Namespace, cgroups 관련 개념 정리 | https://www.notion.so/33644fff78a780aab9a1d269d347338c?source=copy_link, https://www.notion.so/Linux-Namespace-cgroups-33b44fff78a780fd9bffe04e2a94f1a0?source=copy_link| 25% |
| 20245024_김진호 | 자료조사 및 공유 | 도커, 쿠버네티스, Linux Namespace, cgroups 관련 개념 정리 | https://www.notion.so/33644fff78a780a1a65eca2414949fd6?source=copy_link, https://www.notion.so/Linux-namespace-cgroups-33d44fff78a7805cb9d4f5cb53d7d7d0?source=copy_link| 25% |
| 20231754_한지선 | 자료조사 및 공유 | 도커, 쿠버네티스, Linux Namespace, cgroups 관련 개념 정리 | https://www.notion.so/33644fff78a7804fa5c3ddd6f4e72e81?source=copy_link, https://www.notion.so/Linux-namespace-cgroups-33d44fff78a780c9aad0c80de8a928b6?source=copy_link| 25% |

## 이슈 및 해결 방안

- **문제 상황:** Namespace 개념을 익히기 위해 pivot_root를 실습하는 과정에서 mount를 잘못하여 wsl이 날아가는 문제가 발생하였다.
- **해결 현황:** powershell에서 wsl shutdown을 통해 복구하였다.

## 다음 회차 목표

- runc 실행 흐름, 내부 구조 분석

## 참고 자료

- https://www.hanbit.co.kr/channel/view.html?cmscode=CMS8893081462 // 원리부터 이해하는 도커 - 컨테이너, 가상화, 구성요소 (<한 권으로 배우는 도커 & 쿠버네티스 (장철원)>)
- https://ktcloudplatform.tistory.com/69 // 가상화, 컨테이너, 프로세스 격리
- https://jdcyber.tistory.com/69 // 컨테이너 개념
- https://tech.ktcloud.com/73 // 도커 image, 레이어 저장 방식
- https://sseozytank.tistory.com/85 // 도커 명령어
- https://jdcyber.tistory.com/46 // Kubernetes 개념
- https://wooono.tistory.com/700 // Control Plane, Data plane 개념
- https://www.44bits.io/ko/keyword/linux-namespace // 네임스페이스 설명
- https://www.44bits.io/ko/post/is-docker-container-a-virtual-machine-or-a-process // ‘도커 컨테이너는 리눅스 프로세스다’ (실습) & PID Namespace 관련 내용
- https://seungyooon.tistory.com/142 // cgroups 관련 내용
- https://d2.naver.com/helloworld/7248350 // 리눅스의 Control Groups 기능이 Kubernetes에 어떻게 적용되는지 살펴보기
- https://velog.io/@baeyuna97/%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%A3%BC%EC%9A%94%EA%B0%9C%EB%85%90-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-Cgroup-namespace // cgroups 관련 내용
- https://malwareanalysis.tistory.com/763 // chroot - 컨테이너는 어떻게 파일을 실행할까?
- https://malwareanalysis.tistory.com/768 // 컨테이너 원리 - pivot_root(chroot 취약점을 해결)
- https://www.minzkn.com/linuxkernel/pages/cgroups.html // cgroups v1/v2 (Control Groups)