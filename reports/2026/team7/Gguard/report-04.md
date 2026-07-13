---
project_name: "G-Guard: 고도 엔진 기반 취약점 분석 및 전용 안티치트 솔루션 개발"
quad_name: "team7"
members: ["20221809_이채은", "20211677_김영현", "20253327_박성현", "20261616_김인환"]
report_number: 4              
date: "2026-07-07"
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

# [제 4차 프로젝트 진행 보고서] Gguard

- **팀원:** (팀장) 20221809_이채은, (팀원) 20211677_김영현, 20253327_박성현, 20261616_김인환
- **활동 기간:** 2026. 06. 22. ~ 2026. 07. 07. (2주)

# 프로젝트 진행 보고서 (제 4차)

## 팀 전체 진행 현황

- **이번 회차 목표:** 취약점 분석 아이디어 취합, 분석 방법론 탐색
- **현재 진행률:** 40% (전체 일정 대비)
- **주요 달성 사항:**
    - **취약점 분석 아이디어 취합:** 취약점이 발견될 수 있는 각자의 아이디어를 취합, 체크리스트 작성
    - **분석 방법론 탐색:** Fuzzing 방법론 탐색

## 개인별 기여 내역

> 분석을 토대로 취약점이 발견될 수 있는 아이디어를 취합하며, 분석 방법론에 대해 탐색한다.

> 4주차 프로젝트 링크: https://www.notion.so/Gguard-364bc670312680beb3cec12af4ddfd04?source=copy_link

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20221809_이채은 | 스크립트 엔진 분석 (GDScript & GDExtention) | Godot의 고유 스크립트 언어인 GDScript의 컴파일러와 VM을 분석한다. Sandbox Escape, 메모리 취약점 등을 위주로 분석한다. | -| 25% |
| 20211677_김영현 | 리소스 파서 및 미디어 로더 분석 (Resource Parser & I/O) | 이미지(.png , .jpg ), 오디오(.ogg ), 3D 모델(.gltf , .obj ), Godot 씬 파일(.tscn , .scn ) 과 같은 에셋 리소스를 로드하는 부분을 분석한다.  | - | 25% |
| 20253327_박성현 | 네트워크 및 멀티플레이어 분석 (Network & RPC) | Godot 엔진에서 네트워크 및 멀티플레이어를 처리하는 과정에 대해서 분석한다. 외부 네트워크 패킷을 받아서 직렬화 / 역직렬화 하는 과정을 분석한다. | - | 25% |
| 20261616_김인환 | 빌드 환경 및 툴 체인 분석 (Scons & Godot Export) | 엔진 자체의 취약점보다는, 사용자가 프로젝트를 빌드하거나 패키징할 때 발생할 수 있는 취약점(공급망 공격, RCE 등)을 분석한다. 악의적으로 조작된 프로젝트 파일이나 빌드 스크립트를 로드할 때 발생하는 문제에 집중한다. | - | 25% |

## 이슈 및 해결 방안

- **문제 상황:** 분석 방법론의 선정 필요, 개별 분석의 비효율성
- **해결 현황:** 효율적인 분석을 위해 Fuzzing 방법론에 대해 알아보고 환경을 수립함.


## 다음 회차 목표

- **Fuzzing 및 실험 환경 구축:** Fuzzing 환경을 구축.
- **체크리스트 실험 진행:** 작성한 취약점 체크리스트를 기반으로 실험 진행.



## 참고 자료

- Godot Docs: [Godot Docs](https://docs.godotengine.org/en/stable/about/introduction.html)
- Godot Source Code (GitHub): [Godot Source Code](https://github.com/godotengine/godot)
- Godot RE Tools (Github) : [Godot RE Tools](https://github.com/GDRETools/gdsdecomp)
- GDScript Toolkit (Github) : [GDScript Toolkit](https://github.com/Scony/godot-gdscript-toolkit)
- Godot GDscript Linter (Godot asset library) : [Godot GDscript Linter](https://godotengine.org/asset-library/asset/4612)
- LLVM : [LLVM](https://github.com/llvm/llvm-project)
- AFL++ : [AFL++](https://github.com/aflplusplus/aflplusplus)
- OssFuzz : [OssFuzz](https://github.com/google/oss-fuzz)

