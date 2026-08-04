---
project_name: "G-Guard: 고도 엔진 기반 취약점 분석 및 전용 안티치트 솔루션 개발"
quad_name: "team7"
members: ["20221809_이채은", "20211677_김영현", "20253327_박성현", "20261616_김인환"]
report_number: 1              
date: "2026-08-04"
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

# [제 5차 프로젝트 진행 보고서] Gguard

- **팀원:** (팀장) 20221809_이채은, (팀원) 20211677_김영현, 20253327_박성현, 20261616_김인환
- **활동 기간:** 2026. 07. 22. ~ 2026. 08. 04. (2주)

# 프로젝트 진행 보고서 (제 6차)

## 팀 전체 진행 현황

- **이번 회차 목표:** Fuzzing 환경 구성, 분석 시작
- **현재 진행률:** 80% (전체 일정 대비)
- **주요 달성 사항:**
    - **Fuzzing 환경 구성:** Fuzzing 환경 구성
    - **취약점 분석 시작:** AFL++ Fuzzing 환경을 기반으로 취약점 분석 시작 (진행중)

## 개인별 기여 내역

> AFL++ Fuzzing 환경 구성 및 취약점 분석을 시작한다.

> 6주차 프로젝트 링크: https://www.notion.so/Gguard-364bc670312680beb3cec12af4ddfd04?source=copy_link

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20221809_이채은 | 스크립트 엔진 분석 (GDScript & GDExtention) | Godot의 고유 스크립트 언어인 GDScript의 컴파일러와 VM을 분석한다. Sandbox Escape, 메모리 취약점 등을 위주로 분석한다. | -| 25% |
| 20211677_김영현 | 리소스 파서 및 미디어 로더 분석 (Resource Parser & I/O) | 이미지(.png , .jpg ), 오디오(.ogg ), 3D 모델(.gltf , .obj ), Godot 씬 파일(.tscn , .scn ) 과 같은 에셋 리소스를 로드하는 부분을 분석한다.  | - | 25% |
| 20253327_박성현 | 네트워크 및 멀티플레이어 분석 (Network & RPC) | Godot 엔진에서 네트워크 및 멀티플레이어를 처리하는 과정에 대해서 분석한다. 외부 네트워크 패킷을 받아서 직렬화 / 역직렬화 하는 과정을 분석한다. | - | 25% |
| 20261616_김인환 | 빌드 환경 및 툴 체인 분석 (Scons & Godot Export) | 엔진 자체의 취약점보다는, 사용자가 프로젝트를 빌드하거나 패키징할 때 발생할 수 있는 취약점(공급망 공격, RCE 등)을 분석한다. 악의적으로 조작된 프로젝트 파일이나 빌드 스크립트를 로드할 때 발생하는 문제에 집중한다. | - | 25% |

## 이슈 및 해결 방안

- **문제 상황:** Fuzzing 툴 및 환경 선택의 어려움.
- **해결 현황:** 접근성, 컴퓨팅 환경 등을 고려하여 AFL++ Fuzzing 환경으로 결정, 컴포넌트 별로 분리하여 실험을 진행.


## 다음 회차 목표

- **Godot 엔진의 컴포넌트 별 AFL++ Fuzzing 및 결과 분석:** Fuzzing 을 진행하고 결과를 분석.
- **결과 정리:** Fuzzing 및 취약점 분석 결과를 문서화, 컴포넌트별 보고서 작성.



## 참고 자료

- Godot Docs: [Godot Docs](https://docs.godotengine.org/en/stable/about/introduction.html)
- Godot Source Code (GitHub): [Godot Source Code](https://github.com/godotengine/godot)
- Godot RE Tools (Github) : [Godot RE Tools](https://github.com/GDRETools/gdsdecomp)
- GDScript Toolkit (Github) : [GDScript Toolkit](https://github.com/Scony/godot-gdscript-toolkit)
- Godot GDscript Linter (Godot asset library) : [Godot GDscript Linter](https://godotengine.org/asset-library/asset/4612)
- LLVM : [LLVM](https://github.com/llvm/llvm-project)
- AFL++ : [AFL++](https://github.com/aflplusplus/aflplusplus)
- OssFuzz : [OssFuzz](https://github.com/google/oss-fuzz)

