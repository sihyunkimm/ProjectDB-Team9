---
project_name: "G-Guard: 고도 엔진 기반 취약점 분석 및 전용 안티치트 솔루션 개발"
quad_name: "team7"
members: ["20221809_이채은", "20211677_김영현", "20253327_박성현", "20261616_김인환"]
report_number: 1               
date: "2026-04-12"
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

# [제 1차 프로젝트 진행 보고서] Gguard

- **팀원:** (팀장) 20221809_이채은, (팀원) 20211677_김영현, 20253327_박성현, 20261616_김인환
- **활동 기간:** 2026. 03. 29. ~ 2026. 04. 12. (2주)

# 프로젝트 진행 보고서 (제 1차)

## 팀 전체 진행 현황

- **이번 회차 목표:** Godot 엔진 분석을 위한 역할 분담 및 계획 수립
- **현재 진행률:** 5% (전체 일정 대비)
- **주요 달성 사항:**
    - **역할 분담:** Godot 엔진 분석을 효율적으로 진행하기 위한 세부 역할 분담

## 개인별 기여 내역

> Godot 엔진의 공식 문서를 읽고, 그 동작을 충분히 이해 및 파악하기 위해 중점적으로 분석할 부분을 확정하였습니다.

| 팀원 | 역할 | 수행 작업 | 산출물 링크 | 기여도 |
|------|------|----------|------------|--------|
| 20221809_이채은 | SCons 빌드 시스템 분석 | SCons, Sanitizers 등 Godot 엔진에서 사용되는 빌드 시스템 조사 | - | 25% |
| 20211677_김영현 | Godot 오픈소스 코드 분석 | 소스 코드의 구조 파악 및 환경 구축 진행 | - | 25% |
| 20253327_박성현 | Godot docs를 통한 엔진 구조 파악 | Godot 엔진의 핵심 컴포넌트(Core, Scene Tree, Servers, GDScript & VM)의 동작 파악 | - | 25% |
| 20261616_김인환 | 취약점 분석 방법론 비교 | Godot 엔진의 취약점을 분석할 오픈소스 툴 및 라이브러리 조사 (Godot RE Tools, GDScript Toolkit, Godot GDscript Linter) | - | 25% |

## 이슈 및 해결 방안

- **문제 상황:** 소스 코드 분석 시 대형 프로젝트의 흐름 파악 어려움
- **해결 현황:** 공식 문서의 내용과 결합하여 동작에 핵심적인 코드 파일을 우선적으로 분석함
- **문제 상황:** SCons 빌드 도구에 관한 공부 필요
- **해결 현황:** SCons 공식 문서, 오픈소스 등 해당 빌드 도구에 관한 분석을 진행함

## 다음 회차 목표

- **Godot 엔진 빌드 및 환경 구축, 동작 확인:** 소스로부터 빌드, Godot 엔진의 동작 확인, 환경 구축
- **공식 문서 정독 및 코드 리뷰:** 공식 문서와 오픈소스 코드의 내용을 이해
- **분석 방법론 및 도구 채택:** Godot 엔진 및 취약점 분석할 도구 채택
- **취약점 관련 토의:** 분석한 내용을 바탕으로 취약점이 존재할 수 있을 부분들에 대한 토의 진행

## 참고 자료

- Godot Docs: [Godot Docs](https://docs.godotengine.org/en/stable/about/introduction.html)
- Godot Source Code (GitHub): [Godot Source Code](https://github.com/godotengine/godot)
- Godot RE Tools (Github) : [Godot RE Tools](https://github.com/GDRETools/gdsdecomp)
- GDScript Toolkit (Github) : [GDScript Toolkit](https://github.com/Scony/godot-gdscript-toolkit)
- Godot GDscript Linter (Godot asset library) : [Godot GDscript Linter](https://godotengine.org/asset-library/asset/4612)
- SCons (Github) : [SCons](https://github.com/scons/scons)
- SCons Docs: [SCons Docs](https://scons.org/documentation.html)
