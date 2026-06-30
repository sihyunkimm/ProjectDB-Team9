---
project_name: "G-Guard: 고도 엔진 기반 취약점 분석 및 전용 안티치트 솔루션 개발"
quad_name: "team7"
members: ["20221809_이채은", "20211677_김영현", "20253327_박성현", "20261616_김인환"]
report_number: 3               
date: "2026-06-22"
status: "진행 중"
cl_level: "CL1"
field: "게임 보안, 리버싱, 시스템 보안"
contributions:
  - name: "20221809_이채은"
    role: "팀장"
    tasks: "프로젝트 기획 및 보고서 작성"
    percentage: 25
  - name: "20211677_김영현"
    role: "팀원"
    tasks: "프로젝트 기획 및 보고서 작성"
    percentage: 25
  - name: "20253327_박성현"
    role: "팀원"
    tasks: "프로젝트 기획 및 보고서 작성"
    percentage: 25
  - name: "20261616_김인환"
    role: "팀원"
    tasks: "프로젝트 기획 및 보고서 작성"
    percentage: 25
---

# [제 3차 프로젝트 진행 보고서] Gguard

- **팀원:** (팀장) 20221809_이채은, (팀원) 20211677_김영현, 20253327_박성현, 20261616_김인환
- **활동 기간:** 2026. 06. 08. ~ 2026. 06. 22. (2주)

# 프로젝트 진행 보고서 (제 3차)

## 팀 전체 진행 현황

- **이번 회차 목표:** Godot 엔진 분석, 취약점 분석 진행 및 실험 전략 수립
- **현재 진행률:** 30% (전체 일정 대비)
- **주요 달성 사항:**
    - **담당 파트에 대한 코드베이스 분석:** 각자 담당하는 파트의 기본 코드 분석 진행
    - **실험 전략 수립:** 기본 코드 분석 및 취약점 분석을 기반으로 실제 취약점 발견을 위한 실험 전략 수립

## 개인별 기여 내역

> 담당한 파트의 코드 분석 및 개념 학습을 기반으로 취약점 발견을 위한 전략을 수립할 수 있도록 한다.

> 3주차 프로젝트 링크: https://www.notion.so/Gguard-week-3-365bc670312680b999edd826509fbdcf

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20221809_이채은 | 스크립트 엔진 분석 (GDScript & GDExtention) | Godot의 고유 스크립트 언어인 GDScript의 컴파일러와 VM을 분석한다. Sandbox Escape, 메모리 취약점 등을 위주로 분석한다. | https://www.notion.so/2-365bc670312680c78a04c6b13cd548e0 | 25% |
| 20211677_김영현 | 리소스 파서 및 미디어 로더 분석 (Resource Parser & I/O) | 이미지(.png , .jpg ), 오디오(.ogg ), 3D 모델(.gltf , .obj ), Godot 씬 파일(.tscn , .scn ) 과 같은 에셋 리소스를 로드하는 부분을 분석한다.  | https://www.notion.so/4-365bc6703126809ca2bec140267e883e | 25% |
| 20253327_박성현 | 네트워크 및 멀티플레이어 분석 (Network & RPC) | Godot 엔진에서 네트워크 및 멀티플레이어를 처리하는 과정에 대해서 분석한다. 외부 네트워크 패킷을 받아서 직렬화 / 역직렬화 하는 과정을 분석한다. | https://www.notion.so/3-365bc6703126806a8afbcf3a6066a530 | 25% |
| 20261616_김인환 | 빌드 환경 및 툴 체인 분석 (Scons & Godot Export) | 엔진 자체의 취약점보다는, 사용자가 프로젝트를 빌드하거나 패키징할 때 발생할 수 있는 취약점(공급망 공격, RCE 등)을 분석한다. 악의적으로 조작된 프로젝트 파일이나 빌드 스크립트를 로드할 때 발생하는 문제에 집중한다. | https://www.notion.so/1-365bc67031268029b934e9a92a9b2f49 | 25% |

## 이슈 및 해결 방안

- **문제 상황:** 공격 대상의 광범위함.
- **해결 현황:** 더 효율적인 취약점 탐지를 위해 실험을 진행할 취약점 시나리오를 세우고, 이를 추후에 선별하여 취약점 발견을 위한 분석을 진행. 


## 다음 회차 목표

- **취약점 선별:** 토의를 통해 각 파트별로 실험을 시도할 취약점 선별
- **분석 환경 구축 및 타겟 세팅:** Godot 엔진의 소스코드를 적용하여 빌드, 각 파트별로 실험에 필요한 환경 구축.
- **PoC 작성 및 익스플로잇:** 선별된 취약점 시나리오에 대해 실제 PoC 작성 및 익스플로잇 시도.


## 참고 자료

- Godot Docs: [Godot Docs](https://docs.godotengine.org/en/stable/about/introduction.html)
- Godot Source Code (GitHub): [Godot Source Code](https://github.com/godotengine/godot)
- Godot RE Tools (Github) : [Godot RE Tools](https://github.com/GDRETools/gdsdecomp)
- GDScript Toolkit (Github) : [GDScript Toolkit](https://github.com/Scony/godot-gdscript-toolkit)
- Godot GDscript Linter (Godot asset library) : [Godot GDscript Linter](https://godotengine.org/asset-library/asset/4612)

