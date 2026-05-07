# ASC Project DB

ASC 보안 동아리 프로젝트 보고서 관리 시스템

쿼드 팀이 Git PR로 격주 보고서를 제출하면, 관리자 리뷰 후 merge 시 자동으로 Notion DB에 동기화됩니다.

## 마감

- **매주 화요일 23:59** 까지 PR merge 완료 시 해당 주차 제출로 인정

## 구조

```
reports/
└── {YYYY}/
    └── {쿼드조명}/
        └── {프로젝트명}/
            ├── report-00.md    # 프로젝트 계획서 (0회차)
            ├── report-01.md    # 격주 진행 보고서
            ├── report-02.md
            ├── ...
            ├── report-08.md    # 최종 기술 보고서 (is_final: true)
            └── assets/         # 스크린샷, 다이어그램 (선택)
```

## 보고 회차

| 회차 | 제출일 |
|:----:|:-----:|
| 0차 (계획서) | |
| 1차 | |
| 2차 | |
| 3차 | |
| 4차 | |
| 5차 | |
| 6차 | |
| 7차 | |
| 8차 | |

## 보고서 종류

### 프로젝트 계획서 (`project-plan-template.md` → `report-00.md`)

프로젝트 시작 전 0회차로 제출하는 계획서입니다. KUCIS 서식7 양식을 기반으로 합니다. 주요 항목:

- **프로젝트 개요:** 학교명, 동아리명, 프로젝트명, 분야, 개요, 기대효과
- **세부 계획서:** 목적, 세부내용, 기대효과, 수행시 문제점, 요구사항, 장비/물품, 팀원 역할 분담

### 격주 진행 보고서 (`report-template.md`)

2주 단위로 제출하는 진행 보고서입니다. 주요 항목:

- **팀 전체 진행 현황**: 이번 회차 목표, 현재 진행률, 주요 달성 사항
- **개인별 기여 내역**: 수행 작업 + 산출물 링크(GitHub 커밋, PR 등) + 기여도(%)
- **이슈 및 해결 방안**: 기술적 병목, 일정 지연 사유 및 해결 현황
- **다음 회차 목표**: 다음 2주간 완료할 구체적 작업 리스트

### 최종 기술 보고서 (`final-report-template.md`)

프로젝트 마지막 회차에 제출하는 최종 보고서입니다. `is_final: true`, `status: "완료"` 필수.

- **개요 및 목적**: 연구/개발 배경, 해결하고자 한 보안 이슈
- **기술적 상세 분석**: 환경 구성, 핵심 로직/취약점 분석
- **최종 결과물**: 산출물 요약, GitHub repo/데모 링크
- **실전 입증 및 성과** (심화 프로젝트 필수): 성능 수치, PoC, CVE/KISA 등
- **팀원별 기여 상세**: 전체 기간 기여도
- **고찰 및 결론**: 한계점, 기술적 역량 입증

## 빠른 시작

### 1. 레포 Fork & Clone

```bash
# 본인 GitHub 계정으로 Fork 후
git clone https://github.com/<your-username>/ProjectDB.git
cd ProjectDB
```

### 2. 보고서 작성

```bash
# 디렉토리 생성
mkdir -p reports/2026/A조/web-scanner

# 프로젝트 계획서 (0회차) 템플릿 복사
cp templates/project-plan-template.md reports/2026/A조/web-scanner/report-00.md

# 격주 보고서 템플릿 복사
cp templates/report-template.md reports/2026/A조/web-scanner/report-01.md

# 최종 보고서의 경우
cp templates/final-report-template.md reports/2026/A조/web-scanner/report-08.md
```

### 3. 로컬 검증

```bash
pip install -r scripts/requirements.txt
python scripts/validate_frontmatter.py
```

### 4. PR 제출

```bash
git checkout -b project/A조/web-scanner/report-01
git add .
git commit -m "Add report: A조/web-scanner report-01"
git push origin project/A조/web-scanner/report-01
# GitHub에서 PR 생성
```

자세한 제출 방법은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.

## 파이프라인

```
[쿼드 팀] -> fork/branch -> [PR 제출] -> 리뷰 -> [merge] -> [GitHub Actions] -> [Notion DB]
                                 |                              |
                           CI: frontmatter 검증         변경된 .md 파싱 -> 동기화
                                                        + 제출 현황 체크박스 업데이트
```

### 수동 재동기화

merge 없이 보고서를 수정한 뒤 Notion만 새로 갱신해야 할 때는 `Sync to Notion` 워크플로우를 수동 실행하세요.

- GitHub UI: Actions → **Sync to Notion** → **Run workflow**
  - `files`: 동기화할 보고서 경로 (쉼표/개행 구분, 비우면 `reports/` 전체)
  - `week`: 제출 현황 DB의 PW 체크박스를 갱신할 주차 (선택)
- CLI:

  ```bash
  gh workflow run notion-sync.yml \
    -f files="reports/2026/A조/foo/report-01.md" \
    -f week=3
  ```

## 설정 (관리자)

### GitHub Secrets

| Secret | 설명 |
|--------|------|
| `NOTION_API_KEY` | Notion Internal Integration Token |
| `NOTION_PROJECT_DB_ID` | 대상 Notion ProjectDB ID |
| `NOTION_TRACKING_DB_ID` | 제출 현황 DB ID |

### Notion DB 스키마

| 속성명 | 타입 | 비고 |
|--------|------|------|
| 프로젝트명 | Title | PK 역할 |
| 쿼드 조 | Select | A조, B조, ... |
| 조원 | Rich text | members join |
| 보고 회차 | Number | 0~8 |
| 제출일 | Date | |
| 진행 상태 | Status | 시작 전/진행 중/보류/완료 |
| CL 등급 | Select | CL1~CL4 |
| 최종 보고서 | Checkbox | is_final |
| 기여도 | Rich text | 팀원별 기여도 |
| Git 링크 | URL | 보고서 원문 링크 |

### 브랜치 보호 규칙 (권장)

- `main` 브랜치 직접 push 금지
- PR 필수, CI 통과 필수
- 최소 1명 리뷰 승인 필수
